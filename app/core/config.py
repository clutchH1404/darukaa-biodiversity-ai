import os
from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Darukaa.Earth AI Biodiversity Intelligence"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = os.environ.get("APP_ENV", "development")
    API_HOST: str = os.environ.get("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.environ.get("PORT", os.environ.get("API_PORT", 8000)))
    FRONTEND_PORT: int = int(os.environ.get("FRONTEND_PORT", 8501))
    
    # Production CORS Settings
    ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS", "")
    FRONTEND_URL: str = os.environ.get("FRONTEND_URL", "")

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
