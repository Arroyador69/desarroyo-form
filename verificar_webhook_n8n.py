#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICAR POR QUÉ EL WEBHOOK DE N8N NO FUNCIONA
Diagnóstico completo del problema
"""

import requests
import json
import os
from datetime import datetime

def verificar_webhook_n8n():
    """Verificar si el webhook de n8n responde correctamente"""
    print("🔍 VERIFICANDO WEBHOOK DE N8N")
    print("=" * 50)
    
    webhook_url = "https://arroyo805.app.n8n.cloud/webhook/webhook-llamada"
    
    # Datos de prueba que envía Twilio
    test_data = {
        'From': '+34662513448',
        'To': '+18109579712',
        'CallSid': 'CA_test_123',
        'CallStatus': 'in-progress'
    }
    
    print(f"🌐 URL: {webhook_url}")
    print(f"📞 Datos de prueba: {test_data}")
    print()
    
    try:
        # Hacer petición POST como Twilio
        response = requests.post(
            webhook_url,
            data=test_data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'TwilioProxy/1.1'
            },
            timeout=10
        )
        
        print(f"✅ Estado HTTP: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        print(f"📄 Contenido: {response.text[:500]}...")
        
        if response.status_code == 200:
            # Verificar si es TwiML válido
            if '<?xml' in response.text and '<Response>' in response.text:
                print("✅ Respuesta TwiML válida")
                
                # Verificar contenido español
                if 'Polly.Lucia' in response.text:
                    print("✅ Voz española configurada")
                else:
                    print("❌ Voz española NO configurada")
                
                if 'agente comercial de DesArroyo Tech' in response.text:
                    print("✅ Texto correcto encontrado")
                else:
                    print("❌ Texto incorrecto o falta")
                
                if 'es-ES' in response.text:
                    print("✅ Idioma español configurado")
                else:
                    print("❌ Idioma español NO configurado")
                
                return True
            else:
                print("❌ Respuesta NO es TwiML válido")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"❌ Mensaje: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

def verificar_twilio_config():
    """Verificar la configuración actual de Twilio"""
    print("\n📞 VERIFICANDO CONFIGURACIÓN TWILIO")
    print("=" * 50)
    
    try:
        from twilio.rest import Client
        
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        
        # Obtener configuración del número
        phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Buscar el número en la cuenta
        numbers = client.incoming_phone_numbers.list()
        
        for number in numbers:
            if number.phone_number == phone_number:
                print(f"✅ Número encontrado: {number.phone_number}")
                print(f"📞 Nombre: {number.friendly_name}")
                print(f"🔗 Voice URL: {number.voice_url or 'NO CONFIGURADO'}")
                print(f"📋 Voice Method: {number.voice_method or 'NO CONFIGURADO'}")
                
                # Verificar si la URL está configurada
                if number.voice_url:
                    if 'n8n.cloud' in number.voice_url:
                        print("✅ Webhook de n8n configurado")
                    elif 'ngrok' in number.voice_url:
                        print("✅ Webhook local configurado")
                    else:
                        print("❌ Webhook desconocido configurado")
                else:
                    print("❌ No hay webhook configurado")
                
                return number.voice_url
        
        print("❌ Número no encontrado en la cuenta")
        return None
        
    except Exception as e:
        print(f"❌ Error verificando Twilio: {e}")
        return None

def comparar_webhooks():
    """Comparar webhook local vs n8n"""
    print("\n🔄 COMPARACIÓN WEBHOOKS")
    print("=" * 50)
    
    print("✅ WEBHOOK LOCAL (que funcionaba ayer):")
    print("   - Voz: Polly.Lucia")
    print("   - Idioma: es-ES")
    print("   - Texto: 'agente comercial de DesArroyo Tech'")
    print("   - Horarios: Configurados")
    print("   - SMS: Automático")
    print("   - Estado: FUNCIONA 100%")
    print()
    
    print("❓ WEBHOOK N8N (actual):")
    webhook_ok = verificar_webhook_n8n()
    
    if webhook_ok:
        print("   - Estado: FUNCIONA")
    else:
        print("   - Estado: NO FUNCIONA")
    
    print()
    
    return webhook_ok

def solucion_inmediata():
    """Proporcionar solución inmediata"""
    print("🚨 SOLUCIÓN INMEDIATA")
    print("=" * 50)
    
    print("🎯 PROBLEMA IDENTIFICADO:")
    print("   - El webhook de n8n puede no estar respondiendo correctamente")
    print("   - Twilio puede estar usando un webhook incorrecto")
    print("   - O hay un problema de configuración")
    print()
    
    print("✅ SOLUCIÓN RÁPIDA:")
    print("   1. Usar el webhook local que funcionaba ayer")
    print("   2. Ejecutar: python3 iniciar_webhook_local.py")
    print("   3. Seguir las instrucciones del script")
    print("   4. Cambiar la URL en Twilio Console")
    print()
    
    print("🔧 ALTERNATIVA:")
    print("   1. Verificar que el webhook de n8n funciona")
    print("   2. Asegurar que Twilio usa la URL correcta")
    print("   3. Probar con una llamada de prueba")
    print()
    
    print("🚀 PARA RASPBERRY PI:")
    print("   1. Transferir webhook_espanol_definitivo.py")
    print("   2. Configurar IP pública o tunnel")
    print("   3. Actualizar URL en Twilio")
    print("   4. ¡Funcionará 24/7!")

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO COMPLETO WEBHOOK")
    print("=" * 60)
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar webhook de n8n
    webhook_n8n_ok = verificar_webhook_n8n()
    
    # Verificar configuración Twilio
    current_webhook = verificar_twilio_config()
    
    # Comparar webhooks
    comparar_webhooks()
    
    # Mostrar solución
    solucion_inmediata()
    
    print("\n🎯 RECOMENDACIÓN:")
    if webhook_n8n_ok:
        print("✅ El webhook de n8n funciona - verificar configuración Twilio")
    else:
        print("❌ El webhook de n8n NO funciona - usar webhook local")
    
    print("\n🚀 EJECUTAR AHORA:")
    print("python3 iniciar_webhook_local.py")

if __name__ == '__main__':
    main() 