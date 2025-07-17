#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Webhook DesArroyo.tech para Raspberry Pi 24/7
Sistema de llamadas automáticas con ofertas de desarrollo web
"""

import os
import sys
import json
import logging
from datetime import datetime, time
from flask import Flask, request, Response
from twilio.twiml import VoiceResponse
from twilio.rest import Client
from dotenv import load_dotenv
import requests
import pytz

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/desarroyo-webhook/webhook.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuración Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

# Configuración SMS
SMS_SERVICE_SID = os.getenv('SMS_SERVICE_SID')  # Opcional para SMS

# Zona horaria española
SPAIN_TZ = pytz.timezone('Europe/Madrid')

def es_horario_comercial():
    """Verificar si estamos en horario comercial (L-V 9-14h, 16-20h)"""
    try:
        ahora = datetime.now(SPAIN_TZ)
        dia_semana = ahora.weekday()  # 0=Lunes, 6=Domingo
        hora_actual = ahora.time()
        
        # Solo días laborables (L-V)
        if dia_semana > 4:  # Sábado o Domingo
            return False
        
        # Horario comercial: 9-14h y 16-20h
        return (time(9, 0) <= hora_actual <= time(14, 0)) or \
               (time(16, 0) <= hora_actual <= time(20, 0))
    except Exception as e:
        logger.error(f"Error verificando horario: {e}")
        return False

def obtener_mensaje_horario():
    """Obtener mensaje según horario comercial"""
    if es_horario_comercial():
        return {
            'es_comercial': True,
            'mensaje': """¡Hola! Soy un agente comercial de DesArroyo punto tech. 
            Te llamamos porque ofrecemos desarrollo de páginas web profesionales 
            en solo 48 horas. ¿Te interesa recibir más información por SMS? 
            Pulsa 1 para sí, o 2 si no te interesa."""
        }
    else:
        return {
            'es_comercial': False,
            'mensaje': """¡Hola! Soy un agente comercial de DesArroyo punto tech. 
            Te llamamos fuera del horario comercial. Desarrollamos páginas web 
            profesionales en 48 horas. ¿Te interesa recibir información por SMS? 
            Pulsa 1 para sí, o 2 si no te interesa."""
        }

def enviar_sms(numero, mensaje):
    """Enviar SMS usando Twilio"""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=mensaje,
            from_=TWILIO_PHONE_NUMBER,
            to=numero
        )
        
        logger.info(f"SMS enviado a {numero}: {message.sid}")
        return True
    except Exception as e:
        logger.error(f"Error enviando SMS a {numero}: {e}")
        return False

def registrar_interaccion(telefono, accion, datos=None):
    """Registrar interacción en archivo JSON"""
    try:
        registro = {
            'timestamp': datetime.now(SPAIN_TZ).isoformat(),
            'telefono': telefono,
            'accion': accion,
            'horario_comercial': es_horario_comercial(),
            'datos': datos or {}
        }
        
        # Guardar en archivo de log
        log_file = '/home/pi/desarroyo-webhook/interacciones.json'
        try:
            with open(log_file, 'r') as f:
                registros = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            registros = []
        
        registros.append(registro)
        
        # Mantener solo últimos 1000 registros
        registros = registros[-1000:]
        
        with open(log_file, 'w') as f:
            json.dump(registros, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Interacción registrada: {telefono} - {accion}")
        
    except Exception as e:
        logger.error(f"Error registrando interacción: {e}")

@app.route('/webhook-llamada', methods=['POST'])
def webhook_llamada():
    """Webhook principal para llamadas de Twilio"""
    try:
        # Obtener datos de la llamada
        from_number = request.form.get('From', 'Desconocido')
        call_sid = request.form.get('CallSid', 'Desconocido')
        
        logger.info(f"Llamada recibida de {from_number} - CallSid: {call_sid}")
        
        # Registrar llamada
        registrar_interaccion(from_number, 'llamada_recibida', {
            'call_sid': call_sid,
            'timestamp': datetime.now(SPAIN_TZ).isoformat()
        })
        
        # Crear respuesta TwiML
        response = VoiceResponse()
        
        # Obtener mensaje según horario
        info_mensaje = obtener_mensaje_horario()
        
        # Configurar gather para capturar respuesta
        gather = response.gather(
            input='dtmf',
            timeout=10,
            num_digits=1,
            action=f'/webhook-respuesta?from={from_number}',
            method='POST'
        )
        
        # Mensaje de voz (español, voz femenina)
        gather.say(
            info_mensaje['mensaje'],
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        # Si no responde, repetir mensaje
        response.say(
            "No he recibido respuesta. ¡Que tengas un buen día!",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        logger.info(f"Respuesta TwiML generada para {from_number}")
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error en webhook_llamada: {e}")
        
        # Respuesta de error
        response = VoiceResponse()
        response.say(
            "Lo sentimos, ha ocurrido un error. Inténtalo más tarde.",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        return Response(str(response), mimetype='text/xml')

@app.route('/webhook-respuesta', methods=['POST'])
def webhook_respuesta():
    """Procesar respuesta del usuario"""
    try:
        from_number = request.args.get('from') or request.form.get('From')
        digits = request.form.get('Digits', '')
        
        logger.info(f"Respuesta recibida de {from_number}: {digits}")
        
        response = VoiceResponse()
        
        if digits == '1':
            # Usuario interesado - enviar SMS
            mensaje_sms = """🚀 ¡Hola desde DesArroyo.tech!

Gracias por tu interés. Te ofrecemos:

✅ Página web profesional en 48 horas
✅ Diseño moderno y responsive
✅ Optimizada para móviles
✅ Desde 299€ todo incluido

¿Hablamos? Escríbenos a info@desarroyo.tech
O visita: https://desarroyo.tech

¡Llevamos tu negocio al siguiente nivel!"""
            
            if enviar_sms(from_number, mensaje_sms):
                response.say(
                    "Perfecto. Te hemos enviado toda la información por SMS. ¡Gracias por tu interés en DesArroyo punto tech!",
                    voice='Polly.Lucia',
                    language='es-ES'
                )
                
                registrar_interaccion(from_number, 'interesado_sms_enviado')
            else:
                response.say(
                    "Ha ocurrido un error enviando el SMS. Puedes contactarnos en info@desarroyo.tech",
                    voice='Polly.Lucia',
                    language='es-ES'
                )
                
                registrar_interaccion(from_number, 'interesado_sms_error')
            
        elif digits == '2':
            # Usuario no interesado
            response.say(
                "Entendido. Disculpa las molestias. ¡Que tengas un buen día!",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            registrar_interaccion(from_number, 'no_interesado')
            
        else:
            # Respuesta no válida
            response.say(
                "No he entendido tu respuesta. ¡Que tengas un buen día!",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            registrar_interaccion(from_number, 'respuesta_invalida', {'digits': digits})
        
        return Response(str(response), mimetype='text/xml')
        
    except Exception as e:
        logger.error(f"Error en webhook_respuesta: {e}")
        
        response = VoiceResponse()
        response.say(
            "Ha ocurrido un error. ¡Que tengas un buen día!",
            voice='Polly.Lucia',
            language='es-ES'
        )
        
        return Response(str(response), mimetype='text/xml')

@app.route('/estado', methods=['GET'])
def estado():
    """Endpoint para verificar estado del webhook"""
    try:
        info = {
            'estado': 'funcionando',
            'timestamp': datetime.now(SPAIN_TZ).isoformat(),
            'horario_comercial': es_horario_comercial(),
            'version': '1.0.0'
        }
        
        return json.dumps(info, indent=2, ensure_ascii=False)
        
    except Exception as e:
        logger.error(f"Error en endpoint estado: {e}")
        return json.dumps({'error': str(e)}, indent=2)

@app.route('/salud', methods=['GET'])
def salud():
    """Health check endpoint"""
    return "OK", 200

if __name__ == '__main__':
    try:
        logger.info("Iniciando webhook DesArroyo.tech...")
        logger.info(f"Horario comercial actual: {es_horario_comercial()}")
        
        # Ejecutar en puerto 5000
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except Exception as e:
        logger.error(f"Error iniciando aplicación: {e}")
        sys.exit(1) 