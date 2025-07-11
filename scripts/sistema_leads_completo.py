#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA COMPLETO DE LEADS - DESARROYO TECH
Reemplaza n8n por un script Python que hace todo el flujo completo
"""

import os
import sys
import json
import time
import random
from datetime import datetime
import requests
from twilio.rest import Client
import telegram
from scraper_gratis import ScraperGratis

class SistemaLeadsCompleto:
    def __init__(self):
        # Configuración desde variables de entorno
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat = os.getenv('TELEGRAM_CHAT_ID')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.agent_intro = "un agente comercial de DesArroyo Tech"
        
        # Inicializar clientes
        if self.twilio_sid and self.twilio_token:
            self.twilio_client = Client(self.twilio_sid, self.twilio_token)
        
        if self.telegram_token:
            self.telegram_bot = telegram.Bot(token=self.telegram_token)
        
        self.scraper = ScraperGratis()
        
        # Archivo para evitar duplicados
        self.leads_enviados_file = 'leads_enviados.json'
        self.leads_enviados = self.cargar_leads_enviados()
    
    def cargar_leads_enviados(self):
        """Carga la lista de leads ya contactados para evitar duplicados"""
        try:
            if os.path.exists(self.leads_enviados_file):
                with open(self.leads_enviados_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
    
    def guardar_lead_enviado(self, lead_id):
        """Guarda un lead como ya contactado"""
        self.leads_enviados.add(lead_id)
        try:
            with open(self.leads_enviados_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.leads_enviados), f)
        except:
            pass
    
    def filtrar_y_calificar_leads(self, leads_raw):
        """Filtra y califica leads igual que en n8n"""
        leads_calificados = []
        
        for business in leads_raw:
            # Verificar si tiene datos básicos
            if not business.get('name') or not business.get('phone'):
                continue
            
            # Crear ID único para evitar duplicados
            lead_id = f"{business['name'].lower().strip()}_{business['phone']}"
            if lead_id in self.leads_enviados:
                print(f"⏭️  Lead ya contactado: {business['name']}")
                continue
            
            # Filtrar por sectores con potencial
            high_value_sectors = [
                'restaurante', 'café', 'bar', 'pizzería', 'comida',
                'peluquería', 'barbería', 'estética', 'belleza',
                'dentista', 'médico', 'fisioterapeuta', 'clínica',
                'abogado', 'notario', 'asesor', 'consultor',
                'tienda', 'comercio', 'negocio', 'empresa',
                'hotel', 'hostal', 'alojamiento',
                'gimnasio', 'fitness', 'deporte',
                'autoescuela', 'taller', 'mecánico'
            ]
            
            sector_match = any(sector in business['name'].lower() 
                             for sector in high_value_sectors)
            
            if not sector_match:
                continue
            
            # Limpiar y formatear datos
            clean_lead = {
                'id': lead_id,
                'name': business['name'].strip(),
                'phone': business['phone'].replace(' ', '').replace('-', '').replace('+34', ''),
                'address': business.get('address', ''),
                'website': business.get('website', ''),
                'industry': business.get('source', ''),
                'source': business.get('source', 'unknown'),
                'score': 0,
                'status': 'new',
                'timestamp': datetime.now().isoformat()
            }
            
            # Calcular score inicial
            if not clean_lead['website'] or clean_lead['website'] == '':
                clean_lead['score'] += 30  # Sin web = alta prioridad
            
            if clean_lead['phone'] and len(clean_lead['phone']) >= 9:
                clean_lead['score'] += 20  # Tiene teléfono válido
            
            if clean_lead['address'] and len(clean_lead['address']) > 10:
                clean_lead['score'] += 15  # Tiene dirección
            
            # Score por sector
            if any(s in clean_lead['name'].lower() 
                   for s in ['restaurante', 'peluquería', 'dentista', 'abogado']):
                clean_lead['score'] += 25  # Sectores de alto valor
            
            leads_calificados.append(clean_lead)
        
        # Ordenar por score y limitar a los mejores
        leads_calificados.sort(key=lambda x: x['score'], reverse=True)
        return leads_calificados[:5]  # Solo los 5 mejores por ejecución
    
    def generar_mensaje_personalizado(self, lead):
        """Genera mensaje personalizado usando OpenAI"""
        if not self.openai_api_key:
            # Mensaje por defecto si no hay OpenAI
            return f"""¡Hola! Soy {self.your_name} de {self.business_name} 👋

He visto que tienes {lead['name']} y me preguntaba si habías pensado en tener una página web profesional para conseguir más clientes online.

Ayudo a negocios como el tuyo a aumentar sus ventas con webs que realmente funcionan.

¿Te interesaría saber más? Es una conversación rápida 😊"""
        
        try:
            headers = {
                'Authorization': f'Bearer {self.openai_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-4o-mini',  # Más barato que gpt-4
                'messages': [
                    {
                        'role': 'system',
                        'content': f'Eres {self.your_name} de {self.business_name}, experto en desarrollo web. Genera mensajes de WhatsApp amigables y directos para ofrecer páginas web profesionales. Sé personal, menciona beneficios específicos y haz una pregunta que invite a responder.'
                    },
                    {
                        'role': 'user',
                        'content': f'Genera un mensaje de WhatsApp para contactar a {lead["name"]} que parece ser un negocio de {lead.get("industry", "servicios")}. El mensaje debe ser corto (máximo 3 líneas), profesional pero cercano, y generar interés en una página web profesional.'
                    }
                ],
                'max_tokens': 150,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"❌ Error OpenAI: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error generando mensaje: {e}")
        
        # Mensaje por defecto en caso de error
        return f"""¡Hola! Soy {self.your_name} de {self.business_name} 👋

¿Has pensado en tener una página web profesional para {lead['name']}? Te ayudo a conseguir más clientes online.

¿Te interesa saber más?"""
    
    def formatear_telefono_espanol(self, phone):
        """Formatea número español con validación estricta (Error 63024)"""
        import re
        
        # Limpiar número (solo dígitos)
        phone_clean = re.sub(r'[^\d]', '', phone)
        
        # Si ya tiene +34, validar y devolver limpio
        if phone.startswith('+34') and len(phone_clean) == 11:
            return f"+{phone_clean}"
        
        # Si empieza con 34, añadir +
        if phone_clean.startswith('34') and len(phone_clean) == 11:
            return f"+{phone_clean}"
        
        # Si es móvil español (6,7,9) de 9 dígitos
        if len(phone_clean) == 9 and phone_clean[0] in ['6', '7', '9']:
            return f"+34{phone_clean}"
        
        # Si no coincide con patrones españoles, rechazar
        print(f"⚠️ Número no válido para España: {phone}")
        return None
    
    def enviar_whatsapp(self, lead, mensaje):
        """Envía mensaje por WhatsApp con validación anti-error 63024"""
        if not self.twilio_client or not self.twilio_whatsapp:
            print(f"⚠️  WhatsApp no configurado para {lead['name']}")
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
            
            print(f"✅ WhatsApp → {lead['name']}: {phone_formatted} SID: {message.sid}")
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
    
    def notificar_telegram(self, lead, mensaje_enviado):
        """Notifica por Telegram el lead contactado"""
        if not self.telegram_bot or not self.telegram_chat:
            print(f"⚠️  Telegram no configurado")
            return
        
        try:
            texto = f"""🚀 **NUEVO LEAD CONTACTADO**

📋 **Negocio:** {lead['name']}
📞 **Teléfono:** {lead['phone']}
🏢 **Sector:** {lead.get('industry', 'No especificado')}
📍 **Dirección:** {lead.get('address', 'No especificada')}
⭐ **Score:** {lead['score']}/100
📊 **Fuente:** {lead['source']}

💬 **Mensaje enviado:**
{mensaje_enviado[:100]}...

✅ Mensaje enviado vía WhatsApp
⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            self.telegram_bot.send_message(
                chat_id=self.telegram_chat,
                text=texto,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            print(f"❌ Error enviando notificación Telegram: {e}")
    
    def ejecutar_busqueda_completa(self, ciudad, sector):
        """Ejecuta el flujo completo de búsqueda y contacto"""
        print(f"\n🚀 INICIANDO BÚSQUEDA: {sector} en {ciudad}")
        print("=" * 50)
        
        # 1. SCRAPING
        print("🔍 Fase 1: Buscando leads...")
        try:
            google_results = self.scraper.scrape_google_maps_businesses(ciudad, sector)
            pa_results = self.scraper.scrape_paginas_amarillas(ciudad, sector)
            dir_results = self.scraper.scrape_directorio_empresas(ciudad, sector)
            
            todos_leads = google_results + pa_results + dir_results
            print(f"📊 Encontrados {len(todos_leads)} leads brutos")
            
        except Exception as e:
            print(f"❌ Error en scraping: {e}")
            return
        
        # 2. FILTRADO Y CALIFICACIÓN
        print("🎯 Fase 2: Filtrando y calificando...")
        leads_calificados = self.filtrar_y_calificar_leads(todos_leads)
        print(f"⭐ {len(leads_calificados)} leads calificados")
        
        if not leads_calificados:
            print("ℹ️  No se encontraron leads nuevos de calidad")
            return
        
        # 3. CONTACTO AUTOMÁTICO
        print("📱 Fase 3: Contactando leads...")
        leads_contactados = 0
        
        for lead in leads_calificados:
            try:
                print(f"\n📞 Contactando: {lead['name']} (Score: {lead['score']})")
                
                # Generar mensaje personalizado
                mensaje = self.generar_mensaje_personalizado(lead)
                
                # Enviar WhatsApp
                if self.enviar_whatsapp(lead, mensaje):
                    # Marcar como enviado
                    self.guardar_lead_enviado(lead['id'])
                    
                    # Notificar por Telegram
                    self.notificar_telegram(lead, mensaje)
                    
                    leads_contactados += 1
                    
                    # Delay entre mensajes para no ser marcado como spam
                    time.sleep(random.uniform(30, 60))  # 30-60 segundos
                
            except Exception as e:
                print(f"❌ Error contactando {lead['name']}: {e}")
                continue
        
        print(f"\n✅ RESUMEN FINAL:")
        print(f"   🔍 Leads encontrados: {len(todos_leads)}")
        print(f"   ⭐ Leads calificados: {len(leads_calificados)}")
        print(f"   📱 Leads contactados: {leads_contactados}")
        print(f"   🎯 Ciudad: {ciudad}")
        print(f"   🏢 Sector: {sector}")
        print(f"   ⏰ Hora: {datetime.now().strftime('%H:%M')}")

def main():
    """Función principal"""
    if len(sys.argv) < 3:
        print("Uso: python3 sistema_leads_completo.py <ciudad> <sector>")
        sys.exit(1)
    
    ciudad = sys.argv[1]
    sector = sys.argv[2]
    
    sistema = SistemaLeadsCompleto()
    sistema.ejecutar_busqueda_completa(ciudad, sector)

if __name__ == "__main__":
    main() 