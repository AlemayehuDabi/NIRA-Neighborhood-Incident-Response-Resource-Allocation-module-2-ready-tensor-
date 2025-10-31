from typing import List, Dict
import requests

class GoogleSearchTool:
    def __init__(self, api, cx):
        self.api = api
        self.cx = cx
        
    def search(self, query: str, num: int = 5) -> List[Dict]:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"key": self.api, "cx":self.cx,  "q": query, "num": num }
        resp = requests.get(url, params=params)
        results = resp.json().get("items", [])
        return [{"title": r["title"], "link": r["link"], "snippet": r["snippet"]} for r in results]
    
    
class BinSearchTool:
    def __init__(self, api, cx):
        self.api = api
        self.cx = cx
        
    def search(self, query:str, num:int=5) -> List[dict]:
        url = f"https://api.bing.microsoft.com/v7.0/search?q={query}&count={num}"
        headers = {"Ocp-Apim-Subscription-Key": self.api_key}
        resp = requests.get(url, headers=headers)
        results = resp.json().get("webPages", {}).get("value", [])
        return [{"title": r["name"], "link": r["url"], "snippet": r["snippet"]} for r in results]
    
    