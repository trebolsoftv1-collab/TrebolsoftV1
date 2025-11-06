# Facilita importaciones desde otros módulos
from app.core.config import Settings
from app.core.database import Base, get_db

# Instanciar configuración
settings = Settings()

__all__ = ["settings", "Base", "get_db"]