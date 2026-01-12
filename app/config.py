import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OUTPUT_DIR: str = "outputs/charts"

    class Config:
        env_file = ".env"

settings = Settings()

# Ensure output directory exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
