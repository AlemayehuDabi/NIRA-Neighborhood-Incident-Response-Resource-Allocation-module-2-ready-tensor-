from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"  # tells Pydantic to load from .env

@lru_cache()  # cache settings to avoid reloading multiple times
def get_settings():
    return Settings()

settings = get_settings()
