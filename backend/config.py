from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # Anthropic
    ANTHROPIC_API_KEY: str = ""

    # App
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    JWT_SECRET: str = "your-secret-key-change-this"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()  # type: ignore
