# 🔧 CAMBIAR WEBHOOK EN TWILIO - PASO A PASO

## ⚠️ IMPORTANTE: Cambiar de ngrok a n8n

### **PASO 1: Acceder a Twilio Console**
1. Ve a: https://console.twilio.com/
2. Login con tu cuenta
3. Ve a **Phone Numbers** → **Manage** → **Active numbers**

### **PASO 2: Configurar tu número español**
1. Click en tu número: **+34617555255**
2. Busca la sección **"Voice & Fax"**
3. En **"A call comes in"** cambiar de:
   ```
   https://830a63f92d4e.ngrok-free.app/webhook-llamada
   ```
   A:
   ```
   https://arroyo805.app.n8n.cloud/webhook/webhook-llamada
   ```

### **PASO 3: Configurar método**
- **Method**: `POST`
- **Format**: `Form-encoded`

### **PASO 4: Guardar**
- Click **Save configuration**

## 🧪 **PROBAR EL WEBHOOK**

### **Opción 1: Probar con curl**
```bash
curl -X POST https://arroyo805.app.n8n.cloud/webhook/webhook-llamada \
  -d "From=%2B34612345678&To=%2B34617555255&CallSid=CAtest123"
```

### **Opción 2: Hacer llamada real**
1. Usa tu móvil personal
2. Llama a: **+34617555255**
3. Deberías escuchar el mensaje en español

## 📋 **MENSAJES ESPERADOS SEGÚN HORARIO**

### **🏢 HORARIO COMERCIAL (L-V 9-14h y 16-20h, S 10-13h)**
```
"Hola, buenos días. Soy un agente comercial de DesArroyo Tech, 
empresa especializada en desarrollo web profesional.

Le llamo porque hemos identificado que su negocio tiene un gran 
potencial para crecer online..."
```

### **🌙 FUERA DE HORARIO**
```
"Hola, gracias por atender. Soy un agente comercial de DesArroyo Tech.

Le hemos llamado fuera de nuestro horario comercial habitual. 
Nos disculpamos por la molestia..."
```

## ✅ **VERIFICAR QUE FUNCIONA**

### **Indicadores de éxito:**
- ✅ Voz femenina en español (Polly.Lucia)
- ✅ Dice "agente comercial de DesArroyo Tech"
- ✅ Mensaje profesional y claro
- ✅ No suena a scam ni inglés
- ✅ Duración: 30-45 segundos

### **Si hay problemas:**
- ❌ **Voz en inglés**: Webhook no configurado
- ❌ **Error 404**: URL incorrecta
- ❌ **Sin respuesta**: Flujo n8n no activado

## 🎯 **RESULTADO ESPERADO HOY (SÁBADO)**

Como es sábado y dependiendo de la hora:
- **10-13h**: Mensaje comercial completo
- **Resto del día**: Mensaje "fuera de horario"

## 🚀 **RESULTADO ESPERADO LUNES**

- **9-14h y 16-20h**: Mensaje comercial completo
- **Resto del día**: Mensaje "fuera de horario" 