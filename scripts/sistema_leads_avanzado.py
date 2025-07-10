#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA AVANZADO DE LEADS - DESARROYO TECH
Con DeepSeek, plantillas por sector, priorización española y automatización completa
"""

import os
import sys
import json
import time
import random
import re
from datetime import datetime, timedelta
import requests
from twilio.rest import Client
import telegram
from scraper_gratis import ScraperGratis

class SistemaLeadsAvanzado:
    def __init__(self):
        # Configuración desde variables de entorno
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')  # Backup
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.your_name = os.getenv('YOUR_NAME', 'Alberto')
        
        # Inicializar clientes
        if self.twilio_sid and self.twilio_token:
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        
        if self.telegram_token:
            self.telegram_bot = telegram.Bot(token=self.telegram_token)
        
        self.scraper = ScraperGratis()
        
        # Archivos para control
        self.leads_enviados_file = 'leads_enviados.json'
        self.conversaciones_file = 'conversaciones_activas.json'
        self.leads_enviados = self.cargar_leads_enviados()
        self.conversaciones = self.cargar_conversaciones()
        
        # Plantillas CRM por sector
        self.plantillas_sector = self.cargar_plantillas_sector()
        
        # Configuración de canal de comunicación
        self.canal_comunicacion = 'SMS'  # 'SMS', 'WHATSAPP', 'EMAIL'
        # WHATSAPP requiere autorización previa en Sandbox - SMS funciona inmediatamente
    
    def cargar_plantillas_sector(self):
        """Plantillas profesionales orientadas a venta y conversión"""
        return {
            'restaurantes': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He visto {restaurant_name} y detectamos una gran oportunidad para aumentar sus ventas.

🍽️ **NUESTROS SERVICIOS PARA RESTAURANTES:**
✅ Web profesional + reservas y presencia online 24/7
✅ Carta digital actualizable
✅ Sistema de pedidos a domicilio  
✅ Aumentamos ventas hasta 40%

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **Para propuesta personalizada, complete esta encuesta (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Más información:** alberto@desarroyo.tech

Saludos cordiales,
{your_name} - {business_name}
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Reservas online 24/7', 'Carta digital actualizable', 'Pedidos a domicilio', 'Mayor facturación'],
                'urgencia': 'Sus competidores ya están captando clientes online',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'peluquerias': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He visto {salon_name} y detectamos una gran oportunidad para multiplicar sus citas.

💇 **NUESTROS SERVICIOS PARA SALONES:**
✅ Web profesional + reservas y presencia online 24/7
✅ Galería de trabajos que convence
✅ Sistema de citas online
✅ Hasta 60% más reservas confirmadas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **Para propuesta personalizada, complete esta encuesta (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Más información:** alberto@desarroyo.tech

Saludos,
{your_name} - {business_name}
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Reservas automáticas', 'Galería profesional', 'Más citas', 'Presencia digital'],
                'urgencia': 'Sus clientes buscan peluquerías online antes de reservar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'dentistas': {
                'mensaje_inicial': """Estimado Dr./Dra.,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He visto {clinic_name} y detectamos una gran oportunidad para triplicar sus pacientes nuevos.

🦷 **NUESTROS SERVICIOS PARA CLÍNICAS DENTALES:**
✅ Web médica profesional + citas y presencia online 24/7
✅ Información completa de tratamientos
✅ Galería antes/después que genera confianza
✅ Hasta 3x más pacientes nuevos al mes

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **Para propuesta personalizada, complete esta encuesta (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Más información:** alberto@desarroyo.tech

Atentamente,
{your_name} - {business_name}
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más pacientes nuevos', 'Citas online', 'Confianza profesional', 'Información tratamientos'],
                'urgencia': 'Los pacientes eligen dentistas que inspiran confianza online',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'abogados': {
                'mensaje_inicial': """Estimado/a Letrado/a,

Soy {your_name} de {business_name}, especialistas en desarrollo web para despachos de abogados.

He analizado la presencia digital de {law_firm_name} y veo oportunidades importantes de captación.

✅ Web jurídica profesional en máximo 48 horas
✅ Especialidades claramente definidas
✅ Formulario de contacto optimizado
✅ Hasta 5x más consultas cualificadas

Los despachos con presencia digital profesional captan más clientes de calidad.

¿Le interesaría conocer nuestra propuesta? Encuesta rápida (2 minutos):
{website_url}/index_conectado_n8n.html

Saludos profesionales,
{your_name} - {business_name}""",
                'beneficios': ['Más consultas', 'Credibilidad jurídica', 'Especialidades claras', 'Captación profesional'],
                'urgencia': 'Los clientes investigan abogados online antes de contactar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'hoteles': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, especialistas en webs para hoteles independientes.

He analizado {hotel_name} y veo una gran oportunidad para aumentar reservas directas.

✅ Web hotelera profesional en máximo 48 horas
✅ Sistema de reservas sin comisiones
✅ Ahorro del 15-20% en costes de booking
✅ Control total de sus reservas

Los hoteles con web propia aumentan significativamente su rentabilidad.

¿Le interesa conocer cómo? Encuesta personalizada (2 minutos):
{website_url}/index_conectado_n8n.html

Cordialmente,
{your_name} - {business_name}""",
                'beneficios': ['Reservas sin comisiones', 'Mayor rentabilidad', 'Control total', 'Más margen'],
                'urgencia': 'Cada reserva por booking reduce su margen un 15-20%',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'gimnasios': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, especialistas en webs para centros deportivos.

He analizado {gym_name} y detectamos potencial para conseguir más socios.

✅ Web deportiva profesional en máximo 48 horas
✅ Sistema de inscripciones online
✅ Reserva de clases automática
✅ Hasta 50% más inscripciones

Los gimnasios con presencia digital captan más socios que la competencia tradicional.

¿Le interesa nuestra propuesta? Encuesta rápida (2 minutos):
{website_url}/index_conectado_n8n.html

Saludos deportivos,
{your_name} - {business_name}""",
                'beneficios': ['Más socios', 'Inscripciones online', 'Reservas automáticas', 'Gestión digital'],
                'urgencia': 'Las personas buscan gimnasios online antes de apuntarse',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            }
        }
    
    def cargar_leads_enviados(self):
        """Carga leads ya contactados"""
        try:
            if os.path.exists(self.leads_enviados_file):
                with open(self.leads_enviados_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
    
    def cargar_conversaciones(self):
        """Carga conversaciones activas"""
        try:
            if os.path.exists(self.conversaciones_file):
                with open(self.conversaciones_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def guardar_conversacion(self, lead_id, estado, datos_extra=None):
        """Guarda estado de conversación"""
        self.conversaciones[lead_id] = {
            'estado': estado,
            'timestamp': datetime.now().isoformat(),
            'datos_extra': datos_extra or {}
        }
        try:
            with open(self.conversaciones_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversaciones, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def es_telefono_espanol(self, phone):
        """Verifica si es un teléfono español"""
        # Limpiar número
        phone_clean = re.sub(r'[^\d+]', '', phone)
        
        # Patrones españoles
        return (
            phone_clean.startswith('+34') or
            phone_clean.startswith('34') or
            (len(phone_clean) == 9 and phone_clean[0] in ['6', '7', '9'])
        )
    
    def calcular_rating_avanzado(self, lead):
        """Sistema de rating avanzado para priorizar mejor"""
        score = 0
        
        # 1. TELÉFONO ESPAÑOL (MÁXIMA PRIORIDAD)
        if self.es_telefono_espanol(lead['phone']):
            score += 50  # Bonus grande por ser español
        else:
            score -= 20  # Penalización por no ser español
        
        # 2. SIN PÁGINA WEB
        if not lead.get('website') or lead['website'] == '':
            score += 40
        
        # 3. TELÉFONO VÁLIDO
        phone_clean = re.sub(r'[^\d]', '', lead['phone'])
        if len(phone_clean) >= 9:
            score += 25
        
        # 4. TIENE DIRECCIÓN
        if lead.get('address') and len(lead['address']) > 10:
            score += 20
        
        # 5. SECTOR DE ALTO VALOR
        name_lower = lead['name'].lower()
        if any(s in name_lower for s in ['restaurante', 'dental', 'abogado', 'hotel']):
            score += 30
        elif any(s in name_lower for s in ['peluquería', 'gimnasio', 'clínica']):
            score += 25
        
        # 6. PALABRAS CLAVE DE CALIDAD
        if any(word in name_lower for word in ['centro', 'clínica', 'estudio', 'despacho']):
            score += 15
        
        # 7. EVITAR FRANQUICIAS/CADENAS
        if any(word in name_lower for word in ['mc', 'burger', 'telepizza', 'dia%']):
            score -= 30
        
        return max(0, min(100, score))  # Entre 0 y 100
    
    def filtrar_y_calificar_leads_avanzado(self, leads_raw, sector):
        """Filtrado avanzado con priorización española"""
        leads_calificados = []
        
        for business in leads_raw:
            if not business.get('name') or not business.get('phone'):
                continue
            
            # ID único
            lead_id = f"{business['name'].lower().strip()}_{business['phone']}"
            if lead_id in self.leads_enviados:
                continue
            
            # Filtrar por sectores específicos
            name_lower = business['name'].lower()
            sector_keywords = {
                'restaurantes': ['restaurante', 'café', 'bar', 'pizzería', 'comida', 'tapas', 'marisquería'],
                'peluquerias': ['peluquería', 'barbería', 'estética', 'belleza', 'salón'],
                'dentistas': ['dentista', 'dental', 'odontología', 'ortodencia'],
                'abogados': ['abogado', 'bufete', 'jurídico', 'legal', 'notario'],
                'hoteles': ['hotel', 'hostal', 'pensión', 'alojamiento'],
                'gimnasios': ['gimnasio', 'fitness', 'crossfit', 'deportivo']
            }
            
            if sector in sector_keywords:
                if not any(kw in name_lower for kw in sector_keywords[sector]):
                    continue
            
            # Crear lead limpio
            clean_lead = {
                'id': lead_id,
                'name': business['name'].strip(),
                'phone': business['phone'].replace(' ', '').replace('-', '').replace('(', '').replace(')', ''),
                'address': business.get('address', ''),
                'website': business.get('website', ''),
                'sector': sector,
                'source': business.get('source', 'unknown'),
                'timestamp': datetime.now().isoformat()
            }
            
            # Calcular rating avanzado
            clean_lead['score'] = self.calcular_rating_avanzado(clean_lead)
            
            # Solo leads con score mínimo (priorizar calidad)
            if clean_lead['score'] >= 40:  # Mínimo 40/100
                leads_calificados.append(clean_lead)
        
        # Ordenar por score (españoles y de calidad primero)
        leads_calificados.sort(key=lambda x: x['score'], reverse=True)
        
        # Solo los mejores por ejecución (no saturar)
        return leads_calificados[:3]
    
    def generar_mensaje_con_deepseek(self, lead):
        """Genera mensaje personalizado con DeepSeek (más barato)"""
        api_key = self.deepseek_api_key or self.openai_api_key
        api_url = "https://api.deepseek.com/v1/chat/completions" if self.deepseek_api_key else "https://api.openai.com/v1/chat/completions"
        
        if not api_key:
            return self.generar_mensaje_plantilla(lead)
        
        try:
            # Obtener plantilla del sector
            sector = lead.get('sector', 'general')
            plantilla = self.plantillas_sector.get(sector, self.plantillas_sector['restaurantes'])
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt_sistema = f"""Eres {self.your_name} de {self.business_name}, experto en desarrollo web para negocios locales españoles.

SECTOR: {sector}
BENEFICIOS CLAVE: {', '.join(plantilla['beneficios'])}
URGENCIA: {plantilla['urgencia']}

Genera un mensaje de WhatsApp personalizado, amigable y directo que:
1. Sea personal y cercano (usa el nombre del negocio)
2. Mencione beneficios específicos del sector
3. Cree urgencia sin presionar
4. Termine con pregunta que invite a responder
5. Máximo 3 líneas
6. Tono profesional pero cercano"""

            data = {
                'model': 'deepseek-chat' if self.deepseek_api_key else 'gpt-4o-mini',
                'messages': [
                    {'role': 'system', 'content': prompt_sistema},
                    {'role': 'user', 'content': f'Genera mensaje para: {lead["name"]} (Rating: {lead["score"]}/100)'}
                ],
                'max_tokens': 200,
                'temperature': 0.8
            }
            
            response = requests.post(api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                mensaje = result['choices'][0]['message']['content'].strip()
                
                # Personalizar con datos del lead
                mensaje = mensaje.replace('{business_name}', self.business_name)
                mensaje = mensaje.replace('{your_name}', self.your_name)
                mensaje = mensaje.replace('{lead_name}', lead['name'])
                
                return mensaje
            else:
                print(f"❌ Error API: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error generando mensaje IA: {e}")
        
        # Fallback a plantilla
        return self.generar_mensaje_plantilla(lead)
    
    def generar_mensaje_plantilla(self, lead):
        """Mensaje usando plantilla del sector"""
        sector = lead.get('sector', 'restaurantes')
        plantilla = self.plantillas_sector.get(sector, self.plantillas_sector['restaurantes'])
        
        mensaje_base = plantilla['mensaje_inicial']
        
        # Personalizar nombres según sector
        name_replacements = {
            'restaurantes': '{restaurant_name}',
            'peluquerias': '{salon_name}',
            'dentistas': '{clinic_name}',
            'abogados': '{law_firm_name}',
            'hoteles': '{hotel_name}',
            'gimnasios': '{gym_name}'
        }
        
        placeholder = name_replacements.get(sector, '{business_name}')
        
        return mensaje_base.format(
            your_name=self.your_name,
            business_name=self.business_name,
            **{placeholder.strip('{}'): lead['name']}
        )
    
    def generar_mensaje_sms_directo(self, lead):
        """Genera mensaje SMS optimizado - directo y efectivo"""
        sector = lead.get('sector', 'restaurantes')
        
        # Mensajes SMS optimizados por sector (más directos)
        mensajes_sms = {
            'restaurantes': f"""Hola {lead['name']} 👋

Soy Alberto de DesArroyo Tech. ¿Te interesa una web profesional que aumente tus reservas y pedidos online?

✅ Web lista en 48h desde 149€
✅ +40% ventas (clientes reales)
✅ Sistema reservas incluido

Encuesta rápida (2 min): desarroyo.tech/generador_automatizaciones.html

¿Hablamos?""",

            'peluquerias': f"""Hola {lead['name']} 👋

Alberto de DesArroyo Tech. ¿Quieres triplicar tus citas con una web profesional?

✅ Web + reservas online en 48h
✅ Desde 149€, 3 planes disponibles  
✅ +60% citas confirmadas

Encuesta (2 min): desarroyo.tech/generador_automatizaciones.html

¿Te interesa?""",

            'dentistas': f"""Estimado Dr./Dra. {lead['name']}

Alberto de DesArroyo Tech. ¿Le interesa captar 3x más pacientes con una web médica profesional?

✅ Web clínica en 48h desde 149€
✅ Sistema citas online integrado
✅ Resultados garantizados

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Vemos su caso?""",

            'abogados': f"""Estimado/a {lead['name']}

Alberto de DesArroyo Tech. ¿Le interesa captar más clientes con una web de bufete profesional?

✅ Web jurídica en 48h desde 149€  
✅ Presencia digital que genera confianza
✅ +50% consultas online

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Hablamos?""",

            'hoteles': f"""Hola {lead['name']} 👋

Alberto de DesArroyo Tech. ¿Quiere aumentar reservas directas con una web hotelera profesional?

✅ Web + booking en 48h desde 149€
✅ Sin comisiones de OTAs
✅ +30% reservas directas

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Le interesa?""",

            'gimnasios': f"""Hola {lead['name']} 💪

Alberto de DesArroyo Tech. ¿Te interesa captar más socios con una web fitness profesional?

✅ Web + sistema socios en 48h
✅ Desde 149€, resultados garantizados
✅ +40% inscripciones online

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Vemos tu caso?"""
        }
        
        return mensajes_sms.get(sector, mensajes_sms['restaurantes'])
    
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
        print(f"⚠️ Número no válido para España: {phone} (dígitos: {digits_only})")
        return None
    
    def enviar_whatsapp_avanzado(self, lead, mensaje):
        """Envío avanzado con validación anti-error 63024"""
        if not self.twilio_client:
            print(f"⚠️  WhatsApp no configurado")
            return False
        
        # Formatear y validar número
        phone_formatted = self.formatear_telefono_espanol(lead['phone'])
        
        if not phone_formatted:
            print(f"❌ Número inválido para {lead['name']}: {lead['phone']} - SALTANDO")
            return False
        
        try:
            message = self.twilio_client.messages.create(
                from_=f'whatsapp:{self.twilio_whatsapp}',
                body=mensaje,
                to=f'whatsapp:{phone_formatted}'
            )
            
            print(f"✅ WhatsApp → {lead['name']}: {phone_formatted} (Score: {lead['score']}) SID: {message.sid}")
            
            # Guardar conversación iniciada
            self.guardar_conversacion(lead['id'], 'mensaje_inicial_enviado', {
                'phone': phone_formatted,
                'sector': lead['sector'],
                'mensaje': mensaje[:100],
                'twilio_sid': message.sid
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error Twilio {lead['name']}: {e}")
            # Log detallado para diagnóstico
            print(f"   From: whatsapp:{self.twilio_whatsapp}")
            print(f"   To: whatsapp:{phone_formatted}")
            print(f"   Lead: {lead['name']} - {lead['phone']}")
            
            # Análisis específico del error
            error_str = str(e)
            if '63024' in error_str:
                print(f"   🔍 ERROR 63024: Número no autorizado en WhatsApp Sandbox")
                print(f"   💡 SOLUCIÓN: Añadir {phone_formatted} al sandbox de Twilio")
            elif '20003' in error_str:
                print(f"   🔍 ERROR 20003: Credenciales incorrectas")
            elif '21408' in error_str:
                print(f"   🔍 ERROR 21408: Sin permisos WhatsApp")
            
            return False
    
    def enviar_mensaje_automatico(self, lead, mensaje):
        """Envía mensaje por el canal configurado"""
        
        if self.canal_comunicacion == 'SMS':
            # ✅ 100% automático, sin restricciones, ~$0.08/mensaje
            return self.enviar_sms_automatico(lead, mensaje)
        elif self.canal_comunicacion == 'EMAIL':
            # ✅ 100% automático, más económico, requiere emails de leads
            return self.enviar_email_automatico(lead, mensaje)
        elif self.canal_comunicacion == 'WHATSAPP':
            # ⚠️ Requiere autorización manual en Sandbox o API de pago
            return self.enviar_whatsapp_avanzado(lead, mensaje)
        else:
            print(f"❌ Canal no válido: {self.canal_comunicacion}")
            return False
    
    def enviar_sms_automatico(self, lead, mensaje):
        """Envía SMS automático - SIN RESTRICCIONES DE AUTORIZACIÓN"""
        if not self.twilio_client:
            print(f"⚠️  Twilio no configurado")
            return False
        
        # Formatear y validar número
        phone_formatted = self.formatear_telefono_espanol(lead['phone'])
        
        if not phone_formatted:
            print(f"❌ Número inválido para {lead['name']}: {lead['phone']} - SALTANDO")
            return False
        
        try:
            # SMS - NO REQUIERE AUTORIZACIÓN PREVIA
            message = self.twilio_client.messages.create(
                from_=self.twilio_whatsapp,  # Tu número Twilio
                body=mensaje,
                to=phone_formatted  # SIN 'whatsapp:' - es SMS directo
            )
            
            print(f"✅ SMS → {lead['name']}: {phone_formatted} (Score: {lead['score']}) SID: {message.sid}")
            
            # Guardar conversación iniciada
            self.guardar_conversacion(lead['id'], 'sms_inicial_enviado', {
                'phone': phone_formatted,
                'sector': lead['sector'],
                'mensaje': mensaje[:100],
                'twilio_sid': message.sid,
                'canal': 'SMS'
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error Twilio SMS {lead['name']}: {e}")
            print(f"   From: {self.twilio_whatsapp}")
            print(f"   To: {phone_formatted}")
            print(f"   Lead: {lead['name']} - {lead['phone']}")
            
            return False
    
    def enviar_email_automatico(self, lead, mensaje):
        """Envía email profesional - MÁS ECONÓMICO que SMS"""
        # Requiere configurar SMTP (Gmail, Outlook, etc.)
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_user = os.getenv('SMTP_USER')  # tu-email@gmail.com
        smtp_pass = os.getenv('SMTP_PASS')  # contraseña de aplicación
        
        if not smtp_user or not smtp_pass:
            print(f"⚠️  Email no configurado (SMTP_USER, SMTP_PASS)")
            return False
        
        # Buscar email del lead (si está disponible)
        email_lead = lead.get('email')
        if not email_lead:
            print(f"⚠️  {lead['name']} sin email - SALTANDO")
            return False
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            # Crear mensaje profesional
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Propuesta web profesional para {lead['name']}"
            msg['From'] = f"{self.your_name} <{smtp_user}>"
            msg['To'] = email_lead
            
            # HTML profesional
            html_body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                  <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px;">🚀 {self.business_name}</h1>
                    <p style="margin: 10px 0 0; font-size: 16px;">Desarrollo Web Profesional</p>
                  </div>
                  
                  <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); margin-top: 20px;">
                    <h2 style="color: #333; margin-top: 0;">Hola, equipo de {lead['name']} 👋</h2>
                    
                    <p>{mensaje.replace(chr(10), '<br>')}</p>
                    
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                      <h3 style="color: #495057; margin-top: 0;">📋 Nuestros Planes:</h3>
                      <div style="margin: 15px 0;">
                        <strong style="color: #28a745;">🟢 Plan Rápida: 149€</strong><br>
                        ✅ 1 página profesional<br>
                        ✅ Entrega en 72 horas<br>
                        ✅ Optimizada para móviles
                      </div>
                      <div style="margin: 15px 0;">
                        <strong style="color: #ffc107;">🟡 Plan Escalable: 449€</strong><br>
                        ✅ Hasta 5 páginas<br>
                        ✅ SEO básico incluido<br>
                        ✅ Animaciones profesionales
                      </div>
                      <div style="margin: 15px 0;">
                        <strong style="color: #dc3545;">🔴 Plan Pro Digital: 999€</strong><br>
                        ✅ Hasta 10 páginas<br>
                        ✅ Dashboard personalizado<br>
                        ✅ Integración avanzada
                      </div>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                      <a href="{self.website_url}/generador_automatizaciones.html" 
                         style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">
                        📋 Completar Encuesta (2 min)
                      </a>
                    </div>
                    
                    <p style="color: #6c757d; font-size: 14px; border-top: 1px solid #eee; padding-top: 20px; margin-top: 30px;">
                      <strong>{self.your_name}</strong><br>
                      {self.business_name}<br>
                      📧 {smtp_user}<br>
                      🌐 {self.website_url}
                    </p>
                  </div>
                </div>
              </body>
            </html>
            """
            
            # Versión texto plano (fallback)
            text_body = f"""
            {self.business_name} - Propuesta Web Profesional
            
            Hola, equipo de {lead['name']}
            
            {mensaje}
            
            NUESTROS PLANES:
            
            🟢 Plan Rápida: 149€
            - 1 página profesional
            - Entrega en 72 horas
            
            🟡 Plan Escalable: 449€ 
            - Hasta 5 páginas
            - SEO básico incluido
            
            🔴 Plan Pro Digital: 999€
            - Hasta 10 páginas
            - Dashboard personalizado
            
            Completar encuesta: {self.website_url}/generador_automatizaciones.html
            
            Saludos,
            {self.your_name}
            {self.business_name}
            """
            
            # Adjuntar ambas versiones
            msg.attach(MIMEText(text_body, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # Enviar
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            
            print(f"✅ EMAIL → {lead['name']}: {email_lead} (Score: {lead['score']})")
            
            # Guardar conversación iniciada
            self.guardar_conversacion(lead['id'], 'email_inicial_enviado', {
                'email': email_lead,
                'phone': lead.get('phone', 'N/A'),
                'sector': lead['sector'],
                'mensaje': mensaje[:100],
                'canal': 'EMAIL'
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Error enviando email a {lead['name']}: {e}")
            return False
    
    def notificar_telegram_avanzado(self, leads_contactados, ciudad, sector):
        """Notificación avanzada con estadísticas"""
        if not self.telegram_bot:
            return
        
        try:
            total_score = sum(lead['score'] for lead in leads_contactados)
            avg_score = total_score / len(leads_contactados) if leads_contactados else 0
            
            texto = f"""🚀 **LEADS CONTACTADOS - {sector.upper()}**

📍 **Ciudad:** {ciudad}
🏢 **Sector:** {sector}
📱 **Contactados:** {len(leads_contactados)}
⭐ **Score promedio:** {avg_score:.1f}/100

📊 **DETALLES:**"""

            for i, lead in enumerate(leads_contactados, 1):
                es_espanol = "🇪🇸" if self.es_telefono_espanol(lead['phone']) else "🌍"
                texto += f"\n{i}. {es_espanol} {lead['name']} ({lead['score']}/100)"
            
            texto += f"""

💰 **Costo estimado:** $0.15-0.30
⏰ **Próxima ejecución:** En 6 horas
🎯 **Estado:** Sistema funcionando automáticamente

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            self.telegram_bot.send_message(
                chat_id=self.telegram_chat,
                text=texto,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            print(f"❌ Error Telegram: {e}")
    
    def ejecutar_sector_ciudad(self, ciudad, sector):
        """Ejecuta búsqueda completa para sector y ciudad específicos"""
        print(f"\n🚀 BÚSQUEDA AVANZADA: {sector.upper()} en {ciudad.upper()}")
        print("=" * 60)
        
        # 1. SCRAPING
        print("🔍 Fase 1: Buscando leads especializados...")
        try:
            google_results = self.scraper.scrape_google_maps_businesses(ciudad, sector)
            pa_results = self.scraper.scrape_paginas_amarillas(ciudad, sector)
            dir_results = self.scraper.scrape_directorio_empresas(ciudad, sector)
            
            todos_leads = google_results + pa_results + dir_results
            print(f"📊 Encontrados {len(todos_leads)} leads brutos")
            
        except Exception as e:
            print(f"❌ Error scraping: {e}")
            return
        
        # 2. FILTRADO AVANZADO
        print("🎯 Fase 2: Filtrado avanzado (prioridad españoles)...")
        leads_calificados = self.filtrar_y_calificar_leads_avanzado(todos_leads, sector)
        
        if not leads_calificados:
            print("ℹ️  No se encontraron leads de calidad suficiente")
            return
        
        print(f"⭐ {len(leads_calificados)} leads de alta calidad")
        for lead in leads_calificados:
            es_esp = "🇪🇸" if self.es_telefono_espanol(lead['phone']) else "🌍"
            print(f"   {es_esp} {lead['name']} - Score: {lead['score']}/100")
        
        # 3. CONTACTO PERSONALIZADO
        print("📱 Fase 3: Contacto personalizado...")
        leads_contactados = []
        
        for lead in leads_calificados:
            try:
                print(f"\n📞 Contactando: {lead['name']} (Score: {lead['score']})")
                
                # Generar mensaje optimizado según canal
                if self.canal_comunicacion == 'SMS':
                    mensaje = self.generar_mensaje_sms_directo(lead)
                else:
                    mensaje = self.generar_mensaje_con_deepseek(lead)
                print(f"💬 Mensaje: {mensaje[:50]}...")
                
                # Enviar mensaje (SMS o WhatsApp según configuración)
                if self.enviar_mensaje_automatico(lead, mensaje):
                    leads_contactados.append(lead)
                    
                    # Marcar como enviado
                    self.leads_enviados.add(lead['id'])
                    
                    # Delay profesional entre mensajes
                    delay = random.uniform(45, 90)  # 45-90 segundos
                    print(f"⏱️  Esperando {delay:.0f}s antes del siguiente...")
                    time.sleep(delay)
                
            except Exception as e:
                print(f"❌ Error contactando {lead['name']}: {e}")
                continue
        
        # 4. GUARDAR DATOS Y NOTIFICAR
        try:
            with open(self.leads_enviados_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.leads_enviados), f)
        except:
            pass
        
        self.notificar_telegram_avanzado(leads_contactados, ciudad, sector)
        
        print(f"\n✅ RESUMEN FINAL - {sector.upper()} en {ciudad.upper()}:")
        print(f"   🔍 Leads encontrados: {len(todos_leads)}")
        print(f"   ⭐ Leads calificados: {len(leads_calificados)}")
        print(f"   📱 Leads contactados: {len(leads_contactados)}")
        print(f"   🇪🇸 Españoles contactados: {sum(1 for l in leads_contactados if self.es_telefono_espanol(l['phone']))}")
        print(f"   ⏰ Hora: {datetime.now().strftime('%H:%M')}")

def main():
    """Función principal mejorada"""
    if len(sys.argv) < 3:
        print("Uso: python3 sistema_leads_avanzado.py <ciudad> <sector>")
        print("\nSectores disponibles:")
        print("  - restaurantes")
        print("  - peluquerias") 
        print("  - dentistas")
        print("  - abogados")
        print("  - hoteles")
        print("  - gimnasios")
        sys.exit(1)
    
    ciudad = sys.argv[1]
    sector = sys.argv[2]
    
    sistema = SistemaLeadsAvanzado()
    sistema.ejecutar_sector_ciudad(ciudad, sector)

if __name__ == "__main__":
    main() 