from uuid import uuid4

def adapt_web_form(formData):
    return {
        "id": str(uuid4()),
        "category": formData.get('category'),
        "severity": formData.get('severity'),
        "description": formData.get('description'),
        "location": formData.get('location'),
        "phone_number": formData.get("phone_number"),
        "image": formData.get('image') if formData.get('image') else None,
        "source": "web"      
    }
    