from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time 

class GeoCodingTool:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="incident_report_system")
    
    def GeoCoder(self, location_text: str):
        
        try:
            location = self.geolocator.geocode(location_text,addressdetails=True)
            
            if location:
                return {
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "normalized_address": location.address
                }
        
        except (GeocoderServiceError, GeocoderTimedOut):
            
            time.sleep(1)
            
            try:
                location = self.geolocator.geocode(location_text,addressdetails=True)
                
                if location:
                    return {
                        "latitude": location.latitude,
                        "longitude": location.longitude,
                        "normalized_address": location.address
                    }
        
        
            except (GeocoderServiceError, GeocoderTimedOut):
            
                pass
            
        return {
            "latitude": None,
            "longitude": None,
            "normalized_address": location_text                      
        }
            
        