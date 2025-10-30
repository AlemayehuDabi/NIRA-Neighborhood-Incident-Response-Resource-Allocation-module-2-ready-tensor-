from uuid import uuid4

def adapt_web_form(formData):
    return {
        "id": str(uuid4()),
        "category": formData.get('category'),
        "severity": formData.get('severity'),
        "description": formData.get('description'),
        "location": formData.get('location'),
        "image_url": formData.get('uploaded_file').filename if formData.get('uploaded_file') else None       
    }
    