import json
from typing import List, Dict
from src.tools.registry import ToolRegistry
from src.llm.google_llm import llm_tool 
from asyncio import TimeoutError
import asyncio
from src.agents.aggregator_agent import AggregatorAgent
from src.core.message_schema import AgentMessage


class ToolExecutionError(Exception):
    pass

class TriageAgent:
    def __init__(self, tool_registry: ToolRegistry):
        self.llm = llm_tool() 
        self.tools = tool_registry
        self.aggregator = AggregatorAgent()

    async def classify_incident(self, incident: Dict) -> Dict:
        prompt = f"""
        Classify the following emergency:
        Incident: {incident.get('description')}
        Location: {incident.get('location')}
        Coordinates: {incident.get('latitude')},{incident.get('longitude')}
        Return JSON: {{ "category": "...", "severity":"...", "confidence": 0.0, "reason": "..." }}
        """
        resp = await self.llm(prompt)
        try:
            triage = json.loads(resp)
        except Exception:
            # If model didn't return strict JSON, attempt to extract JSON block
            start = resp.find("{")
            end = resp.rfind("}") + 1
            triage = json.loads(resp[start:end])
        # print("triage data", triage)
        return triage

    async def decide_tools(self, incident: Dict, triage: Dict) -> Dict:
        """
        Ask the LLM which tools to call, pass tool registry list and let it choose.
        LLM returns JSON like: {"tools":["serpapi","twitter"], "reason":"..." }
        """
        tools_list = self.tools.list()
        prompt = f"""
        You are an assistant that chooses from available tools to verify incident claims.
        Incident: {incident.get('description')}
        Triage: {json.dumps(triage)}
        Available tools: {tools_list}
        Choose up to 3 tools in preference order and return JSON:
        {{ "tools": ["tool_name1","tool_name2"], "notes": "why these" }}
        """
        resp = await self.llm(prompt)
        try:
            decision = json.loads(resp)
        except Exception:
            # fallback: naive heuristic
            decision = {"tools": ["serpapi", "twitter"], "notes": "fallback selection"}
        return decision

    async def call_tool(self, tool_name: str, query: str, timeout: float = 10.0) -> Dict:
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ToolExecutionError(f"Tool not found: {tool_name}")

        # Try to detect async search method
        coro = (
            getattr(tool, "search", None) or 
            getattr(tool, "fetch", None) or 
            getattr(tool, "search_posts", None) or
            getattr(tool, "fetch_channel_recent", None) or
            getattr(tool, "hashtag_search_recent", None) 
        )
        
        if coro is None:
            raise ToolExecutionError(f"Tool {tool_name} has no callable search/fetch method")

        # run with timeout; exceptions are caught by caller
        try:
            return await asyncio.wait_for(coro(query), timeout=timeout)
        except asyncio.TimeoutError as e:
            raise ToolExecutionError(f"Tool {tool_name} timeout: {e}")
        except Exception as e:
            raise ToolExecutionError(f"Tool {tool_name} error: {e}")

    async def verify_incident(self, state: AgentMessage):
        incident = state.payload
        triage = await self.classify_incident(incident)
        decision = await self.decide_tools(incident, triage)
        selected = decision.get("tools", [])
        results = []
        # execute selected tools with isolation & fallback
        for tool_name in selected:
            try:
                res = await self.call_tool(tool_name, incident.get("description"))
                results.append({"tool": tool_name, "status": "success", "data": res})
            except Exception as e:
                # log and continue; fallback: try other tools registered but not selected
                results.append({"tool": tool_name, "status": "failed", "error": str(e)})
                continue

        # If all selected failed, fallback to other registry tools (best-effort)
        if all(r["status"] == "failed" for r in results) and len(results) > 0:
            for fallback_name in self.tools.list():
                if fallback_name in selected:
                    continue
                try:
                    res = await self.call_tool(fallback_name, incident.get("description"))
                    results.append({"tool": fallback_name, "status": "success", "data": res, "fallback": True})
                    break
                except Exception:
                    continue
        
        # return the incident, triage, and results from verifier agent so langgraph use it
        message = AgentMessage(
            sender="TriageAgent",
            recipient="AggregatorAgent",
            intent="verified_incident",
            # same payload,id,confidence,recieved_message
            tool_results=results
        )
        
        return message
                    
        # Send to aggregator (your aggregator should handle evidence shaping)
        # aggregatorResp = await self.aggregator.handle_aggregator(incident, triage, results)
        # print("aggregator response", aggregatorResp)
        # return {"triage": triage, "tool_results": results, "message": "triage agent done"}
