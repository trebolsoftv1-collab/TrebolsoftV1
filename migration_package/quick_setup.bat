@echo off
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
call .venv\Scripts\activate.bat

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
