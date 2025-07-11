#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE LLAMADA PROPIA - DESARROYO TECH
Prueba el sistema de llamadas haciendo una llamada a tu propio número
"""

import os
import sys
from twilio.rest import Client

def hacer_llamada_prueba():
    """Hacer llamada de prueba al propio número"""
    
    # Configuración
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not all([twilio_sid, twilio_token, twilio_phone]):
        print("❌ ERROR: Variables de Twilio no configuradas")
        print("Necesitas configurar:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN") 
        print("- TWILIO_PHONE_NUMBER")
        return False
    
    # Crear cliente Twilio
    try:
        client = Client(twilio_sid, twilio_token)
        print("✅ Cliente Twilio conectado")
    except Exception as e:
        print(f"❌ Error conectando a Twilio: {e}")
        return False
    
    # Tu número de prueba (puedes cambiarlo)
    print("\n🎯 LLAMADA DE PRUEBA")
    tu_numero = input("📱 ¿Cuál es tu número de móvil? (formato: +34XXXXXXXXX): ").strip()
    
    if not tu_numero.startswith('+34'):
        print("❌ El número debe empezar por +34")
        return False
    
    # URL del webhook (necesitas la URL de ngrok)
    print("\n🌐 CONFIGURACIÓN WEBHOOK")
    webhook_url = input("🔗 Pega aquí tu URL de ngrok (ej: https://xxxxx.ngrok.io): ").strip()
    
    if not webhook_url.startswith('https://'):
        print("❌ La URL debe ser HTTPS de ngrok")
        return False
    
    # URL completa del webhook
    webhook_completa = f"{webhook_url}/webhook-llamada?nombre=Negocio_Prueba&sector=restaurantes&ciudad=Madrid"
    
    print(f"\n📞 REALIZANDO LLAMADA DE PRUEBA:")
    print(f"   📱 Desde: {twilio_phone}")
    print(f"   📞 Hacia: {tu_numero}")
    print(f"   🔗 Webhook: {webhook_completa}")
    
    try:
        # Realizar llamada
        call = client.calls.create(
            to=tu_numero,
            from_=twilio_phone,
            url=webhook_completa,
            method='POST',
            timeout=30,
            record=True  # Grabar para revisar después
        )
        
        print(f"\n🎉 ¡LLAMADA INICIADA EXITOSAMENTE!")
        print(f"📋 Call SID: {call.sid}")
        print(f"⏱️ Estado: {call.status}")
        print(f"\n🎯 QUÉ ESPERAR:")
        print(f"1. 📞 Recibirás una llamada en {tu_numero}")
        print(f"2. 🎙️ Escucharás: 'Soy un agente comercial de DesArroyo Tech...'")
        print(f"3. ❓ Te preguntará: '¿Le interesaría esta información?'")
        print(f"4. 📱 Presiona 1 para SÍ (recibirás SMS) o 2 para NO")
        print(f"\n🔍 SEGUIMIENTO:")
        print(f"   - Ve a Twilio Console → Monitor → Logs → Calls")
        print(f"   - Busca el Call SID: {call.sid}")
        print(f"   - Puedes escuchar la grabación después")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR haciendo llamada: {e}")
        
        # Errores comunes
        if "21614" in str(e):
            print("💡 SOLUCIÓN: Tu número Twilio no tiene capacidad de llamadas")
            print("   Ve a Twilio Console → Phone Numbers → Configurar Voice")
        elif "21217" in str(e):
            print("💡 SOLUCIÓN: Número de destino inválido")
            print("   Verifica el formato: +34XXXXXXXXX")
        elif "20003" in str(e):
            print("💡 SOLUCIÓN: Credenciales incorrectas")
            print("   Verifica TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
        
        return False

if __name__ == '__main__':
    print("🎯 TEST DE LLAMADA PROPIA - DESARROYO TECH")
    print("=" * 50)
    print("Este script te hará una llamada de prueba para que veas")
    print("exactamente cómo funciona tu sistema automático.")
    print("=" * 50)
    
    exito = hacer_llamada_prueba()
    
    if exito:
        print(f"\n✅ ¡Llamada iniciada! Revisa tu teléfono.")
        print(f"📱 Si no recibes llamada en 30 segundos:")
        print(f"   1. Verifica que ngrok esté funcionando")
        print(f"   2. Verifica que el webhook esté activo")
        print(f"   3. Revisa los logs de Twilio")
    else:
        print(f"\n❌ No se pudo realizar la llamada de prueba")
        print(f"   Revisa la configuración y vuelve a intentar") 