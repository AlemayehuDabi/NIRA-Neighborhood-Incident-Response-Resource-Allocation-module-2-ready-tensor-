from typing import List, Dict
import requests
from tweepy.asynchronous import AsyncClient
from tenacity import retry, stop_after_attempt, wait_exponential
import httpx

class TwitterTool:
    def __init__(self, bearer_token: str):
        self.client = AsyncClient(bearer_token=bearer_token, wait_on_rate_limit=True)

    async def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Uses recent search. Query syntax can include place: or geocode filters if you provide them.
        """
        resp = await self.client.search_recent_tweets(query=query, max_results=max_results,
                                                      tweet_fields=["created_at","author_id","geo","attachments","context_annotations"])
        tweets = []
        if resp.data:
            for t in resp.data:
                tweets.append({
                    "id": str(t.id),
                    "text": t.text,
                    "created_at": str(t.created_at),
                    "author_id": str(t.author_id),
                    "geo": getattr(t, "geo", None)
                })
        return tweets

class FacebookTool:
    def __init__(self, access_token: str, api_version: str = "v17.0"):
        self.access_token = access_token
        self.api_version = api_version
        self.base = f"https://graph.facebook.com/{self.api_version}"

    async def search_posts(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Graph API search for public posts requires App Review and search permission; many accounts cannot use 'search' endpoint.
        Alternative: use Pages / Groups you control, or have an ingest pipeline.
        """
        url = f"{self.base}/search"
        params = {"q": query, "type": "post", "limit": limit, "access_token": self.access_token}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json().get("data", [])
            results = []
            for p in data:
                results.append({
                    "id": p.get("id"),
                    "message": p.get("message"),
                    "created_time": p.get("created_time")
                })
            return results

class InstagramTool:
    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id
        self.base = "https://graph.instagram.com"

    async def hashtag_search_recent(self, hashtag_id: str, limit: int = 10) -> List[Dict]:
        # To get hashtag results you must use the Business Discovery endpoints via Facebook Graph with IG Business account
        url = f"https://graph.facebook.com/v17.0/{hashtag_id}/recent_media"
        params = {"user_id": self.user_id, "fields": "id,caption,media_type,media_url,timestamp", "access_token": self.access_token, "limit": limit}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json().get("data", [])
        
class TelegramTool:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base = f"https://api.telegram.org/bot{self.bot_token}"

    async def get_updates(self, offset: int = None) -> Dict:
        params = {}
        if offset:
            params["offset"] = offset
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base}/getUpdates", params=params)
            r.raise_for_status()
            return r.json()

    async def fetch_channel_recent(self, channel_username: str, limit: int = 20) -> List[Dict]:
        """
        Bot must be a member of a public channel to fetch messages via getUpdates/ or via Bot API to read messages sent in groups where bot is present.
        For public channels, consider using Telegram's client API (telethon) to read history, but that is a user-bot approach.
        """
        # A simple approach: maintain updates and parse messages previously seen.
        resp = await self.get_updates()
        messages = []
        for u in resp.get("result", []):
            msg = u.get("message") or u.get("channel_post")
            if not msg:
                continue
            if msg.get("chat", {}).get("username") == channel_username:
                messages.append({
                    "message_id": msg.get("message_id"),
                    "text": msg.get("text"),
                    "date": msg.get("date")
                })
        return messages