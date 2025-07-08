#!/bin/bash

echo "🚀 CONFIGURANDO SISTEMA DE LEADS GRATUITO - DESARROYO TECH"
echo "=========================================================="

# 1. Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip3 install requests beautifulsoup4 lxml selenium

# 2. Dar permisos de ejecución al scraper
echo "🔧 Configurando permisos..."
chmod +x scripts/scraper_gratis.py

# 3. Probar el scraper
echo "🧪 Probando scraper gratuito..."
python3 scripts/scraper_gratis.py Madrid restaurantes

echo ""
echo "✅ ¡CONFIGURACIÓN COMPLETADA!"
echo ""
echo "💰 COSTOS ELIMINADOS:"
echo "  ❌ ScrapingBee: $49/mes → ✅ GRATIS"
echo "  ✅ Total ahorrado: $588/año"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "  1. Configura las variables en .env_leads_config"
echo "  2. Obtén tus API keys:"
echo "     - OpenAI: https://platform.openai.com/"
echo "     - Twilio: https://www.twilio.com/"
echo "     - Telegram: @BotFather"
echo "  3. Importa el flujo en n8n"
echo "  4. ¡Activa y disfruta!"
echo ""
echo "🎯 El sistema buscará leads GRATIS cada 6 horas" 