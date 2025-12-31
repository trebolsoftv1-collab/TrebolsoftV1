# sync-forced-2025
"""
🤖 Sistema de Backup Automático para Render
Este script se ejecuta EN EL SERVIDOR de Render para hacer backups automáticos
"""

import os
import sys
import zipfile
import datetime
import requests
import json
from pathlib import Path

class RenderAutoBackup:
    def __init__(self):
        self.base_dir = Path("/opt/render/project/src")  # Ruta en Render
        self.backup_dir = self.base_dir / "temp_backups"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Configuración desde variables de entorno
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github_repo = os.getenv("GITHUB_REPO", "trebolsoftv1-collab/TrebolsoftV1")
        self.webhook_url = os.getenv("BACKUP_WEBHOOK_URL")  # Para notificaciones
        
    def create_server_backup(self):
        """Crear backup en el servidor de Render."""
        print(f"🛡️ Iniciando backup automático en servidor - {self.timestamp}")
        
        # Crear directorio temporal
        self.backup_dir.mkdir(exist_ok=True)
        backup_file = self.backup_dir / f"render_backup_{self.timestamp}.zip"
        
        try:
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                
                # 1. Base de datos
                db_file = self.base_dir / "dev.db"
                if db_file.exists():
                    zipf.write(db_file, "dev.db")
                    print("✅ Base de datos incluida")
                
                # 2. Aplicación crítica
                app_files = [
                    "app/models",
                    "app/schemas", 
                    "app/api",
                    "app/core",
                    "alembic/versions"
                ]
                
                for app_path in app_files:
                    full_path = self.base_dir / app_path
                    if full_path.exists():
                        if full_path.is_dir():
                            for file_path in full_path.rglob("*"):
                                if file_path.is_file():
                                    arcname = file_path.relative_to(self.base_dir)
                                    zipf.write(file_path, arcname)
                        else:
                            zipf.write(full_path, app_path)
                            
                print("✅ Código de aplicación incluido")
                
                # 3. Configuración
                config_files = ["requirements.txt", "alembic.ini", "render.yaml"]
                for config_file in config_files:
                    file_path = self.base_dir / config_file
                    if file_path.exists():
                        zipf.write(file_path, config_file)
                        
                print("✅ Configuración incluida")
                
                # 4. Manifiesto
                manifest = {
                    "backup_date": datetime.datetime.now().isoformat(),
                    "backup_type": "render_automatic",
                    "server": "render",
                    "app_version": "1.0"
                }
                
                manifest_content = json.dumps(manifest, indent=2)
                zipf.writestr("RENDER_BACKUP_MANIFEST.json", manifest_content)
                
            file_size = backup_file.stat().st_size / (1024 * 1024)
            print(f"📦 Backup creado: {file_size:.2f} MB")
            
            return backup_file
            
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
            return None
            
    def upload_to_github_releases(self, backup_file):
        """Subir backup a GitHub Releases."""
        if not self.github_token:
            print("⚠️ No hay token de GitHub configurado")
            return False
            
        try:
            # 1. Crear release
            release_data = {
                "tag_name": f"backup-{self.timestamp}",
                "name": f"Backup Automático {self.timestamp}",
                "body": f"Backup automático generado en Render el {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "draft": False,
                "prerelease": True
            }
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Crear release
            response = requests.post(
                f"https://api.github.com/repos/{self.github_repo}/releases",
                headers=headers,
                json=release_data
            )
            
            if response.status_code != 201:
                print(f"❌ Error creando release: {response.text}")
                return False
                
            release_id = response.json()["id"]
            upload_url = response.json()["upload_url"].replace("{?name,label}", "")
            
            print(f"✅ Release creado: {release_id}")
            
            # 2. Subir archivo
            file_name = backup_file.name
            upload_headers = {
                "Authorization": f"token {self.github_token}",
                "Content-Type": "application/zip"
            }
            
            with open(backup_file, 'rb') as f:
                file_data = f.read()
                
            upload_response = requests.post(
                f"{upload_url}?name={file_name}",
                headers=upload_headers,
                data=file_data
            )
            
            if upload_response.status_code == 201:
                download_url = upload_response.json()["browser_download_url"]
                print(f"✅ Backup subido: {download_url}")
                return True
            else:
                print(f"❌ Error subiendo archivo: {upload_response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error en GitHub: {e}")
            return False
            
    def send_notification(self, success, backup_info=None):
        """Enviar notificación de resultado."""
        if not self.webhook_url:
            return
            
        try:
            if success:
                message = f"✅ Backup automático completado: {backup_info}"
            else:
                message = f"❌ Error en backup automático: {self.timestamp}"
                
            payload = {
                "text": message,
                "timestamp": self.timestamp
            }
            
            requests.post(self.webhook_url, json=payload, timeout=10)
            
        except Exception as e:
            print(f"⚠️ Error enviando notificación: {e}")
            
    def cleanup_temp_files(self):
        """Limpiar archivos temporales."""
        try:
            if self.backup_dir.exists():
                for file in self.backup_dir.glob("*"):
                    file.unlink()
                self.backup_dir.rmdir()
                print("🧹 Archivos temporales limpiados")
        except Exception as e:
            print(f"⚠️ Error limpiando: {e}")
            
    def run_automatic_backup(self):
        """Ejecutar backup automático completo."""
        print("🤖 INICIANDO BACKUP AUTOMÁTICO EN RENDER")
        print("="*50)
        
        try:
            # Crear backup
            backup_file = self.create_server_backup()
            if not backup_file:
                self.send_notification(False)
                return False
                
            # Subir a GitHub
            upload_success = self.upload_to_github_releases(backup_file)
            
            # Notificar resultado
            if upload_success:
                self.send_notification(True, f"Backup {self.timestamp}")
                print("🎉 BACKUP AUTOMÁTICO COMPLETADO")
            else:
                self.send_notification(False)
                print("⚠️ BACKUP CREADO PERO NO SUBIDO")
                
            return upload_success
            
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: {e}")
            self.send_notification(False)
            return False
            
        finally:
            # Siempre limpiar archivos temporales
            self.cleanup_temp_files()

def main():
    """Función principal para cron/scheduled tasks."""
    backup_system = RenderAutoBackup()
    
    # Verificar si es hora de backup (solo ejecutar una vez al día)
    current_hour = datetime.datetime.now().hour
    target_hour = int(os.getenv("BACKUP_HOUR", "2"))  # Default: 2 AM
    
    if current_hour == target_hour:
        backup_system.run_automatic_backup()
    else:
        print(f"⏰ No es hora de backup. Actual: {current_hour}h, Programado: {target_hour}h")

if __name__ == "__main__":
    main()