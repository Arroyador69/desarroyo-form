#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEMA DE LEADS INMEDIATO - DESARROYO TECH
Versión simplificada sin dependencias problemáticas para conseguir clientes YA
"""

import os
import json
import re
import time
import random
from datetime import datetime
import requests
import sys
sys.path.append('scripts')
from scraper_gratis import ScraperGratis

class SistemaLeadsInmediato:
    def __init__(self):
        print("🚀 SISTEMA DE LEADS INMEDIATO - DESARROYO TECH")
        print("🎯 Versión optimizada para conseguir clientes reales")
        print("=" * 60)
        
        # Configuración básica
        self.website_url = "https://desarroyo.tech"
        self.business_name = "DesArroyo Tech"  
        self.agent_intro = "un agente comercial de DesArroyo Tech"
        
        # Scraper gratis
        self.scraper = ScraperGratis()
        
        # Archivos de control
        self.leads_enviados_file = 'leads_contactados_hoy.json'
        self.leads_enviados = self.cargar_leads_enviados()
        
        # Contadores
        self.leads_encontrados = 0
        self.leads_validos = 0
        self.leads_enviados_hoy = 0
        
    def cargar_leads_enviados(self):
        """Carga leads ya contactados hoy"""
        try:
            if os.path.exists(self.leads_enviados_file):
                with open(self.leads_enviados_file, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            return set()
        except:
            return set()
    
    def guardar_lead_enviado(self, lead_id):
        """Guarda lead contactado"""
        self.leads_enviados.add(lead_id)
        try:
            with open(self.leads_enviados_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.leads_enviados), f)
        except:
            pass
    
    def formatear_telefono_espanol(self, phone):
        """Formatea número español con validación estricta"""
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
        return None
    
    def generar_mensaje_profesional(self, lead, sector):
        """Genera mensaje profesional orientado a venta"""
        
        mensajes_sector = {
            'restaurantes': f"""Buenos días,

Soy {self.your_name} de {self.business_name}, especialistas en desarrollo web para restaurantes.

He analizado la presencia digital de {lead['name']} y veo una gran oportunidad de crecimiento.

✅ Creamos su web profesional en máximo 72 horas
✅ Sistema de reservas online 24/7  
✅ Carta digital y pedidos a domicilio
✅ Aumentamos sus ventas hasta un 40%

Los restaurantes con web profesional facturan significativamente más que la competencia.

Tenemos 3 planes desde 149€:
🟢 Plan Rápida: 149€ 
🟡 Plan Escalable: 449€
🔴 Plan Pro Digital: 999€

¿Le interesaría una propuesta personalizada? Le envío una breve encuesta (2 minutos):
{self.website_url}/generador_automatizaciones.html

Saludos cordiales,
{self.your_name} - {self.business_name}""",

            'peluquerias': f"""Buenos días,

Soy {self.your_name} de {self.business_name}, especialistas en webs para salones de belleza.

He visto {lead['name']} y detectamos una oportunidad de negocio importante.

✅ Web profesional lista en máximo 72 horas
✅ Sistema de reservas automático
✅ Galería de trabajos que convence
✅ Hasta 60% más citas confirmadas

Las peluquerías con presencia digital profesional multiplican sus reservas.

Planes desde 149€ hasta 999€ según sus necesidades.

¿Le interesa conocer nuestra propuesta? Encuesta rápida (2 minutos):
{self.website_url}/generador_automatizaciones.html

Saludos,
{self.your_name} - {self.business_name}""",

            'dentistas': f"""Estimado Dr./Dra.,

Soy {self.your_name} de {self.business_name}, especialistas en desarrollo web para clínicas dentales.

He analizado la presencia online de {lead['name']} y veo potencial para captar más pacientes.

✅ Web médica profesional en máximo 72 horas
✅ Sistema de citas online integrado
✅ Información completa de tratamientos  
✅ Hasta 3x más pacientes nuevos al mes

Las clínicas con web profesional generan más confianza y captan más pacientes que la competencia.

Planes desde 149€ hasta 999€ adaptados a clínicas.

¿Le interesaría una propuesta personalizada? Encuesta breve (2 minutos):
{self.website_url}/generador_automatizaciones.html

Atentamente,
{self.your_name} - {self.business_name}"""
        }
        
        return mensajes_sector.get(sector, mensajes_sector['restaurantes'])
    
    def calcular_score_lead(self, lead):
        """Calcula puntuación del lead"""
        score = 0
        
        # Teléfono español válido
        if self.formatear_telefono_espanol(lead['phone']):
            score += 50
        else:
            return 0  # Sin teléfono válido no vale nada
        
        # Sin página web
        if not lead.get('website'):
            score += 30
        
        # Tiene dirección
        if lead.get('address') and len(lead['address']) > 10:
            score += 20
        
        return min(100, score)
    
    def filtrar_leads_validos(self, leads_raw, sector):
        """Filtra y califica leads válidos"""
        leads_validos = []
        
        for business in leads_raw:
            if not business.get('name') or not business.get('phone'):
                continue
            
            # ID único
            lead_id = f"{business['name'].lower().strip()}_{business['phone']}"
            if lead_id in self.leads_enviados:
                continue
            
            # Crear lead limpio
            lead = {
                'id': lead_id,
                'name': business['name'].strip(),
                'phone': business['phone'].replace(' ', '').replace('-', ''),
                'address': business.get('address', ''),
                'website': business.get('website', ''),
                'sector': sector,
                'timestamp': datetime.now().isoformat()
            }
            
            # Calcular score
            lead['score'] = self.calcular_score_lead(lead)
            
            # Solo leads con score > 40
            if lead['score'] > 40:
                leads_validos.append(lead)
        
        # Ordenar por score
        return sorted(leads_validos, key=lambda x: x['score'], reverse=True)
    
    def simular_envio_whatsapp(self, lead, mensaje):
        """Simula envío WhatsApp (para demo sin APIs reales)"""
        phone_formatted = self.formatear_telefono_espanol(lead['phone'])
        
        if not phone_formatted:
            print(f"❌ RECHAZADO: {lead['name']} - {lead['phone']} (formato inválido)")
            return False
        
        # Simular delay de envío real
        time.sleep(random.uniform(1, 3))
        
        # Generar SID simulado
        fake_sid = f"SM{hash(phone_formatted) % 1000000000000:012d}"
        
        print(f"✅ SIMULADO: {lead['name']} → {phone_formatted}")
        print(f"   📱 Score: {lead['score']}/100 | SID: {fake_sid}")
        print(f"   💬 Mensaje: {mensaje[:100]}...")
        print()
        
        return True
    
    def mostrar_resumen_leads(self, leads_validos, sector, ciudad):
        """Muestra resumen de leads encontrados"""
        print(f"\n📊 RESUMEN - {sector.upper()} en {ciudad.upper()}")
        print("=" * 50)
        print(f"🔍 Leads encontrados: {self.leads_encontrados}")
        print(f"✅ Leads válidos: {len(leads_validos)}")
        print(f"🇪🇸 Números españoles: {sum(1 for l in leads_validos if self.formatear_telefono_espanol(l['phone']))}")
        print(f"⭐ Score promedio: {sum(l['score'] for l in leads_validos) / len(leads_validos):.1f}/100" if leads_validos else "0/100")
        
        if leads_validos:
            print(f"\n🏆 TOP 5 LEADS:")
            for i, lead in enumerate(leads_validos[:5], 1):
                phone_fmt = self.formatear_telefono_espanol(lead['phone'])
                print(f"   {i}. {lead['name']} - {phone_fmt} ({lead['score']}/100)")
    
    def ejecutar_busqueda_completa(self, ciudad, sector):
        """Ejecuta búsqueda completa de leads"""
        print(f"\n🚀 INICIANDO BÚSQUEDA: {sector.upper()} en {ciudad.upper()}")
        print("=" * 60)
        
        # 1. SCRAPING
        print(f"🔍 Fase 1: Buscando leads de {sector} en {ciudad}...")
        leads_raw = []
        
        # Buscar en múltiples fuentes
        print("   🔍 Buscando en Google...")
        google_leads = self.scraper.scrape_google_maps_businesses(ciudad, sector)
        leads_raw.extend(google_leads)
        
        print("   📞 Buscando en Páginas Amarillas...")
        pa_leads = self.scraper.scrape_paginas_amarillas(ciudad, sector)
        leads_raw.extend(pa_leads)
        
        print("   📋 Buscando en directorios...")
        dir_leads = self.scraper.scrape_directorio_empresas(ciudad, sector)
        leads_raw.extend(dir_leads)
        
        self.leads_encontrados = len(leads_raw)
        print(f"   ✅ Encontrados {self.leads_encontrados} leads brutos")
        
        # 2. FILTRADO
        print(f"📊 Fase 2: Filtrando y calificando leads...")
        leads_validos = self.filtrar_leads_validos(leads_raw, sector)
        self.leads_validos = len(leads_validos)
        print(f"   ✅ {self.leads_validos} leads válidos después del filtro")
        
        # 3. MOSTRAR RESUMEN
        self.mostrar_resumen_leads(leads_validos, sector, ciudad)
        
        # 4. CONTACTAR LEADS
        print(f"\n📱 Fase 3: Contactando leads (SIMULADO)...")
        print("-" * 40)
        
        for lead in leads_validos[:10]:  # Máximo 10 por ejecución
            mensaje = self.generar_mensaje_profesional(lead, sector)
            
            if self.simular_envio_whatsapp(lead, mensaje):
                self.guardar_lead_enviado(lead['id'])
                self.leads_enviados_hoy += 1
                
                # Delay profesional entre mensajes
                if self.leads_enviados_hoy < len(leads_validos[:10]):
                    delay = random.uniform(30, 60)
                    print(f"⏱️  Esperando {delay:.0f}s antes del siguiente...")
                    time.sleep(delay)
        
        # 5. RESUMEN FINAL
        print(f"\n🎯 RESULTADOS FINALES:")
        print("=" * 30)
        print(f"✅ Leads contactados: {self.leads_enviados_hoy}")
        print(f"💰 Valor potencial: {self.leads_enviados_hoy * 450}€ (precio promedio)")
        print(f"📈 Ratio conversión esperado: 5-15%")
        print(f"🎯 Ventas esperadas: {int(self.leads_enviados_hoy * 0.1)} webs")
        print(f"⏰ Próxima ejecución: En 6 horas automáticamente")
        
        return self.leads_enviados_hoy

def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) != 3:
        print("❌ Uso: python3 sistema_leads_inmediato.py <ciudad> <sector>")
        print("📋 Ejemplo: python3 sistema_leads_inmediato.py Madrid restaurantes")
        print("🎯 Sectores: restaurantes, peluquerias, dentistas")
        return
    
    ciudad = sys.argv[1]
    sector = sys.argv[2]
    
    # Ejecutar sistema
    sistema = SistemaLeadsInmediato()
    leads_contactados = sistema.ejecutar_busqueda_completa(ciudad, sector)
    
    if leads_contactados > 0:
        print(f"\n🚀 CONFIGURACIÓN PARA APIS REALES:")
        print("=" * 40)
        print("1. Ve a https://console.twilio.com/ (WhatsApp)")
        print("2. Ve a https://platform.deepseek.com/ (IA)")  
        print("3. Configura variables en .env")
        print("4. ¡Sistema funcionará 24/7!")
        
        print(f"\n💡 CON APIS REALES:")
        print(f"   📱 Mensajes llegarán a clientes reales")
        print(f"   🤖 IA responderá automáticamente")
        print(f"   📊 Sistema capturará leads calientes")
        print(f"   💰 ROI: {leads_contactados * 450}€ potenciales al mes")

if __name__ == "__main__":
    main() 