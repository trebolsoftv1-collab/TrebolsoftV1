# 🛡️ Guía de Copias de Seguridad - TrebolSoft

## 🚀 Inicio Rápido

### ✅ ¿Qué está incluido en el backup?
- **Base de datos completa** (todos tus usuarios y clientes)
- **Código de la aplicación** (app/, alembic/)
- **Configuración** (requirements.txt, docker-compose.yml, etc.)
- **Variables de entorno** (.env.example para referencia)
- **Estado de Git** (branch, commit, cambios pendientes)

### 🎯 Uso Simple - 3 Comandos Principales

```bash
# 1. 🛡️ HACER BACKUP COMPLETO AHORA
python backup_center.py
# Selecciona opción 1

# 2. 🔄 RESTAURAR DESDE BACKUP  
python restore_system.py
# Sigue las instrucciones interactivas

# 3. ⚙️ CONFIGURAR BACKUPS AUTOMÁTICOS
python backup_scheduler.py --config
```

---

## 📋 Centro de Control Principal

```bash
python backup_center.py
```

**Menú disponible:**
1. 🔄 Hacer backup completo AHORA
2. 📊 Ver estado de backups
3. ⚙️ Configurar backups automáticos  
4. 🔄 Restaurar desde backup
5. 📂 Abrir carpeta de backups
6. 📋 Ver log de backups
7. 🧹 Limpiar backups antiguos
8. ❓ Ayuda y guía

---

## ⏰ Backups Automáticos

### Configuración Recomendada:
- **Frecuencia**: Diario si tienes >20 usuarios, Semanal si tienes <20
- **Hora**: 02:00 AM (cuando no hay usuarios activos)
- **Retención**: 7 backups (1 semana de historial)

### Activar Automático:
```bash
python backup_scheduler.py --config
# Responde las preguntas para configurar

# Verificar estado
python backup_scheduler.py --status

# Ejecutar backup manual
python backup_scheduler.py --backup
```

---

## 🚨 Situaciones de Emergencia

### 💥 "Se borró mi base de datos"
```bash
python restore_system.py
# Selecciona el backup más reciente
# Sigue las instrucciones paso a paso
```

### 💻 "Mi servidor falló completamente"  
1. **Descargar backup**: Ve a carpeta `backups/`
2. **Nuevo servidor**: Instala Python y Git
3. **Restaurar**: `python restore_system.py`
4. **Configurar**: Revisa `.env` y ajusta variables
5. **Migrar**: `alembic upgrade head`
6. **Iniciar**: `uvicorn app.main:app --reload`

### 🔧 "Algo se rompió después de un cambio"
```bash
# Hacer backup del estado actual (por si acaso)
python backup_complete.py

# Restaurar al estado anterior
python restore_system.py
# Selecciona backup de antes del problema
```

---

## 📊 Monitoreo y Mantenimiento

### Verificar Estado Regular:
```bash
python backup_scheduler.py --status
```

### Información que verás:
- ✅ Si están habilitados los backups automáticos
- 📅 Fecha del último backup
- 💾 Número de backups disponibles
- 📦 Tamaño total ocupado

### Limpiar Espacio:
```bash
python backup_center.py
# Opción 7: Limpiar backups antiguos
```

---

## 🎯 Cuándo Hacer Backup

### 🔴 OBLIGATORIO - Antes de:
- Actualizar la aplicación
- Cambiar estructura de base de datos
- Modificar configuración de producción
- Hacer cambios importantes en el código

### 🟡 RECOMENDADO - Cada:
- Día (si tienes usuarios activos)
- Semana (uso moderado)
- Antes de deployments

### 🟢 OPCIONAL - Cuando:
- Agregues nuevos usuarios importantes
- Hagas cambios menores en la UI
- Antes de vacaciones (por si algo falla)

---

## 📁 Estructura de Archivos

```
TrebolsoftV1/
├── backups/                           # 📦 Carpeta de backups
│   └── trebolsoft_complete_backup_*.zip
├── backup_center.py                   # 🎮 Centro de control principal  
├── backup_complete.py                 # 🛡️ Sistema de backup completo
├── restore_system.py                  # 🔄 Sistema de restauración
├── backup_scheduler.py                # ⏰ Programador automático
├── backup_config.json                 # ⚙️ Configuración (se crea automáticamente)
└── backup_log.txt                     # 📋 Log de operaciones
```

---

## ⚠️ Notas Importantes

### 🔐 Seguridad:
- **`.env`** NO se incluye en backup (por seguridad)
- Se incluye **`.env.example`** como referencia
- **SIEMPRE** verifica `.env` después de restaurar

### 💾 Espacio en Disco:
- Cada backup: ~100KB - 10MB (depende del tamaño de tu DB)
- Se mantienen 7 backups por defecto
- Total estimado: <100MB

### 🚀 Rendimiento:
- Backup completo: 5-30 segundos
- Restauración: 1-5 minutos
- Sin impacto en aplicación en funcionamiento

---

## 🆘 Soporte

### ❓ Si algo no funciona:
1. **Verifica que tengas Python instalado**
2. **Ejecuta desde la carpeta correcta** (TrebolsoftV1/)
3. **Revisa el log**: `backup_log.txt`
4. **Asegúrate de tener permisos** de escritura en la carpeta

### 🐛 Errores Comunes:
- **"No se encuentra sqlite3"**: Normal, el backup de DB funciona igual
- **"Error de permisos"**: Ejecuta como administrador
- **"No hay backups"**: Ejecuta `backup_complete.py` primero

---

## ✅ Lista de Verificación Mensual

- [ ] Ejecutar backup manual
- [ ] Verificar que backups automáticos funcionan
- [ ] Probar restauración (en copia de prueba)
- [ ] Limpiar backups antiguos si es necesario
- [ ] Verificar espacio disponible en disco
- [ ] Revisar log por errores

---

**🛡️ Con este sistema, tu negocio TrebolSoft está 100% protegido contra pérdida de datos.**