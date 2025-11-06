# Script de Backup Manual para SQLite
# backup_database.py

import os
import shutil
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def backup_database():
    """Crear backup de la base de datos SQLite."""
    
    # Configuración
    DB_PATH = "dev.db"  # Tu archivo de base de datos
    BACKUP_DIR = "backups"
    
    # Crear directorio de backups
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Nombre del backup con fecha
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"trebolsoft_backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    try:
        # Copiar archivo
        shutil.copy2(DB_PATH, backup_path)
        
        # Comprimir (opcional)
        import zipfile
        zip_name = backup_path.replace('.db', '.zip')
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            zipf.write(backup_path, backup_name)
        
        # Eliminar .db sin comprimir
        os.remove(backup_path)
        
        print(f"✅ Backup creado: {zip_name}")
        
        # Limpiar backups antiguos (mantener últimos 7)
        cleanup_old_backups(BACKUP_DIR)
        
        return zip_name
        
    except Exception as e:
        print(f"❌ Error en backup: {e}")
        return None

def cleanup_old_backups(backup_dir, keep_count=7):
    """Mantener solo los últimos N backups."""
    backups = []
    for file in os.listdir(backup_dir):
        if file.startswith('trebolsoft_backup_') and file.endswith('.zip'):
            file_path = os.path.join(backup_dir, file)
            backups.append((file_path, os.path.getctime(file_path)))
    
    # Ordenar por fecha de creación
    backups.sort(key=lambda x: x[1], reverse=True)
    
    # Eliminar los más antiguos
    for backup_path, _ in backups[keep_count:]:
        os.remove(backup_path)
        print(f"🗑️ Backup antiguo eliminado: {os.path.basename(backup_path)}")

if __name__ == "__main__":
    backup_database()