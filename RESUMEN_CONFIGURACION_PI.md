# 🎉 RESUMEN CONFIGURACIÓN RASPBERRY PI 24/7

## ✅ ESTADO ACTUAL
- **Raspberry Pi**: Conectado y funcionando (IP: 192.168.0.28)
- **SSH**: Configurado y accesible
- **Sistema**: Debian GNU/Linux con kernel 6.12.25
- **Archivos**: Todos los archivos listos para transferir

## 📁 ARCHIVOS CREADOS

### 1. **webhook_raspberry.py**
- Webhook principal con ofertas de desarrollo web en 48h
- Mensajes en español con voz femenina (Polly.Lucia)
- Horario comercial: L-V 9-14h, 16-20h
- Funcionalidad SMS para interesados
- Logging completo de interacciones

### 2. **instalar_webhook.sh**
- Script de instalación completamente automatizado
- Instala Python, Flask, Twilio, ngrok
- Configura servicio systemd para arranque automático
- Crea scripts de utilidad (ver_estado.sh, reiniciar.sh)

### 3. **env_template**
- Archivo de configuración con todas las variables
- Incluye credenciales Twilio, ngrok, configuración horarios
- Fácil de editar después de la instalación

### 4. **requirements.txt**
- Todas las dependencias Python necesarias
- Versiones específicas para compatibilidad

### 5. **desarroyo-webhook.service**
- Servicio systemd para funcionamiento 24/7
- Arranque automático después de reboot
- Reinicio automático si falla

## 🚀 INSTALACIÓN AUTOMÁTICA

### **OPCIÓN 1: Instalación con un solo comando**
```bash
./transferir_a_pi.sh
```

Este script:
1. ✅ Verifica conexión al Pi
2. ✅ Transfiere todos los archivos
3. ✅ Ejecuta instalación automática
4. ✅ Configura servicio systemd
5. ✅ Crea scripts de utilidad

### **OPCIÓN 2: Instalación manual paso a paso**
1. Conectarse al Pi: `ssh pi@raspberrypi.local`
2. Seguir la guía: `GUIA_RASPBERRY_PI_PASO_A_PASO.md`

## 🔧 CONFIGURACIÓN FINAL

### **En el Raspberry Pi:**
```bash
# 1. Conectarse al Pi
ssh pi@raspberrypi.local

# 2. Editar configuración
nano ~/desarroyo-webhook/.env

# 3. Configurar ngrok
ngrok config add-authtoken TU_TOKEN_AQUI

# 4. Iniciar servicio
sudo systemctl start desarroyo-webhook.service

# 5. Verificar estado
cd ~/desarroyo-webhook && ./ver_estado.sh
```

### **Credenciales necesarias:**
- **TWILIO_ACCOUNT_SID**: De tu cuenta Twilio
- **TWILIO_AUTH_TOKEN**: De tu cuenta Twilio
- **TWILIO_PHONE_NUMBER**: +18109579712 (ya configurado)
- **NGROK_AUTH_TOKEN**: De https://dashboard.ngrok.com

## 🌐 FUNCIONAMIENTO 24/7

### **Servicio automático:**
- ✅ Arranque automático al encender el Pi
- ✅ Reinicio automático si hay errores
- ✅ Logs detallados para debugging
- ✅ Panel de control ngrok en http://localhost:4040

### **Comandos útiles:**
```bash
# Ver estado del webhook
./ver_estado.sh

# Reiniciar webhook
./reiniciar.sh

# Ver logs en tiempo real
sudo journalctl -u desarroyo-webhook.service -f

# Parar servicio
sudo systemctl stop desarroyo-webhook.service

# Iniciar servicio
sudo systemctl start desarroyo-webhook.service
```

## 📱 CONFIGURACIÓN TWILIO

### **Paso final:**
1. Ejecutar `./ver_estado.sh` en el Pi
2. Copiar la URL de ngrok (ej: https://abc123.ngrok-free.app)
3. Ir a [Twilio Console](https://console.twilio.com/us1/develop/phone-numbers/manage/incoming)
4. Actualizar webhook a: `https://abc123.ngrok-free.app/webhook-llamada`

## 🔥 CARACTERÍSTICAS DEL WEBHOOK

### **Mensajes personalizados:**
- ✅ **Nunca dice "Soy Alberto"** → Dice "Soy un agente comercial de DesArroyo.tech"
- ✅ **Oferta 48 horas**: Desarrollo web profesional
- ✅ **SMS informativos**: Solo para interesados
- ✅ **Horario comercial**: Mensajes diferentes dentro/fuera horario
- ✅ **Español nativo**: Voz femenina Polly.Lucia

### **Funcionalidades avanzadas:**
- ✅ **Registro completo**: Todas las interacciones en JSON
- ✅ **Manejo de errores**: Respuestas elegantes ante fallos
- ✅ **Rate limiting**: Control de llamadas por hora
- ✅ **Health checks**: Endpoints de estado y salud

## 💰 COSTOS

### **Raspberry Pi (una vez configurado):**
- ✅ **Costo mensual**: €0 (solo consumo eléctrico ~€2/mes)
- ✅ **Disponibilidad**: 24/7 automática
- ✅ **Escalabilidad**: Ilimitada dentro de límites Twilio
- ✅ **Mantenimiento**: Mínimo después de configuración

### **Comparación con alternativas:**
- **Vercel**: No soporta webhooks Twilio
- **Heroku**: €25-50/mes
- **AWS Lambda**: €10-30/mes
- **VPS**: €15-40/mes

## 📞 FLUJO DE LLAMADAS

### **Llamada entrante:**
1. 📱 Twilio recibe llamada
2. 🌐 Webhook en Pi procesa
3. 🗣️ Mensaje en español con oferta 48h
4. ⌨️ Usuario pulsa 1 (interesado) o 2 (no interesado)
5. 💌 Si interesado → SMS automático con info completa
6. 📊 Registro completo en logs

### **Horarios:**
- **L-V 9-14h, 16-20h**: Mensaje horario comercial
- **Resto**: Mensaje fuera horario comercial
- **Fines de semana**: Mensaje fuera horario comercial

## 🆘 SOPORTE Y MANTENIMIENTO

### **Archivos importantes:**
- **~/desarroyo-webhook/webhook.log**: Logs del webhook
- **~/desarroyo-webhook/interacciones.json**: Registro de llamadas
- **~/desarroyo-webhook/.env**: Configuración
- **~/desarroyo-webhook/ngrok.log**: Logs de ngrok

### **Problemas comunes:**
- **Webhook no responde**: `./reiniciar.sh`
- **Ngrok URL cambió**: Actualizar en Twilio Console
- **Servicio no arranca**: Verificar logs con `journalctl`

## 🎯 PRÓXIMOS PASOS

1. **Ahora**: Ejecutar `./transferir_a_pi.sh`
2. **Después**: Configurar credenciales en `.env`
3. **Luego**: Obtener token ngrok y configurar
4. **Finalmente**: Iniciar servicio y actualizar Twilio

---

**¡Tu sistema 24/7 está listo! 🚀** 