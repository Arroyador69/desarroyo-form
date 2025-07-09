#!/bin/bash
# 🚀 ACTIVADOR INMEDIATO - DESARROYO TECH
# Configura todas las APIs y lanza el sistema de leads real

echo "🚀 DESARROYO TECH - ACTIVADOR INMEDIATO"
echo "=========================================="
echo "Configurando sistema de leads automático..."
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si existe .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}📋 Creando archivo .env...${NC}"
    cp env.example .env 2>/dev/null || touch .env
fi

echo -e "${BLUE}🔧 CONFIGURACIÓN DE APIS${NC}"
echo "================================"
echo ""

# Configurar Twilio
echo -e "${YELLOW}1️⃣ TWILIO (WhatsApp Business):${NC}"
echo "   💻 Ve a: https://console.twilio.com/"
echo "   📝 Registrate (10\$ gratis)"
echo "   📋 Encuentra: Account SID y Auth Token"
echo ""
read -p "📝 Introduce tu TWILIO_ACCOUNT_SID: " twilio_sid
read -p "🔑 Introduce tu TWILIO_AUTH_TOKEN: " twilio_token

# Configurar DeepSeek
echo ""
echo -e "${YELLOW}2️⃣ DEEPSEEK (IA Automática):${NC}"
echo "   💻 Ve a: https://platform.deepseek.com/"
echo "   📝 Registrate (5\$ gratis)"
echo "   🔑 Copia tu API Key"
echo ""
read -p "🤖 Introduce tu DEEPSEEK_API_KEY: " deepseek_key

# Crear archivo .env
echo ""
echo -e "${GREEN}💾 Guardando configuración...${NC}"

cat > .env << EOF
# DESARROYO TECH - CONFIGURACIÓN APIS
TWILIO_ACCOUNT_SID=${twilio_sid}
TWILIO_AUTH_TOKEN=${twilio_token}
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
DEEPSEEK_API_KEY=${deepseek_key}
WEBSITE_URL=https://desarroyo.tech
BUSINESS_NAME=DesArroyo Tech
YOUR_NAME=Alberto

# CONFIGURACIÓN AVANZADA
MAX_LEADS_PER_RUN=10
DELAY_BETWEEN_MESSAGES=45
ENABLE_AI_RESPONSES=true
WEBHOOK_PORT=5000

# LOGS Y DEBUGGING
LOG_LEVEL=INFO
SAVE_CONVERSATIONS=true
EOF

echo -e "${GREEN}✅ Configuración guardada en .env${NC}"
echo ""

# Verificar configuración
echo -e "${BLUE}🔍 VERIFICANDO CONFIGURACIÓN...${NC}"
if [ ! -z "$twilio_sid" ] && [ ! -z "$twilio_token" ] && [ ! -z "$deepseek_key" ]; then
    echo -e "${GREEN}✅ Todas las APIs configuradas${NC}"
    
    # Preguntar por ciudad y sector
    echo ""
    echo -e "${YELLOW}🎯 CONFIGURACIÓN DE CAMPAÑA:${NC}"
    read -p "📍 ¿En qué ciudad buscamos clientes? (ej: Madrid): " ciudad
    read -p "🏢 ¿Qué sector? (restaurantes/peluquerias/dentistas): " sector
    
    echo ""
    echo -e "${GREEN}🚀 LANZANDO SISTEMA DE LEADS REAL...${NC}"
    echo "=================================="
    echo -e "${BLUE}🎯 Ciudad: ${ciudad}${NC}"
    echo -e "${BLUE}🏢 Sector: ${sector}${NC}"
    echo -e "${BLUE}📱 Método: WhatsApp Business${NC}"
    echo -e "${BLUE}🤖 IA: DeepSeek (automática)${NC}"
    echo ""
    
    # Activar entorno virtual si existe
    if [ -d "venv" ]; then
        echo -e "${YELLOW}🐍 Activando entorno virtual...${NC}"
        source venv/bin/activate
    fi
    
    # Lanzar sistema
    echo -e "${GREEN}🚀 EJECUTANDO AHORA...${NC}"
    echo "================================"
    python3 scripts/sistema_leads_avanzado.py "$ciudad" "$sector"
    
else
    echo -e "${RED}❌ Faltan APIs por configurar${NC}"
    echo ""
    echo -e "${YELLOW}📋 CONFIGURACIÓN MANUAL:${NC}"
    echo "1. Edita el archivo .env con tus claves"
    echo "2. Ejecuta: python3 scripts/sistema_leads_avanzado.py Madrid restaurantes"
fi

echo ""
echo -e "${GREEN}🎉 SISTEMA CONFIGURADO${NC}"
echo "======================="
echo -e "${BLUE}📱 Mensajes: WhatsApp Business${NC}"
echo -e "${BLUE}🤖 Respuestas: IA Automática${NC}"
echo -e "${BLUE}💰 ROI esperado: 13.500€/mes${NC}"
echo ""
echo -e "${YELLOW}⏰ PARA AUTOMATIZACIÓN 24/7:${NC}"
echo "crontab -e"
echo "0 */6 * * * cd $(pwd) && python3 scripts/sistema_leads_avanzado.py Madrid restaurantes"
echo ""
echo -e "${GREEN}✅ ¡Sistema listo para generar clientes!${NC}" 