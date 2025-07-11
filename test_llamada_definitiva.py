#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DEFINITIVO - WEBHOOK ESPAÑOL CON SMS
Prueba final del sistema completo
"""

import os
from twilio.rest import Client

def test_llamada_definitiva():
    print("🎯 TEST FINAL - WEBHOOK ESPAÑOL DEFINITIVO")
    print("=" * 50)
    print("🇪🇸 Voz: Polly.Lucia (española)")
    print("🤖 Agente: 'agente comercial de DesArroyo Tech'")
    print("📱 SMS: CORREGIDO con credenciales .env")
    print("=" * 50)
    
    # Configuración automática
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    # Número del usuario (tu móvil)
    numero = "+34662513448"  # Tu número conocido
    
    # URL de ngrok actual
    print("\n🌐 Ve a http://localhost:4040 para tu URL de ngrok")
    ngrok_url = input("🔗 URL de ngrok (ej: https://xxxxx.ngrok.io): ").strip()
    
    if not ngrok_url.startswith('https://'):
        print("❌ Necesitas la URL HTTPS de ngrok")
        return
    
    # Webhook al definitivo (puerto 5001)
    webhook = f"{ngrok_url}/webhook-llamada?nombre=Test_Definitivo&sector=tecnologia&ciudad=Madrid"
    
    print(f"\n📞 LLAMADA DEFINITIVA A {numero}...")
    print(f"🔗 Webhook: {webhook[:60]}...")
    
    try:
        call = client.calls.create(
            to=numero,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            url=webhook,
            timeout=50,  # 50 segundos
            record=True
        )
        
        print(f"\n🎉 ¡LLAMADA DEFINITIVA ENVIADA!")
        print(f"📋 ID: {call.sid}")
        print(f"\n🎯 ESCUCHARÁS:")
        print(f"✅ Voz española perfecta (Polly.Lucia)")
        print(f"✅ 'Soy un agente comercial de DesArroyo Tech...'")
        print(f"✅ Presentación completa en español")
        print(f"✅ Presiona 1 = SÍ → SMS AUTOMÁTICO")
        print(f"✅ Presiona 2 = NO → Despedida cortés")
        print(f"\n📱 SMS llegará a {numero} si presionas 1")
        print(f"🚀 ¡SISTEMA DEFINITIVO FUNCIONANDO!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Verifica que el webhook definitivo esté corriendo")

if __name__ == '__main__':
    test_llamada_definitiva() 