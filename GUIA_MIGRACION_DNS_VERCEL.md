# 🌐 GUÍA DE MIGRACIÓN DNS: GitHub Pages → Vercel

## 📋 RESUMEN RÁPIDO

**Dominio:** `desarroyo.tech`  
**DNS Provider:** Porkbun  
**Migración:** GitHub Pages → Vercel

---

## ✅ PASOS A SEGUIR EN PORKBUN

### **1. ELIMINAR Registros A de GitHub Pages**

Elimina estos 4 registros A que están causando conflicto:

| Tipo | Host | Valor | Acción |
|------|------|-------|--------|
| A | `desarroyo.tech` | `185.199.108.153` | ❌ **ELIMINAR** |
| A | `desarroyo.tech` | `185.199.109.153` | ❌ **ELIMINAR** |
| A | `desarroyo.tech` | `185.199.110.153` | ❌ **ELIMINAR** |
| A | `desarroyo.tech` | `185.199.111.153` | ❌ **ELIMINAR** |

### **2. MANTENER Registro A de Vercel**

| Tipo | Host | Valor | Acción |
|------|------|-------|--------|
| A | `desarroyo.tech` | `216.150.1.1` | ✅ **MANTENER** |

### **3. MANTENER CNAME de www**

| Tipo | Host | Valor | Acción |
|------|------|-------|--------|
| CNAME | `www.desarroyo.tech` | `f8d39c567a60b32e.vercel-dns-017.com.` | ✅ **MANTENER** |

### **4. MANTENER Registros de Email (Zoho)**

**NO TOCAR** estos registros para que tu email siga funcionando:

| Tipo | Host | Valor | Acción |
|------|------|-------|--------|
| MX | `desarroyo.tech` | `mx.zoho.eu` (Priority: 10) | ✅ **MANTENER** |
| MX | `desarroyo.tech` | `mx2.zoho.eu` (Priority: 20) | ✅ **MANTENER** |
| MX | `desarroyo.tech` | `mx3.zoho.eu` (Priority: 50) | ✅ **MANTENER** |
| TXT | `desarroyo.tech` | `v=spf1 include:zohomail.eu ~all` | ✅ **MANTENER** |
| TXT | `zmail._domainkey.desarroyo.tech` | `v=DKIM1; k=rsa; p=...` | ✅ **MANTENER** |

---

## 📝 CONFIGURACIÓN FINAL EN PORKBUN

Después de los cambios, deberías tener **exactamente** estos registros:

### **Registros A:**
- ✅ `desarroyo.tech` → `216.150.1.1` (Vercel)

### **Registros CNAME:**
- ✅ `www.desarroyo.tech` → `f8d39c567a60b32e.vercel-dns-017.com.` (Vercel)

### **Registros MX (Email Zoho):**
- ✅ `desarroyo.tech` → `mx.zoho.eu` (Priority: 10)
- ✅ `desarroyo.tech` → `mx2.zoho.eu` (Priority: 20)
- ✅ `desarroyo.tech` → `mx3.zoho.eu` (Priority: 50)

### **Registros TXT:**
- ✅ `desarroyo.tech` → `v=spf1 include:zohomail.eu ~all` (SPF)
- ✅ `zmail._domainkey.desarroyo.tech` → `v=DKIM1; k=rsa; p=...` (DKIM)

---

## ⏱️ TIEMPO DE PROPAGACIÓN

- **DNS Changes:** 5-30 minutos (normalmente)
- **Máximo:** Hasta 48 horas (raro)
- **Verificación:** Usa `dig desarroyo.tech` o `nslookup desarroyo.tech`

---

## 🔍 VERIFICACIÓN EN VERCEL

1. Ve a tu dashboard de Vercel
2. Settings → Domains
3. Busca `desarroyo.tech`
4. Debería cambiar de "Invalid Configuration" a "Valid Configuration" ✅

---

## ⚠️ IMPORTANTE

- **NO cambies los nameservers** a Vercel si quieres mantener el control en Porkbun
- **NO elimines** los registros MX y TXT (necesarios para email)
- **Espera** la propagación DNS antes de preocuparte si no funciona inmediatamente

---

## 🆘 SI ALGO NO FUNCIONA

1. **Espera 30 minutos** (propagación DNS)
2. **Verifica en Vercel** que el dominio esté validado
3. **Comprueba** que solo tengas el registro A `216.150.1.1`
4. **Limpia caché DNS:** `sudo dscacheutil -flushcache` (Mac) o reinicia router

