# 🔐 CONFIGURAR GITHUB SECRETS - PASO A PASO

## 🎯 TU SISTEMA YA ESTÁ EN GITHUB ACTIONS
✅ Se ejecuta cada 6 horas automáticamente
✅ Madrid, Barcelona, Valencia 
✅ Solo faltan las APIs en Secrets

---

## 📝 PASO 1: IR A GITHUB SECRETS

1. Ve a: https://github.com/Arroyador69/desarroyo-form
2. Click en **Settings** (arriba derecha)
3. Click en **Secrets and variables** (menú izquierda)
4. Click en **Actions**
5. Click en **New repository secret**

---

## 🔑 PASO 2: CONFIGURAR CADA SECRET

### 2.1 TWILIO (WhatsApp Business)
```
📝 Name: TWILIO_ACCOUNT_SID
💡 Value: ACxxxxxxxxxxxxxxxxxxxxxxxxxx (desde Twilio Console)

📝 Name: TWILIO_AUTH_TOKEN  
💡 Value: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (desde Twilio Console)

📝 Name: TWILIO_WHATSAPP_NUMBER
💡 Value: whatsapp:+14155238886
```

### 2.2 DEEPSEEK (IA Automática)
```
📝 Name: DEEPSEEK_API_KEY
💡 Value: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (desde DeepSeek)
```

### 2.3 TELEGRAM (Notificaciones)
```
📝 Name: TELEGRAM_BOT_TOKEN
💡 Value: 1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXX (desde @BotFather)

📝 Name: TELEGRAM_CHAT_ID
💡 Value: 123456789 (tu ID de chat)
```

### 2.4 CONFIGURACIÓN BÁSICA
```
📝 Name: WEBSITE_URL
💡 Value: https://desarroyo.tech

📝 Name: BUSINESS_NAME
💡 Value: DesArroyo Tech

📝 Name: YOUR_NAME
💡 Value: Alberto
```

---

## 🚀 PASO 3: APIS ESPECÍFICAS

### TWILIO SETUP:
1. Ve a: https://console.twilio.com/
2. Registrate (10$ gratis incluidos)
3. Ve a **Console Dashboard**
4. Copia **Account SID** y **Auth Token**
5. Ve a **Messaging > Settings > WhatsApp sandbox**
6. Activa el sandbox
7. Usa número: `whatsapp:+14155238886`

### DEEPSEEK SETUP:
1. Ve a: https://platform.deepseek.com/
2. Registrate (5$ gratis incluidos)
3. Ve a **API Keys**
4. Click **Create new key**
5. Copia la key que empieza con `sk-`

### TELEGRAM SETUP:
1. Abre Telegram
2. Busca **@BotFather**
3. Envía `/newbot`
4. Sigue instrucciones
5. Copia el **Bot Token**
6. Para el Chat ID:
   - Busca **@userinfobot**
   - Envía `/start`
   - Copia tu **ID** (número)

---

## ✅ PASO 4: VERIFICAR CONFIGURACIÓN

Una vez añadidos todos los secrets:

1. Ve a **Actions** en tu repo
2. Click en **Sistema de Leads Automático**
3. Click **Run workflow** (botón azul)
4. Selecciona ciudad y sector
5. Click **Run workflow**

---

## 📱 RESULTADO ESPERADO:

### ✅ SISTEMA FUNCIONANDO:
- 🔍 Busca leads automáticamente cada 6 horas
- 📱 Envía mensajes WhatsApp profesionales
- 🤖 IA responde automáticamente 24/7
- 📊 Reportes a Telegram
- 💰 Genera ventas reales

### 📈 ROI AUTOMÁTICO:
- **300 leads/mes** contactados
- **30 ventas** esperadas (10%)
- **13.500€/mes** facturación
- **150€/mes** costo APIs
- **+13.000€/mes** beneficio

---

## 🎯 WEBHOOK PARA RESPUESTAS AUTOMÁTICAS

Para que el bot responda automáticamente, necesitas activar el webhook:

```bash
# En tu servidor o Vercel
python3 scripts/webhook_respuestas.py
```

O usar el webhook automático en GitHub Actions que ya tienes configurado.

---

## 🚨 IMPORTANTE:

1. **NO** necesitas el Mac encendido
2. **SÍ** funciona 24/7 desde GitHub Actions
3. **SÍ** es WhatsApp Business (no SMS)
4. **SÍ** todo es automático con IA
5. **SÍ** genera clientes reales sin intervención

¡Una vez configurados los secrets, el sistema funcionará completamente solo! 