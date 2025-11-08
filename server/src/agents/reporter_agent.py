from src.core.message_schema import AgentMessage as IncidentMessage
from src.tools.geocode import GeoCodingTool

class ReporterAgent:
    def __init__(self):
        self.geo_coding_tool = GeoCodingTool()

    def handle_incident(self, incident_payload: dict):
        
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
        
        return message
