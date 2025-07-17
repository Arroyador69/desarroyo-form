#!/bin/bash
# Script de instalación automatizada - DesArroyo.tech Webhook
# Raspberry Pi 24/7 Setup

set -e  # Salir si hay error

echo "🚀 INSTALACIÓN WEBHOOK DESARROYO.TECH - RASPBERRY PI"
echo "=================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en Pi
if [[ ! -f /etc/rpi-issue ]]; then
    log_warning "Este script está diseñado para Raspberry Pi"
fi

# PASO 1: Actualizar sistema
log_info "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# PASO 2: Instalar dependencias básicas
log_info "Instalando dependencias básicas..."
sudo apt install -y python3-pip python3-venv git curl wget unzip

# PASO 3: Crear directorio del proyecto
log_info "Creando directorio del proyecto..."
mkdir -p ~/desarroyo-webhook
cd ~/desarroyo-webhook

# PASO 4: Crear entorno virtual
log_info "Creando entorno virtual Python..."
python3 -m venv venv
source venv/bin/activate

# PASO 5: Instalar dependencias Python
log_info "Instalando dependencias Python..."
pip install --upgrade pip

# Crear requirements.txt
cat > requirements.txt << 'EOF'
Flask==2.3.3
twilio==8.10.0
python-dotenv==1.0.0
requests==2.31.0
pytz==2023.3
gunicorn==21.2.0
EOF

pip install -r requirements.txt

# PASO 6: Descargar e instalar ngrok
log_info "Instalando ngrok..."
if [[ $(uname -m) == "aarch64" ]]; then
    NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"
else
    NGROK_URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm.tgz"
fi

wget $NGROK_URL -O ngrok.tgz
tar -xzf ngrok.tgz
sudo mv ngrok /usr/local/bin/
rm ngrok.tgz

# PASO 7: Crear archivos de configuración
log_info "Creando archivos de configuración..."

# Crear .env desde template
if [[ ! -f .env ]]; then
    log_info "Creando archivo .env..."
    cat > .env << 'EOF'
# Configuración DesArroyo.tech Webhook - Raspberry Pi
# IMPORTANTE: Actualizar con tus credenciales reales

# === TWILIO CONFIGURATION ===
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=+18109579712

# === NGROK CONFIGURATION ===
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here

# === WEBHOOK CONFIGURATION ===
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0

# === LOGGING CONFIGURATION ===
LOG_LEVEL=INFO
LOG_FILE=/home/pi/desarroyo-webhook/webhook.log

# === TIMEZONE CONFIGURATION ===
TIMEZONE=Europe/Madrid
EOF
    
    log_warning "¡IMPORTANTE! Edita el archivo .env con tus credenciales reales:"
    log_warning "nano ~/.env"
else
    log_info "Archivo .env ya existe"
fi

# PASO 8: Crear script de inicio con ngrok
log_info "Creando script de inicio..."
cat > start_webhook.sh << 'EOF'
#!/bin/bash
# Script de inicio para webhook + ngrok

# Cargar variables de entorno
source /home/pi/desarroyo-webhook/.env

# Activar entorno virtual
source /home/pi/desarroyo-webhook/venv/bin/activate

# Iniciar ngrok en background
ngrok http 5000 --log=stdout > /home/pi/desarroyo-webhook/ngrok.log 2>&1 &
NGROK_PID=$!

# Esperar a que ngrok esté listo
sleep 5

# Obtener URL pública de ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])" 2>/dev/null || echo "Error obteniendo URL")

echo "🌐 URL del webhook: $NGROK_URL/webhook-llamada"
echo "📊 Panel ngrok: http://localhost:4040"

# Iniciar webhook
echo "🚀 Iniciando webhook..."
python3 /home/pi/desarroyo-webhook/webhook_raspberry.py
EOF

chmod +x start_webhook.sh

# PASO 9: Crear servicio systemd
log_info "Configurando servicio systemd..."
sudo tee /etc/systemd/system/desarroyo-webhook.service > /dev/null << 'EOF'
[Unit]
Description=DesArroyo.tech Webhook Service
After=network.target
Wants=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/desarroyo-webhook
Environment=PATH=/home/pi/desarroyo-webhook/venv/bin
ExecStart=/home/pi/desarroyo-webhook/start_webhook.sh
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Configuración de reinicio
StartLimitInterval=60
StartLimitBurst=3

# Variables de entorno
EnvironmentFile=/home/pi/desarroyo-webhook/.env

# Configuración de recursos
LimitNOFILE=65536
TimeoutStartSec=30
TimeoutStopSec=30

# Configuración de logging
SyslogIdentifier=desarroyo-webhook

[Install]
WantedBy=multi-user.target
EOF

# PASO 10: Habilitar servicio
log_info "Habilitando servicio..."
sudo systemctl daemon-reload
sudo systemctl enable desarroyo-webhook.service

# PASO 11: Crear scripts de utilidad
log_info "Creando scripts de utilidad..."

# Script para ver estado
cat > ver_estado.sh << 'EOF'
#!/bin/bash
echo "🔍 ESTADO DEL WEBHOOK DESARROYO.TECH"
echo "================================="

echo "📊 Estado del servicio:"
sudo systemctl status desarroyo-webhook.service --no-pager -l

echo ""
echo "🌐 URLs de ngrok:"
curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for tunnel in data['tunnels']:
        print(f'  {tunnel['name']}: {tunnel['public_url']}')
except:
    print('  ngrok no está ejecutándose')
"

echo ""
echo "📱 Última actividad:"
tail -5 /home/pi/desarroyo-webhook/webhook.log 2>/dev/null || echo "  No hay logs disponibles"
EOF

chmod +x ver_estado.sh

# Script para reiniciar
cat > reiniciar.sh << 'EOF'
#!/bin/bash
echo "🔄 Reiniciando webhook..."
sudo systemctl restart desarroyo-webhook.service
echo "✅ Webhook reiniciado"
./ver_estado.sh
EOF

chmod +x reiniciar.sh

# PASO 12: Crear directorio para logs
mkdir -p logs

# PASO 13: Mostrar información final
log_info "¡Instalación completada!"
echo ""
echo "🎉 INSTALACIÓN COMPLETADA"
echo "========================"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Edita el archivo .env con tus credenciales:"
echo "   nano ~/desarroyo-webhook/.env"
echo ""
echo "2. Configura tu token de ngrok:"
echo "   ngrok config add-authtoken TU_TOKEN_AQUI"
echo ""
echo "3. Inicia el servicio:"
echo "   sudo systemctl start desarroyo-webhook.service"
echo ""
echo "4. Verifica que todo funciona:"
echo "   ./ver_estado.sh"
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "   ./ver_estado.sh    - Ver estado del webhook"
echo "   ./reiniciar.sh     - Reiniciar webhook"
echo "   sudo systemctl stop desarroyo-webhook.service - Parar webhook"
echo ""
echo "📂 ARCHIVOS IMPORTANTES:"
echo "   ~/.env                    - Configuración"
echo "   ~/desarroyo-webhook/      - Directorio principal"
echo "   ~/desarroyo-webhook/webhook.log - Logs del webhook"
echo ""
echo "🌐 DESPUÉS DE INICIAR:"
echo "   - Panel ngrok: http://localhost:4040"
echo "   - Webhook URL: https://XXXXX.ngrok-free.app/webhook-llamada"
echo ""

log_info "¡Listo para configurar Twilio!" 