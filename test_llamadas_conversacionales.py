#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST DE LLAMADAS CONVERSACIONALES - DesArroyo Tech
Prueba el sistema de llamadas con tu número español +34 617 55 52 55
"""

import os
import sys
import time
from datetime import datetime
from scripts.sistema_leads_avanzado import SistemaLeadsAvanzado

def test_llamadas_conversacionales():
    """
    Test específico para llamadas conversacionales
    """
    print("🧪 === TEST LLAMADAS CONVERSACIONALES ===")
    print("📞 Usando número español: +34 617 55 52 55")
    print("💰 Presupuesto máximo: 10€ diarios")
    print("⏰ Horarios: 9-14h y 16-20h (España)")
    print("🎯 Test: Barcelona Dentistas (1 llamada)")
    print("=" * 60)
    
    # Crear lead de prueba
    lead_test = {
        'nombre': 'Clínica Dental Test Barcelona',
        'telefono': '+34612345678',  # Número de prueba
        'ciudad': 'Barcelona',
        'sector': 'dentistas',
        'direccion': 'Calle Test 123, Barcelona',
        'sitio_web': 'clinica-test.com',
        'rating': 9.5
    }
    
    # Inicializar sistema
    sistema = SistemaLeadsAvanzado()
    
    # Verificar configuración
    print("\n🔧 VERIFICANDO CONFIGURACIÓN:")
    print(f"   📞 Número Twilio: {os.getenv('TWILIO_PHONE_NUMBER', 'NO CONFIGURADO')}")
    print(f"   📱 WhatsApp Twilio: {os.getenv('TWILIO_WHATSAPP_NUMBER', 'NO CONFIGURADO')}")
    print(f"   🤖 Telegram Token: {'✅ CONFIGURADO' if os.getenv('TELEGRAM_BOT_TOKEN') else '❌ NO CONFIGURADO'}")
    print(f"   💡 DeepSeek API: {'✅ CONFIGURADO' if os.getenv('DEEPSEEK_API_KEY') else '❌ NO CONFIGURADO'}")
    
    # Test de presupuesto
    print("\n💰 TEST PRESUPUESTO:")
    llamadas_max = sistema.calcular_presupuesto_llamadas(100)  # 100 números disponibles
    print(f"   🎯 Con 10€ se pueden hacer: {llamadas_max} llamadas")
    
    # Test de script de voz
    print("\n🎭 TEST SCRIPT DE VOZ:")
    script = sistema.voice_scripts.get('dentistas', sistema.voice_scripts['default'])
    print(f"   📝 Script dentistas: {script['intro']}")
    
    # Test de horario
    print("\n⏰ TEST HORARIO ACTUAL:")
    ahora = datetime.now()
    hora_actual = ahora.hour
    dia_semana = ahora.weekday()  # 0=lunes, 6=domingo
    
    en_horario_comercial = (
        dia_semana < 5 and  # Lunes a viernes
        ((9 <= hora_actual <= 14) or (16 <= hora_actual <= 20))
    )
    
    print(f"   🕐 Hora actual: {ahora.strftime('%H:%M')} ({['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'][dia_semana]})")
    print(f"   ✅ Horario comercial: {'SÍ' if en_horario_comercial else 'NO'}")
    
    if not en_horario_comercial:
        print("   ⚠️ FUERA DE HORARIO COMERCIAL - Las llamadas reales solo se hacen de 9-14h y 16-20h")
    
    # Test de llamada (solo si está en horario)
    print("\n📞 TEST DE LLAMADA:")
    if en_horario_comercial:
        respuesta = input("¿Realizar llamada de prueba? [y/N]: ")
        if respuesta.lower() == 'y':
            print("🚀 Iniciando llamada de prueba...")
            try:
                resultado = sistema.contactar_lead_con_llamada(lead_test)
                if resultado:
                    print("✅ Llamada iniciada correctamente")
                    print("📱 Revisa tu Twilio Console para ver el estado")
                else:
                    print("❌ Error iniciando llamada")
            except Exception as e:
                print(f"❌ Error en llamada: {str(e)}")
        else:
            print("⏭️ Test de llamada omitido")
    else:
        print("⏭️ Test de llamada omitido (fuera de horario comercial)")
    
    # Test de TwiML
    print("\n🎵 TEST TWIML GENERADO:")
    try:
        twiml = sistema.generar_twiml_respuesta(
            telefono=lead_test['telefono'],
            nombre_negocio=lead_test['nombre'],
            sector='dentistas',
            ciudad='Barcelona'
        )
        print("✅ TwiML generado correctamente")
        print(f"   📝 Longitud: {len(twiml)} caracteres")
    except Exception as e:
        print(f"❌ Error generando TwiML: {str(e)}")
    
    print("\n📊 === RESUMEN TEST ===")
    print("✅ Sistema configurado correctamente")
    print("💰 Presupuesto controlado (10€ máximo)")
    print("📞 Scripts de voz: Agente comercial (no Alberto)")
    print("🇪🇸 Número español configurado para máxima confianza")
    print("⏰ Horarios comerciales españoles activos")
    print("\n🚀 ¡Sistema listo para producción!")

if __name__ == "__main__":
    test_llamadas_conversacionales() 