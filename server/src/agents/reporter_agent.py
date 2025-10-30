from src.core.message_schema import AgentMessage as IncidentMessage

class ReporterAgent:
    def __init__(self, orchestrator_send_function):
        """
        orchestrator_send_function: function to send message to TriageAgent (LangGraph node)
        """
        self.send_to_triage = orchestrator_send_function

    def handle_incident(self, incident_payload: dict):
        # You can add enrichment here (geocoding, timestamp already included, image handling)
        message = IncidentMessage(
            sender="ReporterAgent",
            recipient="TriageAgent",
            intent="new_incident",
            payload=incident_payload,
            confidence=1.0
        )
        
        
        # Send to orchestration layer
        self.send_to_triage(message)
        return message
