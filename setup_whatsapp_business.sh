#!/bin/bash
# 🚀 CONFIGURACIÓN WHATSAPP BUSINESS API - DESARROYO TECH
# Configuración rápida para WhatsApp Business API profesional

echo "🚀 DESARROYO TECH - WHATSAPP BUSINESS API SETUP"
echo "=============================================="
echo "Configurando WhatsApp Business API para mensajería profesional..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📱 WHATSAPP BUSINESS API SETUP${NC}"
echo "================================="
echo ""

# Configurar Twilio WhatsApp Business API
echo -e "${YELLOW}1️⃣ TWILIO WHATSAPP BUSINESS API:${NC}"
echo "   💻 Ve a: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox"
echo "   📱 O directamente a: https://console.twilio.com/us1/develop/phone-numbers/manage/whatsapp-senders"
echo "   🔑 Necesitas: Account SID, Auth Token, y WhatsApp Sender Number"
echo ""

# Configurar DeepSeek para respuestas IA
echo -e "${YELLOW}2️⃣ DEEPSEEK IA (Respuestas Automáticas):${NC}"
echo "   💻 Ve a: https://platform.deepseek.com/"
echo "   📝 Registrate (5\$ gratis)"
echo "   🔑 Copia tu API Key"
echo ""

# Configurar Telegram para notificaciones
echo -e "${YELLOW}3️⃣ TELEGRAM BOT (Notificaciones):${NC}"
echo "   💻 Busca @BotFather en Telegram"
echo "   📝 Envía /newbot"
echo "   🔑 Copia el token"
echo "   📱 Busca @userinfobot y envía /start para tu Chat ID"
echo ""

# Solicitar credenciales
echo -e "${GREEN}💾 INTRODUCE TUS CREDENCIALES:${NC}"
echo ""

read -p "📱 Introduce tu TWILIO_ACCOUNT_SID: " twilio_sid
read -p "🔑 Introduce tu TWILIO_AUTH_TOKEN: " twilio_token
read -p "📞 Introduce tu TWILIO_WHATSAPP_NUMBER (ej: +14155238886): " twilio_whatsapp
read -p "🤖 Introduce tu DEEPSEEK_API_KEY: " deepseek_key
read -p "📢 Introduce tu TELEGRAM_BOT_TOKEN: " telegram_token
read -p "💬 Introduce tu TELEGRAM_CHAT_ID: " telegram_chat

# Crear archivo .env
echo ""
echo -e "${GREEN}💾 Guardando configuración WhatsApp Business API...${NC}"

cat > .env << EOF
# DESARROYO TECH - WHATSAPP BUSINESS API CONFIGURACIÓN
TWILIO_ACCOUNT_SID=${twilio_sid}
TWILIO_AUTH_TOKEN=${twilio_token}
TWILIO_WHATSAPP_NUMBER=${twilio_whatsapp}
DEEPSEEK_API_KEY=${deepseek_key}
TELEGRAM_BOT_TOKEN=${telegram_token}
TELEGRAM_CHAT_ID=${telegram_chat}

# CONFIGURACIÓN PROFESIONAL
WEBSITE_URL=https://desarroyo.tech
BUSINESS_NAME=DesArroyo Tech
YOUR_NAME=Alberto

# CONFIGURACIÓN WHATSAPP BUSINESS API
WHATSAPP_BUSINESS_MODE=true
MAX_LEADS_PER_RUN=15
DELAY_BETWEEN_MESSAGES=60
ENABLE_AI_RESPONSES=true
WEBHOOK_PORT=5000

# LOGS Y DEBUGGING
LOG_LEVEL=INFO
SAVE_CONVERSATIONS=true
CANAL_COMUNICACION=WHATSAPP
EOF

echo -e "${GREEN}✅ Configuración guardada en .env${NC}"
echo ""

# Verificar configuración
echo -e "${BLUE}🔍 VERIFICANDO CONFIGURACIÓN WHATSAPP BUSINESS API...${NC}"
echo ""

# Test de configuración
echo -e "${YELLOW}🧪 EJECUTANDO PRUEBAS...${NC}"
echo ""

# Verificar Python y dependencias
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✅ Python3 instalado${NC}"
else
    echo -e "${RED}❌ Python3 no encontrado${NC}"
    exit 1
fi

# Verificar requirements
echo -e "${YELLOW}📦 Verificando dependencias...${NC}"
pip3 install -q twilio requests python-telegram-bot openai beautifulsoup4 lxml

# Test básico de conexión
echo -e "${YELLOW}🔌 Probando conexión con Twilio...${NC}"
python3 -c "
import os
from twilio.rest import Client
try:
    client = Client('${twilio_sid}', '${twilio_token}')
    account = client.api.account.fetch()
    print('✅ Conexión Twilio exitosa')
    print(f'   📱 Account: {account.friendly_name}')
except Exception as e:
    print(f'❌ Error Twilio: {e}')
    exit(1)
"

echo ""
echo -e "${GREEN}🎉 CONFIGURACIÓN COMPLETA!${NC}"
echo ""
echo -e "${BLUE}🚀 EJECUTAR SISTEMA WHATSAPP BUSINESS API:${NC}"
echo ""
echo "   📍 Prueba local:"
echo "   python3 scripts/sistema_leads_avanzado.py Madrid restaurantes"
echo ""
echo "   📍 GitHub Actions (automático):"
echo "   Ve a: https://github.com/tu-usuario/desarroyo-form/actions"
echo "   Click: 'Run workflow'"
echo ""
echo -e "${GREEN}💡 VENTAJAS WHATSAPP BUSINESS API:${NC}"
echo "   📱 Mensajes profesionales con plantillas"
echo "   💰 Más económico que SMS (~$0.025 vs $0.08)"
echo "   📈 98% tasa de apertura vs 20% SMS"
echo "   🤖 Respuestas automáticas con IA"
echo "   ✅ Imagen profesional y confiable"
echo ""
echo -e "${YELLOW}🔥 ¡Tu sistema está listo para generar leads con WhatsApp Business API!${NC}" 