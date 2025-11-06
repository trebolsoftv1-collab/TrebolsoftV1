#!/usr/bin/env python3
"""
🔄 Sistema de Restauración para TrebolSoft
Restaura una copia de seguridad completa del sistema
"""

import os
import shutil
import zipfile
import json
import subprocess
from pathlib import Path

class TrebolSoftRestore:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / "backups"
        
    def list_available_backups(self):
        """Listar backups disponibles."""
        print("📦 Backups disponibles:")
        print("-" * 40)
        
        backup_files = []
        for backup_file in self.backup_dir.glob("trebolsoft_complete_backup_*.zip"):
            size_mb = backup_file.stat().st_size / (1024 * 1024)
            mtime = backup_file.stat().st_mtime
            backup_files.append((backup_file, mtime, size_mb))
            
        # Ordenar por fecha (más reciente primero)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        for i, (backup_file, mtime, size_mb) in enumerate(backup_files, 1):
            date_str = Path(backup_file).stem.split('_')[-2:]
            date_str = f"{date_str[0]} {date_str[1][:2]}:{date_str[1][2:4]}:{date_str[1][4:6]}"
            print(f"{i}. {backup_file.name}")
            print(f"   📅 Fecha: {date_str}")
            print(f"   📦 Tamaño: {size_mb:.2f} MB")
            print()
            
        return backup_files
        
    def extract_backup(self, backup_file):
        """Extraer backup seleccionado."""
        print(f"📂 Extrayendo backup: {backup_file.name}")
        
        extract_dir = self.base_dir / "restore_temp"
        extract_dir.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(extract_dir)
            
        print("✅ Backup extraído")
        return extract_dir
        
    def read_manifest(self, extract_dir):
        """Leer manifiesto del backup."""
        manifest_file = extract_dir / "BACKUP_MANIFEST.json"
        if manifest_file.exists():
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            print("📋 Manifiesto del backup:")
            print(f"   📅 Fecha: {manifest['backup_date']}")
            print(f"   🏷️ Tipo: {manifest['backup_type']}")
            print(f"   📱 Aplicación: {manifest['application']}")
            return manifest
        return None
        
    def backup_current_system(self):
        """Crear backup del sistema actual antes de restaurar."""
        print("⚠️ Creando backup de seguridad del sistema actual...")
        
        current_backup_dir = self.base_dir / "pre_restore_backup"
        current_backup_dir.mkdir(exist_ok=True)
        
        # Backup rápido de archivos críticos
        critical_files = ["dev.db", ".env", "requirements.txt"]
        
        for file_name in critical_files:
            source = self.base_dir / file_name
            if source.exists():
                destination = current_backup_dir / file_name
                shutil.copy2(source, destination)
                print(f"✅ Respaldado: {file_name}")
                
    def restore_database(self, extract_dir):
        """Restaurar base de datos."""
        print("📊 Restaurando base de datos...")
        
        db_backup_dir = extract_dir / "database"
        if not db_backup_dir.exists():
            print("⚠️ No se encontró backup de base de datos")
            return False
            
        # Restaurar archivos de base de datos
        db_files = ["dev.db", "dev.db-shm", "dev.db-wal"]
        
        for db_file in db_files:
            source = db_backup_dir / db_file
            if source.exists():
                destination = self.base_dir / db_file
                # Hacer backup del archivo actual si existe
                if destination.exists():
                    backup_dest = self.base_dir / f"{db_file}.bak"
                    shutil.move(destination, backup_dest)
                
                shutil.copy2(source, destination)
                print(f"✅ Restaurado: {db_file}")
                
        return True
        
    def restore_configuration(self, extract_dir):
        """Restaurar configuración."""
        print("⚙️ Restaurando configuración...")
        
        config_backup_dir = extract_dir / "configuration"
        if not config_backup_dir.exists():
            print("⚠️ No se encontró backup de configuración")
            return False
            
        config_files = [
            ".env.example",  # .env NO se restaura por seguridad
            "requirements.txt",
            "alembic.ini",
            "docker-compose.yml",
            "Dockerfile",
            "entrypoint.sh",
            "render.yaml",
            "pyproject.toml"
        ]
        
        for config_file in config_files:
            source = config_backup_dir / config_file
            if source.exists():
                destination = self.base_dir / config_file
                shutil.copy2(source, destination)
                print(f"✅ Restaurado: {config_file}")
                
        print("⚠️ NOTA: .env NO restaurado por seguridad. Revisar manualmente.")
        return True
        
    def restore_application(self, extract_dir):
        """Restaurar código de aplicación."""
        print("💻 Restaurando código de aplicación...")
        
        app_backup_dir = extract_dir / "application"
        if not app_backup_dir.exists():
            print("⚠️ No se encontró backup de aplicación")
            return False
            
        # Restaurar app/
        app_source = app_backup_dir / "app"
        if app_source.exists():
            app_destination = self.base_dir / "app"
            if app_destination.exists():
                shutil.move(app_destination, self.base_dir / "app.bak")
            shutil.copytree(app_source, app_destination)
            print("✅ Código de aplicación restaurado")
            
        # Restaurar alembic/
        alembic_source = app_backup_dir / "alembic"
        if alembic_source.exists():
            alembic_destination = self.base_dir / "alembic"
            if alembic_destination.exists():
                shutil.move(alembic_destination, self.base_dir / "alembic.bak")
            shutil.copytree(alembic_source, alembic_destination)
            print("✅ Migraciones Alembic restauradas")
            
        return True
        
    def show_git_info(self, extract_dir):
        """Mostrar información de Git del backup."""
        git_file = extract_dir / "git_info.json"
        if git_file.exists():
            with open(git_file, 'r') as f:
                git_info = json.load(f)
            
            print("📝 Información de Git del backup:")
            print(f"   🌿 Rama: {git_info.get('branch', 'N/A')}")
            print(f"   📝 Commit: {git_info.get('commit', 'N/A')[:8]}...")
            print(f"   🔗 Remoto: {git_info.get('remote_url', 'N/A')}")
            
            if git_info.get('status'):
                print("   ⚠️ Había cambios sin commitear en el backup")
            else:
                print("   ✅ Estado limpio en el backup")
                
    def post_restore_instructions(self):
        """Mostrar instrucciones post-restauración."""
        print("\n" + "="*50)
        print("🔄 RESTAURACIÓN COMPLETADA")
        print("="*50)
        print("📋 PASOS SIGUIENTES OBLIGATORIOS:")
        print()
        print("1️⃣ Verificar archivo .env:")
        print("   - Revisar variables de entorno")
        print("   - Actualizar si es necesario")
        print()
        print("2️⃣ Instalar dependencias:")
        print("   pip install -r requirements.txt")
        print()
        print("3️⃣ Ejecutar migraciones:")
        print("   alembic upgrade head")
        print()
        print("4️⃣ Probar aplicación:")
        print("   uvicorn app.main:app --reload")
        print()
        print("5️⃣ Verificar base de datos:")
        print("   - Comprobar que los datos estén completos")
        print("   - Probar funcionalidad de login")
        print()
        print("⚠️ ARCHIVOS DE RESPALDO:")
        print("   - Sistema anterior: pre_restore_backup/")
        print("   - Archivos .bak en caso de problemas")
        print("="*50)
        
    def cleanup_restore_temp(self):
        """Limpiar archivos temporales de restauración."""
        temp_dir = self.base_dir / "restore_temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("🧹 Archivos temporales eliminados")
            
    def interactive_restore(self):
        """Proceso interactivo de restauración."""
        print("🔄 SISTEMA DE RESTAURACIÓN TREBOLSOFT")
        print("="*50)
        
        # Listar backups disponibles
        backup_files = self.list_available_backups()
        
        if not backup_files:
            print("❌ No se encontraron backups. Ejecuta backup_complete.py primero.")
            return
            
        # Seleccionar backup
        while True:
            try:
                choice = int(input(f"Selecciona backup (1-{len(backup_files)}) o 0 para cancelar: "))
                if choice == 0:
                    print("Operación cancelada")
                    return
                if 1 <= choice <= len(backup_files):
                    selected_backup = backup_files[choice - 1][0]
                    break
                else:
                    print("Selección inválida")
            except ValueError:
                print("Por favor ingresa un número")
                
        # Confirmación
        print(f"\n⚠️ ADVERTENCIA: Se restaurará desde {selected_backup.name}")
        print("Esto SOBRESCRIBIRÁ los archivos actuales.")
        confirm = input("¿Continuar? (escribe 'SI' para confirmar): ")
        
        if confirm != "SI":
            print("Operación cancelada")
            return
            
        try:
            # Backup del sistema actual
            self.backup_current_system()
            
            # Extraer backup seleccionado
            extract_dir = self.extract_backup(selected_backup)
            
            # Leer manifiesto
            manifest = self.read_manifest(extract_dir)
            
            # Mostrar información de Git
            self.show_git_info(extract_dir)
            
            # Ejecutar restauración
            print("\n🔄 Ejecutando restauración...")
            self.restore_database(extract_dir)
            self.restore_configuration(extract_dir)
            self.restore_application(extract_dir)
            
            # Limpiar archivos temporales
            self.cleanup_restore_temp()
            
            # Instrucciones finales
            self.post_restore_instructions()
            
        except Exception as e:
            print(f"❌ ERROR EN RESTAURACIÓN: {e}")
            print("🔄 Revisa pre_restore_backup/ para recuperar archivos")

def main():
    """Función principal."""
    restore_system = TrebolSoftRestore()
    restore_system.interactive_restore()

if __name__ == "__main__":
    main()