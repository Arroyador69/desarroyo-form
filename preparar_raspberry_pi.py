#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🥧 PREPARAR RASPBERRY PI - WEBHOOK 24/7
Configuración completa para Raspberry Pi con webhook en español
"""

import os
import json
import shutil
import subprocess
import sys
from datetime import datetime

def crear_estructura_raspberry():
    """Crear estructura de archivos para Raspberry Pi"""
    print("🥧 PREPARANDO ESTRUCTURA RASPBERRY PI")
    print("=" * 60)
    
    # Crear directorio para Raspberry Pi
    raspberry_dir = "raspberry_pi_webhook"
    
    if os.path.exists(raspberry_dir):
        print(f"📁 Directorio {raspberry_dir} ya existe")
    else:
        os.makedirs(raspberry_dir)
        print(f"📁 Directorio {raspberry_dir} creado")
    
    return raspberry_dir

def copiar_archivos_necesarios(raspberry_dir):
    """Copiar archivos necesarios para Raspberry Pi"""
    print("\n📋 COPIANDO ARCHIVOS NECESARIOS")
    print("=" * 40)
    
    archivos_necesarios = [
        'webhook_espanol_definitivo.py',
        'requirements.txt',
        '.env',
        'scripts/sistema_leads_avanzado.py'
    ]
    
    for archivo in archivos_necesarios:
        origen = archivo
        destino = os.path.join(raspberry_dir, os.path.basename(archivo))
        
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"✅ Copiado: {archivo} → {destino}")
        else:
            print(f"⚠️ No encontrado: {archivo}")
    
    return True

def crear_requirements_raspberry(raspberry_dir):
    """Crear requirements.txt optimizado para Raspberry Pi"""
    print("\n📦 CREANDO REQUIREMENTS.TXT PARA RASPBERRY PI")
    print("=" * 40)
    
    requirements = """# Dependencias para Raspberry Pi - Webhook DesArroyo Tech
flask==2.3.3
twilio==8.10.0
python-dotenv==1.0.0
pytz==2023.3
requests==2.31.0
urllib3==2.0.7

# Opcional para monitoreo
psutil==5.9.5
"""
    
    requirements_file = os.path.join(raspberry_dir, 'requirements.txt')
    
    with open(requirements_file, 'w') as f:
        f.write(requirements)
    
    print(f"✅ Creado: {requirements_file}")
    return True

def crear_script_instalacion_raspberry(raspberry_dir):
    """Crear script de instalación para Raspberry Pi"""
    print("\n🔧 CREANDO SCRIPT DE INSTALACIÓN")
    print("=" * 40)
    
    script_content = """#!/bin/bash
# Script de instalación para Raspberry Pi - DesArroyo Tech Webhook

echo "🥧 INSTALANDO WEBHOOK DESARROYO TECH EN RASPBERRY PI"
echo "=" * 60

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
echo "🐍 Instalando Python..."
sudo apt install python3 python3-pip python3-venv -y

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv webhook_env
source webhook_env/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

# Configurar variables de entorno
echo "🔐 Configurando variables de entorno..."
if [ ! -f .env ]; then
    echo "⚠️ Archivo .env no encontrado. Creando plantilla..."
    cat > .env << EOF
# Credenciales Twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+18109579712

# Configuración del negocio
BUSINESS_NAME=DesArroyo Tech
WEBSITE_URL=https://desarroyo.tech

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
EOF
    echo "❌ IMPORTANTE: Edita el archivo .env con tus credenciales reales"
    echo "nano .env"
fi

# Crear servicio systemd
echo "🔧 Creando servicio systemd..."
sudo tee /etc/systemd/system/desarroyo-webhook.service > /dev/null <<EOF
[Unit]
Description=DesArroyo Tech Webhook Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/webhook_desarroyo
Environment=PATH=/home/pi/webhook_desarroyo/webhook_env/bin
ExecStart=/home/pi/webhook_desarroyo/webhook_env/bin/python webhook_espanol_definitivo.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable desarroyo-webhook.service

echo "✅ INSTALACIÓN COMPLETADA"
echo "=" * 60
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Edita .env con tus credenciales: nano .env"
echo "2. Inicia el servicio: sudo systemctl start desarroyo-webhook"
echo "3. Verifica el estado: sudo systemctl status desarroyo-webhook"
echo "4. Configura puerto forwarding o tunnel (ngrok/cloudflare)"
echo "5. Actualiza URL en Twilio Console"
echo ""
echo "📱 COMANDOS ÚTILES:"
echo "- Ver logs: sudo journalctl -u desarroyo-webhook -f"
echo "- Reiniciar: sudo systemctl restart desarroyo-webhook"
echo "- Parar: sudo systemctl stop desarroyo-webhook"
echo ""
echo "🥧 ¡RASPBERRY PI LISTA PARA FUNCIONAR 24/7!"
"""
    
    script_file = os.path.join(raspberry_dir, 'install_raspberry.sh')
    
    with open(script_file, 'w') as f:
        f.write(script_content)
    
    # Hacer ejecutable
    os.chmod(script_file, 0o755)
    
    print(f"✅ Creado: {script_file}")
    return True

def crear_readme_raspberry(raspberry_dir):
    """Crear README para Raspberry Pi"""
    print("\n📄 CREANDO README PARA RASPBERRY PI")
    print("=" * 40)
    
    readme_content = """# 🥧 WEBHOOK DESARROYO TECH - RASPBERRY PI

## 🚀 INSTALACIÓN RÁPIDA

### 1. Preparar archivos
```bash
# Copiar todos los archivos a la Raspberry Pi
scp -r raspberry_pi_webhook/ pi@tu_raspberry_ip:/home/pi/webhook_desarroyo/
```

### 2. Instalar en Raspberry Pi
```bash
ssh pi@tu_raspberry_ip
cd /home/pi/webhook_desarroyo
chmod +x install_raspberry.sh
./install_raspberry.sh
```

### 3. Configurar credenciales
```bash
nano .env
# Editar con tus credenciales reales de Twilio
```

### 4. Iniciar servicio
```bash
sudo systemctl start desarroyo-webhook
sudo systemctl status desarroyo-webhook
```

## 🌐 CONFIGURACIÓN DE RED

### Opción 1: Port Forwarding (Recomendado)
```bash
# En tu router, configurar port forwarding:
# Puerto externo: 5001
# Puerto interno: 5001
# IP: IP de tu Raspberry Pi
# URL final: http://tu_ip_publica:5001/webhook-llamada
```

### Opción 2: Ngrok en Raspberry Pi
```bash
# Instalar ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin/

# Configurar token (opcional)
ngrok authtoken tu_token_aqui

# Iniciar tunnel
ngrok http 5001
```

### Opción 3: Cloudflare Tunnel
```bash
# Instalar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# Configurar tunnel
cloudflared tunnel --url http://localhost:5001
```

## 📞 CONFIGURAR TWILIO

1. Ve a: https://console.twilio.com/
2. Phone Numbers → Manage → Active numbers
3. Click en tu número: +18109579712
4. En 'Voice Configuration' → 'A call comes in':
   - URL: http://tu_ip_publica:5001/webhook-llamada
   - Method: POST
5. Guardar cambios

## 🔧 COMANDOS ÚTILES

```bash
# Ver logs en tiempo real
sudo journalctl -u desarroyo-webhook -f

# Reiniciar servicio
sudo systemctl restart desarroyo-webhook

# Parar servicio
sudo systemctl stop desarroyo-webhook

# Ver estado
sudo systemctl status desarroyo-webhook

# Deshabilitar servicio
sudo systemctl disable desarroyo-webhook
```

## 🧪 PROBAR FUNCIONAMIENTO

```bash
# Probar webhook local
curl -X POST http://localhost:5001/webhook-llamada \\
  -d "From=+34662513448&To=+18109579712&CallSid=test123"

# Probar webhook externo
curl -X POST http://tu_ip_publica:5001/webhook-llamada \\
  -d "From=+34662513448&To=+18109579712&CallSid=test123"
```

## 🎯 CARACTERÍSTICAS

- ✅ Webhook en español con voz Polly.Lucia
- ✅ Horarios comerciales automáticos
- ✅ SMS automático después de llamadas
- ✅ Servicio systemd para auto-inicio
- ✅ Logs automáticos
- ✅ Reinicio automático si falla
- ✅ Funciona 24/7 sin intervención

## 🚨 TROUBLESHOOTING

### Webhook no responde
```bash
# Verificar que el servicio está corriendo
sudo systemctl status desarroyo-webhook

# Verificar logs
sudo journalctl -u desarroyo-webhook -f
```

### Llamadas en inglés
```bash
# Verificar que Twilio usa la URL correcta
curl -X POST tu_webhook_url \\
  -d "From=+34662513448&To=+18109579712&CallSid=test123"
```

### Error de dependencias
```bash
# Reinstalar dependencias
source webhook_env/bin/activate
pip install -r requirements.txt --force-reinstall
```

## 🎉 ¡LISTO!

Tu Raspberry Pi está ahora funcionando como servidor webhook 24/7 para las llamadas automáticas de DesArroyo Tech en español perfecto.
"""
    
    readme_file = os.path.join(raspberry_dir, 'README.md')
    
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Creado: {readme_file}")
    return True

def crear_env_template(raspberry_dir):
    """Crear template .env para Raspberry Pi"""
    print("\n🔐 CREANDO TEMPLATE .ENV")
    print("=" * 40)
    
    env_content = """# Credenciales Twilio (OBLIGATORIO)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+18109579712

# Configuración del negocio
BUSINESS_NAME=DesArroyo Tech
WEBSITE_URL=https://desarroyo.tech

# Telegram (opcional para notificaciones)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Configuración adicional
DEBUG=False
PORT=5001
HOST=0.0.0.0
"""
    
    env_file = os.path.join(raspberry_dir, '.env.template')
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Creado: {env_file}")
    return True

def main():
    """Función principal"""
    print("🥧 PREPARANDO RASPBERRY PI PARA WEBHOOK 24/7")
    print("=" * 60)
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Crear estructura
    raspberry_dir = crear_estructura_raspberry()
    
    # Copiar archivos
    copiar_archivos_necesarios(raspberry_dir)
    
    # Crear requirements
    crear_requirements_raspberry(raspberry_dir)
    
    # Crear script de instalación
    crear_script_instalacion_raspberry(raspberry_dir)
    
    # Crear README
    crear_readme_raspberry(raspberry_dir)
    
    # Crear template .env
    crear_env_template(raspberry_dir)
    
    print("\n🎉 PREPARACIÓN COMPLETADA")
    print("=" * 60)
    print(f"📁 Directorio: {raspberry_dir}")
    print("📋 Archivos creados:")
    print("   - webhook_espanol_definitivo.py")
    print("   - requirements.txt")
    print("   - install_raspberry.sh")
    print("   - README.md")
    print("   - .env.template")
    print()
    print("🚀 PRÓXIMOS PASOS:")
    print("1. Copiar carpeta a Raspberry Pi:")
    print(f"   scp -r {raspberry_dir}/ pi@tu_raspberry_ip:/home/pi/webhook_desarroyo/")
    print("2. SSH a Raspberry Pi:")
    print("   ssh pi@tu_raspberry_ip")
    print("3. Ejecutar instalación:")
    print("   cd /home/pi/webhook_desarroyo && ./install_raspberry.sh")
    print("4. Configurar credenciales:")
    print("   nano .env")
    print("5. Iniciar servicio:")
    print("   sudo systemctl start desarroyo-webhook")
    print()
    print("🎯 RESULTADO:")
    print("✅ Webhook funcionando 24/7 en español")
    print("✅ Auto-reinicio si falla")
    print("✅ Logs automáticos")
    print("✅ Servicio systemd configurado")
    print()
    print("📞 DESPUÉS DE INSTALAR:")
    print("- Configurar port forwarding o tunnel")
    print("- Actualizar URL en Twilio Console")
    print("- Hacer llamada de prueba")
    print("- ¡Funciona para siempre!")

if __name__ == '__main__':
    main() 