from fastapi import APIRouter, UploadFile, Form
from src.adaptor.web_form_adaptor import adapt_web_form
from src.adaptor.sms_adaptor import adapt_sms
from src.adaptor.whatup_adaptor import adapt_whatsapp
from src.agents.reporter_agent import ReporterAgent
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class IncidentWebPayload(BaseModel):
    description: str
    location: str
    category: str
    severity: str
    image_url: Optional[str] = None

class IncidentSMSPayload(BaseModel):
    sms_text: str
    phone_number: str

def send_to_triage(message):
    print("Sending to Triage Agent:", message.__dict__)

# reporter agent
reporter = ReporterAgent(send_to_triage)

# Web form endpoint
@router.post("/submit_web_incident")
async def submit_web_incident(payload: IncidentWebPayload):
    payload_dict = payload.dict()
    payload = adapt_web_form(payload_dict)
    print("payload", payload)
    message = reporter.handle_incident(payload)
    return {"status": "received", "report_id": payload["id"]}

# SMS endpoint
@router.post("/submit_sms_incident")
async def submit_sms_incident(data: IncidentSMSPayload):
    print("sms payload", data.sms_text, data.phone_number)
    payload = adapt_sms(data.sms_text, data.phone_number)
    message = reporter.handle_incident(payload)
    return {"status": "received", "report_id": payload["id"], "payload": payload}

# WhatsApp endpoint
@router.post("/submit_whatsapp_incident")
async def submit_whatsapp_incident(whatsapp_json: dict):
    payload = adapt_whatsapp(whatsapp_json)
    message = reporter.handle_incident(payload)
    return {"status": "received", "report_id": payload["id"]}