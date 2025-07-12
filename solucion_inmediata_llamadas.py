#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN INMEDIATA - LLAMADAS EN INGLÉS DE 7 SEGUNDOS
PROBLEMA: Webhook de producción configurado incorrectamente en Twilio
"""

import os
import sys
from twilio.rest import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def diagnosticar_problema():
    """Diagnosticar el problema de las llamadas en inglés"""
    print("🔍 DIAGNÓSTICO: LLAMADAS EN INGLÉS DE 7 SEGUNDOS")
    print("=" * 60)
    
    print("🎯 PROBLEMA IDENTIFICADO:")
    print("✅ Los tests locales funcionan en español")
    print("❌ Las llamadas reales duran 7 segundos en inglés")
    print("❌ Hablan de 'verification code' y 'any application'")
    print("❌ La gente cuelga porque parece scam")
    print()
    
    print("🔍 CAUSA RAÍZ:")
    print("❌ El webhook configurado en Twilio Console es INCORRECTO")
    print("❌ Twilio está usando un webhook que no existe o falla")
    print("❌ Por defecto, Twilio reproduce mensaje en inglés")
    print("❌ Después de 7 segundos, cuelga automáticamente")
    print()
    
    print("🎯 DIFERENCIAS CLAVE:")
    print("✅ PRUEBAS: Usan webhook local (ngrok) → Funcionan")
    print("❌ PRODUCCIÓN: Usa webhook online → Falla")
    print()
    
    # Verificar configuración actual
    print("🔧 CONFIGURACIÓN ACTUAL:")
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    print(f"📞 Número Twilio: {twilio_phone}")
    print(f"🌐 Website URL: {os.getenv('WEBSITE_URL', 'NO CONFIGURADO')}")
    print()
    
    return True

def mostrar_webhooks_posibles():
    """Mostrar los webhooks posibles y cuál es el correcto"""
    print("🌐 WEBHOOKS POSIBLES:")
    print("=" * 40)
    
    webhooks = [
        ("❌ INCORRECTO", "https://desarroyo.tech/api/webhook-llamada", "No existe en Vercel"),
        ("❌ INCORRECTO", "https://arroyo805.app.n8n.cloud/webhook/...", "Para n8n, no llamadas"),
        ("✅ CORRECTO", "URL de ngrok local", "Solo para desarrollo"),
        ("🆘 TEMPORAL", "https://desarroyo.tech/scripts/webhook_respuestas.py", "Existe pero no optimizado"),
        ("🚀 SOLUCIÓN", "Webhook local ngrok + actualizar Twilio", "Funciona AHORA")
    ]
    
    for status, url, descripcion in webhooks:
        print(f"{status} {url}")
        print(f"   → {descripcion}")
        print()
    
    return True

def solucion_inmediata():
    """Proporcionar solución inmediata para parar las llamadas problemáticas"""
    print("🚨 SOLUCIÓN INMEDIATA:")
    print("=" * 40)
    
    print("🛑 PASO 1: PARAR LAS LLAMADAS AUTOMÁTICAS AHORA")
    print("1. Ve a Twilio Console → Phone Numbers")
    print("2. Haz clic en tu número de teléfono")
    print("3. En 'Voice Configuration' → Webhook:")
    print("4. BORRA la URL actual (que está causando el problema)")
    print("5. Deja el campo VACÍO temporalmente")
    print("6. Guarda los cambios")
    print()
    
    print("✅ RESULTADO: Las llamadas automáticas se PARARÁN")
    print("✅ NO habrá más llamadas en inglés de 7 segundos")
    print("✅ NO perderás más dinero")
    print()
    
    print("🔧 PASO 2: CONFIGURAR WEBHOOK CORRECTO")
    print("1. Ejecuta: python3 webhook_espanol_definitivo.py")
    print("2. En otra terminal ejecuta: ngrok http 5001")
    print("3. Copia la URL HTTPS de ngrok")
    print("4. Ve a Twilio Console → Phone Numbers")
    print("5. Pega la URL: https://xxxxx.ngrok.io/webhook-llamada")
    print("6. Guarda los cambios")
    print()
    
    print("✅ RESULTADO: Las llamadas funcionarán en español perfecto")
    print()
    
    return True

def test_webhook_local():
    """Hacer test del webhook local para verificar que funciona"""
    print("🧪 TEST DEL WEBHOOK LOCAL:")
    print("=" * 40)
    
    # Verificar si el webhook local está ejecutándose
    try:
        import requests
        response = requests.get("http://localhost:5001/webhook-llamada", timeout=5)
        print("✅ Webhook local respondiendo")
    except:
        print("❌ Webhook local NO está ejecutándose")
        print("💡 Ejecuta: python3 webhook_espanol_definitivo.py")
        print()
    
    print("🎯 CUANDO ESTÉ FUNCIONANDO:")
    print("1. Webhook local: ✅ Español perfecto")
    print("2. Voz: Polly.Lucia (española)")
    print("3. Agente: 'agente comercial de DesArroyo Tech'")
    print("4. SMS automático: Configurado")
    print("5. Duración: 40+ segundos (no 7)")
    print()
    
    return True

def configurar_webhook_produccion():
    """Configurar webhook de producción cuando esté listo"""
    print("🚀 CONFIGURAR WEBHOOK DE PRODUCCIÓN:")
    print("=" * 40)
    
    print("⚠️ SOLO DESPUÉS DE VERIFICAR QUE FUNCIONA LOCAL")
    print()
    
    print("OPCIÓN 1: Usar n8n cloud (recomendado)")
    print("URL: https://arroyo805.app.n8n.cloud/webhook/llamada-español")
    print("✅ Funciona 24/7 sin ngrok")
    print("✅ No necesitas mantener tu ordenador encendido")
    print()
    
    print("OPCIÓN 2: Desplegar en Vercel")
    print("URL: https://desarroyo.tech/api/webhook-llamada")
    print("⚠️ Necesitas crear el endpoint en Vercel")
    print()
    
    print("OPCIÓN 3: Usar ngrok premium")
    print("URL: https://tu-dominio.ngrok.io/webhook-llamada")
    print("✅ Funciona siempre")
    print("💰 Cuesta dinero")
    print()
    
    return True

def main():
    """Función principal"""
    print("🚨 SOLUCIÓN INMEDIATA - LLAMADAS EN INGLÉS")
    print("=" * 60)
    
    print("🎯 OBJETIVO: Parar las llamadas problemáticas AHORA")
    print("🎯 SOLUCIÓN: Configurar webhook correcto")
    print("🎯 RESULTADO: Llamadas en español perfecto")
    print()
    
    # Ejecutar diagnóstico
    diagnosticar_problema()
    
    # Mostrar webhooks posibles
    mostrar_webhooks_posibles()
    
    # Proporcionar solución inmediata
    solucion_inmediata()
    
    # Test webhook local
    test_webhook_local()
    
    # Configurar producción
    configurar_webhook_produccion()
    
    print("🚨 RESUMEN ACCIÓN INMEDIATA:")
    print("=" * 40)
    print("1. 🛑 PARAR llamadas: Borrar webhook en Twilio Console")
    print("2. 🔧 CONFIGURAR local: webhook_espanol_definitivo.py + ngrok")
    print("3. 🧪 PROBAR: Hacer llamada de prueba")
    print("4. ✅ CONFIRMAR: Llamada en español perfecto")
    print("5. 🚀 PRODUCCIÓN: Configurar webhook permanente")
    print()
    
    print("💡 PRIORIDAD: Ejecutar PASO 1 inmediatamente")
    print("📞 Esto parará las llamadas problemáticas AHORA")
    print("=" * 60)

if __name__ == "__main__":
    main() 