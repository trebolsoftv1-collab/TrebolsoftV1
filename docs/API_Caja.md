# Documentación API — Módulo Caja

## Endpoints principales
- POST /api/v1/caja/create/{user_id} — Crear cajas para usuario
- POST /api/v1/caja/transferir — Transferir base de supervisor a cobrador
- POST /api/v1/caja/gasto — Registrar gasto
- POST /api/v1/caja/microseguro — Registrar microseguro
- POST /api/v1/caja/retiro — Registrar retiro
- POST /api/v1/caja/cierre — Registrar cierre de caja
- POST /api/v1/caja/volado — Marcar cliente como volado
- POST /api/v1/caja/tope — Actualizar tope de préstamo

## Parámetros y respuestas
- Ver ejemplos en el código fuente y en la documentación de cada endpoint

## Seguridad
- Todos los endpoints requieren autenticación y permisos según rol
