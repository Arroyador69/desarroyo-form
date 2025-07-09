#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST WHATSAPP - Diagnóstico Error 63024
Prueba directa de envío WhatsApp para identificar el problema
"""

from twilio.rest import Client
import os
import sys

def test_whatsapp_directo():
    """Prueba WhatsApp con configuración directa"""
    
    print("🧪 TEST WHATSAPP - DIAGNÓSTICO ERROR 63024")
    print("=" * 50)
    
    # Configuración desde variables de entorno
    TWILIO_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_TOKEN = os.getenv('TWILIO_AUTH_TOKEN') 
    TWILIO_WHATSAPP = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    print(f"📋 CONFIGURACIÓN:")
    print(f"   SID: {TWILIO_SID[:8]}... (oculto)")
    print(f"   Token: {TWILIO_TOKEN[:8]}... (oculto)")
    print(f"   WhatsApp: {TWILIO_WHATSAPP}")
    
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_WHATSAPP]):
        print("❌ ERROR: Variables de entorno no configuradas")
        print("   Configura: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER")
        return False
    
    # Pedir número de prueba
    print(f"\n📞 INGRESA TU NÚMERO PERSONAL:")
    print(f"   Formato: +34XXXXXXXXX (ejemplo: +34612345678)")
    tu_numero = input("   Tu número: ").strip()
    
    if not tu_numero.startswith('+34'):
        print(f"❌ ERROR: El número debe empezar con +34")
        return False
    
    if len(tu_numero) != 12:
        print(f"❌ ERROR: El número debe tener 12 caracteres (+34XXXXXXXXX)")
        return False
    
    # Crear cliente Twilio
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        print(f"✅ Cliente Twilio creado correctamente")
    except Exception as e:
        print(f"❌ ERROR creando cliente Twilio: {e}")
        return False
    
    # Enviar mensaje de prueba
    print(f"\n📤 ENVIANDO MENSAJE DE PRUEBA...")
    print(f"   From: whatsapp:{TWILIO_WHATSAPP}")
    print(f"   To: whatsapp:{tu_numero}")
    
    try:
        message = client.messages.create(
            from_=f'whatsapp:{TWILIO_WHATSAPP}',
            body='🧪 PRUEBA: Si recibes este mensaje, WhatsApp funciona correctamente. Error 63024 solucionado.',
            to=f'whatsapp:{tu_numero}'
        )
        
        print(f"\n✅ MENSAJE ENVIADO EXITOSAMENTE!")
        print(f"   SID: {message.sid}")
        print(f"   Estado inicial: {message.status}")
        print(f"   Dirección: {message.direction}")
        print(f"   Precio: {message.price} {message.price_unit}")
        
        # Verificar estado después de unos segundos
        import time
        print(f"\n⏱️ Verificando estado en 10 segundos...")
        time.sleep(10)
        
        # Refrescar estado del mensaje
        message = client.messages(message.sid).fetch()
        print(f"   Estado final: {message.status}")
        
        if message.status == 'delivered':
            print(f"🎉 ÉXITO: Mensaje entregado correctamente")
            print(f"   ✅ No hay error 63024")
            print(f"   ✅ Configuración Twilio correcta")
            return True
        elif message.status == 'failed':
            print(f"❌ FALLO: Mensaje no entregado")
            print(f"   Error code: {message.error_code}")
            print(f"   Error message: {message.error_message}")
            return False
        else:
            print(f"⏳ PENDIENTE: Estado '{message.status}' - espera más tiempo")
            return True
            
    except Exception as e:
        print(f"\n❌ ERROR ENVIANDO MENSAJE:")
        print(f"   {e}")
        
        # Análisis del error
        error_str = str(e)
        if '63024' in error_str:
            print(f"\n🔍 DIAGNÓSTICO ERROR 63024:")
            print(f"   ❌ Número no autorizado en WhatsApp Sandbox")
            print(f"   📝 SOLUCIÓN:")
            print(f"      1. Ve a Twilio Console → WhatsApp Sandbox")
            print(f"      2. Añade tu número: {tu_numero}")
            print(f"      3. Envía el código desde tu WhatsApp")
            print(f"      4. Vuelve a ejecutar este test")
        elif '20003' in error_str:
            print(f"\n🔍 DIAGNÓSTICO ERROR 20003:")
            print(f"   ❌ Credenciales incorrectas")
            print(f"   📝 SOLUCIÓN: Verificar TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
        elif '21408' in error_str:
            print(f"\n🔍 DIAGNÓSTICO ERROR 21408:")
            print(f"   ❌ Sin permisos para WhatsApp")
            print(f"   📝 SOLUCIÓN: Verificar que tienes WhatsApp habilitado en Twilio")
        
        return False

def test_formateo_numeros():
    """Prueba formateo de números españoles"""
    
    print(f"\n🔧 TEST FORMATEO DE NÚMEROS")
    print("=" * 30)
    
    numeros_prueba = [
        "612345678",      # Móvil sin código país
        "+34612345678",   # Móvil correcto
        "34612345678",    # Con código sin +
        "912345678",      # Fijo Madrid sin código
        "+34912345678",   # Fijo Madrid correcto
        "123456789",      # Número inválido
        "+1234567890",    # Número no español
        "(+34) 612 345 678",  # Con espacios y paréntesis
    ]
    
    def formatear_numero_mejorado(phone):
        """Formateo mejorado con validación"""
        import re
        
        # Limpiar número (solo dígitos)
        phone_clean = re.sub(r'[^\d]', '', phone)
        
        # Si ya tiene +34, devolverlo limpio
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
    
    for numero in numeros_prueba:
        resultado = formatear_numero_mejorado(numero)
        estado = "✅ VÁLIDO" if resultado else "❌ INVÁLIDO"
        print(f"   {numero:20} → {resultado or 'RECHAZADO':15} {estado}")

if __name__ == "__main__":
    print("🚀 DESARROYO TECH - DIAGNÓSTICO WHATSAPP")
    print("🎯 Solución para Error 63024 'Invalid message recipient'")
    print()
    
    # Test 1: Formateo de números
    test_formateo_numeros()
    
    # Test 2: Envío directo
    input("\n⌨️ Presiona ENTER para probar envío directo...")
    if test_whatsapp_directo():
        print(f"\n🎉 ¡ÉXITO! WhatsApp funcionando correctamente")
        print(f"   Ya puedes usar el sistema de leads sin error 63024")
    else:
        print(f"\n⚠️ Revisa la configuración según el diagnóstico")
        print(f"   Sigue las instrucciones en SOLUCION_ERROR_CONEXION.md") 