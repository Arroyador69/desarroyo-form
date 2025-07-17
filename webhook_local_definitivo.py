#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
from datetime import datetime
import pytz
import logging

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        
        # Respuesta inmediata para evitar timeouts
        
        # Verificar horario comercial
        if es_horario_comercial():
            # Mensaje durante horario comercial (con ofertas completas)
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, soy un agente comercial de DesArroyo Tech. Creamos páginas web profesionales en 48 horas. Puede solicitar una propuesta personalizada gratuita.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Presione 1 si está interesado y le enviamos una encuesta por SMS, o presione 2 si no está interesado. También puede visitarnos en desarroyo punto tech.
    </Say>
    <Gather input="dtmf" timeout="5" numDigits="1" action="https://426e7c2147d2.ngrok-free.app/webhook-respuesta">
        <Say voice="Polly.Lucia" language="es-ES">
            Esperando su respuesta...
        </Say>
    </Gather>
    <Say voice="Polly.Lucia" language="es-ES">
        Le enviamos información por SMS. Gracias por su tiempo.
    </Say>
</Response>'''
        else:
            # Mensaje fuera de horario comercial (con las mismas ofertas)
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, soy un agente comercial de DesArroyo Tech. Le llamamos fuera de horario comercial. Horario: lunes a viernes 9 a 14 y 16 a 20 horas.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Creamos páginas web profesionales en 48 horas. Presione 1 para recibir información por SMS, o presione 2 si no está interesado.
    </Say>
    <Gather input="dtmf" timeout="5" numDigits="1" action="https://426e7c2147d2.ngrok-free.app/webhook-respuesta">
        <Say voice="Polly.Lucia" language="es-ES">
            Esperando su respuesta...
        </Say>
    </Gather>
    <Say voice="Polly.Lucia" language="es-ES">
        Le enviamos información por SMS. Visite desarroyo punto tech. Gracias.
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
def webhook_respuesta():
    """Webhook para manejar respuestas del TwiML Bin"""
    try:
        # Obtener datos de la respuesta
        call_sid = request.form.get('CallSid', 'Unknown')
        from_number = request.form.get('From', 'Unknown')
        digits = request.form.get('Digits', '')
        
        logger.info(f"Respuesta recibida - CallSid: {call_sid}, From: {from_number}, Digits: {digits}")
        
        if digits == '1':
            # Cliente interesado - Respuesta positiva
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Perfecto, muchas gracias por su interés. Le enviaremos un SMS con información sobre nuestro servicio de páginas web profesionales en 48 horas.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Incluiremos ejemplos de nuestro trabajo y un enlace para solicitar una propuesta personalizada gratuita. También puede contactarnos en desarroyo punto tech.
    </Say>
</Response>'''
            
            # Aquí se enviaría el SMS (implementar después)
            logger.info(f"Cliente interesado - Número: {from_number}")
            
        elif digits == '2':
            # Cliente no interesado - Respuesta cortés
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Entendemos perfectamente. Disculpe las molestias y muchas gracias por su tiempo.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Si en el futuro necesita servicios web, puede encontrarnos en desarroyo punto tech. Que tenga un buen día.
    </Say>
</Response>'''
            
            logger.info(f"Cliente no interesado - Número: {from_number}")
            
        else:
            # No se recibió respuesta válida
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        No hemos recibido una respuesta válida. Le enviaremos información por SMS. Puede contactarnos en desarroyo punto tech. Gracias.
    </Say>
</Response>'''
            
            logger.info(f"Respuesta inválida - Número: {from_number}, Digits: {digits}")
        
        logger.info(f"Respuesta TwiML enviada para CallSid: {call_sid}")
        return Response(twiml_response, mimetype='application/xml')
        
    except Exception as e:
        logger.error(f"Error procesando respuesta: {str(e)}")
        # Respuesta de fallback
        fallback_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Gracias por su tiempo. Puede contactarnos en desarroyo punto tech. Que tenga un buen día.
    </Say>
</Response>'''
        return Response(fallback_response, mimetype='application/xml')

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud"""
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    print("🚀 Webhook de DesArroyo Tech iniciado")
    print("📞 Listo para manejar llamadas en español")
    print("🕐 Horarios comerciales configurados para España")
    print("📡 Puerto: 5001")
    print("🔗 URL local: http://localhost:5001/webhook-llamada")
    app.run(host='0.0.0.0', port=5001, debug=False) 