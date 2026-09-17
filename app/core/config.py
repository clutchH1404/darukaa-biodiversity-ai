import os
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "Darukaa.Earth AI Biodiversity Intelligence"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    FRONTEND_PORT: int = 8501
    
    # LLM Settings
    OPENAI_API_KEY: str = ""
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    LLM_MODEL: str = "gpt-4o-mini"
    LLM_TEMPERATURE: float = 0.2
    
    # Storage Paths
    CHROMA_PERSIST_DIR: str = str(PROJECT_ROOT / "data" / "chroma_db")
    SQLITE_DB_PATH: str = str(PROJECT_ROOT / "data" / "darukaa_biodiversity.db")
    DATA_RAW_DIR: str = str(PROJECT_ROOT / "data" / "raw")
    DATA_PROCESSED_DIR: str = str(PROJECT_ROOT / "data" / "processed")
    DATA_KNOWLEDGE_DIR: str = str(PROJECT_ROOT / "data" / "knowledge")
    
    # Guardrails
    STRICT_GROUNDING: bool = True
    MIN_CONFIDENCE_THRESHOLD: float = 0.50
    MAX_RETRIEVAL_RESULTS: int = 6

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
for path_str in [
    settings.CHROMA_PERSIST_DIR,
    settings.DATA_RAW_DIR,
    settings.DATA_PROCESSED_DIR,
    settings.DATA_KNOWLEDGE_DIR,
    os.path.dirname(settings.SQLITE_DB_PATH)
]:
    Path(path_str).mkdir(parents=True, exist_ok=True)
