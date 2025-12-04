#!/usr/bin/env sh
set -e
sleep 5
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
