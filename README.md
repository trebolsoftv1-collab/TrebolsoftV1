# TrebolSoft API (FastAPI)

Repo: **TrebolsoftV1** · Dominio: **trebolsoft.com** · API: **api.trebolsoft.com**

API inicial con FastAPI + SQLAlchemy 2 + Alembic + Docker + Render (plan Free).

## Requisitos
- Python 3.12+
- Docker (opcional) y Docker Compose

## Variables de entorno
Copia `.env.example` a `.env` y ajusta si es necesario.

## Desarrollo local
```bash
python -m venv .venv
# Windows
. .\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
- Healthcheck: http://localhost:8000/health
- CRUD Items: `GET/POST/PUT/DELETE /api/v1/items`

## Docker local
```bash
docker compose up --build
```
- API: http://localhost:10000
- DB: localhost:5432 (postgres/postgres)

## Despliegue en Render (plan Free)
1. Conecta el repo a Render → New → Blueprint (usa `render.yaml`).
2. Render creará el servicio **trebolsoft-api** y la DB **trebolsoft-db**.
3. Primer deploy: migraciones automáticas (via `entrypoint.sh`).
4. **Custom Domain**: agrega `api.trebolsoft.com` en Settings > Custom Domains y crea un **CNAME** en Namecheap apuntando al host que Render muestre.

> Nota: En Free, el servicio se **apaga** tras 15 min sin tráfico. La siguiente solicitud tarda ~1 min en "despertar". Para evitarlo, cambia a instancia paga cuando pases a producción.

## Estructura
```
app/
  core/ (config, db)
  models/ (SQLAlchemy models)
  schemas/ (Pydantic v2)
  api/ (rutas)
  main.py
alembic/ (migraciones)
render.yaml
Dockerfile
entrypoint.sh
```

## Licencia
MIT
