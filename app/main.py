from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.api.v1 import items_router, users_router, clients_router, credits_router, transactions_router
from app.api.v1.box import router as caja_router
from app.api.v1.auth import router as auth_router
from app.api.v1.stats import router as stats_router

# Nota: La creación de tablas la maneja Alembic vía migraciones en el arranque
# (ver entrypoint.sh que ejecuta `alembic upgrade head`). Evitamos `create_all`
# para no interferir con el esquema gestionado por migraciones.

# Crear aplicación FastAPI
# Force rebuild v5 - disable docs in production for security
# Solo habilitar documentación en desarrollo
docs_url = "/docs" if settings.app_env != "production" else None
redoc_url = "/redoc" if settings.app_env != "production" else None

app = FastAPI(
    title=settings.app_name,
    docs_url=docs_url,
    redoc_url=redoc_url
)

# Configurar CORS
# Aseguramos que los orígenes sean una lista válida y agregamos defaults de desarrollo si es necesario
origins = settings.cors_allowed_origins
if isinstance(origins, str):
    origins = [origin.strip() for origin in origins.split(",")]

# Si la lista está vacía (posible error de configuración), agregamos localhost por defecto para evitar bloqueos
if not origins:
    origins = [
        "https://trebolsoft.com",
        "https://www.trebolsoft.com",
        "http://trebolsoft.com",
        "http://www.trebolsoft.com",
        "http://164.90.145.189",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("CORS_ALLOWED_ORIGINS (Active):", origins)

# Endpoints
@app.get("/")
def root():
    """Endpoint raíz de la API."""
    return {
        "message": "TrebolSoft API",
        "version": "1.0",
        "status": "online",
        "docs": "/docs" if settings.app_env != "production" else "disabled in production"
    }

@app.get("/health")
def health_check():
    """Endpoint de healthcheck."""
    return {"status": "ok"}

# Incluir rutas de la API v1
app.include_router(items_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(auth_router, prefix="/auth", tags=["authentication"])  # Compatibilidad adicional
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(clients_router, prefix="/api/v1/clients", tags=["clients"])
app.include_router(credits_router, prefix="/api/v1/credits", tags=["credits"])
app.include_router(transactions_router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(stats_router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(caja_router, prefix="/api/v1/box", tags=["box"])
