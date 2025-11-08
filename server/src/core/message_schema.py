from pydantic import BaseModel
from typing import Dict, List, Any

# Define state class
class AgentMessage(BaseModel):
    sender: str
    recipient: str
    intent:str
    payload: Dict[str, Any]
    confidence: int
    is_confidence: float
    report_id: int
    recieved_message: str
    tool_results: List[Dict[str, Any]]
    aggregator_message: Dict[str, Any]