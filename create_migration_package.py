#!/usr/bin/env python3
"""
🔄 Creador de Paquete de Migración - TrebolSoft
Prepara todo lo necesario para transferir el proyecto a una nueva computadora
"""

import os
import shutil
import zipfile
import json
import datetime
from pathlib import Path

class MigrationPackageCreator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.migration_dir = self.base_dir / "migration_package"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_migration_directory(self):
        """Crear directorio para el paquete de migración."""
        self.migration_dir.mkdir(exist_ok=True)
        
        # Limpiar contenido anterior
        for item in self.migration_dir.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
                
        print(f"📁 Directorio de migración creado: {self.migration_dir}")
        
    def copy_essential_files(self):
        """Copiar archivos esenciales del proyecto."""
        print("📋 Copiando archivos esenciales...")
        
        essential_files = [
            # Documentación y contexto
            "PROJECT_CONTEXT_FULL.md",
            "BACKUP_LOCATIONS_FINAL.md", 
            "DISASTER_RECOVERY.md",
            "BACKUP_GUIDE.md",
            "FRONTEND_SETUP_GUIDE.md",
            
            # Configuración
            "requirements.txt",
            ".env.example",
            "alembic.ini",
            "docker-compose.yml",
            "Dockerfile",
            "render.yaml",
            "entrypoint.sh",
            
            # Scripts de backup
            "backup_center.py",
            "backup_complete.py",
            "backup_scheduler.py",
            "google_drive_setup.py",
            "restore_system.py",
            
            # Instrucciones específicas
            "manual_backup_to_drive/INSTRUCCIONES_GOOGLE_DRIVE.txt"
        ]
        
        copied_files = []
        for file_path in essential_files:
            source = self.base_dir / file_path
            if source.exists():
                if source.is_file():
                    destination = self.migration_dir / file_path
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
                    copied_files.append(file_path)
                    print(f"✅ Copiado: {file_path}")
                    
        return copied_files
        
    def copy_backup_files(self):
        """Copiar backups más recientes."""
        print("💾 Copiando backups...")
        
        backup_source = self.base_dir / "backups"
        if not backup_source.exists():
            print("⚠️ No hay carpeta de backups")
            return []
            
        backup_destination = self.migration_dir / "backups"
        backup_destination.mkdir(exist_ok=True)
        
        # Copiar últimos 3 backups
        backup_files = list(backup_source.glob("trebolsoft_complete_backup_*.zip"))
        backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        copied_backups = []
        for backup_file in backup_files[:3]:  # Solo últimos 3
            destination = backup_destination / backup_file.name
            shutil.copy2(backup_file, destination)
            copied_backups.append(backup_file.name)
            print(f"💾 Backup copiado: {backup_file.name}")
            
        return copied_backups
        
    def create_migration_checklist(self, copied_files, copied_backups):
        """Crear lista de verificación para la migración."""
        checklist_content = f"""# ✅ LISTA DE VERIFICACIÓN PARA MIGRACIÓN - TrebolSoft

## 📅 **PAQUETE CREADO:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📦 **CONTENIDO DEL PAQUETE DE MIGRACIÓN**

### 📋 **ARCHIVOS ESENCIALES INCLUIDOS:**
{chr(10).join(f"✅ {file}" for file in copied_files)}

### 💾 **BACKUPS INCLUIDOS:**
{chr(10).join(f"💾 {backup}" for backup in copied_backups)}

---

## 🖥️ **PASOS PARA NUEVA COMPUTADORA**

### **PREPARACIÓN:**
- [ ] Instalar Python 3.12+
- [ ] Instalar Git
- [ ] Instalar VS Code
- [ ] Configurar cuenta GitHub (trebolsoftv1-collab)

### **DESCARGA DEL PROYECTO:**
```bash
# Clonar repositorio
git clone https://github.com/trebolsoftv1-collab/TrebolsoftV1.git
cd TrebolsoftV1

# Verificar branch correcto
git branch -a
git checkout main
```

### **RESTAURACIÓN DE ARCHIVOS:**
- [ ] Copiar archivos de migration_package/ al directorio del proyecto
- [ ] Verificar que PROJECT_CONTEXT_FULL.md esté actualizado
- [ ] Copiar backups/ al directorio del proyecto

### **CONFIGURACIÓN DEL ENTORNO:**
```bash
# Crear entorno virtual
python -m venv .venv
.venv\\Scripts\\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con valores reales
```

### **BASE DE DATOS:**
```bash
# Restaurar desde backup MÁS RECIENTE
python restore_system.py
# Seleccionar backup más reciente

# O migrar base de datos
alembic upgrade head
```

### **VERIFICACIÓN:**
```bash
# Probar backend
uvicorn app.main:app --reload
# Verificar: http://localhost:8000/health

# Probar sistema de backup
python backup_center.py
```

### **CONFIGURAR GOOGLE DRIVE:**
```bash
# Configurar backup a Google Drive
python google_drive_setup.py
# Seguir instrucciones para cuenta TrebolSoft
```

---

## 💬 **CONTINUIDAD CON GITHUB COPILOT**

### **EN LA PRIMERA SESIÓN EN NUEVA COMPUTADORA:**

**📝 Mensaje de inicio recomendado:**
```
Hola, estoy continuando el trabajo en TrebolSoft desde una nueva computadora.

CONTEXTO:
- Proyecto: Sistema de créditos con FastAPI + React
- Estado: Sistema completo con usuarios, clientes, backups configurados
- Deployment: Vercel (frontend) + Render (backend) 
- Dominio: app.trebolsoft.com funcionando

Tengo el archivo PROJECT_CONTEXT_FULL.md con todo el contexto.
¿Puedes revisar ese archivo y confirmar que entiendes el estado actual del proyecto?
```

### **ARCHIVOS CLAVE PARA COPILOT:**
- [ ] `PROJECT_CONTEXT_FULL.md` - Contexto completo
- [ ] `BACKUP_LOCATIONS_FINAL.md` - Estado de backups
- [ ] `app/main.py` - Backend principal
- [ ] `src/App.jsx` - Frontend principal (si existe)

---

## 🔐 **CONFIGURACIONES CRÍTICAS**

### **VARIABLES DE ENTORNO (.env):**
```bash
# Backend (NO incluidas en migración por seguridad)
DATABASE_URL=...
SECRET_KEY=...
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
APP_ENV=development
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://app.trebolsoft.com
```

### **CUENTAS NECESARIAS:**
- [ ] GitHub: trebolsoftv1-collab
- [ ] Render: Backend deployment
- [ ] Vercel: Frontend deployment  
- [ ] Cloudinary: Subida de imágenes
- [ ] Google Drive: Backup (cuenta TrebolSoft)
- [ ] Namecheap: Dominio trebolsoft.com

---

## ⚠️ **VERIFICACIONES FINALES**

### **FUNCIONALIDAD BÁSICA:**
- [ ] Login funciona con usuarios existentes
- [ ] CRUD de usuarios operativo
- [ ] CRUD de clientes operativo
- [ ] Subida de fotos funciona
- [ ] Roles y permisos correctos

### **SISTEMA DE BACKUP:**
- [ ] Backup local funciona
- [ ] Sincronización Google Drive configurada
- [ ] Restauración probada
- [ ] Scripts automáticos funcionando

### **DEPLOYMENT:**
- [ ] Frontend despliega automáticamente
- [ ] Backend despliega automáticamente
- [ ] Dominio app.trebolsoft.com funciona
- [ ] CORS configurado correctamente

---

## 📞 **DATOS DE CONTACTO PARA CONTINUIDAD**

**Repositorio principal:** https://github.com/trebolsoftv1-collab/TrebolsoftV1
**Dominio de aplicación:** https://app.trebolsoft.com
**API Backend:** https://trebolsoftv1-latest.onrender.com

---

**🎯 CON ESTA LISTA, LA MIGRACIÓN SERÁ SUAVE Y SIN PÉRDIDA DE CONTEXTO**
"""

        checklist_file = self.migration_dir / "MIGRATION_CHECKLIST.md"
        with open(checklist_file, 'w', encoding='utf-8') as f:
            f.write(checklist_content)
            
        print(f"✅ Lista de verificación creada: {checklist_file}")
        
    def create_quick_setup_script(self):
        """Crear script de configuración rápida."""
        setup_script_content = '''@echo off
REM 🚀 Script de Configuración Rápida - TrebolSoft
echo 🛡️ CONFIGURACIÓN RÁPIDA TREBOLSOFT
echo ====================================

echo 📋 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python no instalado. Instalar desde python.org
    pause
    exit /b 1
)

echo 📋 Verificando Git...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git no instalado. Instalar desde git-scm.com
    pause
    exit /b 1
)

echo 🔧 Creando entorno virtual...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

echo ⚡ Activando entorno virtual...
call .venv\\Scripts\\activate.bat

echo 📦 Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo 📁 Verificando archivos de configuración...
if not exist .env (
    copy .env.example .env
    echo ⚠️ Archivo .env creado. EDITAR con valores reales.
)

echo ✅ CONFIGURACIÓN COMPLETADA
echo 📋 PRÓXIMOS PASOS:
echo 1. Editar .env con valores reales
echo 2. Ejecutar: alembic upgrade head
echo 3. Ejecutar: uvicorn app.main:app --reload
echo 4. Probar: http://localhost:8000/health

pause
'''
        
        setup_script = self.migration_dir / "quick_setup.bat"
        with open(setup_script, 'w', encoding='utf-8') as f:
            f.write(setup_script_content)
            
        print(f"🚀 Script de configuración creado: {setup_script}")
        
    def create_migration_package(self):
        """Crear paquete completo de migración."""
        print("🔄 CREANDO PAQUETE DE MIGRACIÓN COMPLETO")
        print("="*50)
        
        # Crear directorio
        self.create_migration_directory()
        
        # Copiar archivos
        copied_files = self.copy_essential_files()
        copied_backups = self.copy_backup_files()
        
        # Crear documentación
        self.create_migration_checklist(copied_files, copied_backups)
        self.create_quick_setup_script()
        
        # Crear ZIP final
        zip_file = self.base_dir / f"trebolsoft_migration_package_{self.timestamp}.zip"
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.migration_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.migration_dir)
                    zipf.write(file_path, f"trebolsoft_migration/{arcname}")
                    
        # Información del paquete
        size_mb = zip_file.stat().st_size / (1024 * 1024)
        
        print("\n" + "="*50)
        print("🎉 PAQUETE DE MIGRACIÓN COMPLETADO")
        print("="*50)
        print(f"📦 Archivo: {zip_file}")
        print(f"💾 Tamaño: {size_mb:.2f} MB")
        print(f"📁 Contenido: {len(copied_files)} archivos + {len(copied_backups)} backups")
        
        print("\n📤 PASOS PARA TRANSFERIR:")
        print("1. Subir ZIP a Google Drive (cuenta TrebolSoft)")
        print("2. Descargar en nueva computadora")
        print("3. Extraer y seguir MIGRATION_CHECKLIST.md")
        print("4. Ejecutar quick_setup.bat")
        
        return zip_file

def main():
    """Función principal."""
    creator = MigrationPackageCreator()
    migration_package = creator.create_migration_package()
    
    # Abrir carpeta contenedora
    try:
        import os
        os.startfile(migration_package.parent)
    except:
        pass

if __name__ == "__main__":
    main()