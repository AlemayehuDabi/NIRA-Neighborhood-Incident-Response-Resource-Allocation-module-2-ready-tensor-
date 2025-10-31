from src.tools.google_llm import llm_tool

class TriageAgent:
    def __init__(self, send_to_disptach):
        self.llm = llm_tool()
        self.send_to_disptach = send_to_disptach
    
    #  classify as incident prompted
    async def classify_incident(self, incident):
        prompt = f"""
        Classify the following emergency:
        Incident: {incident['description']}
        Location: {incident['location']}
        Longitude = {incident["longitude"]}
        Latitude = {incident["latitude"]}
        Catgories = {incident["latitude"]}
        severity = {incident["severity"]}
        Normalized_address = {incident["normalized_adress"]}

        Return JSON with:
        - category (Fire, Medical, Crime, Flood, Accident, Other)
        - severity (Critical, High, Medium, Low)
        - confidence (0-1)
        - short_reason
        """

        triage = self.llm(prompt)
        return triage