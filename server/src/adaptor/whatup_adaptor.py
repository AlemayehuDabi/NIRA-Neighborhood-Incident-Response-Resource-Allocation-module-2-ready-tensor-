from uuid import uuid4
from datetime import datetime

def adapt_whatsapp(whatsapp_json):
    message = whatsapp_json.get("message", {})

    return {
        "id": str(uuid4()),
        "location": message.get("address"),
        "description": message.get("text"),
        "image_url": message.get("image_url")
    }