#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SERVIDOR WEBHOOK RAILWAY - LLAMADAS EN ESPAÑOL
Sistema de respuestas automáticas 24/7 en la nube
PÚBLICO - Sin autenticación - Control horario comercial
"""

import os
import json
import urllib.parse
from datetime import datetime, timezone
from flask import Flask, request, Response
import pytz

app = Flask(__name__)

# Configuración
TIMEZONE = pytz.timezone('Europe/Madrid')
BUSINESS_HOURS = {
    'monday': [(9, 14), (16, 20)],
    'tuesday': [(9, 14), (16, 20)],
    'wednesday': [(9, 14), (16, 20)],
    'thursday': [(9, 14), (16, 20)],
    'friday': [(9, 14), (16, 20)],
    'saturday': [(10, 13)],
    'sunday': []  # Cerrado domingos
}

def es_horario_comercial():
    """Verificar si estamos en horario comercial español"""
    now = datetime.now(TIMEZONE)
    day_name = now.strftime('%A').lower()
    
    if day_name not in BUSINESS_HOURS:
        return False
    
    hours_today = BUSINESS_HOURS[day_name]
    current_hour = now.hour
    
    for start, end in hours_today:
        if start <= current_hour < end:
            return True
    
    return False

def generar_mensaje_profesional():
    """Generar mensaje profesional en español"""
    return """
    Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web profesional.

    Le llamo porque hemos identificado que su negocio tiene un gran potencial para crecer online.

    Nos especializamos en crear páginas web que ayudan a empresas como la suya a conseguir más clientes a través de internet.

    Nuestros clientes suelen aumentar sus ventas entre un 30% y un 50% después de implementar una presencia web profesional.

    En las próximas 48 horas le enviaremos un ejemplo personalizado de cómo podría ser su página web, completamente gratis y sin compromiso.

    Esto le dará una idea clara de cómo podríamos ayudarle a hacer crecer su negocio online.
    """

def generar_mensaje_fuera_horario():
    """Mensaje para fuera de horario comercial"""
    return """
    Hola, gracias por atender. Soy un agente comercial de DesArroyo Tech.

    Le hemos llamado fuera de nuestro horario comercial habitual. Nos disculpamos por la molestia.

    Nuestro horario de atención es de lunes a viernes de 9 a 14 horas y de 16 a 20 horas, y sábados de 10 a 13 horas.

    Le contactaremos de nuevo en horario comercial para presentarle nuestra propuesta de desarrollo web.
    """

@app.route('/')
def home():
    """Página de inicio"""
    return """
    <h1>🔥 Webhook DesArroyo Tech - ACTIVO</h1>
    <p>✅ Sistema de llamadas automáticas en español</p>
    <p>⏰ Horario comercial: L-V 9-14h y 16-20h, S 10-13h</p>
    <p>🎯 Endpoint: /webhook-llamada</p>
    <p>📞 Estado: FUNCIONANDO</p>
    <p>🕐 Hora actual España: {}</p>
    <p>📋 Horario comercial: {}</p>
    """.format(
        datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S'),
        "✅ SÍ" if es_horario_comercial() else "❌ NO"
    )

@app.route('/webhook-llamada', methods=['GET', 'POST'])
def webhook_llamada():
    """Webhook principal para llamadas de Twilio"""
    
    # Permitir CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/xml; charset=utf-8'
    }
    
    if request.method == 'OPTIONS':
        return Response('', headers=headers)
    
    if request.method == 'GET':
        return Response(
            '<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="Polly.Lucia" language="es-ES">Webhook funcionando correctamente</Say></Response>',
            headers=headers
        )
    
    try:
        # Obtener datos de Twilio
        from_number = request.form.get('From', '')
        to_number = request.form.get('To', '')
        call_sid = request.form.get('CallSid', '')
        
        print(f"📞 Llamada: {from_number} → {to_number}")
        print(f"🆔 Call SID: {call_sid}")
        print(f"⏰ Hora: {datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verificar horario comercial
        if es_horario_comercial():
            mensaje = generar_mensaje_profesional()
            print("✅ Horario comercial - Mensaje completo")
        else:
            mensaje = generar_mensaje_fuera_horario()
            print("⚠️ Fuera de horario - Mensaje reducido")
        
        # Generar TwiML en español
        twiml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        {mensaje.strip()}
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Gracias por su tiempo. Que tenga un buen día.
    </Say>
</Response>'''
        
        print(f"✅ TwiML generado: {len(twiml_response)} caracteres")
        
        return Response(twiml_response, headers=headers)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        error_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Disculpe, ha ocurrido un error técnico. Volveremos a contactar con usted más tarde.
    </Say>
</Response>'''
        
        return Response(error_response, headers=headers)

@app.route('/health')
def health():
    """Endpoint de salud"""
    return {
        'status': 'ok',
        'message': 'Webhook funcionando',
        'timestamp': datetime.now(TIMEZONE).isoformat(),
        'business_hours': es_horario_comercial()
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 