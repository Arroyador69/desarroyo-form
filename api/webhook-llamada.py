#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 WEBHOOK PÚBLICO PARA LLAMADAS - VERCEL
Sistema de respuestas automáticas en español para Twilio
PÚBLICO - Sin autenticación para que funcione con Twilio
"""

import os
import json
import urllib.parse
from datetime import datetime

def handler(request):
    """
    Handler principal para Vercel - PÚBLICO
    """
    
    # Permitir todos los métodos y orígenes
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
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
        # Obtener datos del formulario de Twilio
        if hasattr(request, 'body'):
            body = request.body
        else:
            body = request.get_body()
            
        # Parsear datos de Twilio
        if isinstance(body, bytes):
            body = body.decode('utf-8')
            
        form_data = urllib.parse.parse_qs(body)
        
        # Obtener información de la llamada
        from_number = form_data.get('From', [''])[0]
        to_number = form_data.get('To', [''])[0]
        call_sid = form_data.get('CallSid', [''])[0]
        
        print(f"📞 Llamada recibida: {from_number} → {to_number}")
        print(f"📋 Call SID: {call_sid}")
        
        # Determinar sector basado en datos (si están disponibles)
        sector = "general"
        
        # Configurar mensaje según sector
        if "restaurante" in body.lower() or "comida" in body.lower():
            sector = "restaurante"
        elif "dental" in body.lower() or "dentista" in body.lower():
            sector = "dental"
        elif "peluqueria" in body.lower() or "belleza" in body.lower():
            sector = "peluqueria"
        
        # Generar respuesta TwiML en español
        mensaje = generar_mensaje_sector(sector)
        
        twiml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">{mensaje}</Say>
    <Pause length="1"/>
    <Say voice="Polly.Lucia" language="es-ES">Gracias por su tiempo. Que tenga un buen día.</Say>
</Response>'''
        
        # Log para debugging
        print(f"✅ Respuesta TwiML generada para sector: {sector}")
        print(f"📝 Mensaje: {mensaje[:100]}...")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': twiml_response
        }
        
    except Exception as e:
        print(f"❌ Error en webhook: {e}")
        
        # Respuesta de error en español
        error_response = '''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">Disculpe, ha ocurrido un error técnico. Volveremos a contactar con usted más tarde.</Say>
</Response>'''
        
        return {
            'statusCode': 500,
            'headers': headers,
            'body': error_response
        }

def generar_mensaje_sector(sector):
    """
    Generar mensaje personalizado según sector
    """
    
    # Introducción común
    intro = "Hola, soy un agente comercial de DesArroyo Tech. Le llamo porque hemos visto que su negocio podría beneficiarse de nuestra propuesta."
    
    # Mensajes específicos por sector
    mensajes_sector = {
        "restaurante": """
        Ofrecemos páginas web profesionales para restaurantes que incluyen carta online, reservas automáticas y pedidos a domicilio. 
        Muchos restaurantes han aumentado sus ventas un 40% con nuestras soluciones digitales.
        Si le interesa, podemos prepararle una propuesta personalizada sin compromiso.
        """,
        
        "dental": """
        Nos especializamos en páginas web para clínicas dentales con sistema de citas online, información de tratamientos y testimonios de pacientes.
        Nuestros clientes han reducido las llamadas administrativas en un 60% automatizando las citas.
        Podemos mostrarle cómo mejorar la presencia online de su clínica.
        """,
        
        "peluqueria": """
        Creamos páginas web para peluquerías y centros de belleza con galería de trabajos, reserva de citas online y promociones especiales.
        Nuestros clientes han incrementado su clientela un 35% con mejor presencia digital.
        Le podemos preparar una propuesta adaptada a su salón.
        """,
        
        "general": """
        Nos especializamos en páginas web profesionales que ayudan a los negocios a conseguir más clientes online.
        Ofrecemos diseño personalizado, posicionamiento en Google y herramientas de gestión.
        Muchos de nuestros clientes han aumentado sus ventas significativamente.
        """
    }
    
    mensaje_sector = mensajes_sector.get(sector, mensajes_sector["general"])
    
    # Llamada a la acción
    cta = "En las próximas 48 horas le enviaremos un ejemplo personalizado de cómo podría ser su página web, completamente gratis y sin compromiso."
    
    return f"{intro} {mensaje_sector.strip()} {cta}"

# Para testing local
if __name__ == "__main__":
    print("🧪 Testing webhook local...")
    
    # Simular request de Twilio
    class MockRequest:
        def __init__(self):
            self.method = 'POST'
            self.body = 'From=%2B34612345678&To=%2B34617555255&CallSid=CA123456789'
            
        def get_body(self):
            return self.body
    
    mock_request = MockRequest()
    result = handler(mock_request)
    
    print(f"Status: {result['statusCode']}")
    print(f"Response: {result['body']}") 