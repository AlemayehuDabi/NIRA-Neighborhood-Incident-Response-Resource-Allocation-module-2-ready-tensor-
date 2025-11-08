from src.core.message_schema import AgentMessage
from src.tools.geocode import GeoCodingTool
from src.core.message_schema import AgentMessage

class ReporterAgent:
    def __init__(self):
        self.geo_coding_tool = GeoCodingTool()

    def handle_incident(self, state: AgentMessage):
        
        incident_payload = state
        
        location_txt = incident_payload.get("location")
        
        geo = self.geo_coding_tool.GeoCoder(location_txt)
        
        incident_payload["longitude"] = geo.get("longitude")
        incident_payload['latitude'] = geo.get("latitude")
        incident_payload["normalized_address"] = geo.get("normalized_adress")
        
        message = AgentMessage(
            sender="ReporterAgent",
            recipient="TriageAgent",
            intent="new_incident",
            payload=incident_payload,
            confidence=1.0,
            report_id=incident_payload["id"],
            recieved_message=incident_payload["source"]
        )
        
        return message
