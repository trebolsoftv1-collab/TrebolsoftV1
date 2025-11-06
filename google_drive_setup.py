#!/usr/bin/env python3
"""
🔒 Configurador de Backup para Google Drive - TrebolSoft
Sistema seguro para cuentas independientes (NO corporativas)
"""

import os
import shutil
import time
from pathlib import Path

class GoogleDriveBackupSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / "backups"
        
        # Posibles ubicaciones de Google Drive
        self.google_drive_paths = self.detect_google_drive()
        
    def detect_google_drive(self):
        """Detectar instalaciones de Google Drive."""
        username = os.getenv("USERNAME", "")
        
        possible_paths = [
            # Google Drive para escritorio (nuevo)
            Path(f"C:/Users/{username}/Google Drive"),
            Path("G:/Mi unidad"),  # Drive montado como G:
            Path("G:/My Drive"),   # Drive en inglés
            
            # Google Drive File Stream (empresarial)
            Path(f"C:/Users/{username}/Google Drive File Stream"),
            
            # Ubicaciones personalizadas comunes
            Path("D:/Google Drive"),
            Path("E:/Google Drive"),
            
            # Backup & Sync (versión antigua)
            Path(f"C:/Users/{username}/Google Drive"),
        ]
        
        detected = []
        for path in possible_paths:
            if path.exists() and path.is_dir():
                # Verificar si parece Google Drive real
                if self.is_google_drive_folder(path):
                    detected.append(path)
                    
        return detected
        
    def is_google_drive_folder(self, path):
        """Verificar si es una carpeta real de Google Drive."""
        try:
            # Buscar indicadores de Google Drive
            contents = list(path.iterdir())
            
            # Si tiene archivos típicos de Drive o está vacío/accesible
            return len(contents) >= 0  # Básicamente si podemos acceder
            
        except PermissionError:
            return False
        except Exception:
            return False
            
    def show_google_drive_options(self):
        """Mostrar opciones de Google Drive disponibles."""
        print("🔍 BUSCANDO GOOGLE DRIVE...")
        print("-" * 40)
        
        if not self.google_drive_paths:
            print("❌ No se detectó Google Drive instalado")
            print()
            print("📥 OPCIONES PARA INSTALAR GOOGLE DRIVE:")
            print("1. 🌐 Google Drive para escritorio (RECOMENDADO)")
            print("   - https://www.google.com/drive/download/")
            print("   - Sincronización automática")
            print("   - Gratis hasta 15GB")
            print()
            print("2. 📂 Usar carpeta manual")
            print("   - Crear carpeta que sincronices manualmente")
            print("   - Subir backups cuando quieras")
            print()
            return None
            
        print(f"✅ Google Drive encontrado:")
        for i, path in enumerate(self.google_drive_paths, 1):
            free_space = self.get_free_space(path)
            print(f"{i}. 📁 {path}")
            print(f"   💾 Espacio: {free_space}")
            
        print()
        print("🆕 Crear carpeta manual (si tienes Drive en el navegador)")
        print(f"{len(self.google_drive_paths) + 1}. 📂 Configurar carpeta personalizada")
        
        return self.google_drive_paths
        
    def get_free_space(self, path):
        """Obtener espacio libre."""
        try:
            total, used, free = shutil.disk_usage(path)
            free_gb = free / (1024**3)
            return f"{free_gb:.1f} GB libres"
        except:
            return "Verificando..."
            
    def create_manual_backup_folder(self):
        """Crear carpeta manual para Google Drive."""
        print("📂 CONFIGURACIÓN MANUAL DE GOOGLE DRIVE")
        print("="*45)
        print()
        print("📋 PASOS PARA CONFIGURAR:")
        print("1. Abre tu navegador web")
        print("2. Ve a https://drive.google.com")
        print("3. Inicia sesión con la cuenta de TrebolSoft")
        print("4. Crea una carpeta llamada 'TrebolSoft-Backups'")
        print()
        
        # Crear carpeta local que el usuario subirá manualmente
        manual_folder = self.base_dir / "manual_backup_to_drive"
        manual_folder.mkdir(exist_ok=True)
        
        # Crear instrucciones
        instructions = manual_folder / "INSTRUCCIONES_GOOGLE_DRIVE.txt"
        instructions_content = f"""🛡️ INSTRUCCIONES PARA BACKUP MANUAL A GOOGLE DRIVE

📅 Creado: {time.strftime('%Y-%m-%d %H:%M:%S')}

📋 PASOS A SEGUIR CADA SEMANA:

1. 🔄 HACER BACKUP:
   - Ejecutar: python backup_complete.py
   - Se creará archivo en: backups/trebolsoft_complete_backup_*.zip

2. 📤 SUBIR A GOOGLE DRIVE:
   - Abrir: https://drive.google.com (cuenta TrebolSoft)
   - Ir a carpeta: TrebolSoft-Backups
   - Arrastrar el archivo .zip más reciente
   - Verificar que se subió correctamente

3. 🧹 LIMPIAR LOCAL:
   - Mantener solo 3 backups locales más recientes
   - Eliminar backups antiguos para ahorrar espacio

📁 ESTRUCTURA EN GOOGLE DRIVE:
TrebolSoft-Backups/
├── trebolsoft_complete_backup_20251106_111712.zip
├── trebolsoft_complete_backup_20251113_020000.zip
├── trebolsoft_complete_backup_20251120_020000.zip
└── README.txt (este archivo)

⚠️ IMPORTANTE:
- NUNCA eliminar todos los backups
- Mantener al menos 4 backups (1 mes)
- Verificar que Google Drive tenga espacio suficiente
- Probar restauración cada 3 meses

🔄 PARA RESTAURAR:
1. Descargar .zip desde Google Drive
2. Copiar a: {self.base_dir}/backups/
3. Ejecutar: python restore_system.py
4. Seguir instrucciones en pantalla

💡 TIP: Crear recordatorio semanal en tu calendario
📧 Cuenta recomendada: Gmail de TrebolSoft (NO corporativa)
"""
        
        with open(instructions, 'w', encoding='utf-8') as f:
            f.write(instructions_content)
            
        # Copiar backup actual a la carpeta manual
        if self.backup_dir.exists():
            backup_files = list(self.backup_dir.glob("trebolsoft_complete_backup_*.zip"))
            for backup_file in backup_files:
                destination = manual_folder / backup_file.name
                shutil.copy2(backup_file, destination)
                print(f"📦 Backup copiado: {backup_file.name}")
                
        print(f"📁 Carpeta creada: {manual_folder}")
        print(f"📄 Instrucciones: {instructions}")
        print()
        print("📤 PRÓXIMOS PASOS:")
        print("1. Abrir carpeta manual_backup_to_drive")
        print("2. Subir archivos a https://drive.google.com")
        print("3. Seguir las instrucciones del archivo TXT")
        
        return manual_folder
        
    def create_drive_sync_folder(self, drive_path):
        """Crear carpeta de backup en Google Drive instalado."""
        backup_folder = drive_path / "TrebolSoft-Backups"
        backup_folder.mkdir(exist_ok=True)
        
        # Crear archivo README
        readme_content = f"""🛡️ BACKUPS AUTOMÁTICOS TREBOLSOFT

📅 Configurado: {time.strftime('%Y-%m-%d %H:%M:%S')}
☁️ Ubicación: Google Drive (cuenta TrebolSoft)
🔄 Sincronización: Automática

📦 CONTENIDO DE BACKUPS:
✅ Base de datos completa (usuarios, clientes, créditos)
✅ Código de aplicación (app/, alembic/)
✅ Configuración del sistema
✅ Estado de Git y migraciones

🚨 IMPORTANTE:
- Esta carpeta se sincroniza automáticamente con Google Drive
- NO eliminar archivos manualmente
- Los backups se crean semanalmente
- Se mantienen 7 backups (últimas 7 semanas)

🔄 PARA RESTAURAR:
1. Usar el archivo .zip más reciente
2. Ejecutar: python restore_system.py
3. Seguir instrucciones en pantalla

⚠️ SEGURIDAD:
- Solo para cuenta de Gmail de TrebolSoft
- NO usar cuenta corporativa
- Verificar regularmente que se sincroniza

---
Sistema de Backup TrebolSoft v1.0
"""
        
        readme_file = backup_folder / "README.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        return backup_folder
        
    def copy_backups_to_drive(self, drive_backup_folder):
        """Copiar backups a Google Drive."""
        if not self.backup_dir.exists():
            print("❌ No hay backups locales para copiar")
            return False
            
        backup_files = list(self.backup_dir.glob("trebolsoft_complete_backup_*.zip"))
        
        if not backup_files:
            print("❌ No se encontraron archivos de backup")
            return False
            
        print(f"📤 Copiando {len(backup_files)} backups a Google Drive...")
        
        copied = 0
        for backup_file in backup_files:
            try:
                destination = drive_backup_folder / backup_file.name
                
                if not destination.exists():
                    shutil.copy2(backup_file, destination)
                    print(f"✅ Copiado: {backup_file.name}")
                    copied += 1
                else:
                    print(f"⏭️ Ya existe: {backup_file.name}")
                    
            except Exception as e:
                print(f"❌ Error copiando {backup_file.name}: {e}")
                
        print(f"📦 Total copiado: {copied} archivos")
        return copied > 0
        
    def create_drive_sync_script(self, drive_backup_folder):
        """Crear script de sincronización para Google Drive."""
        sync_script = self.base_dir / "sync_to_google_drive.py"
        
        sync_content = f'''#!/usr/bin/env python3
"""
🔄 Sincronización Automática a Google Drive - TrebolSoft
Cuenta: Gmail de TrebolSoft (NO corporativa)
"""

import shutil
from pathlib import Path

def sync_to_google_drive():
    """Sincronizar backups a Google Drive."""
    backup_dir = Path(__file__).parent / "backups"
    drive_dir = Path(r"{drive_backup_folder}")
    
    if not backup_dir.exists():
        print("❌ No hay carpeta de backups local")
        return
        
    if not drive_dir.exists():
        print("❌ Google Drive no está disponible")
        print("💡 Verifica que Google Drive esté funcionando")
        return
        
    backup_files = list(backup_dir.glob("trebolsoft_complete_backup_*.zip"))
    
    if not backup_files:
        print("📦 No hay backups nuevos para sincronizar")
        return
        
    print(f"🔄 Sincronizando {{len(backup_files)}} backups a Google Drive...")
    
    synced = 0
    for backup_file in backup_files:
        destination = drive_dir / backup_file.name
        
        try:
            # Solo sincronizar si no existe o es más nuevo
            if not destination.exists() or backup_file.stat().st_mtime > destination.stat().st_mtime:
                shutil.copy2(backup_file, destination)
                print(f"✅ Sincronizado: {{backup_file.name}}")
                synced += 1
            else:
                print(f"⏭️ Ya sincronizado: {{backup_file.name}}")
                
        except Exception as e:
            print(f"❌ Error sincronizando {{backup_file.name}}: {{e}}")
            
    if synced > 0:
        print(f"🎉 Sincronización completada: {{synced}} archivos")
        print("☁️ Verifica en https://drive.google.com que se subieron correctamente")
    else:
        print("✅ Todo ya estaba sincronizado")

if __name__ == "__main__":
    sync_to_google_drive()
'''
        
        with open(sync_script, 'w', encoding='utf-8') as f:
            f.write(sync_content)
            
        print(f"✅ Script de sincronización creado: {sync_script}")
        return sync_script
        
    def configure_google_drive_backup(self):
        """Configurar backup completo para Google Drive."""
        print("🔒 CONFIGURACIÓN DE BACKUP PARA GOOGLE DRIVE")
        print("="*50)
        print("📧 Para cuenta INDEPENDIENTE de TrebolSoft")
        print("❌ NO usar cuenta corporativa")
        print()
        
        # Mostrar opciones
        drive_paths = self.show_google_drive_options()
        
        if not drive_paths:
            # No hay Google Drive instalado - configuración manual
            manual_folder = self.create_manual_backup_folder()
            
            print("\n🎯 CONFIGURACIÓN MANUAL COMPLETADA")
            print(f"📁 Carpeta: {manual_folder}")
            print("📧 Cuenta recomendada: Gmail de TrebolSoft")
            
            # Abrir carpeta
            try:
                import os
                os.startfile(manual_folder)
                print("📂 Carpeta abierta automáticamente")
            except:
                pass
                
            return
            
        # Google Drive está instalado
        print(f"Opciones disponibles: 1-{len(drive_paths) + 1}")
        
        while True:
            try:
                choice = int(input("Selecciona opción o 0 para cancelar: "))
                if choice == 0:
                    print("Configuración cancelada")
                    return
                elif 1 <= choice <= len(drive_paths):
                    selected_path = drive_paths[choice - 1]
                    break
                elif choice == len(drive_paths) + 1:
                    # Configuración manual
                    self.create_manual_backup_folder()
                    return
                else:
                    print("Selección inválida")
            except ValueError:
                print("Por favor ingresa un número")
                
        print(f"\n🎯 Configurando Google Drive: {selected_path}")
        
        # Crear carpeta de backup
        drive_backup_folder = self.create_drive_sync_folder(selected_path)
        print(f"📁 Carpeta creada: {drive_backup_folder}")
        
        # Copiar backups existentes
        self.copy_backups_to_drive(drive_backup_folder)
        
        # Crear script de sincronización
        sync_script = self.create_drive_sync_script(drive_backup_folder)
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print(f"☁️ Google Drive: {selected_path}")
        print(f"📁 Backups: {drive_backup_folder}")
        print(f"🔄 Script: {sync_script}")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. ✅ Verificar que Google Drive esté sincronizando")
        print("2. 🔄 Probar: python sync_to_google_drive.py")
        print("3. 🌐 Confirmar en https://drive.google.com")
        print("4. ⏰ Configurar tarea programada (opcional)")

def main():
    """Función principal."""
    setup = GoogleDriveBackupSetup()
    setup.configure_google_drive_backup()

if __name__ == "__main__":
    main()