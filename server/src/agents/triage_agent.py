from src.tools.google_llm import llm_tool
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import requests

# load image processing model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

class TriageAgent:
    def __init__(self, send_to_disptach):
        self.llm = llm_tool()
        self.send_to_disptach = send_to_disptach
    
    #  classify as incident prompted
    async def classify_incident(self, incident):
        prompt = f"""
        Classify the following emergency:
        Incident: {incident['description']}
        Location: {incident['location']}
        Longitude = {incident["longitude"]}
        Latitude = {incident["latitude"]}
        Catgories = {incident["latitude"]}
        severity = {incident["severity"]}
        Normalized_address = {incident["normalized_adress"]}

        Return JSON with:
        - category (Fire, Medical, Crime, Flood, Accident, Other)
        - severity (Critical, High, Medium, Low)
        - confidence (0-1)
        - short_reason
        """

        triage = self.llm(prompt)
        self.compare_image_incident(incident, triage)
        return
        
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
        
        
    # search the web if there is anything new in the news
    
    
    # go through tiktok and youtube for new things