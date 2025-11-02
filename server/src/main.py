from fastapi import FastAPI
from src.api.routes_incidents import router
from src.tools.registry import ToolRegistry
from src.tools.web_search import SerpAPITool
from src.tools.social_media import TelegramTool, TwitterTool, FacebookTool,InstagramTool
import socketio
import os
from fastapi.middleware.cors import CORSMiddleware


fastapi_app = FastAPI(title="NIRA Socket Server")


# Socket.IO server (async mode)
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=False,
)


# Allow CORS for your frontend origin(s)
origins = [
    os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8000"
]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount socket.io ASGI app that wraps FastAPI
# Expose final ASGI app as `app` for uvicorn: uvicorn server.main:app
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

fastapi_app.mount("/sw", app)

# tool registry
registry = ToolRegistry()
registry.register("serpapi", SerpAPITool(api_key="SERPAPI_KEY"))
registry.register("twitter", TwitterTool(bearer_token="TWITTER_BEARER"))
registry.register("facebook", FacebookTool(access_token="FB_TOKEN"))
registry.register("instagram", InstagramTool(access_token="IG_TOKEN", user_id="INST_USER_ID"))
registry.register("telegram", TelegramTool(bot_token="TELEGRAM_BOT_TOKEN"))

fastapi_app.include_router(router)
