#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 WEBHOOK PÚBLICO PARA LLAMADAS - VERCEL
Sistema de respuestas automáticas en español para Twilio
PÚBLICO - Sin autenticación para que funcione con Twilio
"""

from datetime import datetime
import pytz

def es_horario_comercial():
    """Verifica si estamos en horario comercial español"""
    try:
        spain_tz = pytz.timezone('Europe/Madrid')
        now = datetime.now(spain_tz)
        weekday = now.weekday()  # 0=lunes, 6=domingo
        hour = now.hour
        
        # Lunes a viernes: 9-14h y 16-20h
        if weekday <= 4:
            return (9 <= hour < 14) or (16 <= hour < 20)
        # Sábados: 10-13h
        elif weekday == 5:
            return 10 <= hour < 13
        # Domingos: cerrado
        else:
            return False
    except:
        return False

def handler(request):
    """Handler principal para Vercel"""
    
    # Headers para CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/xml; charset=utf-8'
    }
    
    # Responder a OPTIONS (preflight)
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Solo POST para webhooks de Twilio
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="Polly.Lucia" language="es-ES">Método no permitido</Say></Response>'
        }
    
    try:
        # Verificar horario comercial
        if es_horario_comercial():
            twiml = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">Hola, soy un agente comercial de DesArroyo Tech. Creamos páginas web profesionales en 48 horas. Contacte en desarroyo punto tech. Gracias.</Say>
</Response>'''
        else:
            twiml = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">Hola, soy un agente comercial de DesArroyo Tech. Llamamos fuera de horario comercial. Horario: lunes a viernes 9 a 14 y 16 a 20. Visite desarroyo punto tech. Gracias.</Say>
</Response>'''
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': twiml
        }
        
    except Exception as e:
        # Fallback en caso de error
        fallback = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">Hola, soy un agente comercial de DesArroyo Tech. Visite desarroyo punto tech. Gracias.</Say>
</Response>'''
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': fallback
        } 