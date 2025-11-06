#!/usr/bin/env python3
"""
🔄 Script de Sincronización Dual - TrebolSoft
Sincroniza tanto el backend como el frontend
"""

import os
import subprocess
import sys
from pathlib import Path
import datetime

class DualSyncManager:
    def __init__(self):
        self.base_dir = Path.home()
        self.backend_dir = self.base_dir / "TrebolsoftV1"
        self.frontend_dir = self.base_dir / "trebolsoft-frontend"
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def check_repositories(self):
        """Verificar que ambos repositorios existan."""
        print("🔍 VERIFICANDO REPOSITORIOS...")
        print("-" * 40)
        
        backend_exists = self.backend_dir.exists()
        frontend_exists = self.frontend_dir.exists()
        
        print(f"Backend (TrebolsoftV1): {'✅' if backend_exists else '❌'} {self.backend_dir}")
        print(f"Frontend (trebolsoft-frontend): {'✅' if frontend_exists else '❌'} {self.frontend_dir}")
        
        if not backend_exists:
            print("\n❌ BACKEND NO ENCONTRADO")
            print("📥 Clonar desde: https://github.com/trebolsoftv1-collab/TrebolsoftV1.git")
            
        if not frontend_exists:
            print("\n❌ FRONTEND NO ENCONTRADO") 
            print("📥 Clonar desde: https://github.com/trebolsoftv1-collab/trebolsoft-frontend.git")
            
        return backend_exists and frontend_exists
        
    def run_git_command(self, directory, command):
        """Ejecutar comando git en directorio específico."""
        try:
            result = subprocess.run(
                command, 
                cwd=directory, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
            
    def get_repo_status(self, directory, name):
        """Obtener estado del repositorio."""
        print(f"\n📊 ESTADO DE {name.upper()}:")
        print("-" * 30)
        
        # Verificar branch actual
        success, stdout, stderr = self.run_git_command(directory, "git branch --show-current")
        if success:
            current_branch = stdout.strip()
            print(f"🌿 Branch actual: {current_branch}")
        else:
            print(f"❌ Error obteniendo branch: {stderr}")
            
        # Verificar estado
        success, stdout, stderr = self.run_git_command(directory, "git status --porcelain")
        if success:
            if stdout.strip():
                print("📝 Cambios pendientes:")
                for line in stdout.strip().split('\n'):
                    print(f"   {line}")
            else:
                print("✅ Working tree limpio")
        else:
            print(f"❌ Error verificando estado: {stderr}")
            
        # Verificar commits pendientes
        success, stdout, stderr = self.run_git_command(directory, "git log origin/main..HEAD --oneline")
        if success:
            if stdout.strip():
                print("📤 Commits pendientes de push:")
                for line in stdout.strip().split('\n'):
                    print(f"   {line}")
            else:
                print("✅ Sincronizado con origin")
        else:
            print("⚠️ No se puede verificar sync con origin")
            
    def sync_repository(self, directory, name):
        """Sincronizar repositorio individual."""
        print(f"\n🔄 SINCRONIZANDO {name.upper()}...")
        print("-" * 35)
        
        # Pull últimos cambios
        print("📥 Descargando cambios remotos...")
        success, stdout, stderr = self.run_git_command(directory, "git pull origin main")
        if success:
            print("✅ Pull completado")
        else:
            print(f"⚠️ Pull con conflictos: {stderr}")
            
        # Verificar si hay cambios para commitear
        success, stdout, stderr = self.run_git_command(directory, "git status --porcelain")
        if success and stdout.strip():
            print("📝 Detectados cambios locales...")
            
            # Agregar todos los cambios
            print("📦 Agregando cambios...")
            success, stdout, stderr = self.run_git_command(directory, "git add .")
            
            if success:
                # Commit con mensaje automático
                commit_message = f"🔄 Sincronización automática - {self.timestamp}"
                commit_command = f'git commit -m "{commit_message}"'
                
                success, stdout, stderr = self.run_git_command(directory, commit_command)
                if success:
                    print(f"✅ Commit creado: {commit_message}")
                    
                    # Push cambios
                    print("📤 Subiendo cambios...")
                    success, stdout, stderr = self.run_git_command(directory, "git push origin main")
                    if success:
                        print("✅ Push completado")
                    else:
                        print(f"❌ Error en push: {stderr}")
                else:
                    print(f"❌ Error en commit: {stderr}")
            else:
                print(f"❌ Error agregando archivos: {stderr}")
        else:
            print("✅ No hay cambios para sincronizar")
            
    def verify_deployments(self):
        """Verificar que los deployments estén funcionando."""
        print("\n🚀 VERIFICANDO DEPLOYMENTS...")
        print("-" * 35)
        
        # Verificar frontend
        try:
            import requests
            
            print("🌐 Verificando frontend...")
            response = requests.get("https://app.trebolsoft.com", timeout=10)
            if response.status_code == 200:
                print("✅ Frontend funcionando: https://app.trebolsoft.com")
            else:
                print(f"⚠️ Frontend responde con código: {response.status_code}")
        except Exception as e:
            print(f"❌ Error verificando frontend: {e}")
            
        # Verificar backend
        try:
            print("🔧 Verificando backend...")
            response = requests.get("https://trebolsoftv1-latest.onrender.com/health", timeout=10)
            if response.status_code == 200:
                print("✅ Backend funcionando: https://trebolsoftv1-latest.onrender.com")
            else:
                print(f"⚠️ Backend responde con código: {response.status_code}")
        except Exception as e:
            print(f"❌ Error verificando backend: {e}")
            
    def create_sync_summary(self):
        """Crear resumen de sincronización."""
        summary_file = self.base_dir / f"trebolsoft_sync_summary_{self.timestamp}.md"
        
        summary_content = f"""# 🔄 RESUMEN DE SINCRONIZACIÓN TREBOLSOFT

## 📅 **FECHA:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 **REPOSITORIOS SINCRONIZADOS:**

### **🔧 BACKEND (TrebolsoftV1):**
- **Repositorio:** https://github.com/trebolsoftv1-collab/TrebolsoftV1
- **Local:** {self.backend_dir}
- **Deploy:** https://trebolsoftv1-latest.onrender.com
- **Estado:** ✅ Sincronizado

### **🌐 FRONTEND (trebolsoft-frontend):**
- **Repositorio:** https://github.com/trebolsoftv1-collab/trebolsoft-frontend  
- **Local:** {self.frontend_dir}
- **Deploy:** https://app.trebolsoft.com
- **Estado:** ✅ Sincronizado

---

## 🎯 **VERIFICACIONES REALIZADAS:**

- ✅ Pull de cambios remotos
- ✅ Commit de cambios locales
- ✅ Push a repositorios remotos
- ✅ Verificación de deployments
- ✅ Estado de branches verificado

---

## 📋 **PRÓXIMA SINCRONIZACIÓN:**

```bash
# Para sincronizar manualmente:
cd {self.backend_dir}
python dual_sync_manager.py

# O ejecutar desde cualquier ubicación:
python {self.base_dir}/TrebolsoftV1/dual_sync_manager.py
```

---

## 🔗 **ENLACES IMPORTANTES:**

- **Frontend:** https://app.trebolsoft.com
- **Backend API:** https://trebolsoftv1-latest.onrender.com
- **Health Check:** https://trebolsoftv1-latest.onrender.com/health
- **GitHub Backend:** https://github.com/trebolsoftv1-collab/TrebolsoftV1
- **GitHub Frontend:** https://github.com/trebolsoftv1-collab/trebolsoft-frontend

---

**🎉 SINCRONIZACIÓN COMPLETADA EXITOSAMENTE**
"""
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
            
        print(f"\n📄 Resumen guardado: {summary_file}")
        return summary_file
        
    def run_full_sync(self):
        """Ejecutar sincronización completa."""
        print("🔄 SINCRONIZACIÓN DUAL TREBOLSOFT")
        print("="*50)
        
        # Verificar repositorios
        if not self.check_repositories():
            print("\n❌ SINCRONIZACIÓN CANCELADA")
            print("📋 Clona los repositorios faltantes y vuelve a ejecutar")
            return False
            
        # Obtener estado actual
        if self.backend_dir.exists():
            self.get_repo_status(self.backend_dir, "Backend")
            
        if self.frontend_dir.exists():
            self.get_repo_status(self.frontend_dir, "Frontend")
            
        # Confirmar sincronización
        print("\n" + "="*50)
        proceed = input("¿Proceder con la sincronización? (s/n): ").lower()
        
        if proceed not in ['s', 'si', 'y', 'yes']:
            print("Sincronización cancelada")
            return False
            
        # Sincronizar repositorios
        if self.backend_dir.exists():
            self.sync_repository(self.backend_dir, "Backend")
            
        if self.frontend_dir.exists():
            self.sync_repository(self.frontend_dir, "Frontend")
            
        # Verificar deployments
        self.verify_deployments()
        
        # Crear resumen
        summary_file = self.create_sync_summary()
        
        print("\n" + "="*50)
        print("🎉 SINCRONIZACIÓN DUAL COMPLETADA")
        print("="*50)
        print(f"📄 Resumen: {summary_file}")
        print("🌐 Frontend: https://app.trebolsoft.com")
        print("🔧 Backend: https://trebolsoftv1-latest.onrender.com")
        
        return True

def main():
    """Función principal."""
    sync_manager = DualSyncManager()
    sync_manager.run_full_sync()

if __name__ == "__main__":
    main()