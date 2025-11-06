#!/usr/bin/env python3
"""
🛡️ Sistema de Backup Completo para TrebolSoft
Crea copias de seguridad de: Base de datos, archivos, configuración y código
"""

import os
import shutil
import zipfile
import datetime
import json
import subprocess
from pathlib import Path

class TrebolSoftBackup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / "backups"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def create_backup_directory(self):
        """Crear directorio de backups si no existe."""
        self.backup_dir.mkdir(exist_ok=True)
        daily_backup = self.backup_dir / f"backup_{self.timestamp}"
        daily_backup.mkdir(exist_ok=True)
        return daily_backup
        
    def backup_database(self, backup_path):
        """Backup de la base de datos SQLite."""
        print("📊 Realizando backup de base de datos...")
        
        db_files = ["dev.db", "dev.db-shm", "dev.db-wal"]  # Archivos SQLite
        db_backup_dir = backup_path / "database"
        db_backup_dir.mkdir(exist_ok=True)
        
        for db_file in db_files:
            source = self.base_dir / db_file
            if source.exists():
                destination = db_backup_dir / db_file
                shutil.copy2(source, destination)
                print(f"✅ Copiado: {db_file}")
        
        # Crear dump SQL como backup adicional
        try:
            dump_file = db_backup_dir / f"database_dump_{self.timestamp}.sql"
            subprocess.run([
                "sqlite3", str(self.base_dir / "dev.db"), 
                ".dump"
            ], stdout=open(dump_file, 'w'), check=True)
            print(f"✅ Dump SQL creado: {dump_file.name}")
        except Exception as e:
            print(f"⚠️ No se pudo crear dump SQL: {e}")
            
    def backup_configuration(self, backup_path):
        """Backup de archivos de configuración."""
        print("⚙️ Realizando backup de configuración...")
        
        config_backup_dir = backup_path / "configuration"
        config_backup_dir.mkdir(exist_ok=True)
        
        config_files = [
            ".env",
            ".env.example", 
            "requirements.txt",
            "alembic.ini",
            "docker-compose.yml",
            "Dockerfile",
            "entrypoint.sh",
            "render.yaml",
            "pyproject.toml"
        ]
        
        for config_file in config_files:
            source = self.base_dir / config_file
            if source.exists():
                destination = config_backup_dir / config_file
                shutil.copy2(source, destination)
                print(f"✅ Configuración copiada: {config_file}")
                
    def backup_application_code(self, backup_path):
        """Backup del código de la aplicación."""
        print("💻 Realizando backup del código de aplicación...")
        
        code_backup_dir = backup_path / "application"
        
        # Copiar directorio app/ completo
        app_source = self.base_dir / "app"
        if app_source.exists():
            app_destination = code_backup_dir / "app"
            shutil.copytree(app_source, app_destination)
            print("✅ Código de aplicación copiado")
            
        # Copiar alembic/
        alembic_source = self.base_dir / "alembic"
        if alembic_source.exists():
            alembic_destination = code_backup_dir / "alembic"
            shutil.copytree(alembic_source, alembic_destination)
            print("✅ Migraciones Alembic copiadas")
            
    def backup_git_info(self, backup_path):
        """Backup de información de Git."""
        print("📝 Guardando información de Git...")
        
        git_info = {}
        try:
            # Obtener información del repositorio
            git_info['branch'] = subprocess.check_output(
                ['git', 'branch', '--show-current'], 
                cwd=self.base_dir
            ).decode().strip()
            
            git_info['commit'] = subprocess.check_output(
                ['git', 'rev-parse', 'HEAD'], 
                cwd=self.base_dir
            ).decode().strip()
            
            git_info['remote_url'] = subprocess.check_output(
                ['git', 'remote', 'get-url', 'origin'], 
                cwd=self.base_dir
            ).decode().strip()
            
            git_info['status'] = subprocess.check_output(
                ['git', 'status', '--porcelain'], 
                cwd=self.base_dir
            ).decode().strip()
            
            # Guardar info en JSON
            git_file = backup_path / "git_info.json"
            with open(git_file, 'w') as f:
                json.dump(git_info, f, indent=2)
                
            print("✅ Información de Git guardada")
            
        except Exception as e:
            print(f"⚠️ No se pudo obtener info de Git: {e}")
            
    def create_backup_manifest(self, backup_path):
        """Crear manifiesto del backup."""
        print("📋 Creando manifiesto de backup...")
        
        manifest = {
            "backup_date": datetime.datetime.now().isoformat(),
            "backup_type": "complete_system",
            "application": "TrebolSoft",
            "version": "1.0",
            "contents": {
                "database": "Base de datos SQLite completa",
                "configuration": "Archivos de configuración y variables de entorno",
                "application_code": "Código fuente completo",
                "git_info": "Estado del repositorio Git"
            },
            "restoration_notes": [
                "1. Restaurar archivos de configuración",
                "2. Restaurar base de datos dev.db",
                "3. Restaurar código de aplicación",
                "4. Instalar dependencias: pip install -r requirements.txt",
                "5. Ejecutar migraciones: alembic upgrade head",
                "6. Iniciar aplicación: uvicorn app.main:app --reload"
            ]
        }
        
        manifest_file = backup_path / "BACKUP_MANIFEST.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
            
        print("✅ Manifiesto creado")
        
    def compress_backup(self, backup_path):
        """Comprimir backup completo."""
        print("🗜️ Comprimiendo backup...")
        
        zip_file = self.backup_dir / f"trebolsoft_complete_backup_{self.timestamp}.zip"
        
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in backup_path.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(backup_path)
                    zipf.write(file_path, arcname)
                    
        # Eliminar directorio descomprimido
        shutil.rmtree(backup_path)
        
        # Información del archivo
        size_mb = zip_file.stat().st_size / (1024 * 1024)
        print(f"✅ Backup comprimido: {zip_file.name}")
        print(f"📦 Tamaño: {size_mb:.2f} MB")
        
        return zip_file
        
    def cleanup_old_backups(self, keep_count=7):
        """Mantener solo los últimos N backups."""
        print(f"🧹 Limpiando backups antiguos (manteniendo últimos {keep_count})...")
        
        backup_files = []
        for backup_file in self.backup_dir.glob("trebolsoft_complete_backup_*.zip"):
            backup_files.append((backup_file, backup_file.stat().st_mtime))
            
        # Ordenar por fecha de modificación (más reciente primero)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Eliminar los más antiguos
        deleted_count = 0
        for backup_file, _ in backup_files[keep_count:]:
            backup_file.unlink()
            deleted_count += 1
            print(f"🗑️ Eliminado: {backup_file.name}")
            
        if deleted_count == 0:
            print("✅ No hay backups antiguos para eliminar")
            
    def run_complete_backup(self):
        """Ejecutar backup completo."""
        print("🛡️ INICIANDO BACKUP COMPLETO DE TREBOLSOFT")
        print("=" * 50)
        
        try:
            # Crear directorio de backup
            backup_path = self.create_backup_directory()
            print(f"📁 Directorio de backup: {backup_path}")
            
            # Ejecutar todos los backups
            self.backup_database(backup_path)
            self.backup_configuration(backup_path)
            self.backup_application_code(backup_path)
            self.backup_git_info(backup_path)
            self.create_backup_manifest(backup_path)
            
            # Comprimir y limpiar
            zip_file = self.compress_backup(backup_path)
            self.cleanup_old_backups()
            
            print("=" * 50)
            print("🎉 BACKUP COMPLETO EXITOSO")
            print(f"📦 Archivo: {zip_file}")
            print(f"📅 Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("=" * 50)
            
            return zip_file
            
        except Exception as e:
            print(f"❌ ERROR EN BACKUP: {e}")
            return None

def main():
    """Función principal."""
    backup_system = TrebolSoftBackup()
    backup_system.run_complete_backup()

if __name__ == "__main__":
    main()