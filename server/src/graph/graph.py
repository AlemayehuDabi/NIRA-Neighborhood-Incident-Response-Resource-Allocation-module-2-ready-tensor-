from langgraph.graph import StateGraph, START, END
from src.agents.reporter_agent import ReporterAgent
from src.agents.triage_agent import TriageAgent
from src.agents.aggregator_agent import AggregatorAgent
from src.agents.dispatcher_agent import DispatcherAgent
from langgraph.checkpoint.memory import MemorySaver
from src.core.message_schema import AgentMessage

# Instantiate agents
reporter = ReporterAgent()
triage = TriageAgent()
aggregator = AggregatorAgent()
dispatcher = DispatcherAgent()


def create_graph():
    graph = StateGraph(AgentMessage)

    # Add agents (nodes)
    graph.add_node("reporter_agent", reporter.handle_incident)
    graph.add_node("verifier_agent", triage.verify_incident)
    graph.add_node("aggregator_agent", aggregator.handle_aggregator)
    graph.add_node("dispatcher_agent", dispatcher.assign_volunteer)

    # Add edges (flow)
    graph.add_edge("reporter_agent", "verifier_agent")
    graph.add_edge("verifier_agent", "aggregator_agent")
    graph.add_edge("aggregator_agent", "dispatcher_agent")

    # Define start and end
    graph.add_edge(START, "reporter_agent")
    graph.add_edge("dispatcher_agent", END)

    # Optional: Memory or checkpoint
    memory = MemorySaver()
    app = graph.compile(checkpointer=memory)
    return app
