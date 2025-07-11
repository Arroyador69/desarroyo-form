#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST RÁPIDO DE LLAMADA - DESARROYO TECH
"""

import os
from twilio.rest import Client

def hacer_llamada_rapida():
    # Configuración automática
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    print("🎯 TEST RÁPIDO DE LLAMADA")
    print("=" * 40)
    
    # Número del usuario (auto-formateo)
    numero = input("📱 Tu número (ej: 662513448): ").strip()
    
    # Auto-formatear
    if not numero.startswith('+'):
        numero = f"+34{numero}"
    
    # URL de ngrok (simplificada)
    print(f"\n🌐 Ve a http://localhost:4040 y copia tu URL de ngrok")
    ngrok_url = input("🔗 URL de ngrok (ej: https://xxxxx.ngrok.io): ").strip()
    
    if not ngrok_url.startswith('https://'):
        print("❌ Necesitas la URL HTTPS de ngrok")
        return
    
    # Webhook completo
    webhook = f"{ngrok_url}/webhook-llamada?nombre=Restaurante_Test&sector=restaurantes&ciudad=Madrid"
    
    print(f"\n📞 HACIENDO LLAMADA A {numero}...")
    print(f"🔗 Webhook: {webhook[:50]}...")
    
    try:
        call = client.calls.create(
            to=numero,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            url=webhook,
            timeout=50,  # 50 segundos para los 40s de mensaje
            record=True
        )
        
        print(f"\n🎉 ¡LLAMADA ENVIADA!")
        print(f"📋 ID: {call.sid}")
        print(f"\n🎯 QUÉ ESCUCHARÁS:")
        print(f"1. 'Soy un agente comercial de DesArroyo Tech...'")
        print(f"2. '¿Le interesaría esta información?'")
        print(f"3. Presiona 1 = SÍ (recibirás SMS)")
        print(f"4. Presiona 2 = NO (se despide)")
        print(f"\n📱 ¡RESPONDE TU TELÉFONO!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if "credentials" in str(e).lower():
            print("💡 Verifica tus credenciales de Twilio en el .env")

if __name__ == '__main__':
    hacer_llamada_rapida() 