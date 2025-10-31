from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import requests

# load image processing model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

class ImageCompare:
    def __init__(self):
        pass
        
    # compare image and text
    async def compare_image_incident(self, incident, triage):
        if incident.image_url == None:
            return
         # download image from Cloudinary
        img = Image.open(requests.get(incident.image_url, stream=True).raw)

        # prepare image for CLIP
        inputs = processor(images=img, return_tensors="pt")

        # run through model
        with torch.no_grad():
            image_embedding = model.get_image_features(**inputs)

        # convert embedding tensor to list for storing in DB
        return image_embedding[0].tolist()