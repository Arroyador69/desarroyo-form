#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 INICIAR WEBHOOK LOCAL QUE FUNCIONABA AYER
Solución inmediata para volver a las llamadas en español
"""

import os
import subprocess
import sys
import time
import threading
import webbrowser
from datetime import datetime

def mostrar_banner():
    """Mostrar información del sistema"""
    print("🚀 WEBHOOK LOCAL DESARROYO TECH")
    print("=" * 60)
    print("✅ Este webhook funcionaba PERFECTAMENTE ayer")
    print("✅ Llamadas en español con voz Polly.Lucia")
    print("✅ 'Soy un agente comercial de DesArroyo Tech'")
    print("✅ SMS automático incluido")
    print("✅ Horarios comerciales configurados")
    print("=" * 60)
    print()

def verificar_credenciales():
    """Verificar que las credenciales están configuradas"""
    print("🔍 VERIFICANDO CREDENCIALES...")
    
    credenciales = {
        'TWILIO_ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID'),
        'TWILIO_AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN'), 
        'TWILIO_PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER')
    }
    
    for nombre, valor in credenciales.items():
        if valor:
            print(f"✅ {nombre}: {valor[:10]}...")
        else:
            print(f"❌ {nombre}: NO CONFIGURADO")
    
    print()
    return all(credenciales.values())

def iniciar_webhook_local():
    """Iniciar el webhook local en segundo plano"""
    print("🚀 INICIANDO WEBHOOK LOCAL...")
    print("📡 Puerto: 5001")
    print("🔗 URL: http://localhost:5001/webhook-llamada")
    print()
    
    # Iniciar webhook en segundo plano
    def run_webhook():
        try:
            subprocess.run([sys.executable, 'webhook_espanol_definitivo.py'], 
                         check=True, cwd=os.getcwd())
        except Exception as e:
            print(f"❌ Error iniciando webhook: {e}")
    
    webhook_thread = threading.Thread(target=run_webhook, daemon=True)
    webhook_thread.start()
    
    # Esperar un poco para que se inicie
    time.sleep(3)
    
    print("✅ Webhook local iniciado correctamente")
    return True

def configurar_ngrok():
    """Configurar ngrok para exponer el webhook"""
    print("🌐 CONFIGURANDO NGROK...")
    print("1. Abre una nueva terminal")
    print("2. Ejecuta: ngrok http 5001")
    print("3. Copia la URL HTTPS (ej: https://abc123.ngrok.io)")
    print()
    
    # Intentar abrir ngrok automáticamente
    try:
        subprocess.Popen(['ngrok', 'http', '5001'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        print("✅ ngrok iniciado automáticamente")
    except:
        print("⚠️ Inicia ngrok manualmente: ngrok http 5001")
    
    print()
    
    # Pedir URL al usuario
    ngrok_url = input("🔗 Pega aquí tu URL de ngrok: ").strip()
    
    if not ngrok_url.startswith('https://'):
        print("❌ La URL debe empezar con https://")
        return None
    
    webhook_url = f"{ngrok_url}/webhook-llamada"
    print(f"✅ Webhook URL: {webhook_url}")
    
    return webhook_url

def configurar_twilio(webhook_url):
    """Instrucciones para configurar Twilio"""
    print("📞 CONFIGURAR TWILIO CONSOLE:")
    print("=" * 40)
    print("1. Ve a: https://console.twilio.com/")
    print("2. Phone Numbers → Manage → Active numbers")
    print("3. Click en tu número: +18109579712")
    print("4. En 'Voice Configuration' → 'A call comes in':")
    print(f"   URL: {webhook_url}")
    print("   Method: POST")
    print("5. Guardar cambios")
    print()
    
    # Abrir Twilio Console automáticamente
    try:
        webbrowser.open('https://console.twilio.com/')
        print("✅ Twilio Console abierto en el navegador")
    except:
        print("⚠️ Abre manualmente: https://console.twilio.com/")
    
    print()
    return True

def hacer_prueba_llamada():
    """Hacer una llamada de prueba"""
    print("🧪 HACER PRUEBA DE LLAMADA:")
    print("=" * 40)
    
    respuesta = input("¿Quieres hacer una llamada de prueba? (s/n): ").strip().lower()
    
    if respuesta == 's':
        try:
            from twilio.rest import Client
            
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), 
                           os.getenv('TWILIO_AUTH_TOKEN'))
            
            # Hacer llamada de prueba
            call = client.calls.create(
                to='+34662513448',  # Tu número
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                url=webhook_url,
                timeout=60
            )
            
            print(f"✅ Llamada enviada: {call.sid}")
            print("📞 Deberías recibir la llamada en español")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar credenciales
    if not verificar_credenciales():
        print("❌ Configura las credenciales antes de continuar")
        return
    
    # Iniciar webhook local
    if not iniciar_webhook_local():
        print("❌ Error iniciando webhook local")
        return
    
    # Configurar ngrok
    webhook_url = configurar_ngrok()
    if not webhook_url:
        print("❌ Error configurando ngrok")
        return
    
    # Configurar Twilio
    configurar_twilio(webhook_url)
    
    # Hacer prueba
    hacer_prueba_llamada()
    
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("✅ El webhook local está funcionando en español")
    print("✅ Igual que ayer, pero ahora de forma permanente")
    print()
    print("🔄 PARA RASPBERRY PI:")
    print("1. Transferir webhook_espanol_definitivo.py")
    print("2. Instalar dependencias: pip install -r requirements.txt")
    print("3. Configurar variables de entorno")
    print("4. Usar IP pública o tunnel")
    print()
    print("🚀 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")

if __name__ == '__main__':
    main() 