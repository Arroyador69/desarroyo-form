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
            # Mensaje durante horario comercial (optimizado para velocidad)
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, soy un agente comercial de DesArroyo Tech. Creamos páginas web profesionales en 48 horas. Puede contactarnos en desarroyo punto tech para una propuesta personalizada. Gracias.
    </Say>
</Response>'''
        else:
            # Mensaje fuera de horario comercial (optimizado para velocidad)
            twiml_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, soy un agente comercial de DesArroyo Tech. Le llamamos fuera de horario comercial. Horario: lunes a viernes 9 a 14 y 16 a 20 horas. Visite desarroyo punto tech. Gracias.
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