# TrebolSoft API (FastAPI)

Repo: **TrebolsoftV1** · Dominio: **trebolsoft.com** · API: **api.trebolsoft.com**

API de gestión de cobranza y créditos con FastAPI + SQLAlchemy 2 + Alembic + Docker + Render.

## 📋 Requisitos
- Python 3.12+
- PostgreSQL (local) o Docker
- Git

## 🔧 Variables de entorno requeridas

### Para desarrollo local (`.env`)
```bash
# App
APP_ENV=local
APP_NAME=TrebolSoft API
APP_PORT=8000

# Base de datos (SQLite para desarrollo rápido)
DATABASE_URL=sqlite:///./dev.db
# O PostgreSQL local:
# DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/trebolsoft

# Seguridad (JWT)
SECRET_KEY=tu-clave-secreta-de-desarrollo
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30

# CORS
CORS_ALLOWED_ORIGINS=["http://localhost:8000","http://localhost:3000"]
```

### Para producción (Render Environment Variables)
```bash
APP_ENV=production
APP_NAME=TrebolSoft API
DATABASE_URL=postgresql+psycopg2://[render-db-url]
SECRET_KEY=[clave-segura-generada]
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=30
CORS_ALLOWED_ORIGINS=["https://trebolsoft.com","https://api.trebolsoft.com"]
```

### 🔑 Generar SECRET_KEY segura
```powershell
# En Windows PowerShell
python -c "import secrets; print(secrets.token_hex(32))"

# En Linux/Mac
python3 -c "import secrets; print(secrets.token_hex(32))"
```
⚠️ **IMPORTANTE**: Usa claves diferentes para desarrollo y producción. Nunca versiones tu `.env` en Git.

## 🚀 Desarrollo local

### 1. Clonar repositorio
```bash
git clone https://github.com/trebolsoftv1-collab/TrebolsoftV1.git
cd TrebolsoftV1
```

### 2. Crear entorno virtual e instalar dependencias
```bash
# Windows PowerShell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
# Copiar el template
cp .env.example .env

# Editar .env y agregar tu SECRET_KEY
# Usar SQLite para desarrollo rápido: DATABASE_URL=sqlite:///./dev.db
```

### 4. Ejecutar migraciones
```bash
alembic upgrade head
```

### 5. Iniciar servidor
```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Probar la API
- **Healthcheck**: http://localhost:8000/health
- **Documentación (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker local

```bash
docker compose up --build
```
- **API**: http://localhost:10000
- **DB**: localhost:5432 (postgres/postgres)


## 📦 Despliegue en DigitalOcean

### Paso 1: Crear Droplet en DigitalOcean
1. Accede a DigitalOcean y crea un Droplet (Ubuntu recomendado).
2. Configura la IP pública: `164.90.145.189`.
3. Instala Docker y docker-compose en el servidor.

### Paso 2: Configurar base de datos PostgreSQL
1. Puedes usar un contenedor Docker para PostgreSQL o un servicio gestionado.
2. Configura las variables de entorno en `.env` y `docker-compose.yml` para apuntar a la IP del servidor o al contenedor `db`.

### Paso 3: Subir el código al servidor
1. Clona el repositorio en el Droplet:
  ```bash
  git clone https://github.com/trebolsoftv1-collab/TrebolsoftV1.git
  cd TrebolsoftV1
  ```
2. Configura las variables de entorno en `.env`.

### Paso 4: Construir y levantar los servicios
1. Ejecuta:
  ```bash
  docker compose up --build -d
  ```
2. El `entrypoint.sh` ejecutará las migraciones antes de iniciar la API.

### Paso 5: Configurar DNS en Cloudflare
1. En Cloudflare, apunta los registros A de `trebolsoft.com`, `www.trebolsoft.com` y `api.trebolsoft.com` a la IP `164.90.145.189`.
2. Configura el proxy y reglas según tus necesidades.

### Paso 6: Verificar deploy
Prueba estos endpoints:
```bash
# Healthcheck
curl https://api.trebolsoft.com/health

# Documentación
https://api.trebolsoft.com/docs
```

### Paso 7: Seguridad y producción
- Usa HTTPS (Cloudflare puede gestionar el certificado SSL).
- Mantén actualizadas las dependencias y el sistema operativo.
- Realiza backups periódicos de la base de datos y archivos importantes.

## 📁 Estructura del proyecto
```
TrebolsoftV1/
├── app/
│   ├── core/           # Configuración, DB, seguridad
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/         # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── client.py
│   │   ├── credit.py
│   │   └── cash_transaction.py
│   ├── schemas/        # Schemas Pydantic v2
│   ├── api/            # Endpoints REST
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── clients.py
│   │       ├── credits.py
│   │       └── transactions.py
│   └── main.py         # App FastAPI
├── alembic/            # Migraciones de BD
├── tests/              # Tests unitarios
├── requirements.txt    # Dependencias Python
├── Dockerfile          # Imagen Docker
├── docker-compose.yml  # Compose para desarrollo
├── entrypoint.sh       # Script de inicio (migraciones + uvicorn)
└── README.md
```

## 🔐 Autenticación y autorización
La API usa **JWT (JSON Web Tokens)** para autenticación.

### Registrar usuario
```bash
POST /api/v1/auth/register
{
  "username": "admin",
  "email": "admin@trebolsoft.com",
  "password": "password123",
  "role": "admin"
}
```

### Login
```bash
POST /api/v1/auth/login
{
  "username": "admin",
  "password": "password123"
}
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usar el token
Incluir en el header de las siguientes peticiones:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🧪 Tests
```bash
pytest
```

## 📝 Licencia
MIT
