# Guía de Configuración — Producción

## Requisitos
- Servidor DigitalOcean con IP 164.90.145.189
- Dominio www.trebolsoft.com y trebolsoft.com configurados en Cloudflare y Namecheap
- Docker y docker-compose instalados
- Variables de entorno configuradas (.env, docker-compose.yml)
- Certificados SSL activos en Cloudflare

## Pasos
1. Clonar el repositorio desde GitHub
2. Configurar variables de entorno y settings
3. Ejecutar migraciones Alembic
4. Iniciar servicios con docker-compose
5. Verificar acceso desde dominio y IP
6. Monitorear logs y métricas

## Notas
- No dejar endpoints de documentación abiertos en producción
- Revisar CORS y seguridad de la API
- Realizar backups periódicos
