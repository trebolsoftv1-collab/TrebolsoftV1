# Script de Monitoreo - Agregar al backend
# app/api/v1/monitoring.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
import os
import psutil

router = APIRouter()

@router.get("/system-stats")
async def get_system_stats(db: Session = Depends(get_db)):
    """Estadísticas del sistema y base de datos."""
    
    # Tamaño de base de datos
    db_size = 0
    try:
        db_path = "dev.db"  # Ajustar según tu configuración
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path)
    except:
        db_size = 0
    
    # Memoria del sistema
    memory = psutil.virtual_memory()
    
    # Conteos de registros
    from app.models.user import User
    from app.models.client import Client
    
    user_count = db.query(User).count()
    client_count = db.query(Client).count()
    
    return {
        "database": {
            "size_bytes": db_size,
            "size_mb": round(db_size / 1024 / 1024, 2),
            "user_count": user_count,
            "client_count": client_count
        },
        "system": {
            "memory_used_percent": memory.percent,
            "memory_available_mb": round(memory.available / 1024 / 1024, 2)
        },
        "limits": {
            "render_hobby_ram_mb": 512,
            "sqlite_recommended_max_mb": 100,
            "users_before_upgrade": max(0, 100 - user_count)
        }
    }