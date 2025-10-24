from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno."""
    
    # Configuración de la app
    app_env: str = "local"
    app_name: str = "TrebolSoft API"
    app_port: int = 8000
    app_domain: str = "trebolsoft.com"
    api_domain: str = "api.trebolsoft.com"
    
    # Base de datos
    database_url: str
    
    # CORS
    cors_allowed_origins: List[str] = [
        "https://trebolsoft.com",
        "https://api.trebolsoft.com",
        "http://localhost:8000",
        "http://localhost:3000"
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


# Instancia global de configuración
settings = Settings()