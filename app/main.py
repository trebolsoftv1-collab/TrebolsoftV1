from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings
from app.core.database import Base, engine
from app.api.v1 import items_router, users_router, clients_router, credits_router, transactions_router
from app.api.v1.auth import router as auth_router

# Nota: La creación de tablas la maneja Alembic vía migraciones en el arranque
# (ver entrypoint.sh que ejecuta `alembic upgrade head`). Evitamos `create_all`
# para no interferir con el esquema gestionado por migraciones.

# Crear aplicación FastAPI
# Force rebuild v2 - ensure latest code deployed
app = FastAPI(
    title=settings.app_name,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
@app.get("/")
def root():
    """Redirige al explorador de la API para evitar Not Found en la raíz."""
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    """Endpoint de healthcheck."""
    return {"status": "ok"}

# Incluir rutas de la API v1
app.include_router(items_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(clients_router, prefix="/api/v1/clients", tags=["clients"])
app.include_router(credits_router, prefix="/api/v1/credits", tags=["credits"])
app.include_router(transactions_router, prefix="/api/v1/transactions", tags=["transactions"])
