import os
from src.tools._common import async_client, retry_network
from typing import List, Dict

class SerpAPITool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base = "https://serpapi.com/search.json"

    @retry_network()
    async def search(self, q: str, num: int = 5, engine: str = "google") -> List[Dict]:
        params = {
            "q": q,
            "api_key": self.api_key,
            "engine": engine,
            "num": num,
        }
        r = await async_client.get(self.base, params=params)
        r.raise_for_status()
        data = r.json()
        # Normalize common fields (engine-specific fields vary)
        results = []
        for item in data.get("organic_results", [])[:num]:
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet") or item.get("snippet_html"),
                "source": item.get("displayed_link") or item.get("link")
            })
        return results
