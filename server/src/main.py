from fastapi import FastAPI
from src.api.routes_incidents import router

app = FastAPI()

app.include_router(router)
