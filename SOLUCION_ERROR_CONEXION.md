# 🚨 SOLUCIÓN ERROR 63024 - TWILIO WHATSAPP

## ❌ **PROBLEMA IDENTIFICADO: "Invalid message recipient"**

Tu consola de Twilio muestra mensajes "Undelivered" con error 63024, que significa que los números de teléfono no están formateados correctamente para WhatsApp.

---

## 🔍 **DIAGNÓSTICO PASO A PASO**

### **PASO 1: Verificar configuración Twilio**

1. **Ve a tu consola Twilio:** https://console.twilio.com/
2. **Verifica en "Settings" que tienes:**
   - ✅ Account SID correcto
   - ✅ Auth Token correcto
   - ✅ Crédito disponible

### **PASO 2: Verificar WhatsApp Sandbox**

1. **Ve a:** Console → Messaging → Try WhatsApp
2. **Asegúrate de que:**
   - ✅ Tienes el número correcto (ej: +14155238886)
   - ✅ Has enviado el código de activación a tu WhatsApp personal
   - ✅ Aparece "Connected" en tu sandbox

### **PASO 3: Problema de formato de números**

Los números españoles deben enviarse como: `+34XXXXXXXXX`

**❌ FORMATOS INCORRECTOS:**
- `34XXXXXXXXX` (sin +)
- `XXXXXXXXX` (sin código país)
- `0034XXXXXXXXX` (con 00)
- `(+34) XXX XXX XXX` (con espacios/paréntesis)

**✅ FORMATO CORRECTO:**
- `+34612345678` (móvil)
- `+34912345678` (fijo Madrid)

---

## 🛠️ **SOLUCIÓN INMEDIATA**

### **OPCIÓN A: Usar sandbox solo con números autorizados**

1. **Ve a Twilio Console → WhatsApp Sandbox**
2. **Añade tu número personal:** +34TUTELEFONO
3. **Envía desde tu WhatsApp** el código que te dan
4. **Prueba enviando solo a tu número primero**

### **OPCIÓN B: Corregir función de formateo**

Voy a mejorar la función que formatea los números:

```python
def formatear_telefono_espanol_mejorado(self, phone):
    """Formatea número español para WhatsApp con validación estricta"""
    import re
    
    # Limpiar número (solo dígitos)
    phone_clean = re.sub(r'[^\d]', '', phone)
    
    # Si ya tiene +34, devolverlo limpio
    if phone.startswith('+34') and len(phone_clean) == 11:
        return f"+{phone_clean}"
    
    # Si empieza con 34, añadir +
    if phone_clean.startswith('34') and len(phone_clean) == 11:
        return f"+{phone_clean}"
    
    # Si es móvil español (6,7,9) de 9 dígitos
    if len(phone_clean) == 9 and phone_clean[0] in ['6', '7', '9']:
        return f"+34{phone_clean}"
    
    # Si no coincide con patrones españoles, rechazar
    print(f"⚠️ Número no válido para España: {phone}")
    return None

def enviar_whatsapp_seguro(self, lead, mensaje):
    """Envío WhatsApp con validación mejorada"""
    if not self.twilio_client:
        print(f"⚠️ WhatsApp no configurado")
        return False
    
    # Formatear y validar número
    phone_formatted = self.formatear_telefono_espanol_mejorado(lead['phone'])
    
    if not phone_formatted:
        print(f"❌ Número inválido para {lead['name']}: {lead['phone']}")
        return False
    
    try:
        message = self.twilio_client.messages.create(
            from_=f'whatsapp:{self.twilio_whatsapp}',
            body=mensaje,
            to=f'whatsapp:{phone_formatted}'
        )
        
        print(f"✅ WhatsApp → {lead['name']}: {phone_formatted}")
        return True
        
    except Exception as e:
        print(f"❌ Error Twilio: {e}")
        # Log detallado del error
        print(f"   From: whatsapp:{self.twilio_whatsapp}")
        print(f"   To: whatsapp:{phone_formatted}")
        print(f"   Mensaje: {mensaje[:50]}...")
        return False
```

---

## 🧪 **PRUEBA RÁPIDA PARA DIAGNOSTICAR**

### **Script de prueba:**

```python
#!/usr/bin/env python3
# test_whatsapp.py - Prueba WhatsApp directo

from twilio.rest import Client
import os

# Configurar (usar tus valores reales)
TWILIO_SID = 'ACxxxxxxxxxxxxxx'  # Tu Account SID
TWILIO_TOKEN = 'xxxxxxxxxxxxxx'   # Tu Auth Token  
TWILIO_WHATSAPP = '+14155238886'  # Tu número sandbox
TU_NUMERO = '+34XXXXXXXXX'        # TU número personal

# Crear cliente
client = Client(TWILIO_SID, TWILIO_TOKEN)

try:
    message = client.messages.create(
        from_=f'whatsapp:{TWILIO_WHATSAPP}',
        body='🧪 PRUEBA: Si recibes este mensaje, WhatsApp funciona correctamente',
        to=f'whatsapp:{TU_NUMERO}'
    )
    
    print(f"✅ Mensaje enviado exitosamente!")
    print(f"   SID: {message.sid}")
    print(f"   Estado: {message.status}")
    print(f"   From: {message.from_}")
    print(f"   To: {message.to}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print(f"   Verifica:")
    print(f"   - Account SID: {TWILIO_SID}")
    print(f"   - WhatsApp Number: {TWILIO_WHATSAPP}")
    print(f"   - Tu número: {TU_NUMERO}")
```

---

## 🎯 **PASOS INMEDIATOS**

### **1. PRUEBA MANUAL (5 minutos)**
```bash
cd desarroyo-form
python3 test_whatsapp.py
```

### **2. SI LA PRUEBA FALLA:**
- ❌ **Error 63024:** Número no autorizado en sandbox
- ❌ **Error 20003:** Credenciales incorrectas  
- ❌ **Error 21408:** No tienes permisos WhatsApp

### **3. SI LA PRUEBA FUNCIONA:**
- ✅ **El problema está en el formateo** de números del scraper
- ✅ **Necesitas filtrar solo números válidos** antes de enviar

---

## 🔧 **IMPLEMENTAR SOLUCIÓN**

### **Actualizar sistema de leads:**

1. **Mejorar validación de números**
2. **Filtrar solo números españoles válidos**  
3. **Añadir logs detallados**
4. **Probar con tu número primero**

### **Configurar webhook para respuestas:**

Tu Twilio necesita webhook configurado para recibir respuestas:
- **URL:** `https://tu-servidor.com/webhook/whatsapp`
- **Método:** POST
- **Script:** `scripts/webhook_respuestas.py`

---

## 📱 **VERIFICACIÓN FINAL**

Una vez implementado, deberías ver en Twilio:
- ✅ **Status:** "Delivered" (no "Undelivered")
- ✅ **Color:** Verde (no rojo)
- ✅ **Error Code:** Ninguno (no 63024)

---

## 🆘 **SI SIGUES TENIENDO PROBLEMAS**

1. **Comparte tus logs exactos** de la ejecución
2. **Verifica en Twilio Console** el estado exacto
3. **Prueba con UN solo número válido** primero
4. **Revisa que tengas crédito** en Twilio

¿Quieres que implementemos estas mejoras ahora mismo? 