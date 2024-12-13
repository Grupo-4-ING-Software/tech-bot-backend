from functools import lru_cache
from pydantic_settings import BaseSettings
import os
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    AI_PROVIDER: str = "langchain"
    DATABASE_USER: str
    DATABASE_USER_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    GOOGLE_CLIENT_ID: str
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    
    class Config:
        env_file = os.path.join(ROOT_DIR, '.env')
        env_file_encoding = 'utf-8'
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings() 