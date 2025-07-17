#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de reactivación de Raspberry Pi después de traslado
DesArroyo Tech - Sistema de Llamadas Automáticas
"""

import os
import subprocess
import time
import requests
from datetime import datetime

def verificar_conexion_internet():
    """Verifica que hay conexión a internet"""
    print("🌐 Verificando conexión a internet...")
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            print("✅ Conexión a internet OK")
            return True
        else:
            print("❌ Conexión a internet con problemas")
            return False
    except:
        print("❌ Sin conexión a internet")
        return False

def verificar_wifi():
    """Verifica la conexión WiFi"""
    print("📶 Verificando conexión WiFi...")
    try:
        # Comando para verificar WiFi en Raspberry Pi
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        if 'IEEE 802.11' in result.stdout:
            print("✅ WiFi conectado")
            return True
        else:
            print("❌ WiFi no conectado")
            return False
    except:
        print("⚠️  No se pudo verificar WiFi")
        return True  # Continuar anyway

def mostrar_ip_local():
    """Muestra la IP local de la Raspberry Pi"""
    print("🔍 Obteniendo IP local...")
    try:
        # Obtener IP local
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        ip_local = result.stdout.strip()
        print(f"📍 IP local: {ip_local}")
        return ip_local
    except:
        print("⚠️  No se pudo obtener IP local")
        return "Unknown"

def configurar_ngrok():
    """Configura ngrok para el nuevo entorno"""
    print("🔧 Configurando ngrok...")
    
    # Verificar si ngrok está instalado
    try:
        result = subprocess.run(['which', 'ngrok'], capture_output=True)
        if result.returncode != 0:
            print("❌ ngrok no está instalado")
            print("💡 Instalar con: curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null")
            return False
        else:
            print("✅ ngrok instalado")
            return True
    except:
        print("❌ Error verificando ngrok")
        return False

def iniciar_ngrok():
    """Inicia ngrok para el webhook"""
    print("🚀 Iniciando ngrok...")
    try:
        # Iniciar ngrok en segundo plano
        subprocess.Popen(['ngrok', 'http', '5001'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ ngrok iniciado")
        print("⏳ Esperando 5 segundos para que se establezca...")
        time.sleep(5)
        return True
    except:
        print("❌ Error iniciando ngrok")
        return False

def obtener_url_ngrok():
    """Obtiene la URL pública de ngrok"""
    print("🔗 Obteniendo URL pública de ngrok...")
    try:
        # Obtener URL de ngrok API
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['tunnels']:
                url = data['tunnels'][0]['public_url']
                print(f"🎯 URL pública: {url}")
                return url
            else:
                print("❌ No se encontraron túneles activos")
                return None
        else:
            print("❌ Error obteniendo URL de ngrok")
            return None
    except:
        print("❌ Error conectando con ngrok API")
        return None

def iniciar_webhook():
    """Inicia el webhook de DesArroyo Tech"""
    print("📞 Iniciando webhook de DesArroyo Tech...")
    try:
        # Iniciar webhook en segundo plano
        subprocess.Popen(['python', 'webhook_local_definitivo.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ Webhook iniciado")
        print("⏳ Esperando 3 segundos para que se establezca...")
        time.sleep(3)
        return True
    except:
        print("❌ Error iniciando webhook")
        return False

def test_webhook(webhook_url):
    """Prueba que el webhook funciona correctamente"""
    print("🧪 Probando webhook...")
    try:
        # Datos de prueba
        test_data = {
            'CallSid': 'CAtest_reactivacion',
            'From': '+34662513448',
            'To': '+18109579712'
        }
        
        response = requests.post(f"{webhook_url}/webhook-llamada", data=test_data, timeout=10)
        if response.status_code == 200:
            print("✅ Webhook funciona correctamente")
            return True
        else:
            print(f"❌ Webhook error: {response.status_code}")
            return False
    except:
        print("❌ Error probando webhook")
        return False

def mostrar_resumen(webhook_url, ip_local):
    """Muestra resumen final de la reactivación"""
    print("\n" + "="*60)
    print("🎉 REACTIVACIÓN COMPLETADA")
    print("="*60)
    print(f"📍 IP local: {ip_local}")
    print(f"🔗 URL webhook: {webhook_url}/webhook-llamada")
    print(f"📞 URL respuesta: {webhook_url}/webhook-respuesta")
    print(f"❤️  URL health: {webhook_url}/health")
    print("="*60)
    print("🔧 CONFIGURAR EN TWILIO:")
    print(f"   Webhook URL: {webhook_url}/webhook-llamada")
    print("="*60)
    print("📋 PRÓXIMOS PASOS:")
    print("1. Configurar la URL en Twilio Console")
    print("2. Hacer llamada de prueba")
    print("3. Verificar que funciona correctamente")
    print("="*60)

def main():
    """Función principal de reactivación"""
    print("🚀 REACTIVACIÓN RASPBERRY PI - NUEVA CASA")
    print("="*60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🏠 Configurando sistema después del traslado")
    print("="*60)
    
    # Paso 1: Verificar conexión
    if not verificar_conexion_internet():
        print("❌ FALLO: Sin conexión a internet")
        print("💡 Verifica WiFi y router")
        return
    
    # Paso 2: Verificar WiFi
    verificar_wifi()
    
    # Paso 3: Mostrar IP local
    ip_local = mostrar_ip_local()
    
    # Paso 4: Configurar ngrok
    if not configurar_ngrok():
        print("❌ FALLO: ngrok no configurado")
        return
    
    # Paso 5: Iniciar ngrok
    if not iniciar_ngrok():
        print("❌ FALLO: ngrok no iniciado")
        return
    
    # Paso 6: Obtener URL pública
    webhook_url = obtener_url_ngrok()
    if not webhook_url:
        print("❌ FALLO: No se pudo obtener URL pública")
        return
    
    # Paso 7: Iniciar webhook
    if not iniciar_webhook():
        print("❌ FALLO: webhook no iniciado")
        return
    
    # Paso 8: Probar webhook
    if not test_webhook(webhook_url):
        print("❌ FALLO: webhook no funciona")
        return
    
    # Paso 9: Mostrar resumen
    mostrar_resumen(webhook_url, ip_local)
    
    print("\n🎉 ¡SISTEMA REACTIVADO CON ÉXITO!")
    print("💡 El sistema está listo para recibir llamadas")

if __name__ == "__main__":
    main() 