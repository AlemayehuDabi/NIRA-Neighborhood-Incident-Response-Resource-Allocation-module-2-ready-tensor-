from uuid import uuid4
from datetime import datetime

def adapt_sms(sms_text: str, phone_number: str):
    """
    Parse incoming SMS text into a structured incident payload.

    Expected format:
        "description;location;category;severity"

    Example:
        "Fire at market;Addis Ababa;fire;high"
    """

    # Split safely into up to 4 parts
    parts = sms_text.split(";")

    # Ensure exactly 4 fields (fill missing with "")
    description, location, category, severity = (parts + ["", "", "", ""])[:4]

    # Create structured payload (like web form)
    payload = {
        "id": str(uuid4()),             
        "category": category.strip(),
        "severity": severity.strip(),
        "description": description.strip(),
        "location": location.strip(),
        "phone_number": phone_number,             
        "created_at": datetime.utcnow().isoformat(),
        "source": "sms"
    }

    return payload
