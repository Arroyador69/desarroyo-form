# 🔧 **GUÍA GITHUB SECRETS - PASO A PASO**

## 🎯 **OBJETIVO:** Configurar tus API Keys en GitHub para que la automatización funcione

---

## 📝 **PASOS DETALLADOS:**

### **🔸 PASO 1: Acceder a tu repositorio**
1. Ve a **GitHub.com**
2. **Inicia sesión** con tu cuenta
3. Ve a tu repositorio **`desarroyo-form`**
4. ✅ **Verificar:** Estás en la página principal de tu repo

### **🔸 PASO 2: Ir a Settings**
1. **Click en la pestaña "Settings"** (esquina superior derecha)
2. ✅ **Verificar:** Estás en la página de configuración del repositorio

### **🔸 PASO 3: Acceder a Secrets**
1. En el **menú lateral izquierdo**, busca la sección **"Security"**
2. **Click en "Secrets and variables"**
3. **Click en "Actions"**
4. ✅ **Verificar:** Ves una página que dice "Repository secrets"

### **🔸 PASO 4: Crear cada Secret**

**Para CADA una de estas 9 configuraciones:**

#### **SECRET 1: DEEPSEEK_API_KEY**
1. **Click en "New repository secret"**
2. **Name:** `DEEPSEEK_API_KEY`
3. **Secret:** `[TU_DEEPSEEK_KEY_AQUI]`
4. **Click "Add secret"**

#### **SECRET 2: TWILIO_ACCOUNT_SID**
1. **Click en "New repository secret"**
2. **Name:** `TWILIO_ACCOUNT_SID`
3. **Secret:** `[TU_TWILIO_SID_AQUI]`
4. **Click "Add secret"**

#### **SECRET 3: TWILIO_AUTH_TOKEN**
1. **Click en "New repository secret"**
2. **Name:** `TWILIO_AUTH_TOKEN`
3. **Secret:** `[TU_TWILIO_TOKEN_AQUI]`
4. **Click "Add secret"**

#### **SECRET 4: TWILIO_WHATSAPP_NUMBER**
1. **Click en "New repository secret"**
2. **Name:** `TWILIO_WHATSAPP_NUMBER`
3. **Secret:** `[TU_NUMERO_WHATSAPP_AQUI]`
4. **Click "Add secret"**

#### **SECRET 5: TELEGRAM_BOT_TOKEN**
1. **Click en "New repository secret"**
2. **Name:** `TELEGRAM_BOT_TOKEN`
3. **Secret:** `[TU_BOT_TOKEN_AQUI]`
4. **Click "Add secret"**

#### **SECRET 6: TELEGRAM_CHAT_ID**
1. **Click en "New repository secret"**
2. **Name:** `TELEGRAM_CHAT_ID`
3. **Secret:** `[TU_CHAT_ID_AQUI]`
4. **Click "Add secret"**

#### **SECRET 7: WEBSITE_URL**
1. **Click en "New repository secret"**
2. **Name:** `WEBSITE_URL`
3. **Secret:** `https://desarroyo.tech`
4. **Click "Add secret"**

#### **SECRET 8: BUSINESS_NAME**
1. **Click en "New repository secret"**
2. **Name:** `BUSINESS_NAME`
3. **Secret:** `DesArroyo Tech`
4. **Click "Add secret"**

#### **SECRET 9: YOUR_NAME**
1. **Click en "New repository secret"**
2. **Name:** `YOUR_NAME`
3. **Secret:** `Alberto`
4. **Click "Add secret"**

---

## ✅ **VERIFICACIÓN FINAL:**

Al final deberías ver **9 secrets** en tu lista:
- ✅ DEEPSEEK_API_KEY
- ✅ TWILIO_ACCOUNT_SID  
- ✅ TWILIO_AUTH_TOKEN
- ✅ TWILIO_WHATSAPP_NUMBER
- ✅ TELEGRAM_BOT_TOKEN
- ✅ TELEGRAM_CHAT_ID
- ✅ WEBSITE_URL
- ✅ BUSINESS_NAME
- ✅ YOUR_NAME

---

## 🚀 **PRIMERA PRUEBA:**

### **🔸 PASO 5: Ejecutar el workflow**
1. **Ve a la pestaña "Actions"** (arriba en tu repo)
2. **Click en "Sistema de Leads Automático"** (workflow de la izquierda)
3. **Click en "Run workflow"** (botón azul a la derecha)
4. **Configurar:**
   - **Ciudad:** `Madrid`
   - **Sector:** `restaurantes`
5. **Click "Run workflow"**

### **🔸 PASO 6: Verificar ejecución**
1. **Refresh la página** después de 30 segundos
2. **Verás una nueva ejecución** con estado "running" o "completed"
3. **Click en la ejecución** para ver los logs
4. ✅ **Verificar:** No hay errores en rojo

---

## 📱 **VERIFICAR EN TELEGRAM:**

**En los próximos 5-10 minutos deberías recibir:**

```
🚀 LEADS CONTACTADOS - RESTAURANTES

📍 Ciudad: Madrid
🏢 Sector: restaurantes
📱 Contactados: 3
⭐ Score promedio: 78.5/100

📊 DETALLES:
1. 🇪🇸 Restaurante El Buen Sabor (85/100)
2. 🇪🇸 Pizzería La Italiana (80/100)  
3. 🇪🇸 Tapas Casa Manolo (70/100)

💰 Costo estimado: $0.15-0.30
⏰ Próxima ejecución: En 6 horas
```

---

## 🚨 **SI ALGO SALE MAL:**

### **Error común 1: "Secret not found"**
- ✅ **Verificar:** Nombres de secrets exactos (case-sensitive)
- ✅ **Verificar:** Sin espacios extra

### **Error común 2: "API key invalid"**  
- ✅ **Verificar:** API keys copiados completos
- ✅ **Verificar:** Sin espacios al principio/final

### **Error común 3: "Workflow not triggered"**
- ✅ **Verificar:** Estás en la rama correcta (main)
- ✅ **Verificar:** El archivo `.github/workflows/generar_leads.yml` existe

---

## 🎯 **¡LISTO PARA EMPEZAR!**

Una vez configurado, **tu sistema funcionará automáticamente cada 6 horas** y **recibirás leads calientes directamente en Telegram**.

**¡Solo tienes que responder a los leads que lleguen! 🚀** 