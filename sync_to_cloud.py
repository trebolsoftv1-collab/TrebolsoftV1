#!/usr/bin/env python3
"""
🔄 Script de Sincronización Automática
Copia nuevos backups a OneDrive
"""

# sync-forced-2025

import shutil
from pathlib import Path

def sync_backups():
    """Sincronizar backups a la nube."""
    backup_dir = Path(__file__).parent / "backups"
    cloud_dir = Path(r"C:\Users\jpancha\OneDrive\TrebolSoft-Backups")
    
    if not backup_dir.exists():
        print("❌ No hay carpeta de backups")
        return
        
    if not cloud_dir.exists():
        print("❌ Carpeta de nube no disponible")
        return
        
    backup_files = list(backup_dir.glob("trebolsoft_complete_backup_*.zip"))
    
    if not backup_files:
        print("📦 No hay backups nuevos")
        return
        
    print(f"🔄 Sincronizando {len(backup_files)} backups...")
    
    for backup_file in backup_files:
        destination = cloud_dir / backup_file.name
        
        try:
            if not destination.exists():
                shutil.copy2(backup_file, destination)
                print(f"✅ Sincronizado: {backup_file.name}")
            else:
                print(f"⏭️ Ya existe: {backup_file.name}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            
    print("🎉 Sincronización completada")

if __name__ == "__main__":
    sync_backups()
