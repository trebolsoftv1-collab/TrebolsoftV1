#!/usr/bin/env sh
set -e
while IFS='=' read -r key value; do
	case "$key" in
		''|\#*) ;; # ignora líneas vacías o que empiezan con #
		*) export "$key"="$value" ;;
	esac
done < /app/.env
export PORT="${PORT:-10000}"
# Migraciones
alembic upgrade head
# Arranque
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
