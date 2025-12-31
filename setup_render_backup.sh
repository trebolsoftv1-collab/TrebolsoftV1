# sync-forced-2025
#!/bin/bash
# 🤖 Configurador de Backup Automático para Render
# Este script configura un backup automático que se ejecuta en el servidor

echo "🛡️ CONFIGURANDO BACKUP AUTOMÁTICO EN RENDER"
echo "============================================"

# Crear directorio para scripts
mkdir -p /opt/render/project/scripts

# Crear script de backup cron
cat > /opt/render/project/scripts/backup_cron.py << 'EOF'
#!/usr/bin/env python3
"""
Ejecutor de backup para cron en Render
"""
import sys
import os
from pathlib import Path

# Agregar el directorio base al path
base_dir = Path("/opt/render/project/src")
sys.path.insert(0, str(base_dir))

# Importar y ejecutar backup
try:
    from render_auto_backup import RenderAutoBackup
    
    backup_system = RenderAutoBackup()
    result = backup_system.run_automatic_backup()
    
    if result:
        print("✅ Backup automático exitoso")
        sys.exit(0)
    else:
        print("❌ Error en backup automático")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error crítico: {e}")
    sys.exit(1)
EOF

# Hacer ejecutable
chmod +x /opt/render/project/scripts/backup_cron.py

# Crear entrada de crontab
echo "⏰ Configurando cron job..."

# Backup semanal los domingos a las 2:00 AM
CRON_ENTRY="0 2 * * 0 cd /opt/render/project/src && python3 /opt/render/project/scripts/backup_cron.py >> /var/log/backup.log 2>&1"

# Agregar a crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "✅ Cron job configurado: Domingos 2:00 AM"

# Crear script de configuración de variables de entorno
cat > /opt/render/project/scripts/setup_backup_env.sh << 'EOF'
#!/bin/bash
# Variables de entorno necesarias para backup automático

echo "⚙️ CONFIGURACIÓN DE VARIABLES DE ENTORNO"
echo "Agrega estas variables en el panel de Render:"
echo ""
echo "GITHUB_TOKEN=tu_token_aqui"
echo "GITHUB_REPO=trebolsoftv1-collab/TrebolsoftV1"
echo "BACKUP_HOUR=2"
echo "BACKUP_WEBHOOK_URL=https://hooks.slack.com/... (opcional)"
echo ""
echo "📋 Pasos:"
echo "1. Ve a tu panel de Render"
echo "2. Selecciona tu servicio"
echo "3. Ve a Environment"
echo "4. Agrega las variables listadas arriba"
EOF

chmod +x /opt/render/project/scripts/setup_backup_env.sh

echo "📋 CONFIGURACIÓN COMPLETADA"
echo ""
echo "🔧 PRÓXIMOS PASOS:"
echo "1. Ejecutar: /opt/render/project/scripts/setup_backup_env.sh"
echo "2. Configurar variables de entorno en Render"
echo "3. El backup se ejecutará automáticamente cada domingo"
echo ""
echo "🧪 PROBAR MANUALMENTE:"
echo "python3 /opt/render/project/scripts/backup_cron.py"