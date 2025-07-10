#!/bin/bash

# 🇪🇸 CONFIGURACIÓN RÁPIDA TWILIO ESPAÑA - DESARROYO TECH
# Script para configurar llamadas optimizadas con número español

echo "🚀 CONFIGURACIÓN TWILIO OPTIMIZADA PARA ESPAÑA"
echo "================================================"

# Verificar si twilio CLI está instalado
if ! command -v twilio &> /dev/null; then
    echo "📥 Instalando Twilio CLI..."
    npm install -g twilio-cli
fi

# Login si no está autenticado
echo "🔐 Verificando autenticación Twilio..."
twilio profiles:list > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ No estás autenticado en Twilio"
    echo "🔑 Ejecuta: twilio profiles:create"
    echo "   📧 Usa tu Account SID y Auth Token"
    exit 1
fi

echo "✅ Twilio CLI configurado"

# Buscar números disponibles en España
echo ""
echo "🇪🇸 BUSCANDO NÚMEROS ESPAÑOLES DISPONIBLES..."
echo "📞 Números fijos españoles (+34):"
twilio phone-numbers:list:available:local --country-code ES --limit 5

echo ""
echo "📱 Números móviles españoles (+34):"
twilio phone-numbers:list:available:mobile --country-code ES --limit 3

echo ""
echo "💰 PRECIOS APROXIMADOS:"
echo "   📞 Número fijo español: ~€3-8/mes"
echo "   📱 Número móvil español: ~€15-25/mes"
echo "   📞 Llamadas salientes: €0.12/minuto"
echo "   📱 SMS salientes: €0.075/mensaje"

echo ""
echo "🎯 RECOMENDACIÓN PARA DESARROYO TECH:"
echo "   ✅ Usar número FIJO español (+34 9XX XXX XXX)"
echo "   ✅ Caller ID personalizado con tu empresa"
echo "   ✅ Detectar spam/contestadores automáticamente"
echo "   ✅ Timeout 30s para minimizar costes"

echo ""
echo "🔧 CONFIGURACIÓN EN .ENV:"
echo "TWILIO_PHONE_NUMBER=+34XXXXXXXXX  # Tu número español comprado"
echo "TWILIO_ACCOUNT_SID=ACxxxxxxxxx     # Tu Account SID"
echo "TWILIO_AUTH_TOKEN=xxxxxxxxx       # Tu Auth Token"

echo ""
echo "🛒 PARA COMPRAR UN NÚMERO:"
echo "1. Elige un número de la lista de arriba"
echo "2. Ejecuta: twilio phone-numbers:buy --phone-number=+34XXXXXXXXX"
echo "3. Añádelo a tu .env como TWILIO_PHONE_NUMBER"
echo "4. ¡Ya puedes hacer llamadas con caller ID español!"

echo ""
echo "🧪 PRIMERA PRUEBA:"
echo "1. Configura el número en .env"
echo "2. Ejecuta: python3 scripts/sistema_leads_avanzado.py Madrid restaurantes --llamadas --limite 1"
echo "3. Revisa tu teléfono y Telegram para resultados"

echo ""
echo "📊 ESTADÍSTICAS ESPERADAS:"
echo "   📞 Tasa respuesta: 35-50% (números de negocio)"
echo "   💰 Coste por llamada contestada: €0.08-0.15"
echo "   💰 Coste por llamada rechazada: €0.02-0.05"
echo "   🎯 Conversión esperada: 40% de los que contestan dicen SÍ"

echo ""
echo "🚨 PROBLEMAS COMUNES Y SOLUCIONES:"
echo "❌ 'Spam probable' → Usar número español fijo"
echo "❌ 'No contestan' → Llamar en horarios comerciales 10-13h, 16-19h"  
echo "❌ 'Muy caro' → Reducir timeout a 20-30s, filtrar mejor leads"
echo "❌ 'Buzón de voz' → Sistema lo detecta y corta automáticamente"

echo ""
echo "✅ ¡CONFIGURACIÓN LISTA!"
echo "📞 ¡A hacer llamadas inteligentes con DesArroyo Tech!" 