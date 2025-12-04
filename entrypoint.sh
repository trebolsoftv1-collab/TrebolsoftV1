#!/usr/bin/env sh
set -e
export $(grep -v '^#' /app/.env | xargs)
export PORT="${PORT:-10000}"
# Migraciones
alembic upgrade head
# Arranque
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
