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
        self.your_name = os.getenv('YOUR_NAME', 'Alberto')

    def do_POST(self, request):
        """Maneja requests POST del webhook"""
        try:
            # Obtener path
            path = request.url.path
            
            if path == '/webhook/whatsapp':
                return self.handle_whatsapp_webhook(request)
            elif path == '/webhook/encuesta':
                return self.handle_encuesta_webhook(request)
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

    def handle_encuesta_webhook(self, request):
        """Maneja encuestas completadas"""
        try:
            data = json.loads(request.body)
            
            telefono = data.get('telefono', '')
            nombre_negocio = data.get('nombre_negocio', '')
            presupuesto = data.get('presupuesto', '')
            
            # Mensaje de confirmación
            mensaje = f"""¡Excelente! 🎉 He recibido tu encuesta de {nombre_negocio}.

Te voy a contactar en los próximos 30 minutos para revisar los detalles.

¿Te parece bien si te llamo al {telefono}?"""

            # Enviar confirmación
            telefono_formatted = f"whatsapp:+34{telefono}" if not telefono.startswith('+') else f"whatsapp:{telefono}"
            
            if self.enviar_whatsapp(telefono_formatted, mensaje):
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