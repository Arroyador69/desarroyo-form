# ✅ **CHECKLIST CONFIGURACIÓN RÁPIDA - 30 MINUTOS**

## 🎯 **OBJETIVO: Tener leads automáticos funcionando HOY**

### **☑️ PASO 1: API DE DEEPSEEK (10 minutos)**

- [ ] Ir a https://platform.deepseek.com/
- [ ] Registrarse con email
- [ ] Verificar email
- [ ] Ir a "API Keys"
- [ ] Crear nueva API key
- [ ] Copiar key (empieza con `sk-`)
- [ ] ✅ **LISTO**: `DEEPSEEK_API_KEY=sk-xxxxxxxxxx`

### **☑️ PASO 2: TWILIO WHATSAPP (10 minutos)**

- [ ] Ir a https://www.twilio.com/
- [ ] Registrarse y verificar teléfono
- [ ] Ir a Console > Settings > API keys & tokens
- [ ] Copiar Account SID
- [ ] Copiar Auth Token
- [ ] Ir a Messaging > WhatsApp sandbox
- [ ] Copiar número WhatsApp (ej: +14155238886)
- [ ] ✅ **LISTO**: 
  - `TWILIO_ACCOUNT_SID=ACxxxxxxxxxx`
  - `TWILIO_AUTH_TOKEN=xxxxxxxxxx`
  - `TWILIO_WHATSAPP_NUMBER=+14155238886`

### **☑️ PASO 3: BOT TELEGRAM (5 minutos)**

- [ ] Abrir Telegram
- [ ] Buscar "@BotFather"
- [ ] Enviar `/newbot`
- [ ] Nombre del bot: "DesArroyo Leads Bot"
- [ ] Username: "desarroyo_leads_bot"
- [ ] Copiar token del bot
- [ ] Buscar "@userinfobot"
- [ ] Enviar `/start`
- [ ] Copiar Chat ID
- [ ] ✅ **LISTO**:
  - `TELEGRAM_BOT_TOKEN=xxxxxxxxxx:xxxxxxxxxxx`
  - `TELEGRAM_CHAT_ID=xxxxxxxxxx`

### **☑️ PASO 4: CONFIGURAR GITHUB SECRETS (5 minutos)**

- [ ] Ir a GitHub > tu repo > Settings > Secrets and variables > Actions
- [ ] Crear estos secrets:

```
Nombre: DEEPSEEK_API_KEY
Valor: sk-tu_key_aqui

Nombre: TWILIO_ACCOUNT_SID  
Valor: ACtu_sid_aqui

Nombre: TWILIO_AUTH_TOKEN
Valor: tu_token_aqui

Nombre: TWILIO_WHATSAPP_NUMBER
Valor: +14155238886

Nombre: TELEGRAM_BOT_TOKEN
Valor: tu_bot_token_aqui

Nombre: TELEGRAM_CHAT_ID
Valor: tu_chat_id_aqui

Nombre: WEBSITE_URL
Valor: https://desarroyo.tech

Nombre: BUSINESS_NAME
Valor: DesArroyo Tech

Nombre: YOUR_NAME
Valor: Alberto
```

- [ ] ✅ **LISTO**: 9 secrets configurados

---

## 🚀 **PRIMERA PRUEBA (5 minutos)**

### **☑️ OPCIÓN A: Ejecutar desde GitHub**
- [ ] Ir a tu repo > Actions
- [ ] Click en "Sistema de Leads Automático"
- [ ] Click "Run workflow"
- [ ] Ciudad: Madrid
- [ ] Sector: restaurantes
- [ ] Click "Run workflow"
- [ ] ✅ **VERIFICAR**: Que se ejecute sin errores

### **☑️ OPCIÓN B: Ejecutar localmente**
```bash
cd desarroyo-form
python3 scripts/sistema_leads_avanzado.py Madrid restaurantes
```

---

## 📱 **VERIFICACIONES FINALES**

### **☑️ ¿FUNCIONÓ CORRECTAMENTE?**

- [ ] **Telegram**: ¿Recibiste notificación de leads contactados?
- [ ] **GitHub Actions**: ¿Se ejecutó sin errores?
- [ ] **Base de datos**: ¿Se crearon archivos de leads?
- [ ] **WhatsApp**: ¿Se enviaron mensajes? (verificar en logs)

### **☑️ DASHBOARD CRM**
- [ ] Ir a https://desarroyo.tech/dashboard
- [ ] Login: admin / admin123
- [ ] ✅ **VERIFICAR**: Ver leads capturados

### **☑️ RESPUESTAS AUTOMÁTICAS**
- [ ] Webhook funcionando: `scripts/webhook_respuestas.py`
- [ ] Encuesta disponible en: `https://desarroyo.tech/generador_automatizaciones.html`
- [ ] ✅ **VERIFICAR**: Sistema responde automáticamente

---

## 🎯 **CONFIGURACIÓN AUTOMÁTICA**

### **☑️ AUTOMATIZACIÓN ACTIVA**
- [ ] GitHub Actions ejecutándose cada 6 horas
- [ ] Sectores configurados: restaurantes, peluquerias, dentistas, abogados
- [ ] Ciudades objetivo: Madrid, Barcelona, Valencia, Sevilla, Bilbao

### **☑️ PRÓXIMOS PASOS**
- [ ] Preparar respuestas comerciales para leads calientes
- [ ] Configurar tu teléfono para responder rápido
- [ ] Tener presupuestos listos (299€, 499€, 799€)
- [ ] Preparar ejemplos de webs anteriores

---

## 🚨 **SI ALGO NO FUNCIONA**

### **Errores Comunes:**

1. **"Error API DeepSeek"**
   - [ ] Verificar que el API key es correcto
   - [ ] Verificar que tienes crédito en DeepSeek

2. **"Error Twilio WhatsApp"**  
   - [ ] Verificar que estás usando el sandbox number
   - [ ] Verificar que tienes crédito en Twilio

3. **"Error Telegram"**
   - [ ] Verificar bot token
   - [ ] Verificar chat ID
   - [ ] Enviar `/start` a tu bot primero

4. **"No se encuentran leads"**
   - [ ] Es normal, algunos sectores/ciudades tienen pocos leads
   - [ ] Probar con "restaurantes" en "Madrid" (siempre hay)

---

## 📞 **PRIMER LEAD CALIENTE - ¿QUÉ HACER?**

Cuando recibas esto en Telegram:

```
🎉 ¡ENCUESTA COMPLETADA - LEAD CALIENTE!

📋 Negocio: Restaurante El Buen Sabor
📞 Teléfono: +34600123456
💰 Presupuesto: 500-1000€
⏰ Urgencia: En 1-2 semanas
```

### **☑️ ACCIÓN INMEDIATA:**
- [ ] Llamar en máximo 30 minutos
- [ ] Script: "Hola, soy Alberto de DesArroyo Tech. He visto que has completado la encuesta para la web de [NOMBRE NEGOCIO]. ¿Tienes 5 minutos para que te explique cómo podemos ayudarte?"
- [ ] Preparar propuesta personalizada
- [ ] Enviar presupuesto en 24h máximo

---

## 🎯 **EXPECTATIVAS REALÍSTICAS**

### **Primeros 7 días:**
- [ ] 20-50 leads contactados
- [ ] 2-8 respuestas interesadas  
- [ ] 1-3 encuestas completadas
- [ ] 0-1 clientes convertidos

### **Después de 1 mes:**
- [ ] 200+ leads contactados
- [ ] 20+ respuestas interesadas
- [ ] 10+ encuestas completadas  
- [ ] 3-8 clientes convertidos

**ROI:** Con 1 cliente/semana a 500€ = 2000€/mes vs 28€/mes de costos = **ROI de 7000%**

---

## ✅ **CONFIGURACIÓN COMPLETADA**

Si has marcado todas las casillas: **¡FELICIDADES! Tu sistema de leads automático está funcionando.**

### **Próximos pasos automáticos:**
- [x] Sistema busca leads cada 6 horas
- [x] IA genera mensajes personalizados
- [x] WhatsApp envía mensajes automáticamente  
- [x] Sistema responde a interesados
- [x] Envía encuestas automáticamente
- [x] Notifica leads calientes por Telegram
- [x] CRM gestiona todo automáticamente

**¡Solo tienes que responder a los leads calientes que lleguen a tu Telegram! 🚀** 