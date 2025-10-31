from fastapi import APIRouter, UploadFile, File, HTTPException
from src.adaptor.web_form_adaptor import adapt_web_form
from src.adaptor.sms_adaptor import adapt_sms
from src.adaptor.whatup_adaptor import adapt_whatsapp
from src.agents.reporter_agent import ReporterAgent
from pydantic import BaseModel
from typing import Optional
import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

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
    print("Sending to Triage Agent:", message)
    # sending message to triage agent

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

# Cloudinary 
@router.post('/upload-image')
async def upload_image(file: UploadFile= File(...)):
    try:
        # Read file binary
        file_bytes = await file.read()

        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file_bytes,
            folder="fastapi_uploads",
        )

        return {
            "message": "Uploaded successfully",
            "url": result.get("secure_url"),
            "public_id": result.get("public_id")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete-image/{public_id}")
async def delete_image(public_id: str):
    result = cloudinary.uploader.destroy(public_id)
    return {"result": result}