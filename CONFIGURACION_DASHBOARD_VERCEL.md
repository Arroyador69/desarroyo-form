# 🚀 CONFIGURACIÓN DASHBOARD ONLINE - Vercel

## 🎯 **PROBLEMA RESUELTO**
Tu dashboard no funcionaba online porque faltaban configuraciones en Vercel. ¡Ya está solucionado!

---

## 🔧 **PASO 1: AGREGAR SECRETS EN VERCEL**

**Ve a tu proyecto en Vercel → Settings → Environment Variables y agrega:**

### **🔐 NUEVOS SECRETS REQUERIDOS:**

```bash
# Autenticación del Dashboard
JWT_SECRET = desarroyo-secret-key-2024-super-seguro
ADMIN_PASSWORD = tu_contraseña_segura_123

# Ya tienes estos (verificar que estén):
TWILIO_ACCOUNT_SID = (tu valor actual)
TWILIO_AUTH_TOKEN = (tu valor actual) 
TWILIO_PHONE_NUMBER = +34617555255
TWILIO_WHATSAPP_NUMBER = (tu valor actual)
DEEPSEEK_API_KEY = (tu valor actual)
TELEGRAM_BOT_TOKEN = (tu valor actual)
TELEGRAM_CHAT_ID = (tu valor actual)
```

---

## 📋 **PASO 2: CREDENCIALES DE ACCESO**

### **Una vez configurado:**

**URL del Dashboard Online:**
```
https://desarroyo.tech/login.html
```

**Credenciales:**
```
👤 Usuario: admin
🔑 Contraseña: tu_contraseña_segura_123
```

---

## 🚀 **PASO 3: HACER DEPLOY**

```bash
# Hacer push de los cambios
git add .
git commit -m "🔧 Configurar dashboard para Vercel"
git push origin main
```

**Vercel automáticamente desplegará con las nuevas configuraciones.**

---

## ✅ **VERIFICACIÓN**

1. **Esperar deploy** (2-3 minutos)
2. **Ir a**: https://desarroyo.tech/login.html
3. **Login** con tus credenciales
4. **¡Ya tienes acceso completo al dashboard online!**

---

## 🎯 **LO QUE TENDRÁS DISPONIBLE ONLINE:**

### **📊 Dashboard Completo:**
- ✅ Gestión de clientes
- ✅ Sistema de videos  
- ✅ Generador de guiones
- ✅ Analíticas
- ✅ Sistema de llamadas (monitoreo)
- ✅ Automatizaciones

### **📞 Sistema de Llamadas:**
- ✅ Estadísticas en tiempo real
- ✅ Lista negra
- ✅ Llamadas exitosas
- ✅ Control de presupuesto

---

## 🔒 **SEGURIDAD**

### **Cambiar Contraseña por Defecto:**
1. **En Vercel**: Environment Variables
2. **Editar**: `ADMIN_PASSWORD`
3. **Poner**: Una contraseña súper segura
4. **Deploy**: Automático

### **Credenciales Recomendadas:**
```
👤 Usuario: admin
🔑 Contraseña: DesArroyo2024!Seguro
```

---

## 🎉 **¡YA ESTÁ LISTO!**

**Una vez que hagas el deploy con estos cambios, podrás acceder al dashboard online desde cualquier lugar del mundo.**

**URLs importantes:**
- 🔐 **Login**: https://desarroyo.tech/login.html
- 📊 **Dashboard**: https://desarroyo.tech/dashboard  
- 🏠 **Web principal**: https://desarroyo.tech

---

## 🛠️ **SI HAY PROBLEMAS:**

### **1. Dashboard no carga:**
```bash
# Verificar que server.js esté desplegado
curl https://desarroyo.tech/api/dashboard/overview
```

### **2. Login falla:**
```bash
# Verificar variables de entorno en Vercel
echo "JWT_SECRET y ADMIN_PASSWORD configurados"
```

### **3. Token inválido:**
```javascript
// Limpiar cache del navegador
localStorage.clear();
```

---

## 📞 **SOPORTE TÉCNICO:**

Si necesitas ayuda:
- **Email**: alberto@desarroyo.tech  
- **Telegram**: Notificaciones automáticas
- **GitHub**: Issues en el repositorio 