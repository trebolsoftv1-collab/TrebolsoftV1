#!/usr/bin/env python3
"""
🛡️ CENTRO DE CONTROL DE BACKUPS - TrebolSoft
Menú principal para gestionar todas las opciones de backup
"""

import os
import sys
import subprocess
from pathlib import Path

class BackupControlCenter:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        
    def show_header(self):
        """Mostrar encabezado del sistema."""
        print("🛡️" + "="*50 + "🛡️")
        print("    CENTRO DE CONTROL DE BACKUPS - TREBOLSOFT")
        print("🛡️" + "="*50 + "🛡️")
        print()
        
    def show_menu(self):
        """Mostrar menú principal."""
        print("📋 OPCIONES DISPONIBLES:")
        print("-" * 30)
        print("1. 🔄 Hacer backup completo AHORA")
        print("2. 📊 Ver estado de backups")
        print("3. ⚙️ Configurar backups automáticos")
        print("4. 🔄 Restaurar desde backup")
        print("5. ☁️ Configurar backup a Google Drive")
        print("6. 🔄 Sincronizar con Google Drive")
        print("7. �📂 Abrir carpeta de backups")
        print("8. 📋 Ver log de backups")
        print("9. 🧹 Limpiar backups antiguos")
        print("10. ❓ Ayuda y guía")
        print("0. 🚪 Salir")
        print()
        
    def run_script(self, script_name, args=None):
        """Ejecutar script de Python."""
        try:
            script_path = self.base_dir / script_name
            if not script_path.exists():
                print(f"❌ No se encontró el script: {script_name}")
                return False
                
            cmd = [sys.executable, str(script_path)]
            if args:
                cmd.extend(args)
                
            result = subprocess.run(cmd, cwd=self.base_dir)
            return result.returncode == 0
            
        except Exception as e:
            print(f"❌ Error ejecutando {script_name}: {e}")
            return False
            
    def open_folder(self, folder_name):
        """Abrir carpeta en el explorador."""
        try:
            folder_path = self.base_dir / folder_name
            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)
                print(f"📁 Carpeta creada: {folder_name}")
                
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            else:  # Linux/Mac
                subprocess.run(['xdg-open', folder_path])
                
            print(f"📂 Abriendo: {folder_path}")
            
        except Exception as e:
            print(f"❌ Error abriendo carpeta: {e}")
            
    def show_help(self):
        """Mostrar ayuda y guía."""
        print("❓ GUÍA DE BACKUPS TREBOLSOFT")
        print("="*40)
        print()
        print("🎯 ¿QUÉ SE INCLUYE EN EL BACKUP?")
        print("✅ Base de datos completa (dev.db)")
        print("✅ Código de la aplicación (app/)")
        print("✅ Configuración (requirements.txt, .env.example)")
        print("✅ Migraciones de base de datos (alembic/)")
        print("✅ Información del repositorio Git")
        print()
        print("⏰ ¿CUÁNDO HACER BACKUP?")
        print("📅 Diario: Para uso intensivo (>20 usuarios)")
        print("📅 Semanal: Para uso normal (<20 usuarios)")
        print("📅 Antes de cambios importantes")
        print("📅 Antes de actualizaciones")
        print()
        print("💾 ¿DÓNDE SE GUARDAN?")
        print("📁 Carpeta: backups/")
        print("📦 Formato: ZIP comprimido")
        print("🏷️ Nombre: trebolsoft_complete_backup_YYYYMMDD_HHMMSS.zip")
        print()
        print("🔄 ¿CÓMO RESTAURAR?")
        print("1. Seleccionar backup de la lista")
        print("2. El sistema hace backup del estado actual")
        print("3. Restaura archivos seleccionados")
        print("4. Seguir instrucciones post-restauración")
        print()
        print("⚠️ RECOMENDACIONES:")
        print("🔹 Mantener al menos 7 backups")
        print("🔹 Probar restauración periódicamente")
        print("🔹 Verificar que .env esté configurado después de restaurar")
        print("🔹 Hacer backup antes de cambios importantes")
        print()
        input("Presiona Enter para continuar...")
        
    def show_backup_info(self):
        """Mostrar información de backups existentes."""
        backup_dir = self.base_dir / "backups"
        
        if not backup_dir.exists() or not list(backup_dir.glob("*.zip")):
            print("📂 No hay backups disponibles.")
            print("💡 Tip: Ejecuta la opción 1 para crear tu primer backup")
            return
            
        backups = list(backup_dir.glob("trebolsoft_complete_backup_*.zip"))
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        total_size = sum(b.stat().st_size for b in backups)
        total_size_mb = total_size / (1024 * 1024)
        
        print(f"📊 INFORMACIÓN DE BACKUPS:")
        print(f"📦 Total de backups: {len(backups)}")
        print(f"💾 Tamaño total: {total_size_mb:.1f} MB")
        print(f"📁 Ubicación: {backup_dir}")
        print()
        
        if backups:
            latest = backups[0]
            mtime = latest.stat().st_mtime
            import datetime
            date_str = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            size_mb = latest.stat().st_size / (1024 * 1024)
            
            print(f"📅 Último backup: {date_str}")
            print(f"📦 Tamaño: {size_mb:.1f} MB")
            print(f"📄 Archivo: {latest.name}")
            
    def cleanup_old_backups(self):
        """Limpiar backups antiguos interactivamente."""
        backup_dir = self.base_dir / "backups"
        
        if not backup_dir.exists():
            print("📂 No hay carpeta de backups")
            return
            
        backups = list(backup_dir.glob("trebolsoft_complete_backup_*.zip"))
        
        if len(backups) <= 3:
            print("📦 Tienes pocos backups, no se recomienda eliminar ninguno")
            return
            
        print(f"📊 Tienes {len(backups)} backups")
        
        try:
            keep_count = int(input("¿Cuántos backups quieres mantener? [7]: ") or "7")
            if keep_count <= 0:
                print("❌ Número inválido")
                return
                
            if len(backups) <= keep_count:
                print("✅ No hay backups que eliminar")
                return
                
            # Ordenar por fecha (más reciente primero)
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            to_delete = backups[keep_count:]
            total_size = sum(b.stat().st_size for b in to_delete) / (1024 * 1024)
            
            print(f"🗑️ Se eliminarán {len(to_delete)} backups antiguos ({total_size:.1f} MB)")
            
            if input("¿Continuar? (s/n): ").lower() in ['s', 'si', 'y', 'yes']:
                for backup in to_delete:
                    backup.unlink()
                    print(f"🗑️ Eliminado: {backup.name}")
                print("✅ Limpieza completada")
            else:
                print("❌ Operación cancelada")
                
        except ValueError:
            print("❌ Número inválido")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    def show_log(self):
        """Mostrar log de backups."""
        log_file = self.base_dir / "backup_log.txt"
        
        if not log_file.exists():
            print("📋 No hay log de backups disponible")
            return
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if not lines:
                print("📋 El log está vacío")
                return
                
            print("📋 ÚLTIMAS ENTRADAS DEL LOG:")
            print("-" * 40)
            
            # Mostrar últimas 20 líneas
            for line in lines[-20:]:
                print(line.strip())
                
        except Exception as e:
            print(f"❌ Error leyendo log: {e}")
            
    def run(self):
        """Ejecutar centro de control."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla
            
            self.show_header()
            self.show_menu()
            
            try:
                choice = input("Selecciona una opción (0-10): ").strip()
                
                if choice == "0":
                    print("👋 ¡Hasta luego!")
                    break
                    
                elif choice == "1":
                    print("🔄 Ejecutando backup completo...")
                    self.run_script("backup_complete.py")
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "2":
                    self.show_backup_info()
                    print()
                    self.run_script("backup_scheduler.py", ["--status"])
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "3":
                    self.run_script("backup_scheduler.py", ["--config"])
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "4":
                    print("🔄 Iniciando sistema de restauración...")
                    self.run_script("restore_system.py")
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "5":
                    print("☁️ Configurando backup a Google Drive...")
                    self.run_script("google_drive_setup.py")
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "6":
                    print("🔄 Sincronizando con Google Drive...")
                    if (self.base_dir / "sync_to_google_drive.py").exists():
                        self.run_script("sync_to_google_drive.py")
                    elif (self.base_dir / "manual_backup_to_drive").exists():
                        print("📂 Abriendo carpeta manual para subir a Google Drive...")
                        self.open_folder("manual_backup_to_drive")
                    else:
                        print("⚠️ Primero configura backup a Google Drive (opción 5)")
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "7":
                    self.open_folder("backups")
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "8":
                    self.show_log()
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "9":
                    self.cleanup_old_backups()
                    input("\nPresiona Enter para continuar...")
                    
                elif choice == "10":
                    self.show_help()
                    
                else:
                    print("❌ Opción inválida")
                    input("Presiona Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presiona Enter para continuar...")

def main():
    """Función principal."""
    control_center = BackupControlCenter()
    control_center.run()

if __name__ == "__main__":
    main()