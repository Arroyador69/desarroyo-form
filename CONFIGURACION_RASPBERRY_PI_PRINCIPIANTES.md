# 🍓 GUÍA COMPLETA: RASPBERRY PI DESDE CERO

## ⏱️ **TIEMPO ESTIMADO: 2-3 HORAS**

### 📋 **LO QUE NECESITAS ANTES DE EMPEZAR:**
- [ ] **Raspberry Pi 4** (recomendado) o Pi 3
- [ ] **Tarjeta microSD** (32GB mínimo)
- [ ] **Cable de alimentación** USB-C (Pi 4) o micro-USB (Pi 3)
- [ ] **Cable HDMI** para conectar a monitor
- [ ] **Teclado y ratón** USB
- [ ] **Conexión a internet** (WiFi o ethernet)
- [ ] **Ordenador** para preparar la SD

---

## 🎯 **FASE 1: PREPARAR LA RASPBERRY PI (30-45 MIN)**

### 📥 **PASO 1: DESCARGAR RASPBERRY PI IMAGER**
```bash
# En tu Mac, descarga desde:
https://www.raspberrypi.com/software/
# O instala con brew:
brew install raspberry-pi-imager
```

### 💽 **PASO 2: PREPARAR LA TARJETA SD**
1. **Abrir Raspberry Pi Imager**
2. **Elegir OS:** "Raspberry Pi OS (32-bit)" - **RECOMENDADO**
3. **Elegir tarjeta SD:** Tu tarjeta microSD
4. **⚙️ IMPORTANTE - Configuración avanzada:**
   - Clic en **⚙️ (gear icon)**
   - ✅ **Enable SSH** (usuario: pi, contraseña: tu_contraseña)
   - ✅ **Configure WiFi** (tu red WiFi y contraseña)
   - ✅ **Set username and password** (usuario: pi, contraseña: desarroyo123)
5. **Grabar imagen** (15-20 minutos)

### 🔌 **PASO 3: PRIMER ARRANQUE**
1. **Insertar SD** en la Raspberry Pi
2. **Conectar:** HDMI, teclado, ratón, alimentación
3. **Arrancar** (2-3 minutos primera vez)
4. **Completar setup inicial** (país, idioma, etc.)

---

## 🌐 **FASE 2: CONFIGURAR CONEXIÓN (15-20 MIN)**

### 📶 **PASO 4: VERIFICAR CONEXIÓN**
```bash
# Abrir terminal en Raspberry Pi
ping google.com
# Si funciona → continuar
# Si no → configurar WiFi manualmente
```

### 🔧 **PASO 5: CONFIGURAR SSH (OPCIONAL)**
```bash
# Activar SSH si no lo hiciste antes
sudo systemctl enable ssh
sudo systemctl start ssh

# Obtener IP de la Raspberry Pi
hostname -I
# Apunta esta IP: 192.168.X.XXX
```

### 💻 **PASO 6: CONECTAR DESDE TU MAC (OPCIONAL)**
```bash
# Desde tu Mac, conectar por SSH
ssh pi@192.168.X.XXX
# Contraseña: desarroyo123 (o la que pusiste)
```

---

## 🐍 **FASE 3: INSTALAR DEPENDENCIAS (20-30 MIN)**

### 📦 **PASO 7: ACTUALIZAR SISTEMA**
```bash
# En la Raspberry Pi (terminal)
sudo apt update
sudo apt upgrade -y
# TIEMPO: 10-15 minutos
```

### 🐍 **PASO 8: INSTALAR PYTHON Y PIP**
```bash
# Verificar Python
python3 --version
# Debería mostrar: Python 3.9.x o superior

# Instalar pip
sudo apt install python3-pip -y

# Instalar dependencias necesarias
pip3 install flask requests python-dotenv twilio pytz
```

### 🔧 **PASO 9: INSTALAR NGROK**
```bash
# Descargar ngrok para ARM
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip

# Descomprimir
unzip ngrok-stable-linux-arm.zip

# Mover a directorio global
sudo mv ngrok /usr/local/bin/

# Verificar instalación
ngrok --version
```

---

## 📁 **FASE 4: CONFIGURAR PROYECTO (15-20 MIN)**

### 📂 **PASO 10: CREAR DIRECTORIO DE PROYECTO**
```bash
# Crear directorio
mkdir /home/pi/desarroyo-form
cd /home/pi/desarroyo-form

# Crear archivo de configuración
nano .env
```

### 🔑 **PASO 11: CONFIGURAR VARIABLES DE ENTORNO**
```bash
# En el archivo .env (nano), pegar:
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_PHONE_NUMBER=+18109579712
WEBSITE_URL=https://tu-ngrok-url.ngrok.io

# Guardar: Ctrl+X, Y, Enter
```

### 📄 **PASO 12: CREAR WEBHOOK**
```bash
# Crear archivo webhook
nano webhook_raspberry.py
```

### 🐍 **PASO 13: CÓDIGO DEL WEBHOOK**
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEBHOOK RASPBERRY PI - DESARROYO TECH
"""

from flask import Flask, request, Response
from datetime import datetime
import pytz
import logging
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def es_horario_comercial():
    """Verifica si estamos en horario comercial español"""
    spain_tz = pytz.timezone('Europe/Madrid')
    now = datetime.now(spain_tz)
    weekday = now.weekday()
    hour = now.hour
    
    # Lunes a viernes: 9-14h y 16-20h
    if weekday <= 4:
        return (9 <= hour < 14) or (16 <= hour < 20)
    # Sábados: 10-13h
    elif weekday == 5:
        return 10 <= hour < 13
    else:
        return False

@app.route('/webhook-llamada', methods=['POST'])
def webhook_llamada():
    """Webhook para llamadas de Twilio"""
    try:
        call_sid = request.form.get('CallSid', 'Unknown')
        from_number = request.form.get('From', 'Unknown')
        to_number = request.form.get('To', 'Unknown')
        
        logger.info(f"📞 Llamada: {call_sid}, From: {from_number}, To: {to_number}")
        
        if es_horario_comercial():
            mensaje = """
            Hola, soy un agente comercial de DesArroyo Tech. Creamos páginas web profesionales en 48 horas. 
            Puede solicitar una propuesta personalizada gratuita. Presione 1 si está interesado y le enviamos 
            una encuesta por SMS, o presione 2 si no está interesado. También puede visitarnos en desarroyo punto tech.
            """
        else:
            mensaje = """
            Hola, soy un agente comercial de DesArroyo Tech. Le llamamos fuera de horario comercial. 
            Horario: lunes a viernes 9 a 14 y 16 a 20 horas. Creamos páginas web profesionales en 48 horas. 
            Presione 1 para recibir información por SMS, o presione 2 si no está interesado.
            """
        
        twiml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        {mensaje.strip()}
    </Say>
    <Gather input="dtmf" timeout="5" numDigits="1" action="http://localhost:5001/webhook-respuesta">
        <Say voice="Polly.Lucia" language="es-ES">
            Esperando su respuesta...
        </Say>
    </Gather>
    <Say voice="Polly.Lucia" language="es-ES">
        Le enviamos información por SMS. Gracias por su tiempo.
    </Say>
</Response>'''
        
        return Response(twiml_response, mimetype='application/xml')
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return Response('''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        Hola, soy un agente comercial de DesArroyo Tech. Gracias por su tiempo.
    </Say>
</Response>''', mimetype='application/xml')

@app.route('/webhook-respuesta', methods=['POST'])
def webhook_respuesta():
    """Webhook para respuestas"""
    digits = request.form.get('Digits', '')
    
    if digits == '1':
        mensaje = """
        Perfecto, muchas gracias por su interés. Le enviaremos un SMS con información sobre 
        nuestro servicio de páginas web profesionales en 48 horas. Incluiremos ejemplos de 
        nuestro trabajo y un enlace para solicitar una propuesta personalizada gratuita.
        """
    elif digits == '2':
        mensaje = """
        Entendemos perfectamente. Disculpe las molestias y muchas gracias por su tiempo. 
        Si en el futuro necesita servicios web, puede encontrarnos en desarroyo punto tech.
        """
    else:
        mensaje = """
        No hemos recibido una respuesta válida. Le enviaremos información por SMS. 
        Puede contactarnos en desarroyo punto tech. Gracias.
        """
    
    twiml_response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Lucia" language="es-ES">
        {mensaje.strip()}
    </Say>
</Response>'''
    
    return Response(twiml_response, mimetype='application/xml')

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de salud"""
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    print("🍓 Raspberry Pi Webhook - DesArroyo Tech")
    print("📞 Listo para recibir llamadas en español")
    print("🔗 Puerto: 5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
```

### 💾 **PASO 14: GUARDAR Y HACER EJECUTABLE**
```bash
# Guardar: Ctrl+X, Y, Enter
# Hacer ejecutable
chmod +x webhook_raspberry.py
```

---

## 🔗 **FASE 5: CONFIGURAR NGROK (10-15 MIN)**

### 🔑 **PASO 15: CONFIGURAR NGROK**
```bash
# Ir a https://ngrok.com/signup
# Crear cuenta gratuita
# Obtener token de autenticación
ngrok config add-authtoken TU_TOKEN_AQUI
```

### 🚀 **PASO 16: PROBAR WEBHOOK LOCAL**
```bash
# Terminal 1: Iniciar webhook
cd /home/pi/desarroyo-form
python3 webhook_raspberry.py

# Terminal 2: Iniciar ngrok
ngrok http 5001
```

### 🔍 **PASO 17: OBTENER URL PÚBLICA**
```bash
# Buscar en la salida de ngrok:
# Forwarding: https://xxxx.ngrok.io -> http://localhost:5001
# Apunta esta URL: https://xxxx.ngrok.io
```

---

## 🔧 **FASE 6: CONFIGURAR TWILIO (10 MIN)**

### 📞 **PASO 18: CONFIGURAR WEBHOOK EN TWILIO**
1. **Ir a:** https://console.twilio.com/
2. **Phone Numbers** → **Manage** → **Active numbers**
3. **Clic en tu número:** +18109579712
4. **Voice & Fax** → **A call comes in:**
   - **URL:** https://xxxx.ngrok.io/webhook-llamada
   - **Method:** POST
5. **Save Configuration**

---

## 🧪 **FASE 7: PRUEBAS (15-20 MIN)**

### 📱 **PASO 19: LLAMADA DE PRUEBA**
```bash
# Crear script de prueba
nano test_llamada_raspberry.py
```

### 🧪 **PASO 20: SCRIPT DE PRUEBA**
```python
#!/usr/bin/env python3
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# Tu número de teléfono
numero = input("📱 Tu número (ej: +34662513448): ")

try:
    call = client.calls.create(
        to=numero,
        from_=os.getenv('TWILIO_PHONE_NUMBER'),
        url=f"https://xxxx.ngrok.io/webhook-llamada",  # TU URL NGROK
        timeout=60,
        record=True
    )
    
    print(f"✅ Llamada enviada: {call.sid}")
    print("📞 Deberías recibir la llamada en español!")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

### 📞 **PASO 21: EJECUTAR PRUEBA**
```bash
# Ejecutar prueba
python3 test_llamada_raspberry.py
```

---

## 🚀 **FASE 8: AUTOMATIZACIÓN (10 MIN)**

### 🔄 **PASO 22: SCRIPT DE INICIO AUTOMÁTICO**
```bash
# Crear script de inicio
nano start_webhook.sh
```

### 📝 **PASO 23: CONTENIDO DEL SCRIPT**
```bash
#!/bin/bash
# Script de inicio automático - DesArroyo Tech

cd /home/pi/desarroyo-form

echo "🍓 Iniciando Raspberry Pi Webhook..."
echo "📞 DesArroyo Tech - Sistema de Llamadas"

# Iniciar ngrok en background
ngrok http 5001 &
echo "⏳ Esperando ngrok..."
sleep 5

# Obtener URL de ngrok
NGROK_URL=$(curl -s localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*https[^"]*' | head -1 | cut -d'"' -f4)
echo "🔗 URL ngrok: $NGROK_URL"

# Iniciar webhook
echo "🚀 Iniciando webhook..."
python3 webhook_raspberry.py
```

### 🔧 **PASO 24: HACER EJECUTABLE**
```bash
# Hacer ejecutable
chmod +x start_webhook.sh

# Probar
./start_webhook.sh
```

---

## ✅ **VERIFICACIÓN FINAL**

### 📋 **CHECKLIST FINAL:**
- [ ] Raspberry Pi funcionando
- [ ] WiFi conectado
- [ ] Python y dependencias instaladas
- [ ] ngrok configurado
- [ ] Webhook respondiendo
- [ ] Twilio configurado
- [ ] Llamada de prueba exitosa

### 🎉 **¡SISTEMA FUNCIONANDO!**
```
🍓 Raspberry Pi: ✅ Operativa
📞 Twilio: ✅ Configurado
🔗 ngrok: ✅ Conectado
🎯 Webhook: ✅ Respondiendo en español
```

---

## 🆘 **SOLUCIÓN DE PROBLEMAS**

### 🐛 **PROBLEMA: No funciona el webhook**
```bash
# Verificar que Flask está corriendo
ps aux | grep python3

# Verificar puerto
netstat -tuln | grep 5001

# Reiniciar webhook
pkill -f webhook_raspberry.py
python3 webhook_raspberry.py
```

### 🐛 **PROBLEMA: ngrok no conecta**
```bash
# Verificar instalación
ngrok --version

# Verificar token
ngrok config check

# Reiniciar ngrok
pkill ngrok
ngrok http 5001
```

### 🐛 **PROBLEMA: Twilio no llama**
```bash
# Verificar configuración
curl -X POST https://tu-ngrok-url.ngrok.io/webhook-llamada \
  -d "CallSid=test&From=+34662513448&To=+18109579712"
```

---

## 🎯 **MANTENIMIENTO**

### 🔄 **REINICIO AUTOMÁTICO**
```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/desarroyo-webhook.service
```

### 📝 **CONTENIDO DEL SERVICIO**
```ini
[Unit]
Description=DesArroyo Tech Webhook
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/desarroyo-form
ExecStart=/bin/bash /home/pi/desarroyo-form/start_webhook.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 🔧 **ACTIVAR SERVICIO**
```bash
sudo systemctl daemon-reload
sudo systemctl enable desarroyo-webhook
sudo systemctl start desarroyo-webhook
```

---

## 💡 **CONSEJOS FINALES**

### 🎯 **PARA TRASLADOS:**
1. **Apagar correctamente:** `sudo shutdown -h now`
2. **En nueva casa:** Configurar WiFi nuevo
3. **Ejecutar:** `./start_webhook.sh`
4. **Actualizar Twilio:** Nueva URL ngrok

### 📊 **MONITOREO:**
```bash
# Ver logs del webhook
tail -f /var/log/syslog | grep desarroyo

# Ver estado del servicio
sudo systemctl status desarroyo-webhook
```

### 🚀 **PRÓXIMOS PASOS:**
1. **Probar con 10 llamadas**
2. **Analizar tasa de respuesta**
3. **Optimizar mensajes**
4. **Escalar sistema**

---

## 🤔 **¿EMPEZAMOS?**

**¿Tienes todo preparado?**
- Raspberry Pi
- Tarjeta SD
- Cables
- Monitor, teclado, ratón

**¿Cuánto tiempo tienes disponible?**
- 2-3 horas seguidas recomendado
- Podemos hacerlo por fases

**¿Empezamos ahora?** 🚀 