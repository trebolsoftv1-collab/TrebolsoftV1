# Render / GitHub Secrets — Valores a configurar

Pega estas variables en Render (Service -> Environment -> Environment Variables) y en GitHub (Repository -> Settings -> Secrets -> Actions):

## En Render (staging/prod service)
- DATABASE_URL: postgresql+psycopg2://<user>:<pass>@<host>:<port>/<db>
- SECRET_KEY: una cadena larga y aleatoria (ej: 64+ chars generado con `openssl rand -hex 32`)
- ALGORITHM: HS256
- ACCESS_TOKEN_EXPIRE_MINUTES: 30
- CORS_ALLOWED_ORIGINS: https://trebolsoft.com,https://api.trebolsoft.com,http://localhost:8000,http://localhost:3000

Asegúrate de que `entrypoint.sh` está configurado para ejecutar `alembic upgrade head` antes de arrancar la app (el repo ya incluye esto).

## En GitHub (Secrets para workflow)
- STAGING_BASE_URL: URL pública del servicio staging (p.ej. https://trebolsoft-staging.onrender.com)

> Nota: no subas `SECRET_KEY` ni `DATABASE_URL` al repo. Usa los variables/Secrets del servicio en Render y GitHub.
