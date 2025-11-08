from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from src.adaptor.web_form_adaptor import adapt_web_form
from src.adaptor.sms_adaptor import adapt_sms
from src.agents.reporter_agent import ReporterAgent
from pydantic import BaseModel
from typing import Optional
import cloudinary
import os
from dotenv import load_dotenv
from src.agents.triage_agent import TriageAgent
from src.tools.registry import ToolRegistry
from src.graph.graph import create_graph

load_dotenv()

# get all register tools
registry = ToolRegistry()

tools = registry.all()

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


# graph
graph = create_graph()

# triage agent
# triage = TriageAgent(tool_registry=tools)

# # replace by langgraph later
# def send_to_triage(message):
#     print("Sending to Triage Agent:", message)
#     # sending message to triage agent
#     resp = triage.verify_incident(message)
#     print("verification triage agent", resp)

# reporter agent
# reporter = ReporterAgent()  
    
# Web form endpoint
@router.post("/submit_web_incident")
async def submit_web_incident( 
    #   payload: IncidentWebPayload
    description: str = Form(...),
    location: str = Form(...),
    category: str = Form(...),
    severity: str = Form(...),
    uploaded_file: UploadFile = File(None)):
    payload_dict = {
        "description": description,
        "location": location,
        "category": category,
        "severity": severity,
        "image_url": uploaded_file
    }
    # payload_dict = payload.dict()
    payload = adapt_web_form(payload_dict)
    print("payload", payload)
    # send to reporter agent
    # message = reporter.handle_incident(payload)
    # invoke the start of the graph
    message = graph.ainvoke(payload)
    print("data from reporter agent handle_incident", message)
    return {"status": "pending", "report_id": payload["id"], "message": "Incident Reported", "recevied_message": "web"}

# SMS endpoint
@router.post("/submit_sms_incident")
async def submit_sms_incident(data: IncidentSMSPayload):
    print("sms payload", data.sms_text, data.phone_number)
    payload = adapt_sms(data.sms_text, data.phone_number)
    # message = reporter.handle_incident(payload)
    message = graph.ainvoke(payload)
    return {"status": "received", "report_id": payload["id"], "message": "Incident Reported", "recevied_method": "sms"}

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