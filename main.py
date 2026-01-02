# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env (opcional pero recomendado)
load_dotenv()

# --- Importar Routers de la Aplicación ---
# Basado en la estructura de proyectos FastAPI, los routers deberían estar en archivos separados.
# Asegúrate de que los nombres de los archivos y las variables del router coincidan.
# Si tus archivos o variables se llaman diferente, ajusta las importaciones.
from api.v1 import auth, users, clients, caja, credito, empresa, auditoria, dashboard

# --- Creación de la Aplicación FastAPI ---
app = FastAPI(
    title="TrebolSoft API",
    description="API para el sistema de gestión TrebolSoft.",
    version="1.0.0"
)

# --- Configuración de CORS ---
# Orígenes permitidos para las peticiones
origins = [
    "https://www.trebolsoft.com",
    "https://trebolsoft.com",
    # Orígenes para desarrollo local del frontend
    "http://localhost:3000",
    "http://localhost:5173", # Puerto común para Vite
]

# Añadir el middleware de CORS a la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# --- Inclusión de Routers en la Aplicación ---
# Se incluyen todas las rutas de la API con un prefijo común /api/v1
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Usuarios"])
app.include_router(clients.router, prefix="/api/v1/clients", tags=["Clientes"])
app.include_router(caja.router, prefix="/api/v1/caja", tags=["Caja"])
app.include_router(credito.router, prefix="/api/v1/credito", tags=["Créditos"])
app.include_router(empresa.router, prefix="/api/v1/empresa", tags=["Empresa"])
app.include_router(auditoria.router, prefix="/api/v1/auditoria", tags=["Auditoría"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])


# --- Endpoints Raíz y de Verificación de Estado ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de TrebolSoft V1"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Endpoint de verificación de estado para monitoreo.
    """
    return {"status": "ok"}

# --- Ejecución para Desarrollo Local (Opcional) ---
# Esto permite ejecutar `python main.py` para iniciar un servidor de desarrollo.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
