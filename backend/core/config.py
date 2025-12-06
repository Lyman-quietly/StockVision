import os

class Settings:
    PROJECT_NAME: str = "StockVision"
    VERSION: str = "1.0.0"
    API_PREFIX: str = ""
    ALLOWED_ORIGINS: list = ["*"]
    
    # Simple check for simple project. In a larger project, use pydantic-settings.
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
