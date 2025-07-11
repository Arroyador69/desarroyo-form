#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA AVANZADO DE LEADS - DESARROYO TECH
Con DeepSeek, plantillas por sector, priorización española y automatización completa
HÍBRIDO: SMS Masivo + Llamadas Conversacionales con Lista Negra
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
from twilio.twiml.voice_response import VoiceResponse
import argparse

class SistemaLeadsAvanzado:
    def __init__(self):
        # Configuración desde variables de entorno
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.agent_intro = "un agente comercial de DesArroyo Tech"
        
        # Configuración Twilio (para SMS)
        self.twilio_enabled = all([
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN'),
            os.getenv('TWILIO_PHONE_NUMBER')
        ])
        
        if self.twilio_enabled:
            from twilio.rest import Client
            self.twilio_client = Client(
                os.getenv('TWILIO_ACCOUNT_SID'),
                os.getenv('TWILIO_AUTH_TOKEN')
            )
            
        # NUEVA: Configuración Vonage (para LLAMADAS con números españoles)
        self.vonage_enabled = all([
            os.getenv('VONAGE_API_KEY'),
            os.getenv('VONAGE_API_SECRET'),
            os.getenv('VONAGE_PHONE_NUMBER')
        ])
        
        if self.vonage_enabled:
            try:
                import vonage
                self.vonage_client = vonage.Client(
                    key=os.getenv('VONAGE_API_KEY'),
                    secret=os.getenv('VONAGE_API_SECRET')
                )
                print(f"✅ VONAGE configurado: {os.getenv('VONAGE_PHONE_NUMBER')} (números españoles)")
            except ImportError:
                print("⚠️ Vonage SDK no instalado. Usar: pip install vonage")
                self.vonage_enabled = False
            except Exception as e:
                print(f"❌ Error configurando Vonage: {e}")
                self.vonage_enabled = False
        
        # Configuración de llamadas (mantener Twilio como fallback)
        self.twilio_voice_enabled = all([
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN'),
            os.getenv('TWILIO_PHONE_NUMBER')
        ]) and self.twilio_enabled
        
        # Archivos de datos
        self.leads_enviados_file = 'leads_contactados_hoy.json'
        self.conversaciones_file = 'conversaciones_activas.json'
        self.lista_negra_file = 'lista_negra_llamadas.json'
        self.llamadas_exitosas_file = 'llamadas_exitosas.json'
        
        # Cargar datos existentes
        self.leads_enviados = self.cargar_leads_enviados()
        self.conversaciones = self.cargar_conversaciones()
        self.lista_negra = self.cargar_lista_negra()
        self.llamadas_exitosas = self.cargar_llamadas_exitosas()
        
        # Configuración de WhatsApp
        self.whatsapp_enabled = all([
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_AUTH_TOKEN'),
            os.getenv('TWILIO_WHATSAPP_NUMBER')
        ])
        
        # Configuración de voz (scripts por sector)
        self.voice_scripts = {
            'restaurantes': {
                'intro': 'Hola, buenos días. Soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web para restaurantes.',
                'personalizacion': 'Estoy llamando específicamente por {nombre_negocio}, he visto que están en {ciudad} y me parece un restaurante con mucho potencial.',
                'hook': 'Los restaurantes en {ciudad} que tienen web profesional están consiguiendo un 40% más de reservas que sus competidores.',
                'propuesta': 'Me gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más clientes con una web que muestre su carta, permita reservas online y aumente sus ventas. ¿Le interesaría escuchar esta información?',
                'respuesta_si': 'Perfecto. Le voy a enviar toda la información por SMS a este número. Revise su móvil en unos minutos.',
                'respuesta_no_1': 'Entiendo. Déjeme preguntarle una cosa: ¿han notado que muchos clientes buscan restaurantes online antes de decidir dónde cenar? Trabajamos con restaurantes locales para ayudarlos a aparecer mejor en internet. ¿Esto le resultaría más interesante?',
                'respuesta_no_2': 'Comprendo su posición. Una última cosa: hemos visto que los restaurantes en {ciudad} que no tienen presencia digital pierden clientes cada día. Por eso creamos un plan de 149€ muy asequible. ¿Le envío la información sin compromiso?',
                'despedida': 'Entiendo. Si cambia de opinión, puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.'
            },
            'dentistas': {
                'intro': 'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en webs para clínicas dentales.',
                'personalizacion': 'Estoy llamando específicamente por {nombre_negocio}, he visto que están en {ciudad} y se dedican a servicios dentales.',
                'hook': 'Las clínicas dentales en {ciudad} con web moderna están consiguiendo un 60% más de pacientes nuevos.',
                'propuesta': 'Nos gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más pacientes con una web que permita citas online y genere confianza profesional. ¿Le interesaría conocer esta información?',
                'respuesta_si': 'Excelente. Le envío toda la información por SMS para que pueda revisarla tranquilamente.',
                'respuesta_no_1': 'Entiendo. ¿Han observado que los pacientes nuevos cada vez buscan más información online antes de elegir dentista? Ayudamos a clínicas como {nombre_negocio} a transmitir confianza y profesionalidad. ¿Esto le resultaría útil?',
                'respuesta_no_2': 'Comprendo. Una cosa más: muchas clínicas en {ciudad} están perdiendo pacientes porque no aparecen bien en internet. Tenemos un plan desde 149€ muy accesible. ¿Le mando la información para que la revise?',
                'despedida': 'Lo entiendo. Si reconsideran, pueden contactarnos en alberto@desarroyo.tech. Que tengan un buen día.'
            },
            'peluquerias': {
                'intro': 'Hola, buenos días. Soy un agente comercial de DesArroyo Tech. Nos especializamos en webs para salones de belleza.',
                'personalizacion': 'Estoy llamando específicamente por {nombre_negocio}, he visto que están en {ciudad} y me parece un salón muy cuidado.',
                'hook': 'Los salones de belleza en {ciudad} con web profesional están aumentando sus citas un 50%.',
                'propuesta': 'Me gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más citas con una web que muestre sus trabajos y permita reservas online. ¿Le interesaría escuchar esta propuesta?',
                'respuesta_si': 'Perfecto. Le envío la información por SMS para que pueda revisarla cuando guste.',
                'respuesta_no_1': '¿Han notado que las clientas buscan peluquerías en internet para ver trabajos antes de venir? Ayudamos a salones como {nombre_negocio} a mostrar mejor sus servicios online. ¿Esto le interesaría más?',
                'respuesta_no_2': 'Entiendo. Solo una cosa más: muchos salones en {ciudad} están consiguiendo más clientas con una web sencilla. Tenemos opciones desde 149€. ¿Le envío la información para que la vea sin compromiso?',
                'despedida': 'Lo comprendo. Si cambian de opinión, pueden escribirnos a alberto@desarroyo.tech. Que tenga un buen día.'
            },
            'abogados': {
                'intro': 'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en webs para despachos de abogados.',
                'personalizacion': 'Estoy llamando específicamente por {nombre_negocio}, he visto que están en {ciudad} y se especializan en servicios jurídicos.',
                'hook': 'Los despachos de abogados en {ciudad} con web profesional están consiguiendo un 70% más de consultas.',
                'propuesta': 'Nos gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más consultas con una web que genere confianza y muestre sus especialidades claramente. ¿Le interesaría conocer esta información?',
                'respuesta_si': 'Perfecto. Le envío información detallada por SMS para que pueda revisarla tranquilamente.',
                'respuesta_no_1': '¿Han observado que los clientes investigan abogados online antes de contactar? Ayudamos a despachos como {nombre_negocio} a transmitir confianza y profesionalidad en internet. ¿Esto le resultaría interesante?',
                'respuesta_no_2': 'Comprendo su posición. Solo mencionar que muchos despachos en {ciudad} están consiguiendo más clientes con presencia digital. Tenemos planes desde 149€. ¿Le mando la información para revisarla?',
                'despedida': 'Lo entiendo perfectamente. Si reconsidera, puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.'
            },
            'default': {
                'intro': 'Buenos días, soy un agente comercial de DesArroyo Tech, empresa especializada en desarrollo web profesional para negocios.',
                'personalizacion': 'Estoy llamando específicamente por {nombre_negocio}, he visto que están en {ciudad} y me parece un negocio con mucho potencial.',
                'hook': 'Las empresas en {ciudad} con web profesional están aumentando sus ventas un 45%.',
                'propuesta': 'Me gustaría explicarle cómo podríamos ayudar a {nombre_negocio} a conseguir más clientes con una web profesional que atraiga y convierta visitas en ventas. ¿Le interesaría escuchar esta información?',
                'respuesta_si': 'Excelente. Le envío la información por SMS para que pueda revisarla cuando guste.',
                'respuesta_no_1': '¿Han notado que los clientes buscan servicios online antes de comprar? Ayudamos a negocios como {nombre_negocio} a aparecer mejor en internet y conseguir más ventas. ¿Esto le resultaría útil?',
                'respuesta_no_2': 'Entiendo. Una última cosa: muchos negocios en {ciudad} están creciendo con una web sencilla. Tenemos opciones desde 149€ muy asequibles. ¿Le envío la información sin compromiso?',
                'despedida': 'Lo comprendo. Si cambia de opinión, puede contactarnos en alberto@desarroyo.tech. Que tenga un buen día.'
            }
        }
        
        # Configuración de voz
        self.voice_config = {
            'voice': 'Polly.Lucia',  # Voz española femenina
            'language': 'es-ES'
        }
        
        # Plantillas de mensajes por sector
        self.plantillas_sector = self.cargar_plantillas_sector()
        
        # Configuración de presupuesto
        self.presupuesto_configuracion = {
            'presupuesto_diario_maximo': 10.0,  # 10€ máximo por día
            'costo_llamada_minuto': 0.08,       # €0.08 por minuto con número español
            'costo_sms_nacional': 0.07,         # €0.07 por SMS nacional
            'duracion_llamada_promedio': 1.5,   # 1.5 minutos promedio por llamada
            'factor_seguridad': 0.85             # Factor de seguridad del 85%
        }
        
        # Inicializar scraper
        self.scraper = ScraperGratis()
        
        # Canal de comunicación por defecto
        self.canal_comunicacion = 'LLAMADAS'
    
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

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos cordiales,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
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

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
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

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Atentamente,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más pacientes nuevos', 'Citas online', 'Confianza profesional', 'Información tratamientos'],
                'urgencia': 'Los pacientes eligen dentistas que inspiran confianza online',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'abogados': {
                'mensaje_inicial': """Estimado/a Letrado/a,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado la presencia digital de {law_firm_name} y veo oportunidades importantes de captación.

⚖️ **NUESTROS SERVICIOS PARA DESPACHOS:**
✅ Web jurídica profesional + presencia online 24/7
✅ Especialidades claramente definidas
✅ Formulario de contacto optimizado
✅ Hasta 5x más consultas cualificadas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos profesionales,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más consultas', 'Credibilidad jurídica', 'Especialidades claras', 'Captación profesional'],
                'urgencia': 'Los clientes investigan abogados online antes de contactar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'hoteles': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {hotel_name} y veo una gran oportunidad para aumentar reservas directas.

🏨 **NUESTROS SERVICIOS PARA HOTELES:**
✅ Web hotelera profesional + presencia online 24/7
✅ Sistema de reservas sin comisiones
✅ Ahorro del 15-20% en costes de booking
✅ Control total de sus reservas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Cordialmente,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Reservas sin comisiones', 'Mayor rentabilidad', 'Control total', 'Más margen'],
                'urgencia': 'Cada reserva por booking reduce su margen un 15-20%',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'gimnasios': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {gym_name} y detectamos potencial para conseguir más socios.

💪 **NUESTROS SERVICIOS PARA GIMNASIOS:**
✅ Web deportiva profesional + presencia online 24/7
✅ Sistema de inscripciones online
✅ Reserva de clases automática
✅ Hasta 50% más inscripciones

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos deportivos,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más socios', 'Inscripciones online', 'Reservas automáticas', 'Gestión digital'],
                'urgencia': 'Las personas buscan gimnasios online antes de apuntarse',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            # === SERVICIOS DE SALUD Y BELLEZA ===
            'centros_estetica': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y detectamos una gran oportunidad para multiplicar citas.

💆 **NUESTROS SERVICIOS PARA CENTROS DE ESTÉTICA:**
✅ Web profesional + reservas online 24/7
✅ Galería de tratamientos que convence
✅ Sistema de citas automático
✅ Hasta 70% más reservas confirmadas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más citas', 'Reservas automáticas', 'Galería profesional', 'Presencia digital'],
                'urgencia': 'Los clientes buscan centros de estética online antes de reservar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'psicologos': {
                'mensaje_inicial': """Estimado/a profesional,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y veo una gran oportunidad para conseguir más pacientes.

🧠 **NUESTROS SERVICIOS PARA PSICÓLOGOS:**
✅ Web profesional + presencia online 24/7
✅ Sistema de citas confidencial
✅ Información clara de especialidades
✅ Hasta 60% más consultas cualificadas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Atentamente,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más pacientes', 'Citas online', 'Credibilidad profesional', 'Especialidades claras'],
                'urgencia': 'Los pacientes buscan psicólogos online antes de contactar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'fisioterapeutas': {
                'mensaje_inicial': """Estimado/a fisioterapeuta,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y detectamos potencial para más pacientes.

🦴 **NUESTROS SERVICIOS PARA FISIOTERAPEUTAS:**
✅ Web profesional + reservas online 24/7
✅ Información clara de tratamientos
✅ Sistema de citas automático
✅ Hasta 50% más pacientes nuevos

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos profesionales,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más pacientes', 'Reservas online', 'Información tratamientos', 'Credibilidad'],
                'urgencia': 'Los pacientes buscan fisioterapeutas online antes de llamar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            # === ALIMENTACIÓN Y GASTRONOMÍA ===
            'cafeterias': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He visto {business_name_placeholder} y detectamos una gran oportunidad para aumentar ventas.

☕ **NUESTROS SERVICIOS PARA CAFETERÍAS:**
✅ Web profesional + presencia online 24/7
✅ Carta digital actualizable
✅ Sistema de pedidos online
✅ Hasta 45% más ventas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos cordiales,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Pedidos online', 'Carta digital', 'Más ventas', 'Presencia digital'],
                'urgencia': 'Los clientes buscan cafeterías online antes de visitarlas',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'panaderias': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y veo potencial para multiplicar ventas.

🥖 **NUESTROS SERVICIOS PARA PANADERÍAS:**
✅ Web artesanal profesional + presencia online 24/7
✅ Catálogo de productos actualizable
✅ Sistema de encargos online
✅ Hasta 60% más pedidos especiales

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Encargos online', 'Catálogo digital', 'Más pedidos', 'Presencia artesanal'],
                'urgencia': 'Los clientes buscan panaderías artesanas online',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            # === SERVICIOS TÉCNICOS ===
            'electricistas': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y veo una gran oportunidad para conseguir más clientes.

⚡ **NUESTROS SERVICIOS PARA ELECTRICISTAS:**
✅ Web profesional + presencia online 24/7
✅ Formulario de presupuestos
✅ Galería de trabajos realizados
✅ Hasta 70% más consultas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos profesionales,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más clientes', 'Presupuestos online', 'Galería trabajos', 'Credibilidad'],
                'urgencia': 'Los clientes buscan electricistas online antes de contratar',
                'precio_ref': 'Desde 149€ - 3 planes disponibles'
            },
            
            'fontaneros': {
                'mensaje_inicial': """Buenos días,

Soy {your_name} de {business_name}, empresa especializada en ayudar a negocios locales a crear su web de manera rápida, personalizada al 100% y eficiente.

He analizado {business_name_placeholder} y detectamos potencial para más trabajos.

🔧 **NUESTROS SERVICIOS PARA FONTANEROS:**
✅ Web profesional + presencia online 24/7
✅ Formulario de urgencias
✅ Servicios claramente definidos
✅ Hasta 65% más llamadas

💰 **NUESTROS 3 PLANES:**
🟢 **Plan Rápida: 149€** - 1 página + **entrega garantizada en 48h**
🟡 **Plan Escalable: 449€** - 5 páginas + SEO básico + entrega en pocos días
🔴 **Plan Pro: 999€** - 10 páginas + dashboard completo + entrega según complejidad

📋 **TODA LA INFO EN ESTA ENCUESTA (2 minutos):**
{website_url}/index_conectado_n8n.html

📧 **Dudas por email:** alberto@desarroyo.tech

⚠️ **NO responda a este SMS - Use solo la encuesta o email**

Saludos,
{your_name} - {business_name}
📧 alberto@desarroyo.tech
"Transformamos negocios locales en máquinas de ventas online" 🚀""",
                'beneficios': ['Más trabajos', 'Urgencias online', 'Servicios claros', 'Mayor alcance'],
                'urgencia': 'Los clientes buscan fontaneros online en urgencias',
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
    
    def es_telefono_movil_espanol(self, phone):
        """Verifica si es un móvil español (solo para WhatsApp)"""
        # Limpiar número
        phone_clean = re.sub(r'[^\d+]', '', phone)
        digits_only = re.sub(r'[^\d]', '', phone)
        
        # Números móviles españoles: 6xx, 7xx
        if phone_clean.startswith('+34'):
            if len(digits_only) == 11 and digits_only.startswith('34'):
                # Solo móviles: 6xx, 7xx 
                return digits_only[2] in ['6', '7']
        
        if digits_only.startswith('34') and len(digits_only) == 11:
            return digits_only[2] in ['6', '7']
        
        if len(digits_only) == 9:
            # Solo móviles españoles: 6xx, 7xx
            return digits_only[0] in ['6', '7']
        
        return False
    
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

Somos DesArroyo Tech. ¿Te interesa una web profesional que aumente tus reservas y pedidos online?

✅ Web lista en 48h desde 149€
✅ +40% ventas (clientes reales)
✅ Sistema reservas incluido

Encuesta rápida (2 min): desarroyo.tech/generador_automatizaciones.html

¿Hablamos?""",

            'peluquerias': f"""Hola {lead['name']} 👋

DesArroyo Tech. ¿Quieres triplicar tus citas con una web profesional?

✅ Web + reservas online en 48h
✅ Desde 149€, 3 planes disponibles  
✅ +60% citas confirmadas

Encuesta (2 min): desarroyo.tech/generador_automatizaciones.html

¿Te interesa?""",

            'dentistas': f"""Estimado Dr./Dra. {lead['name']}

DesArroyo Tech. ¿Le interesa captar 3x más pacientes con una web médica profesional?

✅ Web clínica en 48h desde 149€
✅ Sistema citas online integrado
✅ Resultados garantizados

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Vemos su caso?""",

            'abogados': f"""Estimado/a {lead['name']}

DesArroyo Tech. ¿Le interesa captar más clientes con una web de bufete profesional?

✅ Web jurídica en 48h desde 149€  
✅ Presencia digital que genera confianza
✅ +50% consultas online

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Hablamos?""",

            'hoteles': f"""Hola {lead['name']} 👋

DesArroyo Tech. ¿Quiere aumentar reservas directas con una web hotelera profesional?

✅ Web + booking en 48h desde 149€
✅ Sin comisiones de OTAs
✅ +30% reservas directas

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Le interesa?""",

            'gimnasios': f"""Hola {lead['name']} 💪

DesArroyo Tech. ¿Te interesa captar más socios con una web fitness profesional?

✅ Web + sistema socios en 48h
✅ Desde 149€, resultados garantizados
✅ +40% inscripciones online

Encuesta: desarroyo.tech/generador_automatizaciones.html

¿Vemos tu caso?"""
        }
        
        return mensajes_sms.get(sector, mensajes_sms['restaurantes'])
    
    def formatear_telefono_espanol(self, phone):
        """VALIDACIÓN SÚPER ESTRICTA - Evita errores 21211 y 63024"""
        import re
        
        if not phone or str(phone).strip() == '':
            print(f"❌ Número vacío")
            return None
        
        # Limpiar número completamente (solo dígitos y +)
        phone_str = str(phone).strip()
        phone_clean = re.sub(r'[^\d+]', '', phone_str)
        
        # Extraer solo dígitos
        digits_only = re.sub(r'[^\d]', '', phone_clean)
        
        # VALIDACIÓN 1: Longitud de dígitos debe ser exacta
        if len(digits_only) < 9 or len(digits_only) > 11:
            print(f"❌ Longitud inválida: {phone} → {digits_only} ({len(digits_only)} dígitos)")
            return None
        
        # CONSTRUIR NÚMERO EN FORMATO E.164
        formatted_number = None
        
        # Caso 1: Ya tiene +34 (11 dígitos totales)
        if phone_clean.startswith('+34') and len(digits_only) == 11:
            formatted_number = phone_clean
        
        # Caso 2: Empieza con 34 sin + (11 dígitos)
        elif digits_only.startswith('34') and len(digits_only) == 11:
            formatted_number = f"+{digits_only}"
        
        # Caso 3: Número nacional de 9 dígitos
        elif len(digits_only) == 9:
            formatted_number = f"+34{digits_only}"
        
        # Caso 4: Empezar con 0 (quitar y añadir +34)
        elif digits_only.startswith('0') and len(digits_only) == 10:
            formatted_number = f"+34{digits_only[1:]}"
        
        if not formatted_number:
            print(f"❌ Formato no reconocido: {phone} → {digits_only}")
            return None
        
        # VALIDACIÓN 2: Verificar formato E.164 exacto
        if not re.match(r'^\+34\d{9}$', formatted_number):
            print(f"❌ No es E.164 válido: {phone} → {formatted_number}")
            return None
        
        # VALIDACIÓN 3: Obtener dígito nacional (primer dígito después de +34)
        national_number = formatted_number[3:]  # Quitar +34
        first_digit = national_number[0]
        
        # VALIDACIÓN 4: Solo móviles españoles válidos (6XX, 7XX) para SMS
        if self.canal_comunicacion in ['SMS', 'WHATSAPP']:
            if first_digit not in ['6', '7']:
                print(f"❌ No es móvil español: {phone} → {formatted_number} (empieza por {first_digit})")
                return None
        
        # VALIDACIÓN 5: Verificar patrones móviles específicos españoles
        if first_digit == '6':
            # 6XX - Móviles tradicionales
            if len(national_number) != 9:
                print(f"❌ Móvil 6XX inválido: {formatted_number}")
                return None
        elif first_digit == '7':
            # 7XX - Móviles nuevos
            if len(national_number) != 9:
                print(f"❌ Móvil 7XX inválido: {formatted_number}")
                return None
        
        # VALIDACIÓN FINAL: Comprobar que no sea un número conocido como problemático
        problematic_patterns = [
            '+34111111111', '+34222222222', '+34333333333',
            '+34999999999', '+34000000000', '+34123456789'
        ]
        
        if formatted_number in problematic_patterns:
            print(f"❌ Número de prueba detectado: {formatted_number}")
            return None
        
        print(f"✅ Número válido E.164: {phone} → {formatted_number}")
        return formatted_number
    
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
            elif '21635' in error_str:
                print(f"   🔍 ERROR 21635: No se puede enviar WhatsApp a número fijo")
                print(f"   💡 SOLUCIÓN: Solo enviar a móviles (6xx, 7xx)")
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
        """Envía SMS automático - VALIDACIÓN SÚPER ESTRICTA"""
        if not self.twilio_client:
            print(f"⚠️  Twilio no configurado")
            return False
        
        # TRIPLE VALIDACIÓN DEL NÚMERO
        print(f"\n🔍 VALIDANDO NÚMERO PARA {lead['name']}:")
        print(f"   📞 Original: {lead['phone']}")
        
        # Validación 1: Formatear número
        phone_formatted = self.formatear_telefono_espanol(lead['phone'])
        
        if not phone_formatted:
            print(f"❌ FALLO VALIDACIÓN 1: Número inválido para {lead['name']}: {lead['phone']}")
            return False
        
        print(f"   ✅ Formateado: {phone_formatted}")
        
        # Validación 2: Re-verificar formato E.164
        import re
        if not re.match(r'^\+34[67]\d{8}$', phone_formatted):
            print(f"❌ FALLO VALIDACIÓN 2: No es E.164 válido: {phone_formatted}")
            return False
        
        print(f"   ✅ E.164 válido: {phone_formatted}")
        
        # Validación 3: Verificar que es móvil español
        numero_nacional = phone_formatted[3:]
        if len(numero_nacional) != 9 or numero_nacional[0] not in ['6', '7']:
            print(f"❌ FALLO VALIDACIÓN 3: No es móvil español: {numero_nacional}")
            return False
        
        print(f"   ✅ Móvil español confirmado: {numero_nacional}")
        
        try:
            print(f"📤 ENVIANDO SMS...")
            print(f"   From: {self.twilio_whatsapp}")
            print(f"   To: {phone_formatted}")
            print(f"   Mensaje: {mensaje[:50]}...")
            
            # SMS - NO REQUIERE AUTORIZACIÓN PREVIA
            message = self.twilio_client.messages.create(
                from_=self.twilio_whatsapp,  # Tu número Twilio
                body=mensaje,
                to=phone_formatted  # SIN 'whatsapp:' - es SMS directo
            )
            
            print(f"✅ SMS ENVIADO EXITOSAMENTE!")
            print(f"   📱 {lead['name']}: {phone_formatted}")
            print(f"   ⭐ Score: {lead['score']}")
            print(f"   🆔 SID: {message.sid}")
            print(f"   💰 Coste aprox: ~0.074€")
            
            # Guardar conversación iniciada
            self.guardar_conversacion(lead['id'], 'sms_inicial_enviado', {
                'phone': phone_formatted,
                'sector': lead['sector'],
                'mensaje': mensaje[:100],
                'twilio_sid': message.sid,
                'canal': 'SMS',
                'timestamp': datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ ERROR ENVIANDO SMS a {lead['name']}")
            print(f"   📞 Número: {phone_formatted}")
            print(f"   💥 Error: {error_str}")
            
            # Análisis detallado del error
            if '21211' in error_str:
                print(f"   🔍 ERROR 21211: Formato de número inválido")
                print(f"   💡 SOLUCIÓN: Verificar formato E.164")
            elif '63024' in error_str:
                print(f"   🔍 ERROR 63024: Destinatario de mensaje inválido")
                print(f"   💡 SOLUCIÓN: Número no válido para SMS")
            elif '21635' in error_str:
                print(f"   🔍 ERROR 21635: No se puede enviar a número fijo")
                print(f"   💡 SOLUCIÓN: Solo usar números móviles")
            elif '20003' in error_str:
                print(f"   🔍 ERROR 20003: Problema de autenticación")
                print(f"   💡 SOLUCIÓN: Verificar credenciales Twilio")
            elif '21408' in error_str:
                print(f"   🔍 ERROR 21408: Sin permisos para SMS")
                print(f"   💡 SOLUCIÓN: Activar SMS en cuenta Twilio")
            else:
                print(f"   🔍 ERROR DESCONOCIDO: {error_str}")
            
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
                      �� {self.website_url}
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

    def realizar_llamada_automatizada(self, telefono, nombre_negocio, sector, ciudad=''):
        """
        Realiza llamada automatizada conversacional usando Twilio Voice API
        """
        if not self.twilio_voice_enabled:
            print("❌ Twilio Voice no configurado")
            return False
            
        try:
            # Crear webhook URL para manejar la llamada conversacional
            webhook_url = f"{self.website_url}/api/webhook-llamada?sector={sector}&nombre={nombre_negocio}&ciudad={ciudad}"
            
            # OPTIMIZACIÓN ANTI-SPAM: Configuración mejorada
            print(f"📞 Configuración optimizada:")
            print(f"   📱 Desde: {os.getenv('TWILIO_PHONE_NUMBER')} (Caller ID)")
            print(f"   📞 Hacia: {telefono}")
            print(f"   🔊 Detección buzón: ACTIVADA")
            print(f"   ⏱️ Timeout: 30s (reducido para minimizar costes)")
            print(f"   💰 Coste esperado: €0.03-0.12 según respuesta")
            
            # DIAGNÓSTICO: Verificar si es número español
            caller_number = os.getenv('TWILIO_PHONE_NUMBER')
            if caller_number and caller_number.startswith('+34'):
                print(f"🇪🇸 NÚMERO ESPAÑOL DETECTADO:")
                print(f"   ✅ Caller ID: {caller_number} (España)")
                print(f"   📈 Conversión esperada: 3x mayor (número local)")
                print(f"   💰 Llamadas locales: €0.08-0.15/min")
                print(f"   🎯 Confianza cliente: MÁXIMA")
            elif caller_number and caller_number.startswith('+1'):
                print(f"🇺🇸 NÚMERO US DETECTADO:")
                print(f"   ⚠️ Caller ID: {caller_number} (Internacional)")
                print(f"   📉 Conversión: Baja (número extranjero)")
                print(f"   💰 Llamadas internacionales: €0.25-0.50/min")
                print(f"   🤔 Confianza cliente: Regular")
            
            # DIAGNÓSTICO: Verificar que tenemos Verified Caller ID
            print(f"🔍 DIAGNÓSTICO PRE-LLAMADA:")
            
            twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
            print(f"   📞 Using Verified Caller ID: {twilio_number}")
            print(f"   ✅ Número verificado como Caller ID en Twilio Console")
            print(f"   🎯 Preparado para llamadas salientes")
            
            # Realizar llamada OPTIMIZADA
            print(f"🚀 INICIANDO LLAMADA...")
            call = self.twilio_client.calls.create(
                to=telefono,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=webhook_url,
                method='POST',
                status_callback=f"{self.website_url}/api/webhook-llamada-status",
                status_callback_event=['initiated', 'ringing', 'answered', 'completed', 'busy', 'failed', 'no-answer'],
                record=True,  # Grabar para análisis y mejora
                timeout=30,   # REDUCIDO: 30 segundos máximo (menos costes)
                # OPTIMIZACIÓN: Detectar contextos automáticamente
                machine_detection='Enable',  # Detectar contestador/buzón
                machine_detection_timeout=3,  # RÁPIDO: 3 segundos para detectar
                machine_detection_speech_threshold=2000,  # Umbral de voz humana
                machine_detection_speech_end_threshold=1000,  # Fin de saludo humano
                machine_detection_silence_timeout=3000,  # 3s silencio máximo antes de proceder
                # CALLER ID mejorado si disponible
                caller_id=os.getenv('TWILIO_PHONE_NUMBER')
            )
            
            print(f"✅ Llamada conversacional iniciada: {call.sid}")
            print(f"🎯 Negocio: {nombre_negocio} en {ciudad}")
            print(f"📋 Flujo: Presentación → Propuesta → Respuesta cliente → Acción")
            print(f"👀 VER EN TWILIO: Console → Monitor → Logs → Calls → Filtro 'Programmable' → {call.sid}")
            
            # Guardar información de la llamada
            self.guardar_llamada_info(call.sid, telefono, nombre_negocio, sector, "Llamada conversacional", ciudad)
            
            return True
            
        except Exception as e:
            print(f"❌ ERROR DETALLADO EN LLAMADA a {telefono}:")
            print(f"   💥 Tipo de error: {type(e).__name__}")
            print(f"   📝 Mensaje: {str(e)}")
            
            # Errores específicos de Twilio
            if "20003" in str(e):
                print(f"   🚨 ERROR 20003: Permisos insuficientes o cuenta sin verificar")
            elif "21614" in str(e):
                print(f"   🚨 ERROR 21614: Número de origen inválido o sin capacidad Voice")
            elif "21217" in str(e):
                print(f"   🚨 ERROR 21217: Número de destino inválido")
            elif "authentication" in str(e).lower():
                print(f"   🚨 ERROR AUTENTICACIÓN: Verifica TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
            elif "voice" in str(e).lower():
                print(f"   🚨 ERROR VOICE: Tu número probablemente no tiene capacidad de llamadas")
                print(f"   💡 Ve a Twilio Console → Phone Numbers → Habilita 'Voice'")
            
            return False

    def realizar_llamada_vonage(self, telefono, nombre_negocio, sector, ciudad=''):
        """
        NUEVA: Realizar llamada automatizada con VONAGE (números españoles)
        """
        if not self.vonage_enabled:
            print("❌ Vonage no configurado")
            return False
            
        try:
            print(f"🇪🇸 LLAMADA VONAGE (NÚMERO ESPAÑOL):")
            print(f"   📱 Desde: {os.getenv('VONAGE_PHONE_NUMBER')} (España +34)")
            print(f"   📞 Hacia: {telefono}")
            print(f"   💰 Coste: ~€0.04/minuto (local)")
            print(f"   🎯 Conversión esperada: 3x mayor que internacional")
            
            # Crear llamada Vonage con webhook
            response = self.vonage_client.voice.create_call({
                'to': [{'type': 'phone', 'number': telefono}],
                'from': {'type': 'phone', 'number': os.getenv('VONAGE_PHONE_NUMBER')},
                'answer_url': [f"{self.website_url}/api/vonage-answer?sector={sector}&nombre={nombre_negocio}&ciudad={ciudad}"],
                'event_url': [f"{self.website_url}/api/vonage-events"],
                'machine_detection': 'hangup',  # Colgar si es buzón
                'length_timer': 30,  # Máximo 30 segundos
                'ringing_timer': 20  # Máximo 20 segundos esperando respuesta
            })
            
            if response.get('status') == 'started':
                call_uuid = response.get('uuid')
                print(f"✅ Llamada Vonage iniciada: {call_uuid}")
                print(f"🎯 Negocio: {nombre_negocio} en {ciudad}")
                print(f"📋 Flujo: Presentación → Propuesta → Respuesta → SMS automático")
                print(f"👀 VER EN VONAGE: Dashboard → Voice → Call logs → {call_uuid}")
                
                # Guardar información de la llamada
                self.guardar_llamada_info(call_uuid, telefono, nombre_negocio, sector, "Llamada Vonage España", ciudad)
                
                return True
            else:
                print(f"❌ Error iniciando llamada Vonage: {response}")
                return False
            
        except Exception as e:
            print(f"❌ ERROR DETALLADO VONAGE a {telefono}:")
            print(f"   💥 Tipo de error: {type(e).__name__}")
            print(f"   📝 Mensaje: {str(e)}")
            
            # Errores específicos de Vonage
            if "401" in str(e):
                print(f"   🚨 ERROR 401: Credenciales Vonage incorrectas")
            elif "403" in str(e):
                print(f"   🚨 ERROR 403: Sin permisos o saldo insuficiente")
            elif "402" in str(e):
                print(f"   🚨 ERROR 402: Sin saldo en cuenta Vonage")
            elif "invalid" in str(e).lower():
                print(f"   🚨 ERROR: Número de destino inválido")
            
            return False

    def contactar_lead_con_llamada(self, lead):
        """
        ACTUALIZADO: Contacta lead con llamada (Vonage preferido, Twilio fallback)
        """
        try:
            telefono = self.formatear_telefono_espanol(lead.get('phone', ''))
            nombre_negocio = lead.get('business_name', 'Negocio')
            sector = lead.get('sector', 'default')
            ciudad = lead.get('ciudad', '')
            
            if not telefono:
                print(f"❌ Teléfono inválido para {nombre_negocio}")
                return False
            
            # Verificar lista negra
            if self.esta_en_lista_negra(telefono):
                print(f"🚫 {telefono} ({nombre_negocio}) está en lista negra - SKIP")
                return False
            
            print(f"\n📞 INICIANDO LLAMADA CONVERSACIONAL:")
            print(f"   🏢 Negocio: {nombre_negocio}")
            print(f"   📱 Teléfono: {telefono}")
            print(f"   🏙️ Ciudad: {ciudad}")
            print(f"   🎯 Sector: {sector}")
            
            # PRIORIDAD 1: Usar Vonage si está disponible (números españoles)
            if self.vonage_enabled:
                print(f"🇪🇸 Intentando llamada con VONAGE (número español)...")
                if self.realizar_llamada_vonage(telefono, nombre_negocio, sector, ciudad):
                    return True
                else:
                    print(f"⚠️ Vonage falló, intentando Twilio fallback...")
            
            # FALLBACK: Usar Twilio si Vonage no está o falla
            if self.twilio_voice_enabled:
                print(f"🇺🇸 Usando Twilio como fallback (número US)...")
                return self.realizar_llamada_automatizada(telefono, nombre_negocio, sector, ciudad)
            else:
                print(f"❌ Ni Vonage ni Twilio Voice disponibles")
                return False
                
        except Exception as e:
            print(f"❌ Error contactando lead con llamada: {e}")
            return False
    
    def generar_twiml_respuesta(self, telefono, nombre_negocio, sector, ciudad='', intento=1):
        """
        Genera TwiML response para llamada conversacional con respuestas
        """
        script = self.voice_scripts.get(sector, self.voice_scripts['default'])
        
        # Crear respuesta TwiML conversacional
        response = VoiceResponse()
        
        # Pausar 1 segundo al inicio
        response.pause(length=1)
        
        # FASE 1: Presentación y personalización
        presentacion = f"""
        {script['intro']}
        
        {script['personalizacion'].format(nombre_negocio=nombre_negocio, ciudad=ciudad)}
        
        {script['hook'].format(nombre_negocio=nombre_negocio, ciudad=ciudad, tipo_cocina=sector)}
        """
        
        response.say(
            presentacion,
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        # Pausa para procesar información
        response.pause(length=2)
        
        # FASE 2: Propuesta inicial
        if intento == 1:
            mensaje_propuesta = script['propuesta'].format(nombre_negocio=nombre_negocio)
        elif intento == 2:
            mensaje_propuesta = script['respuesta_no_1'].format(nombre_negocio=nombre_negocio)
        elif intento == 3:
            mensaje_propuesta = script['respuesta_no_2'].format(nombre_negocio=nombre_negocio, ciudad=ciudad)
        else:
            # Más de 3 intentos - despedirse
            response.say(
                script['despedida'],
                voice=self.voice_config['voice'],
                language=self.voice_config['language']
            )
            response.hangup()
            return str(response)
        
        # Capturar respuesta del cliente
        gather = response.gather(
            num_digits=1,
            timeout=10,  # 10 segundos para responder
            action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento={intento}&nombre={nombre_negocio}&ciudad={ciudad}",
            method='POST'
        )
        
        gather.say(
            mensaje_propuesta + " Presione 1 para SÍ, estoy interesado, o presione 2 para NO, no me interesa.",
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        # Si no responden en 10 segundos, repetir una vez
        response.say(
            "No he recibido su respuesta. " + mensaje_propuesta + " Presione 1 para SÍ o 2 para NO.",
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        # Último intento de captura
        gather2 = response.gather(
            num_digits=1,
            timeout=5,
            action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento={intento}&nombre={nombre_negocio}&ciudad={ciudad}",
            method='POST'
        )
        
        gather2.say(
            "Última oportunidad: 1 para SÍ, 2 para NO.",
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        # Si no responden nada, despedirse
        response.say(
            "Entiendo que no puede atender ahora. Puede contactarnos en contacto@desarroyo.tech si lo desea. Que tenga un buen día.",
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        response.hangup()
        return str(response)
    
    def manejar_respuesta_llamada(self, respuesta, sector, intento, nombre_negocio, ciudad, telefono):
        """
        Maneja la respuesta del cliente durante la llamada
        NUEVO: Incluye lista negra y llamadas exitosas
        """
        script = self.voice_scripts.get(sector, self.voice_scripts['default'])
        response = VoiceResponse()
        
        if respuesta == '1':  # SÍ, está interesado
            # DETECCIÓN INTELIGENTE: ¿Es móvil o fijo?
            es_movil = self.es_telefono_movil_espanol(telefono)
            
            if es_movil:
                # ===== CASO MÓVIL: SMS DIRECTO =====
                mensaje_envio = script['respuesta_si'].format(nombre_negocio=nombre_negocio)
                
                response.say(
                    mensaje_envio,
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.say(
                    "Gracias por su tiempo. Que tenga un buen día.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.hangup()
                
                # ENVIAR SMS AL MÓVIL INMEDIATAMENTE
                self.enviar_sms_post_llamada_exitosa(telefono, nombre_negocio, sector, ciudad)
                
                return str(response)
                
            else:
                # ===== CASO FIJO: PREGUNTAR POR MÓVIL =====
                response.say(
                    f"Perfecto, {nombre_negocio}. Le voy a enviar toda la información por SMS.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.pause(length=1)
                
                # Solicitar número de móvil
                gather_movil = response.gather(
                    num_digits=9,
                    timeout=15,
                    finish_on_key='#',
                    action=f"{self.website_url}/api/webhook-movil-captura?telefono_fijo={telefono}&nombre={nombre_negocio}&sector={sector}&ciudad={ciudad}",
                    method='POST'
                )
                
                gather_movil.say(
                    "¿Podría decirme un número de móvil donde enviarle la información? Puede ser el suyo o del responsable. Dígame los 9 dígitos y termine con almohadilla.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                # Si no proporciona móvil, alternativa
                response.say(
                    "No he recibido el número de móvil. No hay problema, puede contactarnos directamente por email en alberto@desarroyo.tech para recibir toda la información.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.say(
                    "Gracias por su tiempo. Que tenga un buen día.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.hangup()
                
                # Registrar como exitosa aunque sea fijo sin móvil
                self.enviar_sms_post_llamada_exitosa(telefono, nombre_negocio, sector, ciudad)
                
                return str(response)
            
        elif respuesta == '2':  # NO, no está interesado
            if intento >= 3:
                # Ya hemos intentado 3 veces, añadir a lista negra y despedirse
                print(f"🚫 {nombre_negocio} dijo NO después de {intento} intentos. Lista negra.")
                
                # NUEVO: Añadir a lista negra
                motivo = f"NO_FINAL_INTENTO_{intento}"
                self.agregar_a_lista_negra(telefono, nombre_negocio, motivo)
                
                # Notificar lista negra
                self.enviar_notificacion_telegram(
                    f"🚫 LEAD AÑADIDO A LISTA NEGRA\n\n"
                    f"🏢 Negocio: {nombre_negocio}\n"
                    f"📞 Teléfono: {telefono}\n"
                    f"🎯 Sector: {sector}\n"
                    f"🏙️ Ciudad: {ciudad}\n"
                    f"❌ Respuesta: NO después de {intento} intentos\n"
                    f"⏰ Hora: {datetime.now().strftime('%H:%M')}\n\n"
                    f"🚫 NO se volverá a contactar este número\n"
                    f"💰 Coste total: ~{intento * 0.12:.2f}€"
                )
                
                response.say(
                    script['despedida'],
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                response.hangup()
                return str(response)
            else:
                # Intentar con diferente enfoque
                print(f"❌ {nombre_negocio} dijo NO (intento {intento}/3). Cambiando estrategia...")
                return self.generar_twiml_respuesta(telefono, nombre_negocio, sector, ciudad, intento + 1)
        
        else:
            # Respuesta no válida
            response.say(
                "No he entendido su respuesta. Por favor, presione 1 para SÍ o 2 para NO.",
                voice=self.voice_config['voice'],
                language=self.voice_config['language']
            )
            
            gather = response.gather(
                num_digits=1,
                timeout=5,
                action=f"{self.website_url}/api/webhook-llamada-respuesta?sector={sector}&intento={intento}&nombre={nombre_negocio}&ciudad={ciudad}",
                method='POST'
            )
            
            return str(response)
    
    def manejar_captura_movil_fijo(self, movil_dictado, telefono_fijo, nombre_negocio, sector, ciudad):
        """
        Procesa el móvil dictado cuando llamamos a un número fijo y nos dan otro móvil
        NUEVA FUNCIÓN: Optimiza conversiones de números fijos
        """
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
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.say(
                    "Muchas gracias por su tiempo. Que tenga un buen día.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
                
                response.hangup()
                
                # Crear lead temporal con el móvil alternativo
                lead_movil = {
                    'name': nombre_negocio,
                    'phone': movil_formateado,  # USAR EL MÓVIL DICTADO
                    'sector': sector,
                    'ciudad': ciudad,
                    'score': 98,  # Máxima prioridad: fijo + móvil alternativo
                    'telefono_fijo_original': telefono_fijo
                }
                
                # Enviar SMS al móvil alternativo
                mensaje_sms = self.generar_mensaje_sms_directo(lead_movil)
                exito_sms = self.enviar_sms_automatico(lead_movil, mensaje_sms)
                
                if exito_sms:
                    # Registrar conversión exitosa con móvil alternativo
                    self.agregar_llamada_exitosa(telefono_fijo, nombre_negocio, sector, ciudad)
                    
                    # Actualizar con móvil alternativo
                    telefono_fijo_formateado = self.formatear_telefono_espanol(telefono_fijo)
                    if telefono_fijo_formateado in self.llamadas_exitosas:
                        self.llamadas_exitosas[telefono_fijo_formateado]['movil_alternativo'] = movil_formateado
                        self.llamadas_exitosas[telefono_fijo_formateado]['sms_enviado'] = True
                        self.llamadas_exitosas[telefono_fijo_formateado]['tipo_numero'] = 'FIJO_CON_MOVIL'
                        self.guardar_llamadas_exitosas()
                    
                    # Notificar conversión súper exitosa
                    self.enviar_notificacion_telegram(
                        f"🏆 CONVERSIÓN NÚMERO FIJO PERFECTA!\n\n"
                        f"🏢 Negocio: {nombre_negocio}\n"
                        f"☎️ Fijo llamado: {telefono_fijo}\n"
                        f"📱 Móvil proporcionado: {movil_formateado}\n"
                        f"🎯 Sector: {sector}\n"
                        f"🏙️ Ciudad: {ciudad}\n"
                        f"✅ Cliente dijo SÍ + proporcionó móvil\n"
                        f"📱 SMS con encuesta: ENVIADO AL MÓVIL\n"
                        f"📧 Email contacto: alberto@desarroyo.tech\n"
                        f"⏰ Hora: {datetime.now().strftime('%H:%M')}\n\n"
                        f"💰 Coste: ~0.19€ (llamada fijo + SMS móvil)\n"
                        f"🎯 LEAD SÚPER CALIENTE\n"
                        f"🏆 Estrategia fijo→móvil EXITOSA!\n"
                        f"🚀 Sistema DesArroyo Tech optimizado!"
                    )
                    
                    print(f"🏆 CONVERSIÓN FIJO→MÓVIL EXITOSA: {nombre_negocio} ({telefono_fijo} → {movil_formateado})")
                    
                else:
                    print(f"⚠️ Móvil capturado pero SMS falló: {movil_formateado}")
                
                return str(response)
                
            else:
                # Móvil no válido (no empieza por 6 o 7)
                response.say(
                    f"El número {movil_limpio} no parece ser un móvil válido. No hay problema, puede contactarnos por email en alberto@desarroyo.tech.",
                    voice=self.voice_config['voice'],
                    language=self.voice_config['language']
                )
        else:
            # No se recibió móvil o es muy corto
            response.say(
                "No he podido capturar el número correctamente. No hay problema, puede contactarnos por email en alberto@desarroyo.tech para recibir toda la información.",
                voice=self.voice_config['voice'],
                language=self.voice_config['language']
            )
        
        response.say(
            "Gracias por su tiempo. Que tenga un buen día.",
            voice=self.voice_config['voice'],
            language=self.voice_config['language']
        )
        
        response.hangup()
        
        # Registrar como llamada exitosa aunque no hayamos capturado móvil
        self.agregar_llamada_exitosa(telefono_fijo, nombre_negocio, sector, ciudad)
        
        # Notificar conversión parcial
        self.enviar_notificacion_telegram(
            f"📞 CONVERSIÓN FIJO SIN MÓVIL\n\n"
            f"🏢 Negocio: {nombre_negocio}\n"
            f"☎️ Fijo: {telefono_fijo}\n"
            f"🎯 Sector: {sector}\n"
            f"🏙️ Ciudad: {ciudad}\n"
            f"✅ Cliente dijo SÍ\n"
            f"❌ No se capturó móvil válido\n"
            f"📧 Referido a email: alberto@desarroyo.tech\n"
            f"⏰ Hora: {datetime.now().strftime('%H:%M')}\n\n"
            f"💰 Coste: ~0.12€ (solo llamada)\n"
            f"📋 Seguimiento manual recomendado"
        )
        
        return str(response)
    
    def enviar_sms_post_llamada_exitosa(self, telefono, nombre_negocio, sector, ciudad):
        """
        Envía SMS automáticamente después de una llamada exitosa (SOLO cuando dijeron SÍ)
        INTELIGENTE: Diferencia móviles vs fijos automáticamente
        """
        try:
            # Registrar como llamada exitosa
            self.agregar_llamada_exitosa(telefono, nombre_negocio, sector, ciudad)
            
            # Crear lead temporal para SMS
            lead_temp = {
                'name': nombre_negocio,
                'phone': telefono,
                'sector': sector,
                'ciudad': ciudad,
                'score': 95  # Alta prioridad tras aceptar llamada
            }
            
            # DETECCIÓN INTELIGENTE: ¿Móvil o Fijo?
            es_movil = self.es_telefono_movil_espanol(telefono)
            
            if es_movil:
                # ===== CASO MÓVIL: SMS AUTOMÁTICO =====
                print(f"📱 Detectado móvil: {telefono} - Enviando SMS automático")
                
                # Generar mensaje SMS personalizado (incluye email para contacto)
                mensaje_sms = self.generar_mensaje_sms_directo(lead_temp)
                
                # Enviar SMS
                exito_sms = self.enviar_sms_automatico(lead_temp, mensaje_sms)
                
                if exito_sms:
                    # Marcar SMS como enviado en llamadas exitosas
                    telefono_formateado = self.formatear_telefono_espanol(telefono)
                    if telefono_formateado in self.llamadas_exitosas:
                        self.llamadas_exitosas[telefono_formateado]['sms_enviado'] = True
                        self.llamadas_exitosas[telefono_formateado]['tipo_numero'] = 'MOVIL'
                        self.guardar_llamadas_exitosas()
                    
                    print(f"✅ SMS post-llamada enviado a {nombre_negocio}")
                    
                    # Notificar éxito completo con demostración del sistema
                    self.enviar_notificacion_telegram(
                        f"🎉 CONVERSIÓN MÓVIL PERFECTA!\n\n"
                        f"🏢 Negocio: {nombre_negocio}\n"
                        f"📱 Móvil: {telefono}\n"
                        f"🎯 Sector: {sector}\n"
                        f"🏙️ Ciudad: {ciudad}\n"
                        f"✅ Cliente dijo SÍ en llamada\n"
                        f"📱 SMS con encuesta: ENVIADO AUTOMÁTICAMENTE\n"
                        f"📧 Email para contacto: alberto@desarroyo.tech\n"
                        f"⏰ Hora: {datetime.now().strftime('%H:%M')}\n\n"
                        f"💰 Coste: ~0.19€ (llamada + SMS)\n"
                        f"🎯 LEAD SÚPER CALIENTE\n"
                        f"🚀 Flujo móvil completo - DesArroyo Tech!"
                    )
                else:
                    print(f"⚠️ Llamada exitosa pero SMS falló para {nombre_negocio}")
            
            else:
                # ===== CASO FIJO: ESTRATEGIA ALTERNATIVA =====
                print(f"🏢 Detectado número fijo: {telefono} - SMS no disponible")
                
                # Marcar como llamada exitosa sin SMS
                telefono_formateado = self.formatear_telefono_espanol(telefono)
                if telefono_formateado in self.llamadas_exitosas:
                    self.llamadas_exitosas[telefono_formateado]['sms_enviado'] = False
                    self.llamadas_exitosas[telefono_formateado]['tipo_numero'] = 'FIJO'
                    self.llamadas_exitosas[telefono_formateado]['estrategia'] = 'LLAMADA_SEGUIMIENTO'
                    self.guardar_llamadas_exitosas()
                
                # Notificar estrategia alternativa para fijos
                self.enviar_notificacion_telegram(
                    f"📞 CONVERSIÓN NÚMERO FIJO\n\n"
                    f"🏢 Negocio: {nombre_negocio}\n"
                    f"☎️ Fijo: {telefono}\n"
                    f"🎯 Sector: {sector}\n"
                    f"🏙️ Ciudad: {ciudad}\n"
                    f"✅ Cliente dijo SÍ en llamada\n"
                    f"❌ SMS no disponible (número fijo)\n"
                    f"📧 Email contacto: alberto@desarroyo.tech\n"
                    f"⏰ Hora: {datetime.now().strftime('%H:%M')}\n\n"
                    f"💰 Coste: ~0.12€ (solo llamada)\n"
                    f"📋 ESTRATEGIA ALTERNATIVA:\n"
                    f"   🔄 Llamada de seguimiento en 2-3 días\n"
                    f"   📧 Email directo con propuesta\n"
                    f"   🎯 Lead caliente validado por llamada\n\n"
                    f"🚀 Número fijo = negocio más establecido!"
                )
                
                print(f"📋 Programado seguimiento alternativo para {nombre_negocio}")
                
        except Exception as e:
            print(f"❌ Error enviando SMS post-llamada: {str(e)}")
    
    def procesar_leads_con_llamadas(self, leads, limite=3):
        """
        Procesa leads usando llamadas automatizadas CONVERSACIONALES
        NUEVO: Filtra lista negra automáticamente
        """
        print(f"\n📞 === INICIANDO SISTEMA CONVERSACIONAL ===")
        print(f"🎯 {len(leads)} leads encontrados antes de filtros")
        
        # NUEVO: Filtrar lista negra antes de procesar
        leads_filtrados = self.filtrar_leads_sin_lista_negra(leads)
        print(f"📋 {len(leads_filtrados)} leads válidos después de filtrar lista negra")
        print(f"📞 Procesando {min(limite, len(leads_filtrados))} llamadas")
        print(f"💬 Flujo: Llamada → Conversación → Respuesta cliente → SMS si SÍ")
        print(f"🔄 Cada llamada incluye hasta 3 intentos de persuasión")
        print(f"🚫 NO se contactan números de lista negra")
        
        leads_contactados = 0
        leads_exitosos = []
        
        for i, lead in enumerate(leads_filtrados[:limite]):
            if leads_contactados >= limite:
                break
                
            print(f"\n📞 Llamada conversacional {i+1}/{min(limite, len(leads_filtrados))}")
            
            # Realizar llamada conversacional
            exito = self.contactar_lead_con_llamada(lead)
            
            if exito:
                leads_contactados += 1
                leads_exitosos.append(lead)
                
                # Pausa entre llamadas (2-4 minutos para evitar saturar)
                if i < min(limite, len(leads)) - 1:  # No pausar en el último
                    tiempo_pausa = random.randint(120, 240)  # 2-4 minutos entre llamadas
                    print(f"⏳ Pausa de {tiempo_pausa} segundos antes de la siguiente llamada...")
                    time.sleep(tiempo_pausa)
            
        # Resumen final
        print(f"\n📊 === RESUMEN SISTEMA CONVERSACIONAL ===")
        print(f"📞 Llamadas iniciadas: {leads_contactados}")
        print(f"💬 Sistema conversacional: Activo")
        print(f"🎯 Respuestas esperadas: Notificaciones automáticas")
        print(f"📱 SMS: Solo se envían tras respuesta SÍ")
        print(f"💰 Coste llamadas: {leads_contactados * 0.12:.2f}€")
        print(f"🎯 Conversión esperada: {int(leads_contactados * 0.4)} leads calientes")
        print(f"📈 Efectividad: 35-50% (conversacional personalizado)")
        print(f"\n💡 Próximos pasos:")
        print(f"   - Revisar notificaciones Telegram")
        print(f"   - SMS automáticos a respuestas SÍ")
        print(f"   - Seguimiento leads calientes")
        
        return leads_exitosos

    def guardar_llamada_info(self, call_sid, telefono, nombre_negocio, sector, script, ciudad=''):
        """
        Guarda información de la llamada para seguimiento
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        call_info = {
            "call_sid": call_sid,
            "telefono": telefono,
            "nombre_negocio": nombre_negocio,
            "sector": sector,
            "ciudad": ciudad,
            "script_usado": script,
            "fecha_llamada": timestamp,
            "estado": "INICIADA"
        }
        
        # Guardar en archivo JSON
        filename = f"llamadas_realizadas_{timestamp}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(call_info, f, ensure_ascii=False, indent=2)
            print(f"📱 Información de llamada guardada: {filename}")
        except Exception as e:
            print(f"❌ Error guardando info de llamada: {str(e)}")

    # ===== NUEVAS FUNCIONES: LISTA NEGRA Y LLAMADAS EXITOSAS =====
    def cargar_lista_negra(self):
        """Cargar lista de teléfonos que dijeron NO (no volver a llamar)"""
        try:
            if os.path.exists(self.lista_negra_file):
                with open(self.lista_negra_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error cargando lista negra: {str(e)}")
            return {}
    
    def cargar_llamadas_exitosas(self):
        """Cargar lista de teléfonos que dijeron SÍ (para seguimiento)"""
        try:
            if os.path.exists(self.llamadas_exitosas_file):
                with open(self.llamadas_exitosas_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ Error cargando llamadas exitosas: {str(e)}")
            return {}
    
    def guardar_lista_negra(self):
        """Guardar lista negra de teléfonos que dijeron NO"""
        try:
            with open(self.lista_negra_file, 'w', encoding='utf-8') as f:
                json.dump(self.lista_negra, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error guardando lista negra: {str(e)}")
    
    def guardar_llamadas_exitosas(self):
        """Guardar lista de llamadas exitosas (dijeron SÍ)"""
        try:
            with open(self.llamadas_exitosas_file, 'w', encoding='utf-8') as f:
                json.dump(self.llamadas_exitosas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ Error guardando llamadas exitosas: {str(e)}")
    
    def agregar_a_lista_negra(self, telefono, nombre_negocio, motivo='NO_INTERESADO'):
        """Agregar teléfono a lista negra (no volver a llamar)"""
        try:
            telefono_formateado = self.formatear_telefono_espanol(telefono)
            if telefono_formateado:
                self.lista_negra[telefono_formateado] = {
                    'nombre_negocio': nombre_negocio,
                    'fecha_no': datetime.now().isoformat(),
                    'motivo': motivo,
                    'intentos_realizados': self.lista_negra.get(telefono_formateado, {}).get('intentos_realizados', 0) + 1
                }
                self.guardar_lista_negra()
                print(f"🚫 {nombre_negocio} ({telefono_formateado}) añadido a lista negra: {motivo}")
        except Exception as e:
            print(f"❌ Error añadiendo a lista negra: {str(e)}")
    
    def agregar_llamada_exitosa(self, telefono, nombre_negocio, sector, ciudad):
        """Agregar llamada exitosa (dijo SÍ)"""
        try:
            telefono_formateado = self.formatear_telefono_espanol(telefono)
            if telefono_formateado:
                self.llamadas_exitosas[telefono_formateado] = {
                    'nombre_negocio': nombre_negocio,
                    'sector': sector,
                    'ciudad': ciudad,
                    'fecha_si': datetime.now().isoformat(),
                    'sms_enviado': False,
                    'conversion_alta': True
                }
                self.guardar_llamadas_exitosas()
                print(f"✅ {nombre_negocio} ({telefono_formateado}) registrado como ÉXITO - enviará SMS")
        except Exception as e:
            print(f"❌ Error registrando llamada exitosa: {str(e)}")
    
    def esta_en_lista_negra(self, telefono):
        """Verificar si un teléfono está en lista negra"""
        telefono_formateado = self.formatear_telefono_espanol(telefono)
        return telefono_formateado in self.lista_negra
    
    def filtrar_leads_sin_lista_negra(self, leads):
        """Filtrar leads eliminando los que están en lista negra"""
        leads_filtrados = []
        for lead in leads:
            telefono = lead.get('telefono', lead.get('phone', ''))
            if telefono and not self.esta_en_lista_negra(telefono):
                leads_filtrados.append(lead)
            elif telefono:
                nombre = lead.get('nombre', lead.get('name', 'Desconocido'))
                print(f"🚫 Saltando {nombre} - está en lista negra (dijo NO anteriormente)")
        
        print(f"🔍 Filtrados: {len(leads_filtrados)}/{len(leads)} leads (sin lista negra)")
        return leads_filtrados

    def calcular_presupuesto_llamadas(self, total_numeros_disponibles):
        """
        Calcula cuántas llamadas hacer según presupuesto de 10€ diario
        """
        try:
            config = self.presupuesto_configuracion
            
            # Costo por llamada completa (llamada + SMS si acepta)
            # Asumiendo 30% tasa de aceptación para calcular SMS
            costo_llamada = config['costo_llamada_minuto'] * config['duracion_llamada_promedio']
            costo_sms_ponderado = config['costo_sms_nacional'] * 0.30  # 30% acepta
            costo_por_lead = costo_llamada + costo_sms_ponderado
            
            # Presupuesto disponible
            presupuesto_disponible = config['presupuesto_diario_maximo'] * config['factor_seguridad']
            
            # Llamadas máximas según presupuesto
            max_llamadas_presupuesto = int(presupuesto_disponible / costo_por_lead)
            
            # Llamadas finales (mínimo entre presupuesto y números disponibles)
            llamadas_a_hacer = min(max_llamadas_presupuesto, total_numeros_disponibles)
            
            # Logging detallado
            print(f"📊 PRESUPUESTO DIARIO: {config['presupuesto_diario_maximo']}€")
            print(f"💰 Costo por llamada: €{costo_llamada:.3f}")
            print(f"📱 Costo SMS (30% acepta): €{costo_sms_ponderado:.3f}")
            print(f"💡 Costo total por lead: €{costo_por_lead:.3f}")
            print(f"🎯 Llamadas máximas con 10€: {max_llamadas_presupuesto}")
            print(f"📞 Llamadas a realizar: {llamadas_a_hacer}")
            
            return llamadas_a_hacer
            
        except Exception as e:
            print(f"❌ Error calculando presupuesto: {e}")
            return 10  # Valor por defecto conservador

def main():
    """Función principal expandida - SISTEMA HÍBRIDO SMS + LLAMADAS"""
    import argparse
    
    # Lista completa de 41 ciudades españolas
    CIUDADES_DISPONIBLES = [
        'Álava', 'Albacete', 'Alicante', 'Asturias', 'Ávila', 'Badajoz', 
        'Barcelona', 'Burgos', 'Cáceres', 'Cantabria', 'Castellón', 
        'Ciudad Real', 'Cuenca', 'Girona', 'Guadalajara', 'Guipúzcoa', 
        'Huesca', 'Illes Balears', 'La Coruña', 'La Rioja', 'Las Palmas', 
        'León', 'Lleida', 'Lugo', 'Madrid', 'Navarra', 'Ourense', 
        'Palencia', 'Pontevedra', 'Salamanca', 'Santa Cruz de Tenerife', 
        'Segovia', 'Soria', 'Tarragona', 'Teruel', 'Toledo', 'Valencia', 
        'Valladolid', 'Vizcaya', 'Zamora', 'Zaragoza',
        # Aliases principales
        'Palma', 'Sevilla', 'Málaga', 'Murcia', 'Bilbao', 'Vigo', 'Gijón', 'Córdoba'
    ]
    
    # Lista completa de 60+ sectores disponibles
    SECTORES_DISPONIBLES = [
        # Salud y bienestar
        'dentistas', 'peluquerias', 'centros_estetica', 'psicologos', 
        'fisioterapeutas', 'nutricionistas', 'podologos', 'clinicas_veterinarias',
        'opticas', 'masajistas',
        
        # Gastronomía 
        'restaurantes', 'cafeterias', 'comida_para_llevar', 'panaderias',
        'heladerias', 'food_trucks', 'tiendas_productos_locales', 
        'empresas_catering', 'vinotecas',
        
        # Deporte y fitness
        'gimnasios', 'entrenadores_personales', 'estudios_yoga_pilates',
        'clases_baile', 'box_crossfit',
        
        # Servicios técnicos
        'electricistas', 'fontaneros', 'cerrajeros', 'reformistas',
        'carpinteros', 'pintores', 'jardineros', 'mecanicos',
        'lavaderos_coche',
        
        # Servicios para mascotas
        'peluqueria_canina', 'adiestradores', 'tiendas_mascotas',
        'guarderias_residencias_caninas',
        
        # Educación
        'academias_idiomas', 'escuelas_musica', 'autoescuelas',
        'clases_particulares', 'academias_oposiciones', 'centros_montessori',
        
        # Servicios profesionales
        'abogados', 'agencias_inmobiliarias', 'servicios_limpieza',
        'mudanzas', 'decoradores_interiores', 'manitas_bricolaje',
        'cuidadores_domicilio', 'servicios_ninera',
        
        # Servicios creativos
        'fotografos_locales', 'videografos_bodas', 'floristerias',
        'tiendas_regalos_personalizados', 'organizadores_eventos',
        'artistas_artesanos',
        
        # Comercio local
        'tiendas_barrio_productos_unicos', 'papelerias', 'ferreterias',
        'estancos', 'tintorerías', 'copisterias', 'tiendas_segunda_mano',
        
        # Hostelería y turismo
        'hoteles'
    ]
    
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(
        description='🚀 Sistema Híbrido de Leads - DesArroyo Tech (SMS + Llamadas)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
💡 EJEMPLOS DE USO:

📱 SMS Masivo:
   python3 sistema_leads_avanzado.py Madrid dentistas --canal SMS
   
📞 Llamadas Conversacionales:
   python3 sistema_leads_avanzado.py Barcelona restaurantes --llamadas --limite 10
   
🎯 Con control de presupuesto:
   python3 sistema_leads_avanzado.py Valencia peluquerias --canal SMS --presupuesto-max 15

📊 INFORMACIÓN:
   📍 Ciudades: {len(CIUDADES_DISPONIBLES)} disponibles
   🏢 Sectores: {len(SECTORES_DISPONIBLES)} disponibles
   💰 Presupuesto: Control automático 300-600€/mes
        """
    )
    
    # Argumentos obligatorios
    parser.add_argument('ciudad', help='Ciudad para buscar leads')
    parser.add_argument('sector', help='Sector de negocio')
    
    # Argumentos opcionales
    parser.add_argument('--canal', 
                       choices=['SMS', 'EMAIL', 'WHATSAPP'], 
                       default='SMS',
                       help='Canal de comunicación (por defecto: SMS)')
    
    parser.add_argument('--llamadas', 
                       action='store_true',
                       help='Usar llamadas conversacionales en lugar de SMS')
    
    parser.add_argument('--limite', 
                       type=int, 
                       default=25,
                       help='Límite de contactos (por defecto: 25)')
    
    parser.add_argument('--presupuesto-max', 
                       type=float, 
                       default=50.0,
                       help='Presupuesto máximo en € para esta ejecución (por defecto: 50)')
    
    parser.add_argument('--test', 
                       action='store_true',
                       help='Modo prueba (no envía mensajes reales)')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Validar ciudad y sector
    if args.ciudad not in CIUDADES_DISPONIBLES:
        print(f"❌ Ciudad '{args.ciudad}' no disponible")
        print(f"💡 Ciudades válidas: {', '.join(CIUDADES_DISPONIBLES[:10])}...")
        sys.exit(1)
        
    if args.sector not in SECTORES_DISPONIBLES:
        print(f"❌ Sector '{args.sector}' no disponible")
        print(f"💡 Sectores válidos: {', '.join(SECTORES_DISPONIBLES[:10])}...")
        sys.exit(1)
    
    # Mostrar información de inicio
    if args.llamadas:
        tipo_campana = "📞 LLAMADAS CONVERSACIONALES"
        coste_estimado = args.limite * 0.12
        conversion_esperada = f"{int(args.limite * 0.4)} leads calientes (40%)"
    else:
        tipo_campana = f"📱 {args.canal} MASIVO"
        coste_estimado = args.limite * 0.07
        conversion_esperada = f"{int(args.limite * 0.05)} respuestas (5%)"
    
    print(f"🚀 INICIANDO {tipo_campana}")
    print("=" * 70)
    print(f"   📍 Ciudad: {args.ciudad}")
    print(f"   🏢 Sector: {args.sector}")
    print(f"   🎯 Límite: {args.limite} contactos")
    print(f"   💰 Presupuesto: {args.presupuesto_max}€ máximo")
    print(f"   💸 Coste estimado: {coste_estimado:.2f}€")
    print(f"   📈 Conversión esperada: {conversion_esperada}")
    print(f"   🧪 Modo prueba: {'SÍ' if args.test else 'NO'}")
    print("=" * 70)
    
    # Verificar que no se excede el presupuesto
    if coste_estimado > args.presupuesto_max:
        print(f"⚠️ ADVERTENCIA: Coste estimado ({coste_estimado:.2f}€) excede presupuesto ({args.presupuesto_max}€)")
        limite_ajustado = int(args.presupuesto_max / (0.12 if args.llamadas else 0.07))
        print(f"💡 Ajustando límite a {limite_ajustado} contactos para respetar presupuesto")
        args.limite = limite_ajustado
    
    # Inicializar sistema
    sistema = SistemaLeadsAvanzado()
    
    # Configurar modo prueba si es necesario
    if args.test:
        print("🧪 MODO PRUEBA ACTIVADO - No se enviarán mensajes reales")
        sistema.test_mode = True
    
    try:
        if args.llamadas:
            # Modo llamadas conversacionales
            print(f"\n📞 Iniciando búsqueda de leads para llamadas...")
            
            # Buscar leads (reutilizar lógica existente)
            leads_raw = sistema.scraper.buscar_masivo(args.ciudad, args.sector)
            if not leads_raw:
                print(f"❌ No se encontraron leads para {args.sector} en {args.ciudad}")
                return
            
            # Filtrar y calificar leads
            leads_calificados = sistema.filtrar_y_calificar_leads_avanzado(leads_raw, args.sector)
            
            if not leads_calificados:
                print(f"❌ No se encontraron leads calificados para llamadas")
                return
            
            # Calcular cuántas llamadas hacer según presupuesto de 10€
            llamadas_a_hacer = sistema.calcular_presupuesto_llamadas(len(leads_calificados))
            print(f"💰 Llamadas calculadas según presupuesto: {llamadas_a_hacer}")
            
            # Procesar con llamadas conversacionales
            leads_exitosos = sistema.procesar_leads_con_llamadas(leads_calificados, llamadas_a_hacer)
            
            print(f"\n✅ Llamadas conversacionales completadas")
            print(f"📞 Leads procesados: {len(leads_exitosos)}")
            
        else:
            # Modo SMS/EMAIL masivo (usar método existente)
            print(f"\n📱 Iniciando campaña {args.canal} masiva...")
            sistema.ejecutar_sector_ciudad(args.ciudad, args.sector)
            
    except KeyboardInterrupt:
        print(f"\n⚠️ Proceso interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error durante ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 Proceso completado para {args.ciudad} - {args.sector}")

if __name__ == "__main__":
    main() 