from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AI_PROVIDER: str = "langchain"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 