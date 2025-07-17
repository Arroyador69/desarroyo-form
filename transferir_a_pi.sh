#!/bin/bash
# Script para transferir archivos al Raspberry Pi y ejecutar instalación
# DesArroyo.tech Webhook Setup

set -e

echo "🚀 TRANSFERENCIA AL RASPBERRY PI - DESARROYO.TECH"
echo "==============================================="

# Configuración
PI_IP="raspberrypi.local"
PI_USER="pi"
PI_PASS="desarroyo123"

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

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [[ ! -d "raspberry_pi_files" ]]; then
    log_error "No se encuentra el directorio raspberry_pi_files"
    log_error "Ejecuta este script desde el directorio desarroyo-form"
    exit 1
fi

# Verificar conexión al Pi
log_info "Verificando conexión al Raspberry Pi..."
if ! ping -c 1 $PI_IP &> /dev/null; then
    log_error "No se puede conectar al Raspberry Pi en $PI_IP"
    log_error "Verifica que esté encendido y conectado a la red"
    exit 1
fi

log_info "✅ Raspberry Pi encontrado en $PI_IP"

# Transferir archivos
log_info "Transfiriendo archivos al Raspberry Pi..."

# Crear directorio temporal en el Pi
ssh $PI_USER@$PI_IP "mkdir -p ~/temp_webhook_setup"

# Transferir archivos principales
log_info "Transfiriendo webhook_raspberry.py..."
scp raspberry_pi_files/webhook_raspberry.py $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "Transfiriendo script de instalación..."
scp raspberry_pi_files/instalar_webhook.sh $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "Transfiriendo requirements.txt..."
scp raspberry_pi_files/requirements.txt $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "Transfiriendo archivo de configuración..."
scp raspberry_pi_files/env_template $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "Transfiriendo servicio systemd..."
scp raspberry_pi_files/desarroyo-webhook.service $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "Transfiriendo script de configuración rápida..."
scp raspberry_pi_files/configurar_credenciales.sh $PI_USER@$PI_IP:~/temp_webhook_setup/

log_info "✅ Archivos transferidos correctamente"

# Ejecutar instalación en el Pi
log_info "Ejecutando instalación en el Raspberry Pi..."
ssh $PI_USER@$PI_IP << 'EOF'
# Ir al directorio temporal
cd ~/temp_webhook_setup

# Hacer ejecutable el script de instalación
chmod +x instalar_webhook.sh

# Ejecutar instalación
echo "🔧 Iniciando instalación automatizada..."
./instalar_webhook.sh

# Copiar archivos principales al directorio final
echo "📋 Copiando archivos al directorio final..."
cp webhook_raspberry.py ~/desarroyo-webhook/
cp requirements.txt ~/desarroyo-webhook/
cp env_template ~/desarroyo-webhook/.env
cp configurar_credenciales.sh ~/desarroyo-webhook/
chmod +x ~/desarroyo-webhook/configurar_credenciales.sh

# Limpiar directorio temporal
rm -rf ~/temp_webhook_setup

echo "✅ Instalación completada!"
EOF

# Mostrar información final
log_info "🎉 INSTALACIÓN COMPLETADA EN RASPBERRY PI"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Conectarte al Pi y configurar credenciales:"
echo "   ssh pi@raspberrypi.local"
echo "   cd ~/desarroyo-webhook"
echo "   ./configurar_credenciales.sh"
echo ""
echo "2. Iniciar el servicio:"
echo "   sudo systemctl start desarroyo-webhook.service"
echo ""
echo "3. Verificar estado:"
echo "   cd ~/desarroyo-webhook && ./ver_estado.sh"
echo ""
echo "🔧 COMANDOS ÚTILES EN EL PI:"
echo "   ./configurar_credenciales.sh - Configurar credenciales fácilmente"
echo "   ./ver_estado.sh    - Ver estado del webhook"
echo "   ./reiniciar.sh     - Reiniciar webhook"
echo "   sudo systemctl stop desarroyo-webhook.service - Parar webhook"
echo ""
echo "🌐 CONFIGURACIÓN TWILIO:"
echo "   Cuando tengas la URL de ngrok, actualiza el webhook en:"
echo "   https://console.twilio.com/us1/develop/phone-numbers/manage/incoming"
echo ""

log_info "¡Tu Raspberry Pi está listo para funcionar 24/7!" 