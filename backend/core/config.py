from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file from project root into os.environ
# This makes environment variables available to all libraries (including Denario)
project_root = Path(__file__).parent.parent.parent  # Go up to TOMAS root
env_path = project_root / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ Loaded environment from {env_path}")
else:
    print(f"⚠️  No .env file found at {env_path}")

class Settings(BaseSettings):
    """Application settings"""
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

    # Application
    APP_NAME: str = "TOMAS"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./tomas.db"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Workspace
    WORKSPACE_DIR: Path = Path("./workspace")
    CONFIGS_DIR: Path = Path("./configs")

    # Session Configuration
    SESSION_TIMEOUT_HOURS: int = 24
    MAX_UPLOAD_SIZE_MB: int = 100

    # API Keys (can be overridden by user uploads)
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    PERPLEXITY_API_KEY: str = ""
    SEMANTIC_SCHOLAR_KEY: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories
        self.WORKSPACE_DIR.mkdir(exist_ok=True, parents=True)
        self.CONFIGS_DIR.mkdir(exist_ok=True, parents=True)

settings = Settings()
