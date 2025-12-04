#!/usr/bin/env sh
set -e
while IFS='=' read -r key value; do
	if [ -n "$key" ] && [ "${key:0:1}" != "#" ]; then
		export "$key"="$value"
	fi
done < /app/.env
export PORT="${PORT:-10000}"
# Migraciones
alembic upgrade head
# Arranque
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
