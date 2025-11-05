# Guía de configuración de Cloudinary

## ✅ Pasos para configurar Cloudinary (5 minutos)

### 1. Crear cuenta gratuita en Cloudinary

1. Ve a: https://cloudinary.com/users/register_free
2. Regístrate con tu email o GitHub
3. Verifica tu email
4. Accede al Dashboard: https://cloudinary.com/console

### 2. Obtener credenciales

En el Dashboard de Cloudinary, verás un panel que dice **Account Details**:

```
Cloud name: tu-nombre-cloud
API Key: 123456789012345
API Secret: AbCdEfGhIjKlMnOpQrStUvWxYz
```

### 3. Configurar en Render

1. Ve a tu servicio en Render: https://dashboard.render.com
2. Selecciona tu API service `trebolsoft`
3. Ve a la pestaña **Environment**
4. Agrega estas 3 variables:

```
CLOUDINARY_CLOUD_NAME = tu-nombre-cloud
CLOUDINARY_API_KEY = 123456789012345
CLOUDINARY_API_SECRET = AbCdEfGhIjKlMnOpQrStUvWxYz
```

5. Guarda los cambios
6. Render hará un redeploy automático

### 4. Verificar instalación

Una vez que el deploy termine, prueba el endpoint:

```bash
# Login y obtén el token
curl -X POST "https://trebolsoft.onrender.com/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=tu-password"

# Sube una foto de prueba
curl -X POST "https://trebolsoft.onrender.com/api/v1/clients/1/upload-photo" \
  -H "Authorization: Bearer TU_TOKEN_AQUI" \
  -F "file=@/ruta/a/foto.jpg"
```

## 📊 Límites del plan gratuito

| Recurso | Límite mensual |
|---------|----------------|
| Almacenamiento | 25 GB |
| Ancho de banda | 25 GB |
| Transformaciones | 25,000 |
| Archivos | Ilimitados |

**Suficiente para:**
- ~5,000 fotos de alta calidad (5MB cada una)
- ~25,000 vistas/descargas por mes
- Optimización automática de imágenes

## 🔧 Opcional: Configurar para desarrollo local

Si quieres probar la subida de fotos en Docker local:

1. Crea un archivo `.env` en la raíz del proyecto:

```bash
CLOUDINARY_CLOUD_NAME=tu-nombre-cloud
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=AbCdEfGhIjKlMnOpQrStUvWxYz
```

2. Ejecuta Docker Compose:

```bash
docker compose up --build
```

3. Las fotos se subirán a Cloudinary desde tu entorno local.

## ✨ Características incluidas

- **Optimización automática**: Las fotos se optimizan al subir (max 1200x1200px, calidad auto)
- **CDN global**: Las fotos se sirven desde el CDN de Cloudinary (rápido en todo el mundo)
- **Organización**: Las fotos se guardan en carpetas: `trebolsoft/clients/{client_id}/house_photo.jpg`
- **Sobrescritura**: Si subes otra foto, reemplaza la anterior (no ocupa espacio extra)
- **Validación**: Solo acepta JPG, PNG, WEBP, max 5MB

## 🚀 Próximos pasos

Una vez configurado Cloudinary en Render:

1. El backend estará listo para recibir fotos
2. La migración de BD se aplicará automáticamente (campos `latitude`, `longitude`, `house_photo_url`)
3. El endpoint `/api/v1/clients/{id}/upload-photo` estará disponible
4. El frontend podrá capturar y subir fotos desde el móvil

---

**Nota**: Guarda tus credenciales de Cloudinary en un lugar seguro. No las compartas en el código ni en repositorios públicos.
