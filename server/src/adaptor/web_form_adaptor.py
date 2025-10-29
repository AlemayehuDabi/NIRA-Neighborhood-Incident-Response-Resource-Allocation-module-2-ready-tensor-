from uuid import uuid4

def adapt_web_form(formData, uploaded_file:None):
    return {
        "id": str(uuid4()),
        "category": formData.get('category'),
        "severity": formData.get('severity'),
        "description": formData.get('description'),
        "location": formData.get('location'),
        "image_url": uploaded_file.filename if uploaded_file else None       
    }
    