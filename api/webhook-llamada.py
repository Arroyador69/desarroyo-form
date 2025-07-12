#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK SIMPLE PARA VERCEL - LLAMADAS EN ESPAÑOL
Compatible con Vercel Serverless Functions
"""

import os
import json
import urllib.parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Handler principal para Vercel - Llamadas en español"""
    
    def do_GET(self):
        """Manejar requests GET"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Webhook funcionando correctamente')
        
    def do_POST(self):
        """Manejar requests POST de Twilio"""
        try:
            # Obtener parámetros de la URL
            query_string = self.path.split('?')[1] if '?' in self.path else ''
            query_params = urllib.parse.parse_qs(query_string)
            
            sector = query_params.get('sector', ['default'])[0]
            nombre = query_params.get('nombre', ['Negocio'])[0]
            ciudad = query_params.get('ciudad', [''])[0]
            
            # Configurar TwiML para respuesta en español
            twiml_response = generar_twiml_espanol(sector, nombre, ciudad)
            
            # Enviar respuesta
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(twiml_response.encode('utf-8'))
            
        except Exception as e:
            # Si hay error, devolver mensaje en español
            error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Lo siento, ha ocurrido un error técnico. Por favor, contacte con nosotros por email en alberto@desarroyo.tech. Gracias.
    </Say>
    <Hangup/>
</Response>"""
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.end_headers()
            self.wfile.write(error_response.encode('utf-8'))

def generar_twiml_espanol(sector, nombre, ciudad):
    """Genera respuesta TwiML en español perfecto"""
    
    # Configurar script por sector
    scripts = {
        'restaurantes': {
            'intro': f'Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web para restaurantes.',
            'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un restaurante con mucho potencial.',
            'hook': f'Los restaurantes en {ciudad} que tienen web profesional están consiguiendo un 40% más de reservas que sus competidores.',
            'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web que muestre su carta, permita reservas online y aumente sus ventas. Le hacemos la web completamente personalizada en 48 horas.'
        },
        'dentistas': {
            'intro': f'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en webs para clínicas dentales.',
            'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y se dedican a odontología general.',
            'hook': f'Las clínicas dentales en {ciudad} con web moderna están consiguiendo un 60% más de pacientes nuevos.',
            'propuesta': f'Nos gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más pacientes con una web que permita citas online y genere confianza profesional. Le hacemos la web completamente personalizada en 48 horas.'
        },
        'default': {
            'intro': f'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web profesional para negocios.',
            'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un negocio con mucho potencial.',
            'hook': f'Las empresas en {ciudad} con web profesional están aumentando sus ventas un 45%.',
            'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web profesional que atraiga y convierta visitas en ventas. Le hacemos la web completamente personalizada en 48 horas.'
        }
    }
    
    script = scripts.get(sector, scripts['default'])
    
    # Generar TwiML en español
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        {script['intro']}
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        {script['personalizacion']}
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        {script['hook']}
    </Say>
    <Pause length="2"/>
    <Gather numDigits="1" timeout="10" action="https://desarroyo.tech/api/webhook-respuesta?sector={sector}&nombre={nombre}&ciudad={ciudad}" method="POST">
        <Say voice="Polly.Lucia" language="es-ES">
            {script['propuesta']} ¿Le interesaría escuchar esta información? Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.
        </Say>
    </Gather>
    <Say voice="Polly.Lucia" language="es-ES">
        No he recibido su respuesta. {script['propuesta']} Presione 1 para SÍ o 2 para NO.
    </Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">
        Gracias por su tiempo. Si está interesado, puede contactarnos por email en alberto@desarroyo.tech. Que tenga un buen día.
    </Say>
    <Hangup/>
</Response>"""
    
    return twiml 