import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentinel AI: Multi-Agent Disaster Response Copilot"
    API_V1_STR: str = "/api"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentinel_ai.db")
    
    @property
    def is_demo_mode(self) -> bool:
        return not bool(self.GEMINI_API_KEY)

settings = Settings()
