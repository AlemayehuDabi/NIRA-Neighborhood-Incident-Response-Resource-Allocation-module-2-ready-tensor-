from fastapi import FastAPI
from src.api.routes_incidents import router
from src.tools.registry import ToolRegistry
from src.tools.web_search import SerpAPITool
from src.tools.social_media import TelegramTool, TwitterTool, FacebookTool,InstagramTool


app = FastAPI()

# tool registry
registry = ToolRegistry()
registry.register("serpapi", SerpAPITool(api_key="SERPAPI_KEY"))
registry.register("twitter", TwitterTool(bearer_token="TWITTER_BEARER"))
registry.register("facebook", FacebookTool(access_token="FB_TOKEN"))
registry.register("instagram", InstagramTool(access_token="IG_TOKEN", user_id="INST_USER_ID"))
registry.register("telegram", TelegramTool(bot_token="TELEGRAM_BOT_TOKEN"))

app.include_router(router)
