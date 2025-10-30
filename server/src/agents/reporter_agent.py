from src.core.message_schema import AgentMessage as IncidentMessage
from src.tools.geocode import GeoCodingTool
class ReporterAgent:
    def __init__(self, orchestrator_send_function):
        """
        orchestrator_send_function: function to send message to TriageAgent (LangGraph node)
        """
        self.send_to_triage = orchestrator_send_function
        self.geo_coding_tool = GeoCodingTool()

    def handle_incident(self, incident_payload: dict):
        # You can add enrichment here (geocoding, timestamp already included, image handling)
        
        location_txt = incident_payload.get("location")
        
        geo = self.geo_coding_tool.GeoCoder(location_txt)
        
        incident_payload["longitude"] = geo.get("longitude")
        incident_payload['latitude'] = geo.get("latitude")
        incident_payload["normalized_address"] = geo.get("normalized_adress")
        
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
