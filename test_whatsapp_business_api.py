#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST WHATSAPP BUSINESS API - DESARROYO TECH
Prueba que WhatsApp Business API funciona correctamente
"""

import os
import sys
import re
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class TestWhatsAppBusinessAPI:
    def __init__(self):
        print("🚀 TEST WHATSAPP BUSINESS API - DESARROYO TECH")
        print("=" * 50)
        
        # Configuración desde variables de entorno
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        self.website_url = os.getenv('WEBSITE_URL', 'https://desarroyo.tech')
        self.business_name = os.getenv('BUSINESS_NAME', 'DesArroyo Tech')
        self.agent_intro = "un agente comercial de DesArroyo Tech"
        
        # Inicializar cliente Twilio
        self.twilio_client = None
        if self.twilio_sid and self.twilio_token:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(self.twilio_sid, self.twilio_token)
                print("✅ Cliente Twilio inicializado correctamente")
            except Exception as e:
                print(f"❌ Error inicializando Twilio: {e}")
        else:
            print("❌ Credenciales Twilio no encontradas")
    
    def verificar_configuracion(self):
        """Verifica que la configuración esté completa"""
        print("\n🔍 VERIFICANDO CONFIGURACIÓN...")
        
        config_items = [
            ('TWILIO_ACCOUNT_SID', self.twilio_sid),
            ('TWILIO_AUTH_TOKEN', self.twilio_token),
            ('TWILIO_WHATSAPP_NUMBER', self.twilio_whatsapp),
            ('WEBSITE_URL', self.website_url),
            ('BUSINESS_NAME', self.business_name),
            ('YOUR_NAME', self.your_name)
        ]
        
        all_good = True
        for name, value in config_items:
            if value:
                print(f"✅ {name}: {value[:10]}...")
            else:
                print(f"❌ {name}: NO CONFIGURADO")
                all_good = False
        
        return all_good
    
    def formatear_telefono_espanol(self, phone):
        """Formatea número español con validación estricta"""
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
        
        return None
    
    def generar_mensaje_profesional(self, nombre_negocio, sector):
        """Genera mensaje profesional para WhatsApp Business API"""
        
        mensajes_sector = {
            'restaurante': f"""Buenos días,

Soy {self.your_name} de {self.business_name}, especialistas en desarrollo web para restaurantes.

He analizado la presencia digital de {nombre_negocio} y veo una gran oportunidad de crecimiento.

✅ Creamos su web profesional en máximo 48 horas
✅ Sistema de reservas online 24/7  
✅ Carta digital y pedidos a domicilio
✅ Aumentamos sus ventas hasta un 40%

Los restaurantes con web profesional facturan significativamente más que la competencia.

¿Le interesaría una propuesta personalizada? Le envío una breve encuesta (2 minutos):
{self.website_url}/generador_automatizaciones.html

Saludos cordiales,
{self.your_name} - {self.business_name}""",
            
            'peluqueria': f"""Buenos días,

Soy {self.your_name} de {self.business_name}, especialistas en webs para salones de belleza.

He visto {nombre_negocio} y detectamos una oportunidad de negocio importante.

✅ Web profesional lista en máximo 48 horas
✅ Sistema de reservas automático
✅ Galería de trabajos que convence
✅ Hasta 60% más citas confirmadas

Las peluquerías con presencia digital profesional multiplican sus reservas.

¿Le interesa conocer nuestra propuesta? Encuesta rápida (2 minutos):
{self.website_url}/generador_automatizaciones.html

Saludos,
{self.your_name} - {self.business_name}""",
            
            'default': f"""Buenos días,

Soy {self.your_name} de {self.business_name}, especialistas en desarrollo web profesional.

He analizado {nombre_negocio} y veo potencial para impulsar su negocio online.

✅ Web profesional en máximo 48 horas
✅ Diseño moderno y optimizado
✅ Aumentamos su visibilidad online
✅ Más clientes, más ventas

Las empresas con presencia digital profesional superan a la competencia.

¿Le interesaría conocer nuestra propuesta? Encuesta personalizada (2 minutos):
{self.website_url}/generador_automatizaciones.html

Saludos profesionales,
{self.your_name} - {self.business_name}"""
        }
        
        return mensajes_sector.get(sector, mensajes_sector['default'])
    
    def test_envio_whatsapp(self, telefono, nombre_negocio, sector):
        """Prueba envío real de WhatsApp Business API"""
        print(f"\n📱 PROBANDO ENVÍO WHATSAPP BUSINESS API...")
        
        # Formatear número
        phone_formatted = self.formatear_telefono_espanol(telefono)
        if not phone_formatted:
            print(f"❌ Número inválido: {telefono}")
            return False
        
        # Generar mensaje profesional
        mensaje = self.generar_mensaje_profesional(nombre_negocio, sector)
        
        print(f"📞 Enviando a: {phone_formatted}")
        print(f"🏢 Negocio: {nombre_negocio}")
        print(f"📋 Sector: {sector}")
        print(f"💬 Mensaje: {mensaje[:100]}...")
        
        if not self.twilio_client:
            print("❌ Cliente Twilio no disponible")
            return False
        
        try:
            # Enviar mensaje por WhatsApp Business API
            message = self.twilio_client.messages.create(
                from_=f'whatsapp:{self.twilio_whatsapp}',
                body=mensaje,
                to=f'whatsapp:{phone_formatted}'
            )
            
            print(f"✅ MENSAJE ENVIADO EXITOSAMENTE!")
            print(f"   📱 WhatsApp → {nombre_negocio}: {phone_formatted}")
            print(f"   🆔 SID: {message.sid}")
            print(f"   📊 Estado: {message.status}")
            print(f"   💰 Costo aprox: ~$0.025 (WhatsApp Business API)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error enviando WhatsApp: {e}")
            
            # Análisis específico del error
            error_str = str(e)
            if '63024' in error_str:
                print(f"   🔍 ERROR 63024: Número no autorizado en WhatsApp Sandbox")
                print(f"   💡 SOLUCIÓN: Configura WhatsApp Business API de pago")
                print(f"   📱 O añade {phone_formatted} al sandbox de Twilio")
            elif '20003' in error_str:
                print(f"   🔍 ERROR 20003: Credenciales incorrectas")
                print(f"   💡 SOLUCIÓN: Verifica TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
            elif '21408' in error_str:
                print(f"   🔍 ERROR 21408: Sin permisos WhatsApp")
                print(f"   💡 SOLUCIÓN: Activa WhatsApp Business API en Twilio")
            
            return False
    
    def ejecutar_test_completo(self):
        """Ejecuta test completo de WhatsApp Business API"""
        print(f"\n🎯 INICIANDO TEST COMPLETO...")
        print(f"⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Verificar configuración
        if not self.verificar_configuracion():
            print("\n❌ CONFIGURACIÓN INCOMPLETA")
            print("💡 Ejecuta: ./setup_whatsapp_business.sh")
            return False
        
        # Datos de prueba
        print("\n📋 DATOS DE PRUEBA:")
        telefono_test = input("📱 Introduce un número de teléfono para prueba (+34XXXXXXXXX): ")
        nombre_negocio = input("🏢 Nombre del negocio (ej: Restaurante El Buen Sabor): ")
        sector = input("📋 Sector (restaurante/peluqueria/otro): ")
        
        # Ejecutar prueba
        resultado = self.test_envio_whatsapp(telefono_test, nombre_negocio, sector)
        
        # Resumen
        print("\n" + "="*50)
        print("📊 RESUMEN DEL TEST:")
        print("="*50)
        
        if resultado:
            print("✅ WHATSAPP BUSINESS API: FUNCIONANDO CORRECTAMENTE")
            print("📱 Mensaje enviado exitosamente")
            print("🎯 Sistema listo para generar leads")
            print("💰 Costo por mensaje: ~$0.025")
            print("📈 Tasa de apertura esperada: 98%")
            print("")
            print("🚀 SIGUIENTE PASO:")
            print("   python3 scripts/sistema_leads_avanzado.py Madrid restaurantes")
        else:
            print("❌ WHATSAPP BUSINESS API: NECESITA CONFIGURACIÓN")
            print("🔧 Revisa las credenciales de Twilio")
            print("💡 Asegúrate de tener WhatsApp Business API activado")
            print("")
            print("📋 CONFIGURACIÓN NECESARIA:")
            print("   ./setup_whatsapp_business.sh")
        
        return resultado

def main():
    """Función principal"""
    test = TestWhatsAppBusinessAPI()
    test.ejecutar_test_completo()

if __name__ == "__main__":
    main() 