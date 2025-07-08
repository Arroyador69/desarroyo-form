#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TELEGRAM - Verificar configuración
"""

import telegram
import os

# Tus datos de configuración
TELEGRAM_BOT_TOKEN = "8078592045:AAFFYY-CLyn43zU1gOeFqQGANMdUN8dcNnQ"
TELEGRAM_CHAT_ID = "1524177976"

def test_telegram():
    try:
        # Crear bot
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Probar conexión
        me = bot.get_me()
        print(f"✅ Bot conectado: @{me.username}")
        
        # Enviar mensaje de prueba
        mensaje_test = """🧪 **TEST SISTEMA DE LEADS**

Este es un mensaje de prueba para verificar que Telegram funciona correctamente.

Si recibes este mensaje, la configuración es correcta y deberías recibir notificaciones de leads.

⏰ Test enviado desde script de verificación
🤖 Bot: DesArroyo Leads
🔧 Estado: Funcionando"""

        resultado = bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=mensaje_test,
            parse_mode='Markdown'
        )
        
        print(f"✅ Mensaje de prueba enviado correctamente")
        print(f"✅ Message ID: {resultado.message_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error en test Telegram: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Probando configuración de Telegram...")
    test_telegram() 