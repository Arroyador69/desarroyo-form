# 🚀 INSTALACIÓN COMPLETA - SISTEMA SIN n8n

## ✅ **AHORRO TOTAL: $828/año eliminando n8n**

Tu sistema ahora funciona **100% en GitHub Actions GRATIS** - sin servidores, sin n8n, sin complicaciones.

---

## 📋 **CONFIGURACIÓN EN 5 PASOS**

### **PASO 1: Configurar Secrets en GitHub**

Ve a tu repositorio GitHub → Settings → Secrets and variables → Actions → New repository secret

```bash
# APIs NECESARIAS
OPENAI_API_KEY=sk-tu_key_aqui
TWILIO_ACCOUNT_SID=tu_sid_aqui  
TWILIO_AUTH_TOKEN=tu_token_aqui
TWILIO_WHATSAPP_NUMBER=+1234567890

# TELEGRAM (GRATIS)
TELEGRAM_BOT_TOKEN=tu_bot_token
TELEGRAM_CHAT_ID=tu_chat_id

# TU CONFIGURACIÓN
WEBSITE_URL=https://desarroyo.tech
BUSINESS_NAME=DesArroyo Tech
YOUR_NAME=Alberto
```

### **PASO 2: Obtener API Keys**

#### **🤖 OpenAI ($20/mes)**
1. Ve a https://platform.openai.com/
2. Crea cuenta → API Keys → Create new secret key
3. Copia la key que empieza por `sk-`

#### **📱 Twilio WhatsApp ($15/mes)**
1. Ve a https://www.twilio.com/
2. Crea cuenta → Console → Account SID y Auth Token
3. Configurar WhatsApp: Console → Messaging → WhatsApp → Sandbox
4. Copia tu número WhatsApp sandbox

#### **📢 Telegram (GRATIS)**
1. Busca @BotFather en Telegram
2. Envía `/newbot` y sigue instrucciones
3. Copia el token que te da
4. Para Chat ID: busca @userinfobot y envía `/start`

### **PASO 3: Activar GitHub Actions**

```bash
# Tu archivo ya está creado: .github/workflows/generar_leads.yml
# Solo necesitas hacer commit y push
git add .
git commit -m "🚀 Sistema de leads automático sin n8n"
git push
```

### **PASO 4: Verificar Funcionamiento**

1. Ve a tu repo → Actions tab
2. Deberías ver "Sistema de Leads Automático - DesArroyo Tech"
3. Haz clic en "Run workflow" para probar manualmente
4. Revisa los logs para ver si todo funciona

### **PASO 5: ¡Relajate!**

El sistema ahora funciona automáticamente:
- ⏰ **Cada 6 horas** busca leads
- 📱 **Contacta automáticamente** por WhatsApp  
- 📊 **Te notifica** por Telegram
- 💾 **Guarda historial** en GitHub

---

## 🔧 **PERSONALIZACIÓN**

### **Cambiar Ciudades y Sectores:**

Edita `.github/workflows/generar_leads.yml`:

```yaml
# Línea 45: Madrid - Restaurantes
- name: 🔍 Ejecutar scraping Madrid - Restaurantes
  run: python3 scripts/sistema_leads_completo.py Madrid restaurantes

# Línea 60: Barcelona - Peluquerías  
- name: 🔍 Ejecutar scraping Barcelona - Peluquerías
  run: python3 scripts/sistema_leads_completo.py Barcelona peluquerias

# Línea 75: Valencia - Dentistas
- name: 🔍 Ejecutar scraping Valencia - Dentistas
  run: python3 scripts/sistema_leads_completo.py Valencia dentistas

# AÑADIR MÁS:
- name: 🔍 Sevilla - Abogados
  run: python3 scripts/sistema_leads_completo.py Sevilla abogados
```

### **Cambiar Frecuencia:**

```yaml
# Línea 5: Cada 6 horas
schedule:
  - cron: '0 */6 * * *'

# OPCIONES:
# Cada 4 horas: '0 */4 * * *'
# Cada 12 horas: '0 */12 * * *'  
# Solo 9AM y 6PM: '0 9,18 * * *'
# Solo días laborales: '0 */6 * * 1-5'
```

---

## 📊 **MONITOREO**

### **Ver Logs en Tiempo Real:**
1. GitHub → Actions → Último workflow
2. Clic en cualquier job
3. Ver logs detallados

### **Notificaciones Telegram:**
- 📱 Cada lead contactado
- 📊 Reporte diario completo
- ❌ Errores si los hay

### **Archivo de Duplicados:**
- Se guarda automáticamente en `leads_enviados.json`
- GitHub lo mantiene entre ejecuciones
- Nunca contacta el mismo lead dos veces

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **"Workflow failed"**
1. Ve a Actions → clic en el workflow fallido
2. Lee el error en los logs
3. Probablemente sea un Secret mal configurado

### **"No leads found"**
- Normal al principio
- Las páginas web cambian selectores CSS
- El script incluye datos de prueba

### **"WhatsApp/Telegram errors"**
- Revisa que los Secrets estén bien
- Verifica que las APIs funcionen individualmente

### **"Rate limits"**
- GitHub Actions: 2000 minutos/mes gratis
- OpenAI: $20/mes incluye muchas llamadas
- Twilio: $15/mes incluye mensajes

---

## ⚡ **OPTIMIZACIONES AVANZADAS**

### **Múltiples Ciudades Paralelas:**
```yaml
strategy:
  matrix:
    ciudad: [Madrid, Barcelona, Valencia, Sevilla, Bilbao]
    sector: [restaurantes, peluquerias, dentistas]
```

### **Diferentes Horarios por Sector:**
```yaml
# Restaurantes por la mañana
- cron: '0 9 * * *'  
# Servicios por la tarde  
- cron: '0 15 * * *'
```

### **Backup Automático:**
```yaml
- name: 📤 Backup leads
  run: |
    git config --global user.name 'GitHub Actions'
    git add leads_enviados.json
    git commit -m "📊 Backup automático leads $(date)"
    git push
```

---

## 🎉 **¡FUNCIONANDO!**

Tu sistema ahora:
- ✅ **Cuesta $35/mes** vs $104/mes antes ($828/año ahorrados)
- ✅ **100% automático** en GitHub 
- ✅ **Sin dependencias** de n8n o servidores
- ✅ **Fácil de modificar** y escalar
- ✅ **Logs transparentes** y debugging simple
- ✅ **Backup automático** en Git

**¡Es infinitamente mejor que n8n!** 🚀 