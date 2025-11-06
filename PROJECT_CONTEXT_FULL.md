# 🧠 CONTEXTO COMPLETO TREBOLSOFT - Para Continuidad con Copilot

## 📋 **INFORMACIÓN ESENCIAL PARA GITHUB COPILOT**

### 🎯 **PROYECTO:** TrebolSoft - Sistema de gestión de créditos y cobranza
### 📅 **ÚLTIMA ACTUALIZACIÓN:** 6 de noviembre de 2025
### 👨‍💻 **DESARROLLADOR:** jpancha (GitHub: trebolsoftv1-collab)

---

## 🏗️ **ARQUITECTURA ACTUAL DEL SISTEMA**

### **FRONTEND:**
```
🌐 Dominio: https://app.trebolsoft.com
⚡ Framework: Vite 5.4.10 + React 19
🚀 Hosting: Vercel (auto-deploy desde GitHub)
📦 Dependencias principales:
  - React Router DOM (navegación)
  - Axios (HTTP requests)
  - Tailwind CSS (estilos)
  - React Hot Toast (notificaciones)
```

### **BACKEND:**
```
🌐 API: https://trebolsoftv1-latest.onrender.com
⚡ Framework: FastAPI + Python 3.12
🗄️ Base de datos: SQLite (dev.db) -> PostgreSQL (producción)
🚀 Hosting: Render Hobby ($7/mes)
📦 Dependencias principales:
  - SQLAlchemy 2.0 (ORM)
  - Alembic (migraciones)
  - Pydantic v2 (validación)
  - JWT (autenticación)
  - CORS configurado para app.trebolsoft.com
```

### **DOMINIO Y DNS:**
```
🌐 Dominio: trebolsoft.com (Namecheap, pagado 1 año)
📧 Subdominios configurados:
  - app.trebolsoft.com -> Vercel (frontend)
  - api.trebolsoft.com -> Render (backend) [pendiente]
```

---

## 👥 **SISTEMA DE USUARIOS Y ROLES**

### **JERARQUÍA IMPLEMENTADA:**
```
👑 ADMIN (máximo nivel)
├── Puede crear supervisores y cobradores
├── Ve todos los clientes
├── Asigna zonas geográficas
└── Control total del sistema

👔 SUPERVISOR (nivel medio)
├── Puede crear solo cobradores
├── Ve clientes de su zona + cobradores asignados
├── Asigna cobradores a clientes
└── Gestión regional

💼 COBRADOR (nivel básico)
├── Ve solo sus clientes asignados
├── Registra pagos y gestiona créditos
├── Actualiza información de clientes
└── Operación diaria
```

### **CAMPOS DE USUARIO:**
```python
- name: str (nombre completo)
- email: str (único, para login)
- phone: str (teléfono de contacto)
- role: Enum (admin, supervisor, collector)
- zone: str (zona geográfica asignada)
- supervisor_id: int (solo para cobradores)
- is_active: bool (habilitado/deshabilitado)
- password: str (hasheado con bcrypt)
```

---

## 🏠 **SISTEMA DE CLIENTES**

### **CAMPOS IMPLEMENTADOS:**
```python
- name: str (nombre completo)
- email: str (único, opcional)
- phone: str (teléfono principal)
- phone2: str (teléfono secundario)
- address: str (dirección completa)
- city: str (ciudad)
- zone: str (zona geográfica)
- credit_limit: Decimal (límite de crédito)
- current_balance: Decimal (saldo actual)
- collector_id: int (cobrador asignado)
- latitude: float (geolocalización)
- longitude: float (geolocalización)
- profile_photo: str (URL de Cloudinary)
- house_photo: str (URL de Cloudinary)
- is_active: bool (cliente activo)
```

### **LÓGICA DE ASIGNACIÓN:**
```
📋 REGLAS DE NEGOCIO:
- Admin: Puede asignar cualquier cobrador
- Supervisor: Solo cobradores de su zona
- Cobrador: Auto-asignado a sí mismo
- Zona del cliente debe coincidir con zona del cobrador
```

---

## 🛡️ **SISTEMA DE AUTENTICACIÓN**

### **IMPLEMENTACIÓN ACTUAL:**
```python
🔐 JWT Tokens con FastAPI
📧 Login: email + password
⏰ Expiración: configurable
🔒 Hash: bcrypt para passwords
🌐 CORS: configurado para app.trebolsoft.com
```

### **MIDDLEWARE DE SEGURIDAD:**
```python
- get_current_user(): Extrae usuario del token
- require_role(): Verificación de permisos por rol
- database_dependency: Inyección de sesión DB
- CORS habilitado para frontend
```

---

## 📸 **INTEGRACIÓN DE CLOUDINARY**

### **CONFIGURACIÓN:**
```
☁️ Cloudinary configurado para subida de fotos
📸 Tipos: profile_photo, house_photo
🔧 Variables de entorno:
  - CLOUDINARY_CLOUD_NAME
  - CLOUDINARY_API_KEY
  - CLOUDINARY_API_SECRET
```

### **FUNCIONALIDAD:**
```javascript
// Frontend: subida de imágenes
- Selección de archivo
- Upload a Cloudinary
- URL devuelta se guarda en base de datos
- Vista previa en interfaz
```

---

## 🗄️ **BASE DE DATOS Y MIGRACIONES**

### **ALEMBIC CONFIGURADO:**
```bash
📁 alembic/versions/ (migraciones)
⚙️ alembic.ini (configuración)
🔧 env.py (metadata configurado)

# Comandos principales:
alembic revision --autogenerate -m "descripción"
alembic upgrade head
alembic downgrade -1
```

### **MODELOS PRINCIPALES:**
```python
📁 app/models/
├── user.py (Usuario con roles)
├── client.py (Cliente con geolocalización)
└── base.py (Base SQLAlchemy)

📁 app/schemas/
├── user.py (Validación Pydantic)
├── client.py (Validación Pydantic)
└── auth.py (Login/Register schemas)
```

---

## 🛡️ **SISTEMA DE BACKUP CONFIGURADO**

### **ESTRATEGIA ACTUAL:**
```
💻 LOCAL: C:\Users\jpancha\TrebolsoftV1\backups\
  - Backup automático semanal (domingos 2:00 AM)
  - Mantiene 7 copias (7 semanas)
  - Script: backup_complete.py

☁️ GOOGLE DRIVE: Manual upload
  - Carpeta: manual_backup_to_drive/
  - Cuenta: Gmail TrebolSoft (NO corporativa)
  - Script: sync_to_google_drive.py

🌐 GITHUB: Código fuente
  - Repositorio: trebolsoftv1-collab/TrebolsoftV1
  - Auto-deploy configurado
  - NO incluye datos sensibles
```

### **ARCHIVOS DE BACKUP:**
```bash
📦 CONTENIDO COMPLETO:
✅ Base de datos (dev.db)
✅ Código aplicación (app/, alembic/)
✅ Configuración (requirements.txt, docker-compose.yml)
✅ Variables de entorno (.env.example)
✅ Estado de Git (branch, commit, changes)
```

---

## 🚀 **CONFIGURACIÓN DE DEPLOYMENT**

### **FRONTEND (VERCEL):**
```yaml
# Configuración automática
- Git integration: trebolsoftv1-collab/TrebolsoftV1
- Build command: npm run build
- Output directory: dist
- Auto-deploy: main branch
- Custom domain: app.trebolsoft.com
```

### **BACKEND (RENDER):**
```yaml
# render.yaml
- Build command: pip install -r requirements.txt
- Start command: ./entrypoint.sh
- Health check: /health
- Auto-deploy: main branch
- Custom domain: pendiente api.trebolsoft.com
```

### **VARIABLES DE ENTORNO:**
```bash
# Render (Backend)
DATABASE_URL=postgresql://...
APP_ENV=production
CORS_ALLOWED_ORIGINS=https://app.trebolsoft.com
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
SECRET_KEY=...

# Vercel (Frontend)
VITE_API_URL=https://trebolsoftv1-latest.onrender.com
```

---

## 🐛 **PROBLEMAS RESUELTOS**

### **CORS Issues (Resuelto):**
```python
# Problema: CORS bloqueaba requests desde frontend
# Solución: Configurar Settings class correctamente
# Archivo: app/core/__init__.py
# Importar Settings en main.py
```

### **Authentication Flow (Resuelto):**
```javascript
// Problema: Token no persistía entre sesiones
// Solución: localStorage + axios interceptors
// Archivo: frontend/src/services/api.js
```

### **Role-based Permissions (Implementado):**
```python
# Sistema completo de permisos por rol
# Middleware: require_role()
# Frontend: Conditional rendering por rol
```

---

## 📂 **ESTRUCTURA DE ARCHIVOS CRÍTICOS**

### **BACKEND:**
```
app/
├── main.py (punto de entrada)
├── core/
│   ├── __init__.py (Settings configurado)
│   ├── config.py (configuración)
│   └── database.py (conexión DB)
├── models/ (SQLAlchemy models)
├── schemas/ (Pydantic validation)
├── api/v1/ (endpoints REST)
└── utils/ (utilidades comunes)
```

### **FRONTEND:**
```
src/
├── main.jsx (punto de entrada)
├── App.jsx (routing principal)
├── components/
│   ├── UserForm.jsx (gestión usuarios)
│   ├── ClientForm.jsx (gestión clientes)
│   └── Layout.jsx (navbar + sidebar)
├── services/api.js (axios config)
└── pages/ (vistas principales)
```

---

## 🔧 **COMANDOS ESENCIALES**

### **DESARROLLO LOCAL:**
```bash
# Backend
cd TrebolsoftV1
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separado)
cd trebolsoft-frontend
npm install
npm run dev
```

### **BACKUP Y RESTAURACIÓN:**
```bash
# Backup completo
python backup_center.py

# Restaurar
python restore_system.py

# Sincronizar a Google Drive
python sync_to_google_drive.py
```

### **DEPLOYMENT:**
```bash
# Automático con git push
git add .
git commit -m "descripción"
git push  # Despliega automáticamente frontend y backend
```

---

## 🎯 **ESTADO ACTUAL DEL PROYECTO**

### **✅ COMPLETADO:**
- ✅ Sistema de usuarios con roles jerárquicos
- ✅ CRUD completo de clientes con geolocalización
- ✅ Autenticación JWT funcional
- ✅ Subida de fotos a Cloudinary
- ✅ Deployment automático configurado
- ✅ Sistema de backup completo
- ✅ CORS y permisos funcionando
- ✅ Base de datos con migraciones

### **🔄 EN PROCESO:**
- 🔄 Configuración de api.trebolsoft.com
- 🔄 Optimización de performance
- 🔄 Backup automático a Google Drive

### **📋 PENDIENTE:**
- 📋 Sistema de pagos y créditos
- 📋 Reportes y dashboards
- 📋 Notificaciones automáticas
- 📋 App móvil (futuro)

---

## 💼 **CONTEXTO DE NEGOCIO**

### **OBJETIVO:**
```
🎯 Sistema completo de gestión de créditos y cobranza
👥 Múltiples usuarios con roles diferenciados
📱 Interfaz moderna y fácil de usar
☁️ 100% en la nube, accesible desde cualquier lugar
🔒 Seguro y con backups automáticos
```

### **USUARIOS FINALES:**
```
🏢 Empresas de crédito y cobranza
👔 Supervisores de zona
💼 Cobradores de campo
📊 Administradores de sistema
```

---

## 🚀 **SIGUIENTE SESIÓN - PUNTOS CLAVE**

### **PARA CONTINUAR SIN PERDER CONTEXTO:**

1. **📝 Mencionar:** "Estoy trabajando en TrebolSoft, sistema de créditos con FastAPI + React"

2. **🔍 Referenciar:** "Tengo configurado sistema de usuarios con roles (admin/supervisor/collector)"

3. **💾 Estado:** "Backup funcionando, deployment automático configurado"

4. **🎯 Objetivo:** "Necesito continuar con [funcionalidad específica]"

5. **📁 Archivos clave:** 
   - `PROJECT_CONTEXT_FULL.md` (este archivo)
   - `BACKUP_LOCATIONS_FINAL.md` 
   - `app/main.py` y `src/App.jsx`

---

## ⚠️ **NOTAS IMPORTANTES**

### **🔐 SEGURIDAD:**
- NO subir archivos .env con secretos reales
- Usar .env.example como referencia
- Cuentas separadas (NO corporativas)

### **💾 BACKUP:**
- Siempre hacer backup antes de cambios grandes
- Verificar que Google Drive esté sincronizado
- Probar restauración cada mes

### **🚀 DEPLOYMENT:**
- Git push despliega automáticamente
- Verificar que frontend y backend estén funcionando
- Monitorear logs en Render y Vercel

---

**📞 CON ESTA INFORMACIÓN, CUALQUIER SESIÓN DE COPILOT PUEDE CONTINUAR EXACTAMENTE DONDE QUEDAMOS**