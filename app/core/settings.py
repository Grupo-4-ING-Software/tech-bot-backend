from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AI_PROVIDER: str = "langchain"
    DATABASE_USER: str
    DATABASE_USER_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    GOOGLE_CLIENT_ID: str
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 