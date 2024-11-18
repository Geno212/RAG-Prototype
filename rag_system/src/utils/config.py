from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CHROMA_DB_DIR: str = "./chroma_db"
    TEMP_UPLOAD_DIR: str = "./temp_uploads"
    MODEL_NAME: str = "gpt-3.5-turbo"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_SEARCH_RESULTS: int = 4

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    Path(settings.TEMP_UPLOAD_DIR).mkdir(exist_ok=True)
    Path(settings.CHROMA_DB_DIR).mkdir(exist_ok=True)
    return settings
