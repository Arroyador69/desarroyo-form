# 🤖 Configuración de DeepSeek en Vercel

## 🚀 Pasos para Activar el Generador de Shortcuts con IA

### **Paso 1: Obtener API Key de DeepSeek**

1. **Ve a DeepSeek Platform:**
   - URL: https://platform.deepseek.com/
   - Regístrate o inicia sesión

2. **Crear API Key:**
   - Ve a "API Keys" en el dashboard
   - Haz clic en "Create New API Key"
   - Dale un nombre (ej: "DesArroyo Shortcuts")
   - Copia la API key generada

### **Paso 2: Configurar en Vercel**

1. **Ve al Dashboard de Vercel:**
   - URL: https://vercel.com/dashboard
   - Selecciona tu proyecto "desarroyo-form"

2. **Añadir Variable de Entorno:**
   - Ve a "Settings" → "Environment Variables"
   - Haz clic en "Add New"
   - **Name:** `DEEPSEEK_API_KEY`
   - **Value:** `tu_api_key_deepseek_aqui`
   - **Environment:** Production
   - Haz clic en "Save"

3. **Redesplegar:**
   - Ve a "Deployments"
   - Haz clic en "Redeploy" en el último deployment

### **Paso 3: Verificar Funcionamiento**

1. **Ve al Dashboard:**
   - URL: https://desarroyo-form.vercel.app/dashboard
   - Login: `admin` / `admin123`

2. **Probar Generador:**
   - Ve a "Shortcuts iPhone"
   - Usa el "🤖 Generador de Shortcuts con IA"
   - Crea un shortcut de prueba

## ✅ **Resultado Esperado**

Una vez configurado, deberías ver:
- ✅ No más errores de "DeepSeek API no configurada"
- ✅ Generación exitosa de shortcuts
- ✅ QR codes funcionando
- ✅ Shortcuts que se instalan en iPhone

## 🔧 **Solución Alternativa Temporal**

Si no tienes API key de DeepSeek, puedes:

1. **Usar el generador básico** (sin IA)
2. **Crear shortcuts manualmente** con la estructura correcta
3. **Usar plantillas predefinidas**

## 📞 **Soporte**

Si necesitas ayuda:
- Email: alberto@desarroyo.tech
- Telegram: @desarroyo_tech

---

**¡Con DeepSeek configurado, tendrás el generador de shortcuts más potente del mundo!** 🚀 