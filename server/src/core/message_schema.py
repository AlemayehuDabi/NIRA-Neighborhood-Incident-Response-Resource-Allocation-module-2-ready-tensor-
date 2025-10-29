from pydantic import BaseModel

class AgentMessage(BaseModel):
    sender: str
    recipient: str
    intent: str
    payload: dict
    confidence: float
