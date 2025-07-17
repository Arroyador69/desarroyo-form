#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para webhook mejorado de DesArroyo Tech
Verifica que los mensajes incluyan las ofertas de web personalizada en 48 horas
"""

import requests
import json
from datetime import datetime

def test_webhook_llamada():
    """Prueba el webhook de llamada"""
    webhook_url = "https://426e7c2147d2.ngrok-free.app/webhook-llamada"
    
    # Datos simulados de Twilio
    test_data = {
        'CallSid': 'CAtest_webhook_mejorado',
        'From': '+34662513448',
        'To': '+18109579712',
        'CallStatus': 'ringing'
    }
    
    print("🧪 Probando webhook de llamada mejorado...")
    print(f"📞 CallSid: {test_data['CallSid']}")
    print(f"📱 From: {test_data['From']}")
    print(f"📲 To: {test_data['To']}")
    print("-" * 50)
    
    try:
        # Hacer la petición POST
        response = requests.post(webhook_url, data=test_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Webhook responde correctamente")
            print(f"📊 Status Code: {response.status_code}")
            print(f"📄 Content Type: {response.headers.get('content-type', 'N/A')}")
            
            # Mostrar el TwiML generado
            print("\n🎯 TwiML generado:")
            print(response.text)
            
            # Verificar que incluye las ofertas esperadas
            twiml_text = response.text.lower()
            
            print("\n🔍 Verificando ofertas incluidas:")
            
            # Verificar web personalizada en 48 horas
            if "48 horas" in twiml_text:
                print("✅ Incluye oferta de web personalizada en 48 horas")
            else:
                print("❌ NO incluye oferta de web personalizada en 48 horas")
            
            # Verificar SMS
            if "sms" in twiml_text:
                print("✅ Incluye opción de SMS")
            else:
                print("❌ NO incluye opción de SMS")
            
            # Verificar botones de respuesta
            if "presione 1" in twiml_text:
                print("✅ Incluye botón de respuesta (Presione 1)")
            else:
                print("❌ NO incluye botón de respuesta")
            
            # Verificar gather para capturar respuesta
            if "<gather" in twiml_text:
                print("✅ Incluye captura de respuesta del usuario")
            else:
                print("❌ NO incluye captura de respuesta")
                
        else:
            print(f"❌ Error en webhook: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

def test_webhook_respuesta():
    """Prueba el webhook de respuesta"""
    webhook_url = "https://426e7c2147d2.ngrok-free.app/webhook-respuesta"
    
    # Datos simulados de respuesta interesado
    test_data = {
        'CallSid': 'CAtest_respuesta_mejorado',
        'From': '+34662513448',
        'Digits': '1'
    }
    
    print("\n🧪 Probando webhook de respuesta mejorado...")
    print(f"📞 CallSid: {test_data['CallSid']}")
    print(f"📱 From: {test_data['From']}")
    print(f"🔢 Digits: {test_data['Digits']}")
    print("-" * 50)
    
    try:
        response = requests.post(webhook_url, data=test_data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Webhook de respuesta funciona correctamente")
            print(f"📊 Status Code: {response.status_code}")
            
            # Mostrar el TwiML generado
            print("\n🎯 TwiML de respuesta generado:")
            print(response.text)
            
            # Verificar que incluye las ofertas esperadas
            twiml_text = response.text.lower()
            
            print("\n🔍 Verificando mensaje de respuesta:")
            
            # Verificar web personalizada en 48 horas
            if "48 horas" in twiml_text:
                print("✅ Menciona web personalizada en 48 horas")
            else:
                print("❌ NO menciona web personalizada en 48 horas")
            
            # Verificar SMS
            if "sms" in twiml_text:
                print("✅ Menciona envío de SMS")
            else:
                print("❌ NO menciona envío de SMS")
                
        else:
            print(f"❌ Error en webhook de respuesta: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")

if __name__ == "__main__":
    print("🚀 DesArroyo Tech - Test Webhook Mejorado")
    print("=" * 60)
    print(f"⏰ Tiempo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Verificando ofertas de web personalizada en 48 horas y SMS")
    print("=" * 60)
    
    # Probar webhook de llamada
    test_webhook_llamada()
    
    # Probar webhook de respuesta
    test_webhook_respuesta()
    
    print("\n" + "=" * 60)
    print("🎉 Pruebas completadas")
    print("💡 Si todo está OK, tu webhook está listo para llamadas reales")
    print("🔗 URL del webhook: https://426e7c2147d2.ngrok-free.app/webhook-llamada") 