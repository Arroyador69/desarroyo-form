#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicio rápido para webhook mejorado de DesArroyo Tech
Incluye ofertas de web personalizada en 48 horas y SMS en todos los mensajes
"""

import subprocess
import sys
import os
import time
from datetime import datetime

def verificar_entorno():
    """Verifica que el entorno esté listo"""
    print("🔍 Verificando entorno...")
    
    # Verificar que existe el archivo webhook
    if not os.path.exists('webhook_local_definitivo.py'):
        print("❌ No se encuentra webhook_local_definitivo.py")
        return False
    
    # Verificar puerto 5001
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5001))
        sock.close()
        if result == 0:
            print("⚠️  Puerto 5001 ya está en uso")
            print("   Esto puede ser el webhook anterior ejecutándose")
            return True
        else:
            print("✅ Puerto 5001 disponible")
            return True
    except:
        print("✅ Puerto 5001 disponible")
        return True

def mostrar_mejoras():
    """Muestra las mejoras implementadas"""
    print("\n🎯 MEJORAS IMPLEMENTADAS:")
    print("=" * 50)
    print("📞 HORARIO COMERCIAL:")
    print("  • Ofrece web personalizada en 48 horas")
    print("  • Solicita presionar 1 para SMS")
    print("  • Solicita presionar 2 si no interesado")
    print("  • Incluye enlace desarroyo.tech")
    print()
    print("📞 FUERA DE HORARIO:")
    print("  • Explica horario comercial")
    print("  • Ofrece web personalizada en 48 horas")
    print("  • Solicita presionar 1 para SMS")
    print("  • Solicita presionar 2 si no interesado")
    print()
    print("📞 RESPUESTA AL PRESIONAR 1:")
    print("  • Confirma envío de SMS")
    print("  • Menciona web personalizada en 48 horas")
    print("  • Promete ejemplos y propuesta gratuita")
    print("=" * 50)

def iniciar_webhook():
    """Inicia el webhook mejorado"""
    print("\n🚀 Iniciando webhook mejorado...")
    print("📞 Incluye ofertas de web personalizada y SMS")
    print("🕐 Configurado para horarios comerciales de España")
    print("🔗 URL: https://426e7c2147d2.ngrok-free.app/webhook-llamada")
    print("-" * 60)
    
    try:
        # Ejecutar el webhook
        os.system('python webhook_local_definitivo.py')
    except KeyboardInterrupt:
        print("\n\n⏹️  Webhook detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando webhook: {str(e)}")

def mostrar_instrucciones():
    """Muestra instrucciones de uso"""
    print("\n📋 INSTRUCCIONES DE USO:")
    print("=" * 50)
    print("1. 🏃 Ejecuta este script para iniciar el webhook")
    print("2. 🧪 Usa test_webhook_mejorado.py para probar")
    print("3. 🔗 Configura Twilio con la URL ngrok")
    print("4. 📱 Haz llamadas de prueba")
    print("5. 📊 Revisa los logs para verificar funcionamiento")
    print("=" * 50)
    print("🎯 URLs importantes:")
    print("  • Webhook: https://426e7c2147d2.ngrok-free.app/webhook-llamada")
    print("  • Respuesta: https://426e7c2147d2.ngrok-free.app/webhook-respuesta")
    print("  • Health: https://426e7c2147d2.ngrok-free.app/health")
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 DesArroyo Tech - Webhook Mejorado")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Incluye ofertas de web personalizada en 48 horas y SMS")
    print("=" * 60)
    
    # Mostrar mejoras
    mostrar_mejoras()
    
    # Verificar entorno
    if not verificar_entorno():
        print("\n❌ No se puede iniciar el webhook")
        sys.exit(1)
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    # Confirmar inicio
    print("\n🤔 ¿Quieres iniciar el webhook mejorado?")
    respuesta = input("   Presiona ENTER para continuar o Ctrl+C para salir: ")
    
    # Iniciar webhook
    iniciar_webhook()
    
    print("\n👋 ¡Hasta luego!") 