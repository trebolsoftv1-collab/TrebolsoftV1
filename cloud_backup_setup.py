#!/usr/bin/env python3
"""
☁️ Backup Automático a Google Drive / OneDrive
Sistema simple para subir backups automáticamente a la nube
"""

import os
import shutil
import subprocess
import time
from pathlib import Path

class CloudBackupManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / "backups"
        
        # Detectar servicios de nube instalados
        self.cloud_paths = self.detect_cloud_services()
        
    def detect_cloud_services(self):
        """Detectar servicios de nube instalados en Windows."""
        possible_paths = {
            "Google Drive": [
                Path.home() / "Google Drive",
                Path("C:/Users") / os.getenv("USERNAME", "") / "Google Drive",
                Path("G:/Mi unidad"),  # Drive montado
                Path("G:/My Drive")
            ],
            "OneDrive": [
                Path.home() / "OneDrive",
                Path("C:/Users") / os.getenv("USERNAME", "") / "OneDrive",
                Path.home() / "OneDrive - Personal"
            ],
            "Dropbox": [
                Path.home() / "Dropbox",
                Path("C:/Users") / os.getenv("USERNAME", "") / "Dropbox"
            ],
            "iCloud": [
                Path.home() / "iCloudDrive",
                Path("C:/Users") / os.getenv("USERNAME", "") / "iCloudDrive"
            ]
        }
        
        detected = {}
        for service, paths in possible_paths.items():
            for path in paths:
                if path.exists() and path.is_dir():
                    detected[service] = path
                    break
                    
        return detected
        
    def show_cloud_options(self):
        """Mostrar servicios de nube disponibles."""
        print("☁️ SERVICIOS DE NUBE DETECTADOS:")
        print("-" * 40)
        
        if not self.cloud_paths:
            print("❌ No se detectaron servicios de nube instalados")
            print("💡 Instala Google Drive, OneDrive o Dropbox")
            return None
            
        for i, (service, path) in enumerate(self.cloud_paths.items(), 1):
            free_space = self.get_free_space(path)
            print(f"{i}. {service}")
            print(f"   📁 Ruta: {path}")
            print(f"   💾 Espacio libre: {free_space}")
            print()
            
        return self.cloud_paths
        
    def get_free_space(self, path):
        """Obtener espacio libre en directorio."""
        try:
            total, used, free = shutil.disk_usage(path)
            free_gb = free / (1024**3)
            return f"{free_gb:.1f} GB"
        except:
            return "No disponible"
            
    def create_cloud_backup_folder(self, cloud_path, service_name):
        """Crear carpeta de backup en servicio de nube."""
        backup_folder = cloud_path / "TrebolSoft-Backups"
        backup_folder.mkdir(exist_ok=True)
        
        # Crear archivo README
        readme_content = f"""# 🛡️ Backups TrebolSoft

Esta carpeta contiene copias de seguridad automáticas de tu aplicación TrebolSoft.

📅 **Configurado**: {time.strftime('%Y-%m-%d %H:%M:%S')}
☁️ **Servicio**: {service_name}
🔄 **Frecuencia**: Semanal (domingos)

## 📦 Contenido de los backups:
- Base de datos completa (usuarios, clientes, créditos)
- Código de la aplicación
- Configuración del sistema
- Información de Git

## 🔄 Cómo restaurar:
1. Descargar el archivo .zip más reciente
2. Extraer en una carpeta nueva
3. Ejecutar: `python restore_system.py`
4. Seguir las instrucciones

## ⚠️ IMPORTANTE:
- NO eliminar esta carpeta
- Los backups se sincronizan automáticamente
- Mantener al menos 4 backups (1 mes)

---
Generado automáticamente por TrebolSoft Backup System
"""
        
        readme_file = backup_folder / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        return backup_folder
        
    def copy_backups_to_cloud(self, cloud_backup_folder):
        """Copiar backups locales a la nube."""
        if not self.backup_dir.exists():
            print("❌ No hay backups locales para copiar")
            return False
            
        backup_files = list(self.backup_dir.glob("trebolsoft_complete_backup_*.zip"))
        
        if not backup_files:
            print("❌ No se encontraron archivos de backup")
            return False
            
        print(f"📤 Copiando {len(backup_files)} backups a la nube...")
        
        copied = 0
        for backup_file in backup_files:
            try:
                destination = cloud_backup_folder / backup_file.name
                
                # Solo copiar si no existe o es más nuevo
                if not destination.exists() or backup_file.stat().st_mtime > destination.stat().st_mtime:
                    shutil.copy2(backup_file, destination)
                    print(f"✅ Copiado: {backup_file.name}")
                    copied += 1
                else:
                    print(f"⏭️ Ya existe: {backup_file.name}")
                    
            except Exception as e:
                print(f"❌ Error copiando {backup_file.name}: {e}")
                
        print(f"📦 Backups copiados: {copied}")
        return copied > 0
        
    def setup_automatic_sync(self, cloud_backup_folder, service_name):
        """Configurar sincronización automática."""
        print(f"⚙️ Configurando sincronización automática con {service_name}...")
        
        # Crear script de sincronización
        sync_script = self.base_dir / "sync_to_cloud.py"
        
        sync_content = f'''#!/usr/bin/env python3
"""
🔄 Script de Sincronización Automática
Copia nuevos backups a {service_name}
"""

import shutil
from pathlib import Path

def sync_backups():
    """Sincronizar backups a la nube."""
    backup_dir = Path(__file__).parent / "backups"
    cloud_dir = Path(r"{cloud_backup_folder}")
    
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
        
    print(f"🔄 Sincronizando {{len(backup_files)}} backups...")
    
    for backup_file in backup_files:
        destination = cloud_dir / backup_file.name
        
        try:
            if not destination.exists():
                shutil.copy2(backup_file, destination)
                print(f"✅ Sincronizado: {{backup_file.name}}")
            else:
                print(f"⏭️ Ya existe: {{backup_file.name}}")
                
        except Exception as e:
            print(f"❌ Error: {{e}}")
            
    print("🎉 Sincronización completada")

if __name__ == "__main__":
    sync_backups()
'''
        
        with open(sync_script, 'w', encoding='utf-8') as f:
            f.write(sync_content)
            
        print(f"✅ Script de sincronización creado: {sync_script}")
        
        # Instrucciones para programar en Windows
        print("\n📋 CONFIGURAR TAREA PROGRAMADA EN WINDOWS:")
        print("1. Abrir 'Programador de tareas' (Task Scheduler)")
        print("2. Crear tarea básica")
        print("3. Nombre: 'TrebolSoft Sync to Cloud'")
        print("4. Programar: Semanal, domingos, 3:00 AM")
        print(f"5. Acción: Iniciar programa")
        print(f"6. Programa: python")
        print(f"7. Argumentos: {sync_script}")
        print(f"8. Directorio: {self.base_dir}")
        
        return sync_script
        
    def test_cloud_access(self, cloud_path):
        """Probar acceso a la nube."""
        try:
            test_file = cloud_path / "trebolsoft_test.txt"
            test_file.write_text("Test de acceso TrebolSoft")
            
            if test_file.exists():
                test_file.unlink()
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Error de acceso: {e}")
            return False
            
    def configure_cloud_backup(self):
        """Configurar backup automático a la nube."""
        print("☁️ CONFIGURACIÓN DE BACKUP A LA NUBE")
        print("="*45)
        
        # Mostrar opciones
        cloud_options = self.show_cloud_options()
        if not cloud_options:
            return
            
        # Seleccionar servicio
        while True:
            try:
                choice = int(input(f"Selecciona servicio (1-{len(cloud_options)}) o 0 para cancelar: "))
                if choice == 0:
                    print("Configuración cancelada")
                    return
                if 1 <= choice <= len(cloud_options):
                    selected_service = list(cloud_options.keys())[choice - 1]
                    selected_path = cloud_options[selected_service]
                    break
                else:
                    print("Selección inválida")
            except ValueError:
                print("Por favor ingresa un número")
                
        print(f"\n🎯 Configurando backup en: {selected_service}")
        
        # Probar acceso
        if not self.test_cloud_access(selected_path):
            print("❌ No se puede acceder al servicio de nube")
            return
            
        # Crear carpeta de backup
        cloud_backup_folder = self.create_cloud_backup_folder(selected_path, selected_service)
        print(f"📁 Carpeta creada: {cloud_backup_folder}")
        
        # Copiar backups existentes
        self.copy_backups_to_cloud(cloud_backup_folder)
        
        # Configurar sincronización automática
        sync_script = self.setup_automatic_sync(cloud_backup_folder, selected_service)
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print(f"☁️ Servicio: {selected_service}")
        print(f"📁 Carpeta: {cloud_backup_folder}")
        print(f"🔄 Script: {sync_script}")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Configurar tarea programada en Windows (instrucciones arriba)")
        print("2. Probar sincronización: python sync_to_cloud.py")
        print("3. Verificar que se sincronice en tu aplicación de nube")

def main():
    """Función principal."""
    cloud_manager = CloudBackupManager()
    cloud_manager.configure_cloud_backup()

if __name__ == "__main__":
    main()