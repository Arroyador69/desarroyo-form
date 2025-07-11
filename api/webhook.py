#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK VERCEL - RESPUESTAS AUTOMÁTICAS WHATSAPP
Sistema de respuestas automáticas optimizado para Vercel Serverless
"""

import os
import json
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler
import urllib.parse
import requests

class WebhookHandler(BaseHTTPRequestHandler):
    def __init__(self):
        # Configuración desde variables de entorno
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.agent_intro = "un agente comercial de DesArroyo Tech"

    def do_POST(self, request):
        """Maneja requests POST del webhook"""
        try:
            # Obtener path
            path = request.url.path
            
            if path == '/webhook/whatsapp':
                return self.handle_whatsapp_webhook(request)
            elif path == '/webhook/encuesta':
                return self.handle_encuesta_webhook(request)
            elif path == '/api/webhook-llamada':
                return self.handle_llamada_webhook(request)
            elif path == '/api/webhook-llamada-respuesta':
                return self.handle_llamada_respuesta_webhook(request)
            elif path == '/api/webhook-movil-captura':
                return self.handle_captura_movil_webhook(request)
            elif path == '/api/webhook-llamada-status':
                return self.handle_llamada_status_webhook(request)
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Endpoint no encontrado'})
                }
                
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def do_GET(self, request):
        """Maneja requests GET"""
        if request.url.path == '/health':
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'ok',
                    'message': 'Webhook funcionando correctamente',
                    'timestamp': datetime.now().isoformat()
                })
            }

    def handle_whatsapp_webhook(self, request):
        """Maneja respuestas de WhatsApp desde Twilio"""
        try:
            # Parsear form data de Twilio
            body = request.body.decode('utf-8')
            form_data = urllib.parse.parse_qs(body)
            
            from_phone = form_data.get('From', [''])[0]
            mensaje = form_data.get('Body', [''])[0]
            
            if not from_phone or not mensaje:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Datos incompletos'})
                }

            # Procesar respuesta automáticamente
            respuesta = self.generar_respuesta_inteligente(mensaje)
            
            # Enviar respuesta
            if self.enviar_whatsapp(from_phone, respuesta):
                # Notificar por Telegram
                self.notificar_telegram_respuesta(from_phone, mensaje, respuesta)
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'success', 'message': 'Respuesta enviada'})
                }
            else:
                return {
                    'statusCode': 500,
                    'body': json.dumps({'error': 'Error enviando respuesta'})
                }
                
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def handle_llamada_webhook(self, request):
        """Maneja webhook inicial de llamada automatizada"""
        try:
            # Obtener parámetros de la URL
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
            sector = query_params.get('sector', ['default'])[0]
            nombre = query_params.get('nombre', ['Negocio'])[0]
            ciudad = query_params.get('ciudad', [''])[0]
            
            # Importar TwiML localmente
            from twilio.twiml.voice_response import VoiceResponse
            
            # Scripts de voz por sector
            voice_scripts = {
                'restaurantes': {
                    'intro': 'Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web para restaurantes.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un restaurante con mucho potencial.',
                    'hook': f'Los restaurantes en {ciudad} que tienen web profesional están consiguiendo un 40% más de reservas que sus competidores.',
                    'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web que muestre su carta, permita reservas online y aumente sus ventas. ¿Le interesaría escuchar esta información?',
                },
                'dentistas': {
                    'intro': 'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en webs para clínicas dentales.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y se dedican a odontología general.',
                    'hook': f'Las clínicas dentales en {ciudad} con web moderna están consiguiendo un 60% más de pacientes nuevos.',
                    'propuesta': f'Nos gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más pacientes con una web que permita citas online y genere confianza profesional. ¿Le interesaría conocer esta información?',
                },
                'default': {
                    'intro': 'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web profesional para negocios.',
                    'personalizacion': f'Estoy llamando específicamente por {nombre}, he visto que están en {ciudad} y me parece un negocio con mucho potencial.',
                    'hook': f'Las empresas en {ciudad} con web profesional están aumentando sus ventas un 45%.',
                    'propuesta': f'Me gustaría explicarle cómo podríamos ayudar a {nombre} a conseguir más clientes con una web profesional que atraiga y convierta visitas en ventas. ¿Le interesaría escuchar esta información?',
                }
            }
            
            script = voice_scripts.get(sector, voice_scripts['default'])
            
            # Crear respuesta TwiML conversacional
            response = VoiceResponse()
            
            # Pausar 1 segundo al inicio
            response.pause(length=1)
            
            # Presentación personalizada
            presentacion = f"""
            {script['intro']}
            
            {script['personalizacion']}
            
            {script['hook']}
            """
            
            response.say(
                presentacion,
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # Pausa para procesar información
            response.pause(length=2)
            
            # Propuesta con captura de respuesta
            gather = response.gather(
                num_digits=1,
                timeout=10,
                action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento=1&nombre={nombre}&ciudad={ciudad}",
                method='POST'
            )
            
            gather.say(
                script['propuesta'] + " Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            # Si no responden, repetir
            response.say(
                "No he recibido su respuesta. " + script['propuesta'] + " Presione 1 para SÍ o 2 para NO.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.hangup()
            
            # Devolver XML de TwiML
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }
            
        except Exception as e:
            # En caso de error, devolver TwiML simple
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say(
                "Lo siento, ha ocurrido un error técnico. Puede contactarnos en alberto@desarroyo.tech",
                voice='Polly.Lucia',
                language='es-ES'
            )
            response.hangup()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }

    def handle_llamada_respuesta_webhook(self, request):
        """Maneja respuesta del cliente durante la llamada"""
        try:
            # Parsear form data de Twilio
            body = request.body.decode('utf-8')
            form_data = urllib.parse.parse_qs(body)
            
            # Obtener parámetros
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
            sector = query_params.get('sector', ['default'])[0]
            intento = int(query_params.get('intento', ['1'])[0])
            nombre = query_params.get('nombre', ['Negocio'])[0]
            ciudad = query_params.get('ciudad', [''])[0]
            
            # Obtener respuesta del cliente
            respuesta = form_data.get('Digits', [''])[0]
            telefono = form_data.get('To', [''])[0]
            
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            
            if respuesta == '1':  # SÍ, está interesado
                response.say(
                    f"Perfecto. Le voy a enviar ahora mismo por SMS una encuesta personalizada para {nombre} con ejemplos específicos y nuestros precios. Gracias por su tiempo.",
                    voice='Polly.Lucia',
                    language='es-ES'
                )
                response.hangup()
                
                # ENVIAR SMS AUTOMÁTICAMENTE
                self.enviar_sms_post_llamada_exitosa(telefono, nombre, sector, ciudad)
                
                # Notificar éxito por Telegram
                self.notificar_llamada_exitosa(telefono, nombre, sector, ciudad)
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/xml'},
                    'body': str(response)
                }
                
            elif respuesta == '2':  # NO, no está interesado
                if intento >= 3:
                    # Ya hemos intentado 3 veces, despedirse
                    response.say(
                        "Entiendo. Si cambia de opinión, puede contactarnos en contacto@desarroyo.tech. Que tenga un buen día.",
                        voice='Polly.Lucia',
                        language='es-ES'
                    )
                    response.hangup()
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/xml'},
                        'body': str(response)
                    }
                else:
                    # Intentar con diferente enfoque
                    return self.generar_reintento_llamada(sector, intento + 1, nombre, ciudad)
            
            else:
                # Respuesta no válida
                response.say(
                    "No he entendido su respuesta. Por favor, presione 1 para SÍ o 2 para NO.",
                    voice='Polly.Lucia',
                    language='es-ES'
                )
                
                gather = response.gather(
                    num_digits=1,
                    timeout=5,
                    action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento={intento}&nombre={nombre}&ciudad={ciudad}",
                    method='POST'
                )
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/xml'},
                    'body': str(response)
                }
                
        except Exception as e:
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say(
                "Ha ocurrido un error. Puede contactarnos en contacto@desarroyo.tech",
                voice='Polly.Lucia',
                language='es-ES'
            )
            response.hangup()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }

    def generar_reintento_llamada(self, sector, intento, nombre, ciudad):
        """Genera reintento con diferente estrategia"""
        try:
            from twilio.twiml.voice_response import VoiceResponse
            
            # Scripts alternativos por intento
            scripts_reintento = {
                2: {
                    'restaurantes': f"Entiendo. Déjeme preguntarle una cosa: ¿han notado que muchos clientes buscan restaurantes online antes de decidir dónde cenar? Nosotros ayudamos a restaurantes como {nombre} a aparecer mejor en internet. ¿Esto le resultaría más interesante?",
                    'dentistas': f"Entiendo. ¿Han observado que los pacientes nuevos cada vez buscan más información online antes de elegir dentista? Nosotros ayudamos a clínicas como {nombre} a transmitir confianza y profesionalidad. ¿Esto le resultaría útil?",
                    'default': f"Entiendo. ¿Han notado que los clientes buscan servicios online antes de comprar? Nosotros ayudamos a negocios como {nombre} a aparecer mejor en internet y conseguir más ventas. ¿Esto le resultaría útil?"
                },
                3: {
                    'restaurantes': f"Comprendo su posición. Una última cosa: trabajamos con restaurantes en {ciudad} y hemos visto que los que no tienen presencia digital pierden clientes cada día. Por eso creamos un plan de 149€ muy asequible. ¿Le envío la información sin compromiso?",
                    'dentistas': f"Comprendo. Una cosa más: muchas clínicas en {ciudad} están perdiendo pacientes porque no aparecen bien en internet. Tenemos un plan desde 149€ muy accesible. ¿Le mando la información para que la revise?",
                    'default': f"Entiendo. Una última cosa: muchos negocios en {ciudad} están creciendo con una web sencilla. Tenemos opciones desde 149€ muy asequibles. ¿Le envío la información sin compromiso?"
                }
            }
            
            mensaje = scripts_reintento.get(intento, {}).get(sector, scripts_reintento.get(intento, {}).get('default', ''))
            
            response = VoiceResponse()
            
            gather = response.gather(
                num_digits=1,
                timeout=10,
                action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento={intento}&nombre={nombre}&ciudad={ciudad}",
                method='POST'
            )
            
            gather.say(
                mensaje + " Presione 1 para SÍ o 2 para NO.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.say(
                "Entiendo. Si cambia de opinión, puede contactarnos en contacto@desarroyo.tech. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.hangup()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }
            
        except Exception as e:
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say(
                "Puede contactarnos en contacto@desarroyo.tech. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            response.hangup()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }

    def handle_captura_movil_webhook(self, request):
        """
        NUEVO: Maneja captura de móvil cuando llamamos a número fijo
        Optimiza conversiones fijo→móvil para envío SMS
        """
        try:
            # Parsear form data de Twilio
            body = request.body.decode('utf-8')
            form_data = urllib.parse.parse_qs(body)
            
            # Obtener datos
            movil_dictado = form_data.get('Digits', [''])[0]
            
            # Obtener parámetros de la URL
            query_params = urllib.parse.parse_qs(urllib.parse.urlparse(request.url).query)
            telefono_fijo = query_params.get('telefono_fijo', [''])[0]
            nombre_negocio = query_params.get('nombre', [''])[0]
            sector = query_params.get('sector', ['default'])[0]
            ciudad = query_params.get('ciudad', [''])[0]
            
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            
            # Limpiar y validar el móvil dictado
            if movil_dictado and len(movil_dictado) >= 9:
                # Tomar solo los primeros 9 dígitos
                movil_limpio = movil_dictado[:9]
                
                # Validar que es móvil español (6xx o 7xx)
                if movil_limpio.startswith('6') or movil_limpio.startswith('7'):
                    # Formatear móvil a E.164
                    movil_formateado = f"+34{movil_limpio}"
                    
                    # Confirmar móvil al cliente
                    response.say(
                        f"Perfecto, he apuntado el {movil_limpio[:3]} {movil_limpio[3:6]} {movil_limpio[6:]}. Le envío la información ahora mismo.",
                        voice='Polly.Lucia',
                        language='es-ES'
                    )
                    
                    response.say(
                        "Muchas gracias por su tiempo. Que tenga un buen día.",
                        voice='Polly.Lucia',
                        language='es-ES'
                    )
                    
                    response.hangup()
                    
                    # Enviar SMS al móvil alternativo inmediatamente
                    exito_sms = self.enviar_sms_movil_alternativo(movil_formateado, nombre_negocio, sector, ciudad)
                    
                    if exito_sms:
                        # Registrar conversión exitosa
                        self.registrar_llamada_exitosa(telefono_fijo, nombre_negocio, sector, ciudad)
                        
                        # Notificar conversión súper exitosa
                        self.notificar_conversion_fijo_movil(telefono_fijo, movil_formateado, nombre_negocio, sector, ciudad)
                        
                        print(f"🏆 CONVERSIÓN FIJO→MÓVIL EXITOSA: {nombre_negocio} ({telefono_fijo} → {movil_formateado})")
                    else:
                        print(f"⚠️ Móvil capturado pero SMS falló: {movil_formateado}")
                    
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/xml'},
                        'body': str(response)
                    }
                    
                else:
                    # Móvil no válido (no empieza por 6 o 7)
                    response.say(
                        f"El número {movil_limpio} no parece ser un móvil válido. No hay problema, puede contactarnos por email en contacto@desarroyo.tech.",
                        voice='Polly.Lucia',
                        language='es-ES'
                    )
            else:
                # No se recibió móvil o es muy corto
                response.say(
                    "No he podido capturar el número correctamente. No hay problema, puede contactarnos por email en contacto@desarroyo.tech para recibir toda la información.",
                    voice='Polly.Lucia',
                    language='es-ES'
                )
            
            response.say(
                "Gracias por su tiempo. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            
            response.hangup()
            
            # Registrar como llamada exitosa aunque no hayamos capturado móvil válido
            self.registrar_llamada_exitosa(telefono_fijo, nombre_negocio, sector, ciudad)
            
            # Notificar conversión parcial
            self.notificar_conversion_fijo_sin_movil(telefono_fijo, nombre_negocio, sector, ciudad)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }
            
        except Exception as e:
            # En caso de error, devolver TwiML simple
            from twilio.twiml.voice_response import VoiceResponse
            response = VoiceResponse()
            response.say(
                "Ha ocurrido un error técnico. Puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.",
                voice='Polly.Lucia',
                language='es-ES'
            )
            response.hangup()
            
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/xml'},
                'body': str(response)
            }

    def handle_llamada_status_webhook(self, request):
        """Maneja actualizaciones de estado de llamada"""
        try:
            # Parsear form data de Twilio
            body = request.body.decode('utf-8')
            form_data = urllib.parse.parse_qs(body)
            
            call_sid = form_data.get('CallSid', [''])[0]
            call_status = form_data.get('CallStatus', [''])[0]
            
            # Notificar estado por Telegram si es relevante
            if call_status in ['completed', 'failed', 'no-answer']:
                self.notificar_estado_llamada(call_sid, call_status)
            
            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'ok'})
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def enviar_sms_post_llamada_exitosa(self, telefono, nombre, sector, ciudad):
        """Envía SMS automáticamente después de llamada exitosa"""
        try:
            # Generar mensaje SMS personalizado
            mensaje_sms = f"""Buenos días,

Soy de DesArroyo Tech, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He visto {nombre} y detectamos una gran oportunidad para aumentar sus ventas.

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{self.website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos cordiales,
DesArroyo Tech
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀"""

            # Formatear teléfono para SMS
            telefono_limpio = telefono.replace('whatsapp:', '').replace('+', '')
            if not telefono_limpio.startswith('34'):
                telefono_limpio = '34' + telefono_limpio
            telefono_sms = '+' + telefono_limpio
            
            # Enviar SMS usando Twilio
            if self.twilio_sid and self.twilio_token:
                from twilio.rest import Client
                client = Client(self.twilio_sid, self.twilio_token)
                
                message = client.messages.create(
                    body=mensaje_sms,
                    from_='+34910886507',  # Tu número Twilio
                    to=telefono_sms
                )
                
                print(f"✅ SMS post-llamada enviado: {message.sid}")
                return True
            
        except Exception as e:
            print(f"❌ Error enviando SMS post-llamada: {str(e)}")
            return False

    def notificar_llamada_exitosa(self, telefono, nombre, sector, ciudad):
        """Notifica llamada exitosa por Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""🎉 **¡LLAMADA EXITOSA - CLIENTE DIJO SÍ!**

🏢 Negocio: {nombre}
🏙️ Ciudad: {ciudad}
📞 Teléfono: {telefono}
🎯 Sector: {sector}
✅ Cliente INTERESADO en llamada
📱 SMS con encuesta: ENVIADO AUTOMÁTICAMENTE

🔥 **LEAD SÚPER CALIENTE - ALTA PROBABILIDAD CONVERSIÓN**

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram: {e}")

    def notificar_estado_llamada(self, call_sid, status):
        """Notifica estado de llamada por Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            estados = {
                'completed': '✅ Llamada completada',
                'failed': '❌ Llamada falló',
                'no-answer': '📵 No contestaron'
            }
            
            texto = f"""📞 **ESTADO LLAMADA**

🆔 {call_sid[:20]}...
📊 {estados.get(status, status)}

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram: {e}")

    def formatear_telefono_espanol(self, phone):
        """Formatea número español con validación estricta (Error 63024)"""
        import re
        
        # Limpiar número (solo dígitos y +)
        phone_clean = re.sub(r'[^\d+]', '', phone)
        
        # Extraer solo dígitos
        digits_only = re.sub(r'[^\d]', '', phone)
        
        # Si ya tiene +34 y es correcto, validar longitud
        if phone_clean.startswith('+34'):
            if len(digits_only) == 11 and digits_only.startswith('34'):
                # Validar que el número móvil sea válido (6, 7, 9)
                if digits_only[2] in ['6', '7', '9']:
                    return phone_clean
                # Validar que el número fijo sea válido (8, 9)
                elif digits_only[2] in ['8', '9']:
                    return phone_clean
        
        # Si empieza con 34 pero sin +, añadir +
        if digits_only.startswith('34') and len(digits_only) == 11:
            mobile_digit = digits_only[2]
            if mobile_digit in ['6', '7', '8', '9']:
                return f"+{digits_only}"
        
        # Si es número español de 9 dígitos (móviles: 6,7,9 | fijos: 8,9)
        if len(digits_only) == 9:
            first_digit = digits_only[0]
            if first_digit in ['6', '7']:  # Móviles
                return f"+34{digits_only}"
            elif first_digit in ['8', '9']:  # Fijos y algunos móviles
                return f"+34{digits_only}"
        
        # Si no coincide con patrones españoles válidos, rechazar
        return None

    def handle_encuesta_webhook(self, request):
        """Maneja webhook de encuesta completada"""
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Validar datos requeridos
            telefono = data.get('telefono', '').strip()
            if not telefono:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Teléfono requerido'})
                }
            
            # Formatear teléfono con validación mejorada
            telefono_formatted = self.formatear_telefono_espanol(telefono)
            if not telefono_formatted:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Número de teléfono no válido para España'})
                }

            mensaje_confirmacion = f"""¡Perfecto! He recibido tu información.

📋 Negocio: {data.get('nombre_negocio', 'No especificado')}
💰 Presupuesto: {data.get('presupuesto', 'A consultar')}

Te voy a contactar en los próximos 30 minutos para revisar los detalles.

¿Te parece bien si te llamo al {telefono_formatted}?"""

            # Enviar confirmación con número formateado correctamente
            telefono_whatsapp = f"whatsapp:{telefono_formatted}"
            
            if self.enviar_whatsapp(telefono_whatsapp, mensaje_confirmacion):
                # Notificar LEAD CALIENTE por Telegram
                self.notificar_lead_caliente(data)
                
                return {
                    'statusCode': 200,
                    'body': json.dumps({'status': 'success'})
                }
            
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Error enviando confirmación'})
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    def generar_respuesta_inteligente(self, mensaje_cliente):
        """Genera respuesta usando DeepSeek IA"""
        if not self.deepseek_api_key:
            return self.respuesta_por_defecto(mensaje_cliente)
            
        try:
            headers = {
                'Authorization': f'Bearer {self.deepseek_api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""Eres {self.your_name} de {self.business_name}, experto en desarrollo web con 10 años de experiencia.

RESPONDE AL CLIENTE que dice: "{mensaje_cliente}"

PRECIOS OFICIALES:
🟢 Plan Rápida: 149€ (1 página, entrega 72h)
🟡 Plan Escalable: 449€ (hasta 5 páginas, SEO)  
🔴 Plan Pro Digital: 999€ (hasta 10 páginas, dashboard)

OBJETIVO: Siempre dirigir hacia la encuesta: {self.website_url}/generador_automatizaciones.html

ESTILO:
- Profesional pero cercano
- Máximo 3 líneas
- Siempre ofrecer valor/ROI
- Generar urgencia suave
- Terminar con pregunta o llamada a acción"""

            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': mensaje_cliente}
                ],
                'max_tokens': 150,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
                
        except Exception as e:
            print(f"Error IA: {e}")
            
        return self.respuesta_por_defecto(mensaje_cliente)

    def respuesta_por_defecto(self, mensaje):
        """Respuesta por defecto si falla la IA"""
        if any(word in mensaje.lower() for word in ['precio', 'cuanto', 'cuesta', 'tarifa']):
            return f"""Perfecto. Tenemos 3 planes adaptados:

🟢 Plan Rápida: 149€ (1 página, 72h)
🟡 Plan Escalable: 449€ (5 páginas, SEO)  
🔴 Plan Pro Digital: 999€ (10 páginas, dashboard)

ROI garantizado: recuperas inversión en 2-4 semanas.

¿Vemos cuál se adapta mejor?
{self.website_url}/generador_automatizaciones.html"""

        elif any(word in mensaje.lower() for word in ['si', 'sí', 'vale', 'ok', 'interesa']):
            return f"""¡Excelente! 🎯

Para hacer tu web perfecta, completa esta encuesta estratégica (2 minutos):
{self.website_url}/generador_automatizaciones.html

Entrega garantizada en máximo 48 horas. ¿Empezamos?"""

        else:
            return f"""Entiendo las dudas. Nuestros clientes ven resultados desde la primera semana.

Casos reales: restaurantes +40% ventas, clínicas +3x citas...

¿Vemos tu caso específico?
{self.website_url}/generador_automatizaciones.html"""

    def enviar_whatsapp(self, to_phone, mensaje):
        """Envía mensaje por WhatsApp usando Twilio"""
        if not self.twilio_sid or not self.twilio_token:
            return False
            
        try:
            from twilio.rest import Client
            client = Client(self.twilio_sid, self.twilio_token)
            
            message = client.messages.create(
                from_=f'whatsapp:{self.twilio_whatsapp}',
                body=mensaje,
                to=to_phone
            )
            
            print(f"✅ WhatsApp enviado: {message.sid}")
            return True
            
        except Exception as e:
            print(f"❌ Error WhatsApp: {e}")
            return False

    def notificar_telegram_respuesta(self, phone, mensaje_cliente, respuesta):
        """Notifica respuesta por Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""💬 **RESPUESTA DE CLIENTE**

📞 {phone}
📥 Cliente: "{mensaje_cliente}"
📤 Respuesta: "{respuesta[:100]}..."

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram: {e}")

    def notificar_lead_caliente(self, data):
        """Notifica lead caliente por Telegram"""
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""🔥 **¡ENCUESTA COMPLETADA - LEAD CALIENTE!**

📋 {data.get('nombre_negocio', 'Sin nombre')}
📞 {data.get('telefono', 'Sin teléfono')}
💰 Presupuesto: {data.get('presupuesto', 'No especificado')}
🏢 Sector: {data.get('sector', 'No especificado')}

🚀 **¡LEAD LISTO PARA VENTA!**

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram: {e}")

    # ===== NUEVAS FUNCIONES: LISTA NEGRA Y LLAMADAS EXITOSAS =====
    
    def registrar_llamada_exitosa(self, telefono, nombre_negocio, sector, ciudad):
        """Registra una llamada exitosa (cliente dijo SÍ)"""
        try:
            # Simular registro local para webhook
            timestamp = datetime.now().isoformat()
            print(f"✅ LLAMADA EXITOSA: {nombre_negocio} ({telefono}) - {timestamp}")
            
            # En un entorno real, aquí guardaríamos en base de datos
            # o archivo JSON como hace el sistema principal
            
        except Exception as e:
            print(f"❌ Error registrando llamada exitosa: {str(e)}")
    
    def agregar_a_lista_negra(self, telefono, nombre_negocio, motivo='NO_INTERESADO'):
        """Añade un teléfono a la lista negra (no volver a llamar)"""
        try:
            # Simular registro en lista negra para webhook
            timestamp = datetime.now().isoformat()
            print(f"🚫 LISTA NEGRA: {nombre_negocio} ({telefono}) - {motivo} - {timestamp}")
            
            # En un entorno real, aquí guardaríamos en base de datos
            # o archivo JSON como hace el sistema principal
            
        except Exception as e:
            print(f"❌ Error añadiendo a lista negra: {str(e)}")
    
    def notificar_lista_negra(self, telefono, nombre_negocio, sector, ciudad, intentos):
        """Notifica nuevo número en lista negra"""
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""🚫 **NÚMERO AÑADIDO A LISTA NEGRA**

🏢 Negocio: {nombre_negocio}
📞 Teléfono: {telefono}
🎯 Sector: {sector}
🏙️ Ciudad: {ciudad}
❌ Intentos fallidos: {intentos}

⚠️ **NO se volverá a contactar este número**

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram lista negra: {e}")

    def enviar_sms_movil_alternativo(self, movil_alternativo, nombre_negocio, sector, ciudad):
        """
        NUEVO: Envía SMS al móvil alternativo proporcionado tras llamada a fijo
        """
        try:
            # Generar mensaje SMS personalizado para móvil alternativo
            mensaje_sms = f"""Buenos días,

Soy de DesArroyo Tech, acabamos de hablar por teléfono sobre {nombre_negocio}.

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{self.website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos cordiales,
DesArroyo Tech
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀"""

            # Formatear teléfono móvil
            telefono_limpio = movil_alternativo.replace('+', '')
            if not telefono_limpio.startswith('34'):
                telefono_limpio = '34' + telefono_limpio
            telefono_sms = '+' + telefono_limpio
            
            # Enviar SMS usando Twilio
            if self.twilio_sid and self.twilio_token:
                from twilio.rest import Client
                client = Client(self.twilio_sid, self.twilio_token)
                
                message = client.messages.create(
                    body=mensaje_sms,
                    from_='+34910886507',  # Tu número Twilio
                    to=telefono_sms
                )
                
                print(f"✅ SMS móvil alternativo enviado: {message.sid}")
                return True
            
        except Exception as e:
            print(f"❌ Error enviando SMS móvil alternativo: {str(e)}")
            return False

    def notificar_conversion_fijo_movil(self, telefono_fijo, movil_alternativo, nombre_negocio, sector, ciudad):
        """
        NUEVO: Notifica conversión súper exitosa: fijo→móvil
        """
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""🏆 **¡CONVERSIÓN NÚMERO FIJO PERFECTA!**

🏢 Negocio: {nombre_negocio}
☎️ Fijo llamado: {telefono_fijo}
📱 Móvil proporcionado: {movil_alternativo}
🎯 Sector: {sector}
🏙️ Ciudad: {ciudad}
✅ Cliente dijo SÍ + proporcionó móvil
📱 SMS con encuesta: **ENVIADO AL MÓVIL**
📧 Email contacto: alberto@desarroyo.tech

💰 Coste: ~0.19€ (llamada fijo + SMS móvil)
🎯 **LEAD SÚPER CALIENTE**
🏆 **Estrategia fijo→móvil EXITOSA!**
🚀 **Sistema DesArroyo Tech optimizado!**

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram conversión fijo-móvil: {e}")

    def notificar_conversion_fijo_sin_movil(self, telefono_fijo, nombre_negocio, sector, ciudad):
        """
        NUEVO: Notifica conversión parcial: fijo sin móvil válido
        """
        if not self.telegram_token or not self.telegram_chat:
            return
            
        try:
            texto = f"""📞 **CONVERSIÓN FIJO SIN MÓVIL**

🏢 Negocio: {nombre_negocio}
☎️ Fijo: {telefono_fijo}
🎯 Sector: {sector}
🏙️ Ciudad: {ciudad}
✅ Cliente dijo SÍ
❌ No se capturó móvil válido
📧 Referido a email: alberto@desarroyo.tech

💰 Coste: ~0.12€ (solo llamada)
📋 **Seguimiento manual recomendado**

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            requests.post(
                f'https://api.telegram.org/bot{self.telegram_token}/sendMessage',
                json={
                    'chat_id': self.telegram_chat,
                    'text': texto,
                    'parse_mode': 'Markdown'
                }
            )
            
        except Exception as e:
            print(f"Error Telegram conversión fijo sin móvil: {e}")

# Función principal para Vercel
def handler(request, context):
    """Handler principal para Vercel"""
    webhook = WebhookHandler()
    
    if request.method == 'POST':
        return webhook.do_POST(request)
    elif request.method == 'GET':
        return webhook.do_GET(request)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Método no permitido'})
        } 