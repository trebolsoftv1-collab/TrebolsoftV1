"""
Dependencies compartidas para las rutas API.
Re-exporta get_db desde core para consistencia.
"""

from app.core import get_db

__all__ = ["get_db"]