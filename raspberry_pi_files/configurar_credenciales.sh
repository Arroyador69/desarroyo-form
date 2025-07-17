#!/bin/bash
# Script de configuración rápida de credenciales
# DesArroyo.tech Webhook - Raspberry Pi

echo "🔐 CONFIGURACIÓN RÁPIDA DE CREDENCIALES"
echo "======================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [[ ! -f "webhook_raspberry.py" ]]; then
    echo "❌ Error: Ejecuta este script desde ~/desarroyo-webhook/"
    exit 1
fi

log_info "Configurando credenciales para DesArroyo.tech Webhook..."

# Solicitar credenciales
echo ""
log_warning "Necesitas las siguientes credenciales:"
echo "1. Twilio Account SID (desde https://console.twilio.com)"
echo "2. Twilio Auth Token (desde https://console.twilio.com)"
echo "3. Ngrok Auth Token (desde https://dashboard.ngrok.com)"
echo ""

# Twilio Account SID
read -p "🔑 Ingresa tu Twilio Account SID: " TWILIO_SID
while [[ -z "$TWILIO_SID" ]]; do
    log_warning "El Account SID no puede estar vacío"
    read -p "🔑 Ingresa tu Twilio Account SID: " TWILIO_SID
done

# Twilio Auth Token
read -p "🔑 Ingresa tu Twilio Auth Token: " TWILIO_TOKEN
while [[ -z "$TWILIO_TOKEN" ]]; do
    log_warning "El Auth Token no puede estar vacío"
    read -p "🔑 Ingresa tu Twilio Auth Token: " TWILIO_TOKEN
done

# Ngrok Auth Token
read -p "🔑 Ingresa tu Ngrok Auth Token: " NGROK_TOKEN
while [[ -z "$NGROK_TOKEN" ]]; do
    log_warning "El Ngrok Token no puede estar vacío"
    read -p "🔑 Ingresa tu Ngrok Auth Token: " NGROK_TOKEN
done

# Crear archivo .env
log_info "Creando archivo .env..."
cat > .env << EOF
# Configuración DesArroyo.tech Webhook - Raspberry Pi
# Generado automáticamente el $(date)

# === TWILIO CONFIGURATION ===
TWILIO_ACCOUNT_SID=$TWILIO_SID
TWILIO_AUTH_TOKEN=$TWILIO_TOKEN
TWILIO_PHONE_NUMBER=+18109579712

# === NGROK CONFIGURATION ===
NGROK_AUTH_TOKEN=$NGROK_TOKEN

# === WEBHOOK CONFIGURATION ===
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0

# === LOGGING CONFIGURATION ===
LOG_LEVEL=INFO
LOG_FILE=/home/pi/desarroyo-webhook/webhook.log

# === TIMEZONE CONFIGURATION ===
TIMEZONE=Europe/Madrid

# === BUSINESS HOURS (24h format) ===
BUSINESS_START_MORNING=09:00
BUSINESS_END_MORNING=14:00
BUSINESS_START_AFTERNOON=16:00
BUSINESS_END_AFTERNOON=20:00

# === CONTACT INFORMATION ===
BUSINESS_EMAIL=info@desarroyo.tech
BUSINESS_WEBSITE=https://desarroyo.tech
BUSINESS_NAME=DesArroyo.tech

# === PRICING INFORMATION ===
WEBSITE_PRICE=299
DEVELOPMENT_TIME=48

# === NOTIFICATION SETTINGS ===
ENABLE_SMS=true
ENABLE_EMAIL_NOTIFICATIONS=false
ADMIN_EMAIL=admin@desarroyo.tech

# === RATE LIMITING ===
MAX_CALLS_PER_HOUR=100
MAX_SMS_PER_HOUR=50

# === DEBUG SETTINGS ===
DEBUG=false
TEST_MODE=false
EOF

# Configurar ngrok
log_info "Configurando ngrok..."
ngrok config add-authtoken $NGROK_TOKEN

# Verificar configuración
log_info "Verificando configuración..."
if [[ -f ".env" ]]; then
    log_info "✅ Archivo .env creado correctamente"
else
    log_warning "❌ Error creando archivo .env"
    exit 1
fi

# Verificar ngrok
if ngrok config check &>/dev/null; then
    log_info "✅ Ngrok configurado correctamente"
else
    log_warning "❌ Error configurando ngrok"
fi

echo ""
log_info "🎉 ¡Configuración completada!"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Iniciar el servicio:"
echo "   sudo systemctl start desarroyo-webhook.service"
echo ""
echo "2. Verificar que todo funciona:"
echo "   ./ver_estado.sh"
echo ""
echo "3. Copiar la URL de ngrok y actualizar Twilio:"
echo "   https://console.twilio.com/us1/develop/phone-numbers/manage/incoming"
echo ""
echo "🔧 COMANDOS ÚTILES:"
echo "   ./ver_estado.sh    - Ver estado del webhook"
echo "   ./reiniciar.sh     - Reiniciar webhook"
echo ""

log_info "¡Tu webhook está listo para funcionar 24/7!" 