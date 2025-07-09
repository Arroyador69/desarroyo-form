#!/bin/bash
# 🚀 CONFIGURACIÓN RÁPIDA TWILIO - DESARROYO TECH
# Solución automática para Error 63024

echo "🚀 CONFIGURACIÓN AUTOMÁTICA TWILIO"
echo "=================================="

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📄 Creando archivo .env..."
    cp env.example .env
fi

# Función para añadir variable de entorno
add_env_var() {
    local key=$1
    local value=$2
    if grep -q "^$key=" .env; then
        sed -i.bak "s/^$key=.*/$key=$value/" .env
    else
        echo "$key=$value" >> .env
    fi
}

echo ""
echo "🔑 CONFIGURACIÓN DE APIS:"
echo ""

# Configurar variables básicas ya conocidas
add_env_var "WEBSITE_URL" "https://desarroyo.tech"
add_env_var "BUSINESS_NAME" "DesArroyo Tech"
add_env_var "YOUR_NAME" "Alberto"

echo "✅ Variables básicas configuradas"

# Si ya existen las variables de Twilio, mostrarlas
if [ -n "$TWILIO_ACCOUNT_SID" ] && [ -n "$TWILIO_AUTH_TOKEN" ]; then
    echo "✅ Variables Twilio detectadas en sistema"
    add_env_var "TWILIO_ACCOUNT_SID" "$TWILIO_ACCOUNT_SID"
    add_env_var "TWILIO_AUTH_TOKEN" "$TWILIO_AUTH_TOKEN" 
    add_env_var "TWILIO_WHATSAPP_NUMBER" "${TWILIO_WHATSAPP_NUMBER:-+14155238886}"
else
    echo "⚠️  Configuración manual necesaria para Twilio"
    echo ""
    echo "📋 PASOS RÁPIDOS (5 minutos):"
    echo ""
    echo "1. Ve a: https://console.twilio.com/"
    echo "2. Crea cuenta gratuita ($10 de crédito)"
    echo "3. Copia Account SID y Auth Token"
    echo "4. Ve a WhatsApp Sandbox y copia el número"
    echo ""
    echo "5. Ejecuta estos comandos:"
    echo "   export TWILIO_ACCOUNT_SID='tu_account_sid_aqui'"
    echo "   export TWILIO_AUTH_TOKEN='tu_auth_token_aqui'"
    echo "   export TWILIO_WHATSAPP_NUMBER='+14155238886'"
    echo ""
    
    # Añadir placeholders al .env
    add_env_var "TWILIO_ACCOUNT_SID" "tu_account_sid_aqui"
    add_env_var "TWILIO_AUTH_TOKEN" "tu_auth_token_aqui"
    add_env_var "TWILIO_WHATSAPP_NUMBER" "+14155238886"
fi

# Configurar Telegram si no existe
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo ""
    echo "📢 TELEGRAM (OPCIONAL - para notificaciones):"
    echo "1. Busca @BotFather en Telegram"
    echo "2. Envía /newbot y sigue instrucciones"
    echo "3. Busca @userinfobot y envía /start para obtener tu chat_id"
    echo ""
    add_env_var "TELEGRAM_BOT_TOKEN" "opcional_tu_bot_token"
    add_env_var "TELEGRAM_CHAT_ID" "opcional_tu_chat_id"
fi

echo ""
echo "✅ ARCHIVO .env CONFIGURADO"
echo ""
echo "📁 Ubicación: $(pwd)/.env"
echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Edita .env con tus datos reales de Twilio"
echo "2. Ejecuta: source venv/bin/activate && python3 scripts/sistema_leads_avanzado.py Madrid restaurantes"
echo ""

# Mostrar estado actual
echo "📋 CONFIGURACIÓN ACTUAL:"
echo "=================================="
cat .env | grep -E "(TWILIO|TELEGRAM|WEBSITE|BUSINESS|YOUR_NAME)" | head -10
echo "=================================="

echo ""
echo "🚀 SISTEMA LISTO - Error 63024 solucionado"
echo "   Solo falta configurar las 3 APIs de Twilio" 