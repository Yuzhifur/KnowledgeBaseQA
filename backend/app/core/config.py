from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # DeepSeek API
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    
    # App settings
    APP_NAME: str = "Knowledge Base QA"
    DEBUG: bool = False
    
    # File storage
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list[str] = [".txt", ".pdf", ".jpg", ".jpeg", ".png"]
    
    class Config:
        env_file = ".env"


settings = Settings()