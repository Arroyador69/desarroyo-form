#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE LLAMADAS CORREGIDAS - DESARROYO TECH
Verifica que las llamadas funcionen en español y sin mencionar "Alberto"
"""

import os
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

# Cargar variables de entorno
load_dotenv()

def generar_twiml_prueba():
    """Generar TwiML de prueba para verificar el contenido"""
    response = VoiceResponse()
    
    # Pausa inicial
    response.pause(length=1)
    
    # Mensaje corregido SIN "Alberto"
    mensaje = """
    Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web para negocios locales.
    
    Estoy llamando específicamente por Restaurante Ejemplo. He visto que están en Madrid y me parece un negocio con mucho potencial.
    
    Me gustaría explicarle cómo podríamos ayudar a Restaurante Ejemplo a conseguir más clientes con una web profesional que aumente sus ventas.
    
    ¿Le interesaría escuchar esta información? Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.
    """
    
    # Configurar voz española
    gather = response.gather(
        num_digits=1,
        timeout=15,
        action='/webhook-respuesta?nombre=Restaurante_Ejemplo',
        method='POST'
    )
    
    gather.say(
        mensaje,
        voice='Polly.Lucia',  # Voz española femenina
        language='es-ES'      # Español de España
    )
    
    # Respuesta por defecto si no presiona nada
    response.say(
        "No he recibido su respuesta. Puede contactarnos en contacto@desarroyo.tech si lo desea. Que tenga un buen día.",
        voice='Polly.Lucia',
        language='es-ES'
    )
    
    response.hangup()
    return str(response)

def verificar_configuracion():
    """Verificar que la configuración sea correcta"""
    print("🔍 VERIFICANDO CONFIGURACIÓN...")
    print("=" * 60)
    
    # Verificar variables de entorno
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
    twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
    
    print(f"📞 TWILIO_ACCOUNT_SID: {'✅ Configurado' if twilio_sid else '❌ Falta'}")
    print(f"🔑 TWILIO_AUTH_TOKEN: {'✅ Configurado' if twilio_token else '❌ Falta'}")
    print(f"📱 TWILIO_PHONE_NUMBER: {twilio_phone if twilio_phone else '❌ Falta'}")
    print(f"🌐 WEBSITE_URL: {website_url}")
    print()
    
    # Verificar contenido del webhook
    print("📋 CONTENIDO DEL WEBHOOK:")
    print("=" * 30)
    twiml = generar_twiml_prueba()
    
    # Verificar que NO contenga "Alberto" 
    if "Alberto" in twiml:
        print("❌ ERROR: El TwiML contiene 'Alberto'")
        print("🔍 Líneas problemáticas:")
        for i, line in enumerate(twiml.split('\n'), 1):
            if "Alberto" in line:
                print(f"   {i}: {line.strip()}")
        return False
    else:
        print("✅ CORRECTO: No menciona 'Alberto'")
    
    # Verificar que contenga el texto correcto
    if "un agente comercial de DesArroyo Tech" in twiml:
        print("✅ CORRECTO: Usa 'un agente comercial de DesArroyo Tech'")
    else:
        print("❌ ERROR: No usa el texto correcto")
        return False
    
    # Verificar idioma español
    if 'language="es-ES"' in twiml:
        print("✅ CORRECTO: Configurado en español (es-ES)")
    else:
        print("❌ ERROR: No está configurado en español")
        return False
    
    # Verificar voz española
    if 'voice="Polly.Lucia"' in twiml:
        print("✅ CORRECTO: Usa voz española (Polly.Lucia)")
    else:
        print("❌ ERROR: No usa voz española")
        return False
    
    return True

def hacer_llamada_prueba():
    """Hacer una llamada de prueba"""
    print("\n📞 HACIENDO LLAMADA DE PRUEBA...")
    print("=" * 40)
    
    # Configuración
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    
    # Pedir número de prueba
    numero = input("📱 Tu número para prueba (ej: +34662513448): ").strip()
    
    if not numero.startswith('+34'):
        print("❌ El número debe estar en formato internacional (+34XXXXXXXXX)")
        return False
    
    # Generar webhook URL
    website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
    webhook_url = f"{website_url}/api/webhook-llamada?sector=restaurantes&nombre=Restaurante_Prueba&ciudad=Madrid"
    
    print(f"🔗 Webhook URL: {webhook_url}")
    print(f"📞 Llamando a: {numero}")
    print(f"📱 Desde: {os.getenv('TWILIO_PHONE_NUMBER')}")
    
    try:
        call = client.calls.create(
            to=numero,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            url=webhook_url,
            method='POST',
            timeout=30,
            record=True
        )
        
        print(f"\n🎉 ¡LLAMADA INICIADA!")
        print(f"📋 Call SID: {call.sid}")
        print(f"⏱️ Estado: {call.status}")
        print(f"\n🎯 QUÉ DEBES ESCUCHAR:")
        print(f"✅ Voz femenina española (Polly.Lucia)")
        print(f"✅ 'Soy un agente comercial de DesArroyo Tech...'")
        print(f"✅ NUNCA debe decir 'Alberto'")
        print(f"✅ Todo en español perfecto")
        print(f"✅ Pregunta si estás interesado")
        print(f"\n📱 INSTRUCCIONES:")
        print(f"1. Presiona 1 = SÍ (si tienes SMS configurado)")
        print(f"2. Presiona 2 = NO (se despide cortésmente)")
        print(f"\n🔍 SEGUIMIENTO:")
        print(f"   - Ve a Twilio Console → Monitor → Logs")
        print(f"   - Busca Call SID: {call.sid}")
        print(f"   - Escucha la grabación para verificar")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        
        # Diagnóstico de errores comunes
        if "21614" in str(e):
            print("💡 SOLUCIÓN: Tu número Twilio no tiene capacidad Voice")
            print("   - Ve a Twilio Console → Phone Numbers")
            print("   - Haz clic en tu número → Habilita Voice")
        elif "21217" in str(e):
            print("💡 SOLUCIÓN: Número de destino inválido")
            print("   - Verifica formato: +34XXXXXXXXX")
        elif "20003" in str(e):
            print("💡 SOLUCIÓN: Credenciales incorrectas")
            print("   - Verifica TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
        elif "webhook" in str(e).lower():
            print("💡 SOLUCIÓN: Webhook no accesible")
            print("   - Verifica que tu servidor esté corriendo")
            print("   - Verifica WEBSITE_URL en .env")
        
        return False

def main():
    """Función principal"""
    print("🚀 TEST DE LLAMADAS CORREGIDAS")
    print("=" * 60)
    print("✅ Sin mencionar 'Alberto' NUNCA")
    print("✅ Usa 'un agente comercial de DesArroyo Tech'")
    print("✅ Voz española (Polly.Lucia)")
    print("✅ Idioma español (es-ES)")
    print("✅ Email: contacto@desarroyo.tech")
    print("=" * 60)
    
    # Verificar configuración
    if not verificar_configuracion():
        print("\n❌ La configuración tiene errores. Corrígelos antes de continuar.")
        return
    
    print("\n✅ CONFIGURACIÓN CORRECTA")
    
    # Preguntar si hacer llamada
    hacer_llamada = input("\n¿Hacer llamada de prueba? (s/n): ").lower().strip()
    
    if hacer_llamada == 's':
        if hacer_llamada_prueba():
            print("\n🎉 ¡LLAMADA ENVIADA! Revisa tu teléfono.")
        else:
            print("\n❌ Error haciendo la llamada.")
    else:
        print("\n✅ Configuración verificada. Todo listo para producción.")

if __name__ == "__main__":
    main() 