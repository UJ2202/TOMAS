from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Workspace
    WORKSPACE_DIR: str = "./workspaces"

    class Config:
        env_file = ".env"

settings = Settings()
