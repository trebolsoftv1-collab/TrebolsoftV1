#!/usr/bin/env sh
set -e
while IFS='=' read -r key value; do
	# Ignora líneas vacías, comentarios y variables sin nombre o sin valor
	if [ -n "$key" ] && [ "${key#\#}" = "$key" ] && [ -n "$value" ]; then
		export "$key"="$value"
	fi
done < /app/.env
export PORT="${PORT:-10000}"
# Migraciones
alembic upgrade head
# Arranque
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
