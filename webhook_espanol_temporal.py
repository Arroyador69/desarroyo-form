#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK TEMPORAL DE EMERGENCIA - LLAMADAS EN ESPAÑOL
Solución temporal para el problema de "application code" en inglés
INCLUYE: SMS automático + detección móvil/fijo
"""

import os
import re
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configuración Twilio para SMS
try:
    twilio_client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    print("✅ Twilio configurado para SMS automático")
except:
    twilio_client = None
    print("⚠️ Twilio no configurado - SMS manual")

def es_telefono_movil_espanol(phone):
    """Detectar si es móvil español (6XX, 7XX)"""
    if not phone:
        return False
    
    # Limpiar número
    clean_phone = re.sub(r'[^\d]', '', phone)
    
    # Si empieza con +34, quitar
    if clean_phone.startswith('34'):
        clean_phone = clean_phone[2:]
    
    # Debe ser 9 dígitos y empezar por 6 o 7
    return len(clean_phone) == 9 and clean_phone[0] in ['6', '7']

def formatear_telefono_espanol(phone):
    """Formatear a E.164 español"""
    if not phone:
        return None
    
    # Limpiar número
    clean_phone = re.sub(r'[^\d]', '', phone)
    
    # Quitar +34 si ya lo tiene
    if clean_phone.startswith('34'):
        clean_phone = clean_phone[2:]
    
    # Debe ser 9 dígitos
    if len(clean_phone) != 9:
        return None
    
    return f"+34{clean_phone}"

def enviar_sms_automatico(telefono, nombre_negocio):
    """Enviar SMS con la encuesta automáticamente"""
    if not twilio_client:
        print(f"❌ No se puede enviar SMS - Twilio no configurado")
        return False
    
    try:
        mensaje = f"""¡Perfecto! Gracias por su interés.

🚀 DESARROYO TECH - Web profesional para {nombre_negocio}

📋 COMPLETE NUESTRA ENCUESTA (2 minutos):
https://desarroyo.tech/index_conectado_n8n.html

💰 3 PLANES DISPONIBLES:
🟢 Plan Rápida: 149€ (48h)
🟡 Plan Escalable: 449€
🔴 Plan Pro: 999€

📧 Dudas: alberto@desarroyo.tech

⚠️ NO responda a este SMS - Use la encuesta

¡Gracias por confiar en nosotros! 🚀"""

        message = twilio_client.messages.create(
            body=mensaje,
            from_=twilio_phone,
            to=telefono
        )
        
        print(f"✅ SMS enviado a {telefono}: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando SMS a {telefono}: {e}")
        return False

@app.route('/webhook-llamada', methods=['POST'])
def manejar_llamada():
    """Webhook de emergencia que habla SOLO en español"""
    
    # Obtener datos del formulario
    from_number = request.form.get('From', '')
    to_number = request.form.get('To', '')
    call_sid = request.form.get('CallSid', '')
    
    # Nombre del negocio desde parámetros o por defecto
    nombre_negocio = request.args.get('nombre', 'su negocio')
    sector = request.args.get('sector', 'restaurantes')
    ciudad = request.args.get('ciudad', '')
    
    print(f"📞 LLAMADA EN ESPAÑOL: {from_number} → {to_number}")
    print(f"🏢 Negocio: {nombre_negocio}, Sector: {sector}, Ciudad: {ciudad}")
    
    # Crear respuesta TwiML EN ESPAÑOL
    response = VoiceResponse()
    
    # PAUSA inicial
    response.pause(length=1)
    
    # MENSAJE PRINCIPAL EN ESPAÑOL
    mensaje = f"""
    Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web para negocios locales.
    
    Estoy llamando específicamente por {nombre_negocio}. He visto que están en {ciudad} y me parece un negocio con mucho potencial.
    
    Me gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más clientes con una web profesional que aumente sus ventas.
    
    ¿Le interesaría escuchar esta información? Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.
    """
    
    # Configurar voz española
    gather = response.gather(
        num_digits=1,
        timeout=15,  # Más tiempo para responder
        action=f'/webhook-respuesta?nombre={nombre_negocio}',
        method='POST'
    )
    
    gather.say(
        mensaje,
        voice='Polly.Lucia',  # Voz española femenina
        language='es-ES'      # Español de España
    )
    
    # Si no responde, despedirse en español
    response.say(
        "No he recibido su respuesta. Puede contactarnos en alberto@desarroyo.tech si lo desea. Que tenga un buen día.",
        voice='Polly.Lucia',
        language='es-ES'
    )
    
    response.hangup()
    
    return str(response)

@app.route('/webhook-respuesta', methods=['POST'])
def manejar_respuesta():
    """Maneja la respuesta del cliente con SMS automático"""
    
    digits = request.form.get('Digits', '')
    from_number = request.form.get('From', '')
    nombre_negocio = request.args.get('nombre', 'su negocio')
    
    response = VoiceResponse()
    
    if digits == '1':  # SÍ, interesado
        print(f"✅ INTERESADO: {from_number} - {nombre_negocio}")
        
        # DETECCIÓN INTELIGENTE: ¿Es móvil o fijo?
        es_movil = es_telefono_movil_espanol(from_number)
        telefono_formateado = formatear_telefono_espanol(from_number)
        
        if es_movil and telefono_formateado:
            # ===== CASO MÓVIL: SMS AUTOMÁTICO =====
            response.say(
                f"Perfecto, {nombre_negocio}. Le voy a enviar toda la información por SMS a este número. Revise su móvil en unos minutos.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.say(
                "Gracias por su tiempo. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # ENVIAR SMS AUTOMÁTICAMENTE
            enviar_sms_automatico(telefono_formateado, nombre_negocio)
            
        else:
            # ===== CASO FIJO: SOLICITAR MÓVIL =====
            response.say(
                f"Perfecto, {nombre_negocio}. Para enviarle la información por SMS, necesito un número de móvil.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.pause(length=1)
            
            # Solicitar número de móvil
            gather_movil = response.gather(
                num_digits=9,
                timeout=15,
                finish_on_key='#',
                action=f'/webhook-captura-movil?telefono_fijo={from_number}&nombre={nombre_negocio}',
                method='POST'
            )
            
            gather_movil.say(
                "¿Podría decirme un número de móvil donde enviarle la información? Dígame los 9 dígitos y termine con almohadilla.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # Si no proporciona móvil
            response.say(
                "No he recibido el número de móvil. No hay problema, puede contactarnos directamente por email en alberto@desarroyo.tech para recibir toda la información.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.say(
                "Gracias por su tiempo. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
        
    elif digits == '2':  # NO, no interesado
        response.say(
            "Entiendo. Si cambia de opinión, puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        print(f"❌ NO INTERESADO: {from_number}")
        
    else:  # Respuesta no válida
        response.say(
            "No he entendido su respuesta. Por favor, presione 1 para SÍ o 2 para NO.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        print(f"⚠️ RESPUESTA NO VÁLIDA: {from_number} - {digits}")
        
        # Dar otra oportunidad
        gather = response.gather(
            num_digits=1,
            timeout=5,
            action=f'/webhook-respuesta?nombre={nombre_negocio}',
            method='POST'
        )
        
        gather.say(
            "1 para SÍ, 2 para NO.",
            voice='Polly.Lucia',
            language='es-ES'
        )
    
    response.hangup()
    return str(response)

@app.route('/webhook-captura-movil', methods=['POST'])
def manejar_captura_movil():
    """Maneja el móvil dictado cuando el número original es fijo"""
    
    movil_dictado = request.form.get('Digits', '')
    telefono_fijo = request.args.get('telefono_fijo', '')
    nombre_negocio = request.args.get('nombre', 'su negocio')
    
    response = VoiceResponse()
    
    if movil_dictado and len(movil_dictado) == 9:
        # Formatear móvil dictado
        movil_formateado = f"+34{movil_dictado}"
        
        # Verificar que sea móvil válido
        if es_telefono_movil_espanol(movil_formateado):
            response.say(
                f"Perfecto. Le envío la información al móvil {movil_dictado}. Revise su móvil en unos minutos.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.say(
                "Gracias por su tiempo. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # ENVIAR SMS al móvil dictado
            enviar_sms_automatico(movil_formateado, nombre_negocio)
            
            print(f"✅ SMS enviado a móvil dictado: {movil_formateado} (desde fijo {telefono_fijo})")
            
        else:
            response.say(
                "El número que me ha dictado no parece un móvil válido. Puede contactarnos en alberto@desarroyo.tech para recibir la información.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            print(f"❌ Móvil dictado inválido: {movil_dictado}")
    else:
        response.say(
            "No he recibido un número válido. Puede contactarnos en alberto@desarroyo.tech para recibir toda la información.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        print(f"⚠️ No se recibió móvil válido: {movil_dictado}")
    
    response.hangup()
    return str(response)

@app.route('/status', methods=['GET'])
def status():
    """Estado del webhook"""
    return {
        'status': 'activo',
        'idioma': 'español',
        'voz': 'Polly.Lucia (es-ES)',
        'mensaje': 'Webhook funcionando correctamente en español'
    }

if __name__ == '__main__':
    print("🇪🇸 WEBHOOK ESPAÑOL COMPLETO INICIADO")
    print("✅ Las llamadas ahora hablarán en español")
    print("🎙️ Voz: Polly.Lucia (española femenina)")
    print("🤖 Agente: 'agente comercial de DesArroyo.tech'")
    print("📱 SMS automático: ACTIVADO")
    print("📞 Detección móvil/fijo: ACTIVADA")
    print("📋 Encuesta automática: INCLUIDA")
    print("📱 Puerto: 5001")
    print("🔗 URL: http://localhost:5001/webhook-llamada")
    print("\n🎯 FLUJO COMPLETO:")
    print("  1. Llamada → Presentación en español")
    print("  2. Si MÓVIL + SÍ → SMS automático con encuesta")
    print("  3. Si FIJO + SÍ → Pide móvil → SMS automático")
    print("  4. Si NO → Despedida cortés")
    print("\n🚨 INSTRUCCIONES TWILIO:")
    print("1. Ve a Twilio Console → Phone Numbers")
    print("2. Haz clic en tu número de teléfono")
    print("3. En 'Voice Configuration' → Webhook:")
    print("   URL: https://tu-dominio.ngrok.io/webhook-llamada")
    print("4. Guarda los cambios")
    print("\n🚀 ¡Todo el trabajo anterior CONSERVADO!")
    
    app.run(debug=True, port=5001, host='0.0.0.0') 