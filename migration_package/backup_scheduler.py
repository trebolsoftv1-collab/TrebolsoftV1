#!/usr/bin/env python3
"""
⏰ Programador de Backups Automáticos para TrebolSoft
Configura backups automáticos diarios/semanales
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class BackupScheduler:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "backup_config.json"
        self.log_file = self.base_dir / "backup_log.txt"
        
    def create_default_config(self):
        """Crear configuración por defecto."""
        default_config = {
            "backup_enabled": True,
            "backup_frequency": "daily",  # daily, weekly
            "backup_time": "02:00",  # HH:MM
            "keep_backups": 7,  # Número de backups a mantener
            "email_notifications": {
                "enabled": False,
                "email": "",
                "smtp_server": "",
                "smtp_port": 587,
                "username": "",
                "password": ""
            },
            "backup_locations": {
                "local": True,
                "cloud": False,  # Para futuro: Google Drive, Dropbox, etc.
                "external_drive": False
            },
            "last_backup": null,
            "backup_size_limit_mb": 500
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
            
        return default_config
        
    def load_config(self):
        """Cargar configuración."""
        if not self.config_file.exists():
            return self.create_default_config()
            
        with open(self.config_file, 'r') as f:
            return json.load(f)
            
    def save_config(self, config):
        """Guardar configuración."""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
            
    def log_message(self, message):
        """Escribir mensaje en log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(log_entry.strip())
        
    def check_backup_needed(self, config):
        """Verificar si es necesario hacer backup."""
        if not config.get("backup_enabled", False):
            return False
            
        last_backup = config.get("last_backup")
        if not last_backup:
            return True  # Primer backup
            
        last_backup_date = datetime.fromisoformat(last_backup)
        now = datetime.now()
        
        frequency = config.get("backup_frequency", "daily")
        
        if frequency == "daily":
            return (now - last_backup_date).days >= 1
        elif frequency == "weekly":
            return (now - last_backup_date).days >= 7
            
        return False
        
    def run_backup(self):
        """Ejecutar backup usando el script principal."""
        try:
            self.log_message("🛡️ Iniciando backup automático...")
            
            # Ejecutar script de backup
            backup_script = self.base_dir / "backup_complete.py"
            result = subprocess.run([
                sys.executable, str(backup_script)
            ], capture_output=True, text=True, cwd=self.base_dir)
            
            if result.returncode == 0:
                self.log_message("✅ Backup completado exitosamente")
                return True
            else:
                self.log_message(f"❌ Error en backup: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_message(f"❌ Excepción durante backup: {e}")
            return False
            
    def update_last_backup(self, config):
        """Actualizar fecha del último backup."""
        config["last_backup"] = datetime.now().isoformat()
        self.save_config(config)
        
    def check_disk_space(self):
        """Verificar espacio disponible en disco."""
        try:
            total, used, free = shutil.disk_usage(self.base_dir)
            free_mb = free / (1024 * 1024)
            
            if free_mb < 1000:  # Menos de 1GB libre
                self.log_message(f"⚠️ Poco espacio libre: {free_mb:.0f} MB")
                return False
                
            return True
            
        except Exception as e:
            self.log_message(f"❌ Error verificando espacio: {e}")
            return False
            
    def cleanup_logs(self):
        """Limpiar logs antiguos (mantener últimos 30 días)."""
        try:
            if not self.log_file.exists():
                return
                
            # Leer todas las líneas
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Filtrar líneas de los últimos 30 días
            cutoff_date = datetime.now() - timedelta(days=30)
            filtered_lines = []
            
            for line in lines:
                if line.startswith('['):
                    try:
                        date_str = line[1:20]  # [YYYY-MM-DD HH:MM:SS]
                        line_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        if line_date >= cutoff_date:
                            filtered_lines.append(line)
                    except:
                        filtered_lines.append(line)  # Mantener líneas que no se puedan parsear
                else:
                    filtered_lines.append(line)
                    
            # Escribir líneas filtradas
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.writelines(filtered_lines)
                
        except Exception as e:
            print(f"Error limpiando logs: {e}")
            
    def show_backup_status(self):
        """Mostrar estado de los backups."""
        config = self.load_config()
        
        print("📊 ESTADO DEL SISTEMA DE BACKUP")
        print("=" * 40)
        print(f"🔧 Habilitado: {'✅ Sí' if config.get('backup_enabled') else '❌ No'}")
        print(f"⏰ Frecuencia: {config.get('backup_frequency', 'No configurado')}")
        print(f"🕐 Hora: {config.get('backup_time', 'No configurado')}")
        print(f"📦 Mantener: {config.get('keep_backups', 0)} backups")
        
        last_backup = config.get('last_backup')
        if last_backup:
            last_date = datetime.fromisoformat(last_backup)
            print(f"📅 Último backup: {last_date.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("📅 Último backup: Nunca")
            
        # Verificar backups disponibles
        backup_dir = self.base_dir / "backups"
        if backup_dir.exists():
            backups = list(backup_dir.glob("trebolsoft_complete_backup_*.zip"))
            print(f"💾 Backups disponibles: {len(backups)}")
            
            if backups:
                total_size = sum(b.stat().st_size for b in backups)
                total_size_mb = total_size / (1024 * 1024)
                print(f"📦 Tamaño total: {total_size_mb:.1f} MB")
        else:
            print("💾 Backups disponibles: 0")
            
    def configure_scheduler(self):
        """Configurar programador de backups."""
        config = self.load_config()
        
        print("⚙️ CONFIGURACIÓN DE BACKUPS AUTOMÁTICOS")
        print("=" * 45)
        
        # Habilitar/deshabilitar backups
        while True:
            enable = input(f"¿Habilitar backups automáticos? (s/n) [{config.get('backup_enabled', True)}]: ").lower()
            if enable in ['s', 'si', 'y', 'yes', '']:
                config['backup_enabled'] = True
                break
            elif enable in ['n', 'no']:
                config['backup_enabled'] = False
                break
            else:
                print("Respuesta inválida. Usa 's' o 'n'")
                
        if not config['backup_enabled']:
            self.save_config(config)
            print("❌ Backups automáticos deshabilitados")
            return
            
        # Configurar frecuencia
        print("\nFrecuencia de backup:")
        print("1. Diario")
        print("2. Semanal")
        
        while True:
            freq_choice = input(f"Selecciona (1-2) [{1 if config.get('backup_frequency') == 'daily' else 2}]: ")
            if freq_choice == '1' or freq_choice == '':
                config['backup_frequency'] = 'daily'
                break
            elif freq_choice == '2':
                config['backup_frequency'] = 'weekly'
                break
            else:
                print("Selección inválida")
                
        # Configurar hora
        while True:
            time_input = input(f"Hora de backup (HH:MM) [{config.get('backup_time', '02:00')}]: ")
            if time_input == '':
                break
            try:
                # Validar formato de hora
                datetime.strptime(time_input, '%H:%M')
                config['backup_time'] = time_input
                break
            except ValueError:
                print("Formato inválido. Usa HH:MM (ej: 02:00)")
                
        # Configurar retención
        while True:
            keep_input = input(f"Número de backups a mantener [{config.get('keep_backups', 7)}]: ")
            if keep_input == '':
                break
            try:
                keep_count = int(keep_input)
                if keep_count > 0:
                    config['keep_backups'] = keep_count
                    break
                else:
                    print("Debe ser un número mayor a 0")
            except ValueError:
                print("Debe ser un número válido")
                
        # Guardar configuración
        self.save_config(config)
        
        print("\n✅ Configuración guardada")
        print("\n📋 IMPORTANTE:")
        print("Este script debe ejecutarse regularmente para funcionar.")
        print("Opciones recomendadas:")
        print("1. Ejecutar manualmente: python backup_scheduler.py --check")
        print("2. Programar en Tareas Programadas de Windows")
        print("3. Ejecutar al inicio de Windows")
        
    def manual_backup(self):
        """Ejecutar backup manual."""
        print("🔄 Ejecutando backup manual...")
        
        if not self.check_disk_space():
            print("❌ No hay suficiente espacio en disco")
            return
            
        config = self.load_config()
        
        if self.run_backup():
            self.update_last_backup(config)
            print("✅ Backup manual completado")
        else:
            print("❌ Error en backup manual")
            
    def check_and_run(self):
        """Verificar si es necesario backup y ejecutar."""
        config = self.load_config()
        
        if not config.get('backup_enabled', False):
            return
            
        if self.check_backup_needed(config):
            self.log_message("⏰ Es hora de hacer backup automático")
            
            if self.check_disk_space():
                if self.run_backup():
                    self.update_last_backup(config)
                    self.log_message("✅ Backup automático completado")
                else:
                    self.log_message("❌ Error en backup automático")
            else:
                self.log_message("❌ Backup cancelado: poco espacio en disco")
        else:
            # Solo log en modo verbose
            pass
            
        # Limpiar logs antiguos
        self.cleanup_logs()

def main():
    """Función principal."""
    scheduler = BackupScheduler()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--check":
            scheduler.check_and_run()
        elif command == "--status":
            scheduler.show_backup_status()
        elif command == "--backup":
            scheduler.manual_backup()
        elif command == "--config":
            scheduler.configure_scheduler()
        else:
            print("Comandos disponibles:")
            print("  --check    Verificar y ejecutar backup si es necesario")
            print("  --status   Mostrar estado del sistema de backup")
            print("  --backup   Ejecutar backup manual")
            print("  --config   Configurar programador de backups")
    else:
        # Modo interactivo
        scheduler.configure_scheduler()

if __name__ == "__main__":
    main()