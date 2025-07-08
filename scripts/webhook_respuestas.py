#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK PARA RESPUESTAS DE WHATSAPP - SISTEMA AUTOMATIZADO
Maneja conversaciones automáticamente hasta enviar la encuesta
"""

import os
import json
import re
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.rest import Client
import telegram
import requests

app = Flask(__name__)

class ManejadorRespuestas:
    def __init__(self):
        # Configuración
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.your_name = os.getenv('YOUR_NAME', 'Alberto')
        
        # Clientes
        if self.twilio_sid and self.twilio_token:
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        
        if self.telegram_token:
            self.telegram_bot = telegram.Bot(token=self.telegram_token)
        
        # Archivos
        self.conversaciones_file = 'conversaciones_activas.json'
        self.conversaciones = self.cargar_conversaciones()
        
        # Patrones de respuesta
        self.patrones_interes = [
            r'\b(si|sí|vale|ok|bueno|interesa|me gusta|perfecto|genial|estupendo)\b',
            r'\b(cuanto|precio|coste|tarifa|presupuesto)\b',
            r'\b(mas info|más info|informacion|información|detalles)\b',
            r'\b(hablamos|llamar|reunion|reunión|cita)\b'
        ]
        
        self.patrones_no_interes = [
            r'\b(no|nada|gracias|paso|tengo|ya tengo)\b',
            r'\b(no me interesa|no gracias|no necesito)\b',
            r'\b(ahora no|otro momento|más adelante)\b'
        ]
    
    def cargar_conversaciones(self):
        """Carga conversaciones activas"""
        try:
            if os.path.exists(self.conversaciones_file):
                with open(self.conversaciones_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def guardar_conversacion(self, phone, estado, datos_extra=None):
        """Guarda estado de conversación"""
        phone_key = phone.replace('whatsapp:', '').replace('+', '')
        self.conversaciones[phone_key] = {
            'estado': estado,
            'timestamp': datetime.now().isoformat(),
            'datos_extra': datos_extra or {}
        }
        try:
            with open(self.conversaciones_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversaciones, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def analizar_interes(self, mensaje):
        """Analiza si el mensaje muestra interés"""
        mensaje_lower = mensaje.lower()
        
        # Puntuación de interés
        score_interes = 0
        score_no_interes = 0
        
        for patron in self.patrones_interes:
            if re.search(patron, mensaje_lower):
                score_interes += 1
        
        for patron in self.patrones_no_interes:
            if re.search(patron, mensaje_lower):
                score_no_interes += 1
        
        if score_interes > score_no_interes:
            return 'interesado'
        elif score_no_interes > score_interes:
            return 'no_interesado'
        else:
            return 'neutro'
    
    def generar_respuesta_ia(self, mensaje_cliente, contexto):
        """Genera respuesta inteligente usando DeepSeek"""
        api_key = self.deepseek_api_key or self.openai_api_key
        api_url = "https://api.deepseek.com/v1/chat/completions" if self.deepseek_api_key else "https://api.openai.com/v1/chat/completions"
        
        if not api_key:
            return self.generar_respuesta_plantilla(mensaje_cliente, contexto)
        
        try:
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt_sistema = f"""Eres {self.your_name} de {self.business_name}, experto en desarrollo web.

CONTEXTO: Cliente respondió a nuestra propuesta de página web.
SECTOR: {contexto.get('sector', 'general')}
ESTADO CONVERSACIÓN: {contexto.get('estado', 'inicial')}

REGLAS:
1. Responde como humano, natural y cercano
2. Si muestra interés → dirige hacia la encuesta de evaluación
3. Si tiene dudas → resuelve y ofrece más info
4. Si pregunta precio → menciona "desde 299€" y enfoca en valor
5. Máximo 2-3 líneas
6. SIEMPRE incluir una pregunta para continuar conversación
7. Si está muy interesado → enviar link de encuesta

OBJETIVO: Llevar al cliente a completar la encuesta de evaluación."""

            data = {
                'model': 'deepseek-chat' if self.deepseek_api_key else 'gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': prompt_sistema},
                    {'role': 'user', 'content': f'Cliente dice: "{mensaje_cliente}"'}
                ],
                'max_tokens': 150,
                'temperature': 0.7
            }
            
            response = requests.post(api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            
        except Exception as e:
            print(f"❌ Error IA: {e}")
        
        return self.generar_respuesta_plantilla(mensaje_cliente, contexto)
    
    def generar_respuesta_plantilla(self, mensaje_cliente, contexto):
        """Respuestas predefinidas según el tipo de interés"""
        interes = self.analizar_interes(mensaje_cliente)
        estado = contexto.get('estado', 'inicial')
        
        if interes == 'interesado':
            if 'precio' in mensaje_cliente.lower() or 'cuanto' in mensaje_cliente.lower():
                return f"""¡Perfecto! Los precios van desde 299€ según las necesidades específicas de tu negocio.

Para darte un presupuesto exacto, ¿podrías completar esta encuesta rápida? Solo 2 minutos:
{self.website_url}/encuesta-evaluacion

¿Te parece bien?"""
            
            else:
                return f"""¡Genial que te interese! 🎉

Para ofrecerte la mejor solución, necesito conocer un poco más sobre tu negocio. ¿Puedes completar esta encuesta súper rápida?

{self.website_url}/encuesta-evaluacion

Solo 2 minutos y te hago una propuesta personalizada. ¿Vale?"""
        
        elif interes == 'no_interesado':
            return f"""Lo entiendo perfectamente. 

Si en algún momento cambias de opinión o conoces a alguien que le pueda interesar, aquí estoy.

¡Que tengas un gran día! 😊"""
        
        else:  # neutro o dudas
            return f"""Entiendo que tengas dudas. Es normal.

Te explico: creamos páginas web que realmente consiguen más clientes. Nuestros clientes ven resultados desde el primer mes.

¿Te gustaría ver algunos ejemplos de trabajos que hemos hecho en tu sector?"""
    
    def enviar_respuesta_whatsapp(self, to_phone, mensaje):
        """Envía respuesta por WhatsApp"""
        try:
            if not self.twilio_client:
                return False
            
            message = self.twilio_client.messages.create(
                from_=f'whatsapp:{self.twilio_whatsapp}',
                body=mensaje,
                to=to_phone
            )
            
            print(f"✅ Respuesta enviada a {to_phone}")
            return True
            
        except Exception as e:
            print(f"❌ Error enviando respuesta: {e}")
            return False
    
    def notificar_telegram_respuesta(self, phone, mensaje_cliente, respuesta_enviada, interes):
        """Notifica respuesta del cliente por Telegram"""
        try:
            if not self.telegram_bot:
                return
            
            emoji_interes = {
                'interesado': '🔥',
                'no_interesado': '❄️',
                'neutro': '🤔'
            }
            
            texto = f"""{emoji_interes.get(interes, '💬')} **RESPUESTA DE CLIENTE**

📞 **Teléfono:** {phone}
📥 **Cliente dice:** "{mensaje_cliente}"
📤 **Nuestra respuesta:** "{respuesta_enviada[:100]}..."
🎯 **Nivel interés:** {interes.upper()}

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            self.telegram_bot.send_message(
                chat_id=self.telegram_chat,
                text=texto,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            print(f"❌ Error notificación Telegram: {e}")
    
    def procesar_respuesta(self, from_phone, mensaje_cliente):
        """Procesa respuesta del cliente y responde automáticamente"""
        try:
            # Buscar conversación existente
            phone_key = from_phone.replace('whatsapp:', '').replace('+', '')
            conversacion = self.conversaciones.get(phone_key, {})
            
            # Analizar interés
            interes = self.analizar_interes(mensaje_cliente)
            
            # Generar contexto
            contexto = {
                'estado': conversacion.get('estado', 'respuesta_inicial'),
                'sector': conversacion.get('datos_extra', {}).get('sector', 'general'),
                'historial': conversacion.get('datos_extra', {}).get('historial', [])
            }
            
            # Generar respuesta inteligente
            respuesta = self.generar_respuesta_ia(mensaje_cliente, contexto)
            
            # Enviar respuesta
            if self.enviar_respuesta_whatsapp(from_phone, respuesta):
                # Actualizar conversación
                nuevo_estado = 'interesado' if interes == 'interesado' else 'seguimiento'
                if 'encuesta-evaluacion' in respuesta:
                    nuevo_estado = 'encuesta_enviada'
                
                historial = contexto.get('historial', [])
                historial.append({
                    'timestamp': datetime.now().isoformat(),
                    'cliente': mensaje_cliente,
                    'respuesta': respuesta,
                    'interes': interes
                })
                
                self.guardar_conversacion(phone_key, nuevo_estado, {
                    'sector': contexto.get('sector'),
                    'historial': historial[-5:],  # Solo últimas 5 interacciones
                    'ultimo_interes': interes
                })
                
                # Notificar por Telegram
                self.notificar_telegram_respuesta(from_phone, mensaje_cliente, respuesta, interes)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")
            return False

# Instancia global
manejador = ManejadorRespuestas()

@app.route('/webhook/whatsapp', methods=['POST'])
def webhook_whatsapp():
    """Endpoint webhook para respuestas de WhatsApp via Twilio"""
    try:
        # Obtener datos de Twilio
        from_phone = request.form.get('From', '')
        mensaje = request.form.get('Body', '')
        
        if not from_phone or not mensaje:
            return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
        
        print(f"📥 Respuesta recibida de {from_phone}: {mensaje}")
        
        # Procesar respuesta automáticamente
        if manejador.procesar_respuesta(from_phone, mensaje):
            return jsonify({'status': 'success', 'message': 'Respuesta procesada'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Error procesando'}), 500
    
    except Exception as e:
        print(f"❌ Error webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/webhook/encuesta', methods=['POST'])
def webhook_encuesta():
    """Endpoint para cuando completan la encuesta"""
    try:
        data = request.get_json()
        
        # Datos de la encuesta
        telefono = data.get('telefono', '')
        nombre_negocio = data.get('nombre_negocio', '')
        sector = data.get('sector', '')
        presupuesto = data.get('presupuesto', '')
        urgencia = data.get('urgencia', '')
        descripcion = data.get('descripcion', '')
        
        # Mensaje de confirmación
        mensaje_confirmacion = f"""¡Excelente! 🎉 He recibido tu encuesta de {nombre_negocio}.

Veo que tienes un proyecto muy interesante con presupuesto de {presupuesto}.

Te voy a contactar en los próximos 30 minutos para revisar todos los detalles y hacerte una propuesta personalizada.

¿Te parece bien si te llamo al {telefono}?"""

        # Enviar confirmación
        telefono_formatted = f"whatsapp:+34{telefono}" if not telefono.startswith('+') else f"whatsapp:{telefono}"
        
        if manejador.enviar_respuesta_whatsapp(telefono_formatted, mensaje_confirmacion):
            # Notificar por Telegram - LEAD CALIENTE
            try:
                texto_telegram = f"""🎉 **¡ENCUESTA COMPLETADA - LEAD CALIENTE!**

📋 **Negocio:** {nombre_negocio}
📞 **Teléfono:** {telefono}
🏢 **Sector:** {sector}
💰 **Presupuesto:** {presupuesto}
⏰ **Urgencia:** {urgencia}

📝 **Descripción:**
{descripcion}

🚀 **¡LEAD LISTO PARA VENTA!**
💬 Confirmación enviada por WhatsApp

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

                manejador.telegram_bot.send_message(
                    chat_id=manejador.telegram_chat,
                    text=texto_telegram,
                    parse_mode='Markdown'
                )
            except:
                pass
            
            return jsonify({'status': 'success', 'message': 'Encuesta procesada'}), 200
        
        return jsonify({'status': 'error', 'message': 'Error enviando confirmación'}), 500
    
    except Exception as e:
        print(f"❌ Error webhook encuesta: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check del webhook"""
    return jsonify({'status': 'ok', 'service': 'webhook-respuestas'}), 200

if __name__ == '__main__':
    print("🚀 Iniciando webhook para respuestas automáticas...")
    print(f"📡 Endpoints disponibles:")
    print(f"   POST /webhook/whatsapp - Respuestas WhatsApp")
    print(f"   POST /webhook/encuesta - Encuestas completadas")
    print(f"   GET /health - Health check")
    
    app.run(host='0.0.0.0', port=5000, debug=False) 