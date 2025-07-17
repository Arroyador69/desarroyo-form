# 🔧 GUÍA RASPBERRY PI 24/7 - PASO A PASO

## ✅ PASO 1: CONEXIÓN INICIAL (YA HECHO)
```bash
# YA CONECTADO - IP: 192.168.0.28 (raspberrypi.local)
# SSH: pi@raspberrypi.local
# Password: desarroyo123
```

## 🔄 PASO 2: ACTUALIZAR SISTEMA
```bash
# Ejecutar en el Pi:
sudo apt update && sudo apt upgrade -y
```

## 🐍 PASO 3: INSTALAR PYTHON Y DEPENDENCIAS
```bash
# Instalar Python y pip:
sudo apt install python3-pip python3-venv git -y

# Crear directorio del proyecto:
mkdir ~/desarroyo-webhook
cd ~/desarroyo-webhook

# Crear entorno virtual:
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias:
pip install flask twilio requests python-dotenv
```

## 🌐 PASO 4: INSTALAR NGROK
```bash
# Descargar ngrok para ARM64:
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
tar -xzf ngrok-v3-stable-linux-arm64.tgz
sudo mv ngrok /usr/local/bin/
```

## 📁 PASO 5: CREAR ARCHIVOS DEL WEBHOOK
```bash
# Crear archivo principal del webhook:
nano ~/desarroyo-webhook/webhook_raspberry.py
```

## 🔧 PASO 6: CONFIGURAR VARIABLES DE ENTORNO
```bash
# Crear archivo .env:
nano ~/desarroyo-webhook/.env
```

## 🚀 PASO 7: CONFIGURAR SERVICIO AUTOMÁTICO
```bash
# Crear servicio systemd:
sudo nano /etc/systemd/system/desarroyo-webhook.service
```

## 🔒 PASO 8: CONFIGURAR NGROK AUTH
```bash
# Configurar token de ngrok:
ngrok config add-authtoken TU_TOKEN_AQUI
```

## ⚡ PASO 9: ACTIVAR SERVICIOS
```bash
# Recargar servicios:
sudo systemctl daemon-reload

# Habilitar servicio:
sudo systemctl enable desarroyo-webhook.service

# Iniciar servicio:
sudo systemctl start desarroyo-webhook.service

# Ver estado:
sudo systemctl status desarroyo-webhook.service
```

## 🧪 PASO 10: PROBAR EL SISTEMA
```bash
# Ver logs en tiempo real:
sudo journalctl -u desarroyo-webhook.service -f

# Verificar que ngrok está funcionando:
curl http://localhost:4040/api/tunnels
```

## 📱 PASO 11: ACTUALIZAR TWILIO
- Ir a Twilio Console
- Actualizar webhook URL con la nueva URL de ngrok
- Probar con una llamada

## 🎯 COMANDOS ÚTILES
```bash
# Reiniciar servicio:
sudo systemctl restart desarroyo-webhook.service

# Parar servicio:
sudo systemctl stop desarroyo-webhook.service

# Ver logs:
sudo journalctl -u desarroyo-webhook.service -n 50

# Ver estado de ngrok:
curl -s http://localhost:4040/api/tunnels | python3 -m json.tool
```

## 🔄 REBOOT AUTOMÁTICO
El sistema se reiniciará automáticamente después de un reboot del Pi.

---
**ESTADO ACTUAL**: ✅ Pi conectado (192.168.0.28)
**SIGUIENTE**: Ejecutar comandos paso a paso 