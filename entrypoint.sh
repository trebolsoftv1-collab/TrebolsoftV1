#!/usr/bin/env sh
set -e
/app/wait-for-it.sh 172.18.0.2:5432 --timeout=60 --strict -- echo "DB is up"
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 10000
