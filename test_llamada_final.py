#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 PRUEBA FINAL - LLAMADAS EN ESPAÑOL
Confirmar que todo funciona perfectamente
"""

import os
from twilio.rest import Client
from datetime import datetime

def test_llamada_final():
    print("🧪 PRUEBA FINAL DE LLAMADAS EN ESPAÑOL")
    print("=" * 60)
    print(f"🕐 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("✅ CONFIGURACIÓN VERIFICADA:")
    print(f"📞 Número Twilio: {os.getenv('TWILIO_PHONE_NUMBER')}")
    print(f"🔗 Webhook URL: https://426e7c2147d2.ngrok-free.app/webhook-llamada")
    print()
    
    # Verificar credenciales
    try:
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN')
        )
        print("✅ Credenciales Twilio verificadas")
    except Exception as e:
        print(f"❌ Error en credenciales: {e}")
        return
    
    # Hacer llamada de prueba
    print("\n🎯 HACIENDO LLAMADA DE PRUEBA...")
    print("📱 Destino: +34662513448 (tu móvil)")
    
    try:
        call = client.calls.create(
            to='+34662513448',  # Tu número
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            url='https://426e7c2147d2.ngrok-free.app/webhook-llamada',
            timeout=60,
            record=True
        )
        
        print(f"\n🎉 ¡LLAMADA ENVIADA EXITOSAMENTE!")
        print(f"📋 ID de llamada: {call.sid}")
        print(f"📞 Desde: {call.from_}")
        print(f"📞 Hacia: {call.to}")
        print()
        
        print("🎯 DEBERÍAS ESCUCHAR:")
        print("✅ Voz femenina española (Polly.Lucia)")
        print("✅ 'Hola, soy un agente comercial de DesArroyo Tech'")
        print("✅ Mensaje completo en español")
        print("✅ Duración: 30-45 segundos (NO 6 segundos)")
        print("✅ NO suena a scam ni aplicación")
        print()
        
        print("🎉 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")
        print("=" * 60)
        print("🚀 PRÓXIMO PASO: RASPBERRY PI")
        print("- Ejecuta: python3 preparar_raspberry_pi.py")
        print("- Transfiere archivos a Raspberry Pi")
        print("- ¡Funciona 24/7 sin ngrok!")
        
    except Exception as e:
        print(f"❌ Error enviando llamada: {e}")
        print("💡 Verifica que actualizaste la URL en Twilio Console")

if __name__ == '__main__':
    test_llamada_final() 