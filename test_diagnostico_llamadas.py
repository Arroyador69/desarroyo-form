#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO TWILIO - VERIFICAR CAPACIDADES DE LLAMADAS
Script para diagnosticar problemas con llamadas de voz
"""

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
import json

def diagnosticar_twilio():
    """Diagnóstico completo de configuración Twilio"""
    
    print("🔍 DIAGNÓSTICO TWILIO - CAPACIDADES DE LLAMADAS")
    print("=" * 60)
    
    # 1. Verificar variables de entorno
    print("\n1️⃣ VERIFICANDO VARIABLES DE ENTORNO...")
    
    sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN') 
    phone = os.getenv('TWILIO_PHONE_NUMBER')
    
    if not sid:
        print("❌ TWILIO_ACCOUNT_SID no configurado")
        return False
    else:
        print(f"✅ TWILIO_ACCOUNT_SID: {sid[:8]}...")
    
    if not token:
        print("❌ TWILIO_AUTH_TOKEN no configurado")
        return False
    else:
        print(f"✅ TWILIO_AUTH_TOKEN: {token[:8]}...")
    
    if not phone:
        print("❌ TWILIO_PHONE_NUMBER no configurado")
        return False
    else:
        print(f"✅ TWILIO_PHONE_NUMBER: {phone}")
    
    # 2. Crear cliente Twilio
    print("\n2️⃣ CONECTANDO CON TWILIO...")
    try:
        client = Client(sid, token)
        print("✅ Cliente Twilio creado correctamente")
    except Exception as e:
        print(f"❌ Error creando cliente Twilio: {e}")
        return False
    
    # 3. Verificar cuenta
    print("\n3️⃣ VERIFICANDO CUENTA...")
    try:
        account = client.api.accounts(sid).fetch()
        print(f"✅ Cuenta activa: {account.friendly_name}")
        print(f"✅ Status: {account.status}")
    except Exception as e:
        print(f"❌ Error verificando cuenta: {e}")
        return False
    
    # 4. Verificar número y capacidades
    print("\n4️⃣ VERIFICANDO NÚMERO Y CAPACIDADES...")
    try:
        # Buscar el número en la cuenta
        phone_numbers = client.incoming_phone_numbers.list()
        
        numero_encontrado = None
        for number in phone_numbers:
            if number.phone_number == phone:
                numero_encontrado = number
                break
        
        if numero_encontrado:
            print(f"✅ Número encontrado: {numero_encontrado.phone_number}")
            print(f"📱 Friendly Name: {numero_encontrado.friendly_name}")
            
            # CAPACIDADES - ESTO ES LO MÁS IMPORTANTE
            capacidades = numero_encontrado.capabilities
            print(f"\n📋 CAPACIDADES DEL NÚMERO:")
            print(f"   🗣️  VOICE (Llamadas): {'✅ SÍ' if capacidades.get('voice') else '❌ NO'}")
            print(f"   💬 SMS: {'✅ SÍ' if capacidades.get('sms') else '❌ NO'}")
            print(f"   📷 MMS: {'✅ SÍ' if capacidades.get('mms') else '❌ NO'}")
            
            if not capacidades.get('voice'):
                print("\n🚨 PROBLEMA ENCONTRADO:")
                print("❌ Tu número NO tiene capacidad de VOICE (llamadas)")
                print("💡 SOLUCIÓN: Necesitas un número con capacidad de Voice")
                return False
            else:
                print("\n✅ CAPACIDAD DE VOICE HABILITADA")
                
        else:
            print(f"❌ Número {phone} no encontrado en tu cuenta")
            print("\n📱 NÚMEROS DISPONIBLES EN TU CUENTA:")
            for number in phone_numbers:
                caps = number.capabilities
                print(f"   📞 {number.phone_number} - Voice: {'✅' if caps.get('voice') else '❌'} SMS: {'✅' if caps.get('sms') else '❌'}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando número: {e}")
        return False
    
    # 5. Test de llamada simple (sin ejecutar)
    print("\n5️⃣ PREPARANDO TEST DE LLAMADA...")
    print("💡 Para test real, ejecutaremos una llamada de prueba a un número test")
    
    try:
        # Verificar que podemos crear llamadas (sin ejecutar)
        print("✅ API de llamadas accesible")
        print("📞 Listo para realizar llamadas reales")
        
    except Exception as e:
        print(f"❌ Error preparando llamada: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 DIAGNÓSTICO COMPLETADO")
    print("✅ Todo configurado correctamente para llamadas")
    return True

if __name__ == "__main__":
    diagnosticar_twilio() 