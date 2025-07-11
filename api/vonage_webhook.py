#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VONAGE VOICE WEBHOOK - NÚMEROS ESPAÑOLES
Manejo de llamadas conversacionales con números españoles via Vonage
"""

import os
import json
import urllib.parse
from datetime import datetime

class VonageVoiceHandler:
    def __init__(self):
        self.vonage_api_key = os.getenv('VONAGE_API_KEY')
        self.vonage_api_secret = os.getenv('VONAGE_API_SECRET')
        self.vonage_phone = os.getenv('VONAGE_PHONE_NUMBER')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = "DesArroyo Tech"
        self.agent_intro = "un agente comercial de DesArroyo Tech"

    def handle_answer_webhook(self, request):
        """Maneja webhook inicial de llamada (answer)"""
        try:
            # Obtener parámetros de la llamada
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
            sector = query_params.get('sector', ['default'])[0]
            nombre = query_params.get('nombre', ['Negocio'])[0]
            ciudad = query_params.get('ciudad', [''])[0]
            
            # Scripts de voz por sector (adaptados para Vonage)
            voice_scripts = {
                'restaurantes': {
                    'intro': f'Hola, buenos días. Soy {self.agent_intro}, empresa especializada en desarrollo web para restaurantes.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un restaurante con mucho potencial.',
                    'hook': f'Los restaurantes en {ciudad} que tienen web profesional están consiguiendo un 40% más de reservas que sus competidores.',
                    'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web que muestre su carta, permita reservas online y aumente sus ventas.',
                },
                'dentistas': {
                    'intro': f'Buenos días, soy {self.agent_intro}, empresa especializada en webs para clínicas dentales.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y se dedican a odontología.',
                    'hook': f'Las clínicas dentales en {ciudad} con web moderna están consiguiendo un 60% más de pacientes nuevos.',
                    'propuesta': f'Nos gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más pacientes con una web que permita citas online y genere confianza profesional.',
                },
                'default': {
                    'intro': f'Buenos días, soy {self.agent_intro}, empresa especializada en desarrollo web profesional.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un negocio con mucho potencial.',
                    'hook': f'Las empresas en {ciudad} con web profesional están aumentando sus ventas un 45%.',
                    'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web profesional que atraiga y convierta visitas en ventas.',
                }
            }
            
            script = voice_scripts.get(sector, voice_scripts['default'])
            
            # Crear respuesta NCCO (Vonage Call Control Object)
            ncco = [
                {
                    "action": "talk",
                    "text": f"{script['intro']} {script['personalizacion']} {script['hook']}",
                    "language": "es-ES",
                    "style": 1,  # Voz femenina más natural
                    "premium": True
                },
                {
                    "action": "pause",
                    "length": 2
                },
                {
                    "action": "input",
                    "eventUrl": [f"{self.website_url}/api/vonage-input?sector={sector}&nombre={nombre}&ciudad={ciudad}"],
                    "type": ["dtmf"],
                    "dtmf": {
                        "maxDigits": 1,
                        "timeOut": 10,
                        "submitOnHash": False
                    },
                    "speech": {
                        "uuid": ["call-uuid"],
                        "endOnSilence": 2,
                        "language": "es-ES",
                        "context": ["si", "no", "interesado", "no_interesado"]
                    }
                },
                {
                    "action": "talk", 
                    "text": f"{script['propuesta']} Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.",
                    "language": "es-ES",
                    "style": 1,
                    "premium": True
                },
                {
                    "action": "input",
                    "eventUrl": [f"{self.website_url}/api/vonage-input?sector={sector}&nombre={nombre}&ciudad={ciudad}"],
                    "type": ["dtmf"],
                    "dtmf": {
                        "maxDigits": 1,
                        "timeOut": 8
                    }
                },
                {
                    "action": "talk",
                    "text": "Entiendo que no puede atender ahora. Puede contactarnos en alberto@desarroyo.tech si lo desea. Que tenga un buen día.",
                    "language": "es-ES"
                }
            ]
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(ncco)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def handle_input_webhook(self, request):
        """Maneja respuesta del cliente (input)"""
        try:
            # Parsear datos de entrada
            if request.method == 'POST':
                body = request.body.decode('utf-8')
                data = json.loads(body) if body else {}
            else:
                query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
                data = {k: v[0] if v else '' for k, v in query_params.items()}
            
            sector = data.get('sector', 'default')
            nombre = data.get('nombre', 'Negocio')
            ciudad = data.get('ciudad', '')
            dtmf = data.get('dtmf', '')
            
            if dtmf == '1':  # SÍ, está interesado
                # Enviar SMS inmediatamente
                self.enviar_sms_post_llamada(data.get('from', ''), nombre, sector, ciudad)
                
                ncco = [
                    {
                        "action": "talk",
                        "text": f"Perfecto, {nombre}. Le acabamos de enviar toda la información por SMS a este número. Revise su móvil en unos minutos. Gracias por su tiempo y que tenga un buen día.",
                        "language": "es-ES",
                        "style": 1
                    }
                ]
                
            elif dtmf == '2':  # NO, no está interesado
                # Añadir a lista negra
                self.agregar_a_lista_negra(data.get('from', ''), nombre)
                
                ncco = [
                    {
                        "action": "talk", 
                        "text": "Entiendo perfectamente. Disculpe las molestias y que tenga un buen día.",
                        "language": "es-ES"
                    }
                ]
                
            else:  # Sin respuesta o respuesta inválida
                ncco = [
                    {
                        "action": "talk",
                        "text": "No he recibido una respuesta clara. Si está interesado, puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.",
                        "language": "es-ES"
                    }
                ]
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(ncco)
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def handle_events_webhook(self, request):
        """Maneja eventos de llamada (started, answered, completed, etc.)"""
        try:
            if request.method == 'POST':
                body = request.body.decode('utf-8')
                event_data = json.loads(body) if body else {}
                
                # Log del evento
                print(f"📞 VONAGE EVENT: {event_data.get('status', 'unknown')} - {event_data.get('uuid', 'no-uuid')}")
                
                # Notificar a Telegram si es relevante
                if event_data.get('status') in ['completed', 'answered', 'failed']:
                    self.notificar_evento_telegram(event_data)
                
            return {
                'statusCode': 200,
                'body': json.dumps({'received': True})
            }
            
        except Exception as e:
            return {
                'statusCode': 500, 
                'body': json.dumps({'error': str(e)})
            }

    def enviar_sms_post_llamada(self, telefono, nombre, sector, ciudad):
        """Envía SMS usando Twilio después de llamada exitosa Vonage"""
        # Reutilizar la función SMS de Twilio que ya funciona
        try:
            # Importar sistema existente
            import sys
            sys.path.append('/usr/src/app/scripts')
            from sistema_leads_avanzado import SistemaLeadsAvanzado
            
            sistema = SistemaLeadsAvanzado()
            sistema.enviar_sms_post_llamada_exitosa(telefono, nombre, sector, ciudad)
            
        except Exception as e:
            print(f"❌ Error enviando SMS post-llamada: {e}")

    def agregar_a_lista_negra(self, telefono, nombre):
        """Añade número a lista negra"""
        try:
            lista_negra_file = '/tmp/lista_negra_llamadas.json'
            
            # Cargar lista actual
            try:
                with open(lista_negra_file, 'r') as f:
                    lista_negra = json.load(f)
            except:
                lista_negra = {}
            
            # Añadir número
            lista_negra[telefono] = {
                'nombre': nombre,
                'fecha': datetime.now().isoformat(),
                'motivo': 'NO_INTERESADO_VONAGE'
            }
            
            # Guardar
            with open(lista_negra_file, 'w') as f:
                json.dump(lista_negra, f, ensure_ascii=False, indent=2)
                
            print(f"🚫 Añadido a lista negra: {telefono} - {nombre}")
            
        except Exception as e:
            print(f"❌ Error añadiendo a lista negra: {e}")

    def notificar_evento_telegram(self, event_data):
        """Notifica eventos importantes a Telegram"""
        # Implementar notificación Telegram si necesario
        pass

# Funciones handler para Vercel
def handle_vonage_answer(request):
    handler = VonageVoiceHandler()
    return handler.handle_answer_webhook(request)

def handle_vonage_input(request):
    handler = VonageVoiceHandler()
    return handler.handle_input_webhook(request)

def handle_vonage_events(request):
    handler = VonageVoiceHandler()
    return handler.handle_events_webhook(request) 