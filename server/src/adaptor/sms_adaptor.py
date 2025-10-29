from uuid import uuid4

def adapt_sms(sms_text, phone_number):
    try:
        description, location, category, severity = sms_text.split(';', 3)
    except:
        description, location, category, severity  = sms_text, None, "", ""
       
    return {
        "id": str(uuid4()),
        "category": category,
        "severity": severity,
        "description": description,
        "location": location,
        "phone_number": phone_number,
        "image_url": None
    }