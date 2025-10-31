from src.llm.google_llm import llm_tool

class AggregatorAgent:
    def __init__(self):
        self.llm = llm_tool()
        
        # take the main incident, classified triage and the search result
    async def handle_aggregator(self, incident, triage, results):
        """
        aggeregator calls llm and conclude the result
        """
        prompt = f"""
                You are an AI Incident Aggregation and Confidentiality Analyst. Your task is to analyze two distinct structured data inputs regarding a physical incident (e.g., fire, accident) and synthesize them into a single, comprehensive, structured JSON output.

                **Input Data Structure:**

                1.  **PRELIMINARY TRIAGE DATA:** The initial analysis from an upstream agent.
                    * Format: `{"category": "...", "severity":"...", "confidence": 0.0, "reason": "..."}`
                2.  **TOOL EXECUTION RESULTS:** An array of results from external searches (Web, Social Media, Photo Match).
                    * Format: `[{"tool": tool_name, "status": "success", "data": res}, ...]`

                **Synthesis and Confidence Rules:**
                1.  **Confidence Check:** The final `confidence` should primarily reflect the corroboration of the **TOOL EXECUTION RESULTS**. Use the initial confidence from the PRELIMINARY TRIAGE DATA as a base only if tool results are ambiguous or empty.
                    * **Corroboration:** Assign high confidence if multiple, independent tools confirm the same key details (location, incident type).
                    * **Discrepancy:** Lower confidence if sources conflict on major details, the tool status is 'failure', or the photo match confidence is weak.
                2.  **Confidentiality:** Flag as `true` if any data from the TOOL EXECUTION RESULTS contains specific PII (names, phone numbers, specific addresses beyond a general intersection) of affected individuals, or non-public internal company data related to the incident cause. General public details are *not* confidential.

                **Your Response:**
                You **must** respond with *only* a single, valid JSON object. Do not add any explanatory text, markdown formatting, or conversational text before or after the JSON block.

                **FINAL JSON Output Format:**
                The output must be a JSON object with the following required fields:
                * `is_confidential`: A boolean (`true` or `false`).
                * `confidence`: A float between `0.0` and `1.0` regarding the incident's **existence and key facts**.
                * `aggregation_summary`: A brief (2-3 sentence) synthesis of all findings, noting corroboration/discrepancies and summarizing the initial triage and tool results.
                * `original_info_given`: The exact, full raw input text provided below (including both the Preliminary Triage and Tool Results).
                * `incident_type`: A single word or short phrase describing the incident (e.g., 'Car Accident', 'Structure Fire').
                * `initial_category`: The value of the `category` field from the PRELIMINARY TRIAGE DATA.
                * `initial_severity`: The value of the `severity` field from the PRELIMINARY TRIAGE DATA.

                **Now, analyze the following input data and return ONLY the FINAL JSON object:**

                ---
                **PRELIMINARY TRIAGE DATA:**
                {triage}

                **TOOL EXECUTION RESULTS:**
                {results}
                ---
        """
        
        resp = await self.llm(prompt)
        if  resp.get("confidence") > 0.5:
            # call dispatcher agent
            return resp
        else:
            # human in loop
            return resp
            