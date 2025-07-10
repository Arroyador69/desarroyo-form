#!/usr/bin/env python3
"""
🔧 SCRIPT DIAGNÓSTICO: Error 63024 WhatsApp Twilio
Verifica configuración y formateo de números
"""

import os
from twilio.rest import Client
import re
from datetime import datetime

class DiagnosticoWhatsApp:
    def __init__(self):
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN') 
        self.twilio_whatsapp = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        print("🔧 DIAGNÓSTICO WHATSAPP - ERROR 63024")
        print("=" * 50)
        
        # Verificar configuración
        self.verificar_configuracion()
        
        # Verificar formateo de números
        self.probar_formateo_numeros()
        
        # Test de envío si está configurado
        if self.twilio_sid and self.twilio_token:
            self.test_envio_sandbox()

    def verificar_configuracion(self):
        print("\n1️⃣ VERIFICACIÓN DE CONFIGURACIÓN:")
        
        configs = {
            'TWILIO_ACCOUNT_SID': self.twilio_sid,
            'TWILIO_AUTH_TOKEN': self.twilio_token,
            'TWILIO_WHATSAPP_NUMBER': self.twilio_whatsapp
        }
        
        for key, value in configs.items():
            if value:
                masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if len(value) > 8 else "***"
                print(f"   ✅ {key}: {masked_value}")
            else:
                print(f"   ❌ {key}: NO CONFIGURADO")
        
        if not all(configs.values()):
            print(f"\n⚠️  SOLUCIÓN: Configurar variables de entorno faltantes en GitHub Secrets")

    def formatear_telefono_espanol(self, phone):
        """Formatea número español con validación estricta (Error 63024)"""
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
        
        return None

    def probar_formateo_numeros(self):
        print("\n2️⃣ PRUEBA DE FORMATEO DE NÚMEROS:")
        
        # Números de prueba (incluye los que aparecen en tu dashboard)
        numeros_test = [
            "998622614",      # Del dashboard sin +34
            "+34998622614",   # Del dashboard completo
            "982678857",      # Del dashboard sin +34
            "+34982678857",   # Del dashboard completo
            "612345678",      # Móvil típico
            "+34612345678",   # Móvil correcto
            "912345678",      # Fijo Madrid
            "+34912345678",   # Fijo Madrid correcto
            "34612345678",    # Con 34 pero sin +
            "(+34) 612 345 678",  # Con espacios y paréntesis
            "1234567890",     # Número no español
            "abc123def456",   # Con letras
        ]
        
        for numero in numeros_test:
            resultado = self.formatear_telefono_espanol(numero)
            status = "✅" if resultado else "❌"
            print(f"   {status} {numero:15} → {resultado if resultado else 'INVÁLIDO'}")

    def test_envio_sandbox(self):
        print("\n3️⃣ TEST DE ENVÍO (SANDBOX):")
        
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            
            # Número de prueba formateado correctamente
            numero_prueba = "+34612345678"  # Cambia por tu número real
            
            print(f"\n🧪 ENVIANDO MENSAJE DE PRUEBA A: {numero_prueba}")
            print("⚠️  IMPORTANTE: Este número debe estar en tu WhatsApp Sandbox")
            
            mensaje_test = """🔧 TEST DIAGNÓSTICO
            
Este es un mensaje de prueba para verificar la configuración de WhatsApp.

Si recibes este mensaje, la configuración es correcta."""
            
            message = client.messages.create(
                from_=f'whatsapp:{self.twilio_whatsapp}',
                body=mensaje_test,
                to=f'whatsapp:{numero_prueba}'
            )
            
            print(f"✅ MENSAJE ENVIADO EXITOSAMENTE")
            print(f"   SID: {message.sid}")
            print(f"   Estado: {message.status}")
            
        except Exception as e:
            error_str = str(e)
            print(f"❌ ERROR EN ENVÍO: {error_str}")
            
            # Análisis específico del error
            if '63024' in error_str:
                self.diagnosticar_error_63024()
            elif '20003' in error_str:
                print("   🔍 ERROR 20003: Credenciales de Twilio incorrectas")
                print("   💡 SOLUCIÓN: Verificar TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
            elif '21408' in error_str:
                print("   🔍 ERROR 21408: Sin permisos para WhatsApp")
                print("   💡 SOLUCIÓN: Activar WhatsApp en la consola de Twilio")

    def diagnosticar_error_63024(self):
        print("\n🔍 DIAGNÓSTICO ESPECÍFICO ERROR 63024:")
        print("   ⚠️  Este error indica que el número no está autorizado en el Sandbox")
        print("\n💡 SOLUCIONES:")
        print("   1. Ve a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
        print("   2. Añade los números de tu dashboard al Sandbox:")
        print("      • +34998622614")
        print("      • +34982678857") 
        print("      • +34919115769")
        print("      • +34953125590")
        print("      • +34932850618")
        print("      • +34989628987")
        print("      • +34911437050")
        print("   3. Cada número debe enviar 'join [código]' a tu WhatsApp Sandbox")
        print("   4. O actualiza a WhatsApp Business API (sin Sandbox)")

    def mostrar_instrucciones_finales(self):
        print("\n🎯 INSTRUCCIONES FINALES:")
        print("1. Configurar números en Sandbox de Twilio")
        print("2. O actualizar a WhatsApp Business API completa")
        print("3. Verificar que TWILIO_WHATSAPP_NUMBER sea correcto")
        print("4. Ejecutar de nuevo el sistema de leads")
        
        print(f"\n⏰ {self.__class__.__name__} completado a las {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    diagnostico = DiagnosticoWhatsApp()
    diagnostico.mostrar_instrucciones_finales() 