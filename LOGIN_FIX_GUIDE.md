# 🔧 GUÍA DE SOLUCIÓN - Problema de Login en TrebolSoft

## ❌ PROBLEMA
No puedes iniciar sesión en https://app.trebolsoft.com

## 🔍 POSIBLES CAUSAS Y SOLUCIONES

### 1️⃣ **No existe ningún usuario en la base de datos**

**Síntoma:** El login dice "usuario o contraseña incorrectos" incluso con credenciales correctas.

**Solución (LOCAL):**
```powershell
# Crear usuario administrador por defecto
python create_admin.py
```

**Credenciales creadas:**
- Username: `admin`
- Password: `admin123`
- Email: `admin@trebolsoft.com`

⚠️ **Cambiar la contraseña después del primer login**

---

### 2️⃣ **Olvidaste la contraseña de tu usuario**

**Solución (LOCAL):**
```powershell
# Resetear contraseña de cualquier usuario
python reset_password.py
```

El script te permitirá:
1. Ver todos los usuarios disponibles
2. Seleccionar el usuario
3. Asignar una nueva contraseña

---

### 3️⃣ **El frontend no se conecta al backend correcto**

**Verificar variables de entorno en Vercel:**

1. Ve a https://vercel.com/tu-proyecto
2. Settings → Environment Variables
3. Verifica que `VITE_API_URL` apunte a:
   ```
   https://trebolsoftv1-latest.onrender.com
   ```

---

### 4️⃣ **El backend no está corriendo en Render**

**Verificar el backend:**
```powershell
# Probar healthcheck
curl https://trebolsoftv1-latest.onrender.com/health
```

Debería responder: `{"status":"ok"}`

Si no responde:
1. Ve a https://render.com/dashboard
2. Abre tu servicio `trebolsoftv1-latest`
3. Verifica que esté en estado "Live"
4. Revisa los logs por errores

---

### 5️⃣ **CORS bloqueando las peticiones**

**Verificar CORS en Render:**

Variables de entorno en Render deben incluir:
```bash
CORS_ALLOWED_ORIGINS=["https://app.trebolsoft.com","http://localhost:3000"]
```

**Abrir navegador y revisar Console:**
1. F12 → Console
2. Intentar login
3. Si ves errores CORS, actualizar variable en Render

---

### 6️⃣ **Usuario existe pero está inactivo**

**Verificar usuarios localmente:**
```powershell
python check_users.py
```

Si el usuario existe pero `is_active = False`:
1. Usar script reset_password.py
2. O manualmente activar en la BD

---

## 🚀 SOLUCIÓN RÁPIDA (PASO A PASO)

### Para BASE DE DATOS LOCAL (dev.db):

```powershell
# 1. Crear usuario admin
python create_admin.py

# 2. Probar login localmente
# Ir a http://localhost:8000/docs
# Probar endpoint /api/v1/auth/token con:
#   username: admin
#   password: admin123
```

### Para PRODUCCIÓN (Render + Vercel):

**Opción A: Crear usuario desde la API en producción**
```powershell
# 1. Usar Swagger UI de producción
# https://trebolsoftv1-latest.onrender.com/docs

# 2. Ejecutar endpoint POST /api/v1/users (necesitas otro admin)
```

**Opción B: Conectar a BD de producción (PostgreSQL)**
```powershell
# 1. Obtener DATABASE_URL de Render
# 2. Conectar con psql o DBeaver
# 3. Ejecutar:
INSERT INTO users (username, email, hashed_password, full_name, phone, zone, role, is_active)
VALUES ('admin', 'admin@trebolsoft.com', '[hash]', 'Admin', '0000', 'Todas', 'admin', true);
```

---

## 🧪 PRUEBAS DE DIAGNÓSTICO

### Test 1: Backend responde
```powershell
curl https://trebolsoftv1-latest.onrender.com/health
# Esperado: {"status":"ok"}
```

### Test 2: Endpoint de login disponible
```powershell
curl -X POST https://trebolsoftv1-latest.onrender.com/api/v1/auth/token `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=admin&password=admin123"
```

### Test 3: Frontend carga
```
Abrir: https://app.trebolsoft.com
Debería cargar sin errores
```

### Test 4: Frontend se conecta a backend
```
F12 → Network → Intentar login
Ver si la petición va a la URL correcta de Render
```

---

## 📞 SIGUIENTE PASO

**Si sigues con problemas:**
1. Comparte el error exacto que ves en la consola del navegador (F12)
2. Comparte si el healthcheck del backend responde
3. Indica si estás probando local o producción

---

## ⚡ RESUMEN EJECUTIVO

```powershell
# SOLUCIÓN MÁS COMÚN (99% de los casos):

# Paso 1: Crear usuario admin
python create_admin.py

# Paso 2: Probar login con:
# Username: admin
# Password: admin123

# ✅ ¡Listo! Deberías poder entrar
```
