"""Application configuration management."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="Inkle Tourism System", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # Server
    port: int = Field(default=8000, alias="PORT")
    host: str = Field(default="0.0.0.0", alias="HOST")
    
    # CORS - Production ready
    allowed_origins: List[str] = Field(
        default=["*"],  # Will be overridden by environment variable
        alias="ALLOWED_ORIGINS"
    )
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # API Configuration
    api_timeout: int = Field(default=30, alias="API_TIMEOUT")
    
    # External API URLs
    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    openmeteo_url: str = "https://api.open-meteo.com/v1/forecast"
    overpass_url: str = "https://overpass-api.de/api/interpreter"
    
    # Rate limiting
    nominatim_delay: float = 1.0  # Delay between Nominatim requests (seconds)
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @staticmethod
        def parse_env_var(field_name: str, raw_val: str):
            # Parse ALLOWED_ORIGINS as comma-separated list
            if field_name == 'allowed_origins':
                return [origin.strip() for origin in raw_val.split(',')]
            return raw_val


# Global settings instance
settings = Settings()
