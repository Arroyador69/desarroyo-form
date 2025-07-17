# 🚚 GUÍA COMPLETA: TRASLADO DE RASPBERRY PI

## 📋 **CHECKLIST PRE-TRASLADO**

### 🔧 **ANTES DE DESCONECTAR:**
- [ ] Anotar **IP local actual** de la Raspberry Pi
- [ ] Hacer **backup** de archivos importantes
- [ ] Verificar que tienes **acceso a Twilio Console**
- [ ] Apuntar **URL ngrok actual** (si la necesitas)
- [ ] **Apagar correctamente** la Raspberry Pi: `sudo shutdown -h now`

### 📦 **PARA EL TRASLADO:**
- [ ] **Desconectar** cables de alimentación
- [ ] **Proteger** la Raspberry Pi (caja antiestática)
- [ ] **Llevar** cable de alimentación y cables de red
- [ ] **Llevar** tarjeta SD de backup (si tienes)

---

## 🏠 **UBICACIÓN IDEAL EN LA NUEVA CASA**

### 📍 **LUGAR RECOMENDADO:**
```
🏠 CASA NUEVA
├── 📡 Router WiFi (ubicación central)
├── 💻 Zona de trabajo
└── 🖥️ Raspberry Pi (cerca del router)
```

### ✅ **CRITERIOS DE UBICACIÓN:**
- **📶 Señal WiFi fuerte** (al menos 3 barras)
- **🌡️ Lugar fresco** (no cerca de radiadores)
- **🌬️ Ventilación adecuada** (no en espacios cerrados)
- **🔌 Fuente de alimentación estable**
- **🛠️ Acceso fácil** para mantenimiento
- **🧹 Protegida del polvo**

### 📋 **OPCIONES POR UBICACIÓN:**

#### 🏠 **SALON/SALA:**
- ✅ **Ventajas:** Señal WiFi fuerte, acceso fácil
- ⚠️ **Desventajas:** Puede estar expuesta, polvo

#### 🏢 **DESPACHO/OFICINA:**
- ✅ **Ventajas:** Protegida, profesional, acceso fácil
- ✅ **Recomendada:** La mejor opción

#### 🏠 **DORMITORIO:**
- ⚠️ **Desventajas:** Puede ser ruidosa, señal WiFi débil

#### 🏠 **COCINA:**
- ❌ **No recomendada:** Humedad, calor, grasa

---

## 🔄 **PROCESO DE REACTIVACIÓN**

### 🚀 **PASO 1: CONECTAR EN NUEVA CASA**
1. **Conectar** alimentación a la Raspberry Pi
2. **Conectar** cable Ethernet (opcional pero recomendado)
3. **Encender** la Raspberry Pi
4. **Esperar** 2-3 minutos para que inicie

### 🌐 **PASO 2: CONFIGURAR WIFI**
```bash
# Si necesitas configurar WiFi nuevo
sudo raspi-config
# Seleccionar: Network Options → WiFi
# Introducir nombre y contraseña de la nueva red
```

### 🚀 **PASO 3: EJECUTAR REACTIVACIÓN**
```bash
# Ir al directorio del proyecto
cd /home/pi/desarroyo-form

# Ejecutar script de reactivación
python reactivar_raspberry_nueva_casa.py
```

### 🔧 **PASO 4: CONFIGURAR TWILIO**
1. **Ir a Twilio Console**
2. **Cambiar webhook URL** por la nueva URL ngrok
3. **Hacer llamada de prueba**

---

## ⏰ **TIEMPO DE INACTIVIDAD**

### 📊 **DURANTE EL TRASLADO:**
- **⏸️ Sistema desconectado:** SÍ
- **📞 Llamadas funcionando:** NO
- **⏱️ Tiempo estimado:** 1-3 días (dependiendo del traslado)

### 🔄 **DESPUÉS DEL TRASLADO:**
- **⏱️ Tiempo de reactivación:** 10-15 minutos
- **🧪 Pruebas:** 5-10 minutos
- **🎯 Total:** 15-25 minutos hasta estar operativo

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS**

### 🌐 **PROBLEMA: Sin conexión a internet**
```bash
# Verificar conexión
ping google.com

# Verificar WiFi
iwconfig

# Reconfigurar WiFi
sudo raspi-config
```

### 📡 **PROBLEMA: ngrok no funciona**
```bash
# Verificar ngrok
which ngrok

# Reinstalar ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin/
```

### 🐍 **PROBLEMA: Webhook no inicia**
```bash
# Verificar Python
python --version

# Verificar dependencias
pip install flask requests pytz

# Ejecutar manualmente
python webhook_local_definitivo.py
```

---

## 📱 **NOTIFICACIÓN DURANTE TRASLADO**

### 📞 **PARA CLIENTES:**
Si alguien llama durante el traslado:
- **🔊 Mensaje:** "The number you have dialed is not in service"
- **📱 Alternativa:** Pueden contactar via web (desarroyo.tech)

### 💼 **PARA TI:**
- **📊 Monitoreo:** Revisa Twilio Console para ver llamadas perdidas
- **📝 Seguimiento:** Contacta clientes que llamaron durante el traslado

---

## 🎯 **RECOMENDACIONES ADICIONALES**

### 📦 **BACKUP ANTES DEL TRASLADO:**
```bash
# Hacer backup de archivos importantes
cp -r /home/pi/desarroyo-form /home/pi/backup-desarroyo-form
```

### 🔧 **CONFIGURACIÓN DE INICIO AUTOMÁTICO:**
```bash
# Crear servicio systemd para auto-inicio
sudo nano /etc/systemd/system/desarroyo-webhook.service
sudo systemctl enable desarroyo-webhook
```

### 📡 **MEJORAR ESTABILIDAD:**
- **🔌 UPS:** Considera un SAI pequeño para cortes de luz
- **🌐 4G:** Router 4G como backup si falla internet
- **📱 Monitoring:** Script para notificar si el sistema cae

---

## 📋 **CHECKLIST POST-TRASLADO**

### ✅ **VERIFICACIONES FINALES:**
- [ ] Raspberry Pi encendida y conectada
- [ ] WiFi funcionando correctamente
- [ ] ngrok iniciado y URL obtenida
- [ ] Webhook funcionando
- [ ] URL configurada en Twilio
- [ ] **Llamada de prueba exitosa**
- [ ] Sistema monitoreado por 24h

### 🎉 **¡TRASLADO COMPLETADO!**
- **🚀 Sistema:** Operativo en nueva ubicación
- **📞 Llamadas:** Funcionando correctamente
- **🔧 Mantenimiento:** Programado para verificaciones regulares

---

## 🆘 **SOPORTE DE EMERGENCIA**

### 📞 **SI ALGO FALLA:**
1. **🔍 Ejecutar:** `python reactivar_raspberry_nueva_casa.py`
2. **📊 Revisar:** Logs del sistema
3. **🧪 Probar:** Webhook manualmente
4. **📱 Contactar:** Soporte técnico si es necesario

### 💡 **ALTERNATIVA TEMPORAL:**
- **💻 Usar:** Webhook local en tu ordenador
- **🔗 ngrok:** Misma configuración pero desde tu Mac
- **⏰ Tiempo:** Hasta resolver problema en Raspberry Pi 