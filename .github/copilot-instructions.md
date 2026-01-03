## TrebolSoftV1 — Copilot instructions for code contributors

This file gives actionable, repository-specific guidance to help AI coding agents be productive quickly.

- Primary stack: Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, psycopg2-binary. See `requirements.txt`.
- App layout: the application root is `app/` with subfolders like `core/` (config + DB), `models/` (SQLAlchemy models), `schemas/` (Pydantic v2), `api/` (routes), and `main.py`.

Key workflows (examples and exact commands)

- Local dev (venv):
  - Create & activate venv (Windows PowerShell):
    - `. .\.venv\Scripts\Activate.ps1`
  - Install deps: `pip install -r requirements.txt`
  - Apply DB migrations (local DB or dockerized DB): `alembic upgrade head`
  - Run server: `uvicorn app.main:app --reload --port 8000`

- Docker / compose (recommended reproducer):
  - `docker compose up --build`
  - API is exposed at `localhost:10000` (container port 10000 → host 10000). DB on `localhost:5432`.

- Production deploy (DigitalOcean):
  - Server IP: 164.90.145.189
  - User: trebolsoft
  - Path: /home/trebolsoft/TrebolsoftV1
  - `entrypoint.sh` runs `alembic upgrade head` before starting `uvicorn`
  - Nginx proxy: trebolsoft.com/api/* → http://127.0.0.1:10000
  - SSL: Let's Encrypt via Certbot

Important integration details and conventions

- Database URL format used in `docker-compose.yml`:
  - `postgresql+psycopg2://postgres:postgres@db:5432/trebolsoft`
- Ports & health: healthcheck path is `/health`. CRUD example routes: `/api/v1/items` (GET/POST/PUT/DELETE) as documented in `README.md`.
- Migrations: Alembic configuration is in `alembic/`. Note `alembic/env.py` sets `target_metadata = None` (no autogenerate metadata by default). If you need autogenerate, import the project's Base/metadata into `env.py` and set `target_metadata = Base.metadata`.

Project-specific patterns to follow (found in repo)

- Pinned, minimal dependencies: `requirements.txt` pins exact versions. Match that style for quick reproducible builds.
- Entrypoint-driven migrations: rely on `entrypoint.sh` (Docker image runs migrations on startup). Don't duplicate migration automation unless required for a different environment.

Where to look first (high-value files)

- `README.md` — project setup and host/port conventions
- `Dockerfile`, `docker-compose.yml`, `entrypoint.sh` — container/deploy behaviour
- `requirements.txt` — exact dependency versions
- `alembic/` (especially `env.py`) — migrations and autogenerate behaviour
- `app/` — application code (core config, models, schemas, api)

How to make small, safe changes (guidance for AI edits)

- Prefer editing only files under `app/` and `alembic/` unless the change is about CI/CD or containers.
- When changing DB models, also update or create corresponding Alembic migrations; do not assume autogenerate will work unless `env.py` is wired to the project's metadata.
- When adding runtime config, follow existing use of env vars (see `docker-compose.yml` for `DATABASE_URL`, `APP_ENV`, `CORS_ALLOWED_ORIGINS`).

Quick examples to include in PR descriptions

- "Ran `alembic revision --autogenerate -m 'msg'` and `alembic upgrade head` locally using the repo's venv and verified `/health` returns 200." — include this when changing models.

If something's missing or unclear

- If you can't find models or metadata: search `app/models` and confirm a Base/metadata object (if absent, migrations are manual).
- If autogenerate fails, check `alembic/env.py` for `target_metadata` and add `from app.models import Base` then set `target_metadata = Base.metadata`.

Feedback request

If any section is unclear or you'd like more detail (examples of model imports for Alembic, typical tests to run, or CI/deploy hooks), tell me which area to expand.
