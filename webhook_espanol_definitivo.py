#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK ESPAÑOL DEFINITIVO - DESARROYO TECH
Sistema completo de llamadas automáticas en español con SMS
INCLUYE: Detección móvil/fijo, SMS automático, conversación natural
"""

import os
import re
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
import pytz
import logging

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Twilio para SMS
try:
    twilio_client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
    print("✅ Twilio configurado correctamente para SMS")
except Exception as e:
    twilio_client = None
    print(f"⚠️ Error configurando Twilio: {e}")

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
        
        print(f"✅ SMS enviado correctamente a {telefono}: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ Error enviando SMS a {telefono}: {e}")
        return False

def es_horario_comercial():
    """Verifica si estamos en horario comercial español"""
    # Zona horaria de España
    spain_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(spain_tz)
    
    # Día de la semana (0=lunes, 6=domingo)
    weekday = now.weekday()
    hour = now.hour
    
    # Lunes a viernes: 9-14h y 16-20h
    if weekday <= 4:  # Lunes a viernes
        return (9 <= hour < 14) or (16 <= hour < 20)
    
    # Sábados: 10-13h
    elif weekday == 5:  # Sábado
        return 10 <= hour < 13
    
    # Domingos: cerrado
    else:
        return False

@app.route('/webhook-llamada', methods=['POST'])
def webhook_llamada():
    """Webhook para manejar llamadas entrantes de Twilio"""
    try:
        # Log de la llamada
        call_sid = request.form.get('CallSid', 'Unknown')
        from_number = request.form.get('From', 'Unknown')
        to_number = request.form.get('To', 'Unknown')
        
        logger.info(f"Llamada recibida - CallSid: {call_sid}, From: {from_number}, To: {to_number}")
        
        # Verificar horario comercial
        if es_horario_comercial():
            # Mensaje durante horario comercial
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, gracias por atender. Soy un agente comercial de DesArroyo Tech, una empresa especializada en desarrollo web y automatización empresarial.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Le contactamos porque hemos identificado que su empresa podría beneficiarse de nuestros servicios de desarrollo web profesional. Podemos crear una página web personalizada para su negocio en tan solo 48 horas.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Nuestros servicios incluyen diseño web responsivo, optimización para móviles, integración con redes sociales y sistemas de gestión de contenido. Todo adaptado a las necesidades específicas de su empresa.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Si está interesado en conocer más sobre nuestros servicios, puede contactarnos a través de nuestra página web desarroyo punto tech, o llamarnos directamente. Estaremos encantados de preparar una propuesta personalizada para su negocio.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Gracias por su tiempo y esperamos poder ayudarle a potenciar su presencia digital. Que tenga un excelente día.
    </Say>
</Response>'''
        else:
            # Mensaje fuera de horario comercial
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, gracias por atender. Soy un agente comercial de DesArroyo Tech. Le hemos llamado fuera de nuestro horario comercial habitual. Nos disculpamos por la molestia.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Nuestro horario de atención es de lunes a viernes de 9 a 14 horas y de 16 a 20 horas, y sábados de 10 a 13 horas. Le contactaremos de nuevo en horario comercial para presentarle nuestra propuesta de desarrollo web.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Puede visitarnos en desarroyo punto tech para conocer más sobre nuestros servicios. Gracias por su tiempo. Que tenga un buen día.
    </Say>
</Response>'''
        
        logger.info(f"Respuesta TwiML enviada para CallSid: {call_sid}")
        return Response(twiml_response, mimetype='application/xml')
        
    except Exception as e:
        logger.error(f"Error procesando webhook: {str(e)}")
        # Respuesta de fallback en caso de error
        fallback_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, gracias por atender. Soy un agente comercial de DesArroyo Tech. Disculpe, tenemos un problema técnico temporal. Puede contactarnos en desarroyo punto tech. Gracias.
    </Say>
</Response>'''
        return Response(fallback_response, mimetype='application/xml')

@app.route('/webhook-respuesta', methods=['POST'])
def manejar_respuesta():
    """Maneja la respuesta del cliente con SMS automático inteligente"""
    
    digits = request.form.get('Digits', '')
    from_number = request.form.get('From', '')
    nombre_negocio = request.args.get('nombre', 'su negocio')
    
    response = VoiceResponse()
    
    if digits == '1':  # SÍ, interesado
        print(f"✅ CLIENTE INTERESADO: {from_number} - {nombre_negocio}")
        
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
            
            response.say(
                "Dígame su número de móvil después del tono. Le responderemos cuanto antes.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # Capturar número de móvil con timeout generoso
            response.record(
                action=f'/webhook-captura-movil?nombre={nombre_negocio}',
                method='POST',
                max_length=30,
                timeout=10,
                play_beep=True
            )
        
    elif digits == '2':  # NO interesado
        print(f"❌ No interesado: {from_number} - {nombre_negocio}")
        
        response.say(
            "Entiendo perfectamente. Muchas gracias por su tiempo y disculpe las molestias. Que tenga un buen día.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
    else:  # Respuesta no válida
        print(f"⚠️ Respuesta no válida: {digits} - {from_number}")
        
        response.say(
            "No he entendido su respuesta. Presione 1 para SÍ o 2 para NO.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        # Volver a preguntar
        gather = response.gather(
            num_digits=1,
            timeout=10,
            action=f'/webhook-respuesta?nombre={nombre_negocio}',
            method='POST'
        )
    
    response.hangup()
    return str(response)

@app.route('/webhook-captura-movil', methods=['POST'])
def manejar_captura_movil():
    """Captura número de móvil para envío de SMS"""
    
    from_number = request.form.get('From', '')
    nombre_negocio = request.args.get('nombre', 'su negocio')
    recording_url = request.form.get('RecordingUrl', '')
    
    print(f"📱 Capturado móvil para: {from_number} - {nombre_negocio}")
    print(f"🎙️ Grabación: {recording_url}")
    
    response = VoiceResponse()
    
    response.say(
        "Perfecto. Hemos recibido su número de móvil. Le enviaremos la información por SMS en unos minutos. Gracias.",
        voice='Polly.Lucia',
        language='es-ES'
    )
    
    response.hangup()
    
    # TODO: Procesar grabación para extraer número
    # Por ahora, notificar manualmente
    print(f"🔄 ACCIÓN REQUERIDA: Procesar grabación {recording_url} para extraer móvil")
    
    return str(response)

@app.route('/status', methods=['GET'])
def status():
    """Estado del webhook español definitivo"""
    return {
        'status': 'activo',
        'version': 'español_definitivo_v1.0',
        'funciones': [
            'Voz española (Polly.Lucia)',
            'Agente comercial (NO Alberto)',
            'Detección móvil/fijo',
            'SMS automático',
            'Conversación natural'
        ],
        'twilio_configurado': twilio_client is not None
    }

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    print("🚀 Webhook de DesArroyo Tech iniciado")
    print("📞 Listo para manejar llamadas en español")
    print("🕐 Horarios comerciales configurados para España")
    app.run(host='0.0.0.0', port=5000, debug=False) 