# ⚡ REFERENCIA RÁPIDA - CRM DesArroyo.tech

## 🚀 **COMANDOS ESENCIALES**

### **Iniciar CRM:**
```bash
npm run crm        # Inicio automático (RECOMENDADO)
npm start          # Inicio manual
```

### **Deployment Online:**
```bash
git add .
git commit -m "🚀 CRM listo para producción"
git push origin main    # ¡Disponible en https://desarroyo.tech!
```

### **Solucionar problemas:**
```bash
node scripts/reset-admin-password.js    # Resetear admin
npm run crm                             # Reiniciar todo
```

---

## 🌐 **ENLACES DIRECTOS**

### **🏠 Local (desarrollo):**
| **Función** | **URL** | **Credenciales** |
|-------------|---------|------------------|
| 🔐 **Login** | `http://localhost:3000/login.html` | `admin` / `admin123` |
| 📊 **Dashboard** | `http://localhost:3000/dashboard` | Después del login |
| 🤖 **Chatbot** | `http://localhost:3000` | Sin login |
| 🎬 **Videos** | `http://localhost:3000/dashboard#videos` | Después del login |

### **🌐 Online (producción):**
| **Función** | **URL** | **Credenciales** |
|-------------|---------|------------------|
| 🔐 **Login** | `https://desarroyo.tech/login.html` | `admin` / `admin123` |
| 📊 **Dashboard** | `https://desarroyo.tech/dashboard` | Después del login |
| 🤖 **Chatbot** | `https://desarroyo.tech` | Sin login |
| 🎬 **Videos** | `https://desarroyo.tech/dashboard#videos` | Después del login |

---

## 📚 **DOCUMENTACIÓN POR TEMA**

### **🔧 Problemas de Acceso:**
- 📄 **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Soluciones paso a paso

### **🌐 Deployment Online:**
- 📄 **[DESPLIEGUE_ONLINE.md](DESPLIEGUE_ONLINE.md)** - Cómo ponerlo online

### **🎭 Generar Guiones:**
- 📄 **[GUIA_GENERADOR_GUIONES.md](GUIA_GENERADOR_GUIONES.md)** - Cómo usar el generador

### **📖 Guía Completa:**
- 📄 **[GUIA_MAESTRA_CRM.md](GUIA_MAESTRA_CRM.md)** - TODO en detalle

### **🏠 Inicio General:**
- 📄 **[README.md](README.md)** - Descripción del proyecto

---

## 🎯 **FLUJO DE TRABAJO TÍPICO**

### **1. Iniciar Sistema:**
```bash
npm run crm
```

### **2. Acceder al CRM:**
- Ve a: `http://localhost:3000/login.html`
- Login: `admin` / `admin123`

### **3. Crear Contenido:**
1. **Videos** → **Clips** → Subir MP4
2. **Videos** → **Plantillas** → Seleccionar
3. **🎭 Guión** → Generar con IA
4. **Videos** → **Generados** → Crear video
5. **🤖 IA Contenido** → Generar título viral

### **4. Gestionar Clientes:**
1. **Dashboard** → **➕ Nuevo Cliente**
2. **Asignar proyecto**
3. **Configurar automatizaciones**

---

## 🆘 **SOLUCIONES RÁPIDAS**

### **❌ No puedo entrar:**
```bash
node scripts/reset-admin-password.js
npm run crm
```

### **❌ Puerto ocupado:**
```bash
kill -9 $(lsof -t -i:3000)
npm run crm
```

### **❌ Error de base de datos:**
```bash
rm dashboard.db
npm run crm
```

---

## 📞 **CONTACTO INMEDIATO**

**🆘 Necesitas ayuda YA:**
- 📧 **Email**: alberto@desarroyo.tech
- 💬 **WhatsApp**: [Contacta aquí](https://wa.me/message/YOURWHATSAPPLINK)

**🐛 Reportar bug:**
- 📝 **GitHub**: [Crear issue](https://github.com/Arroyador69/desarroyo-form/issues)

---

## 🎉 **¡LISTO PARA USAR!**

**🚀 Comando mágico para empezar:**
```bash
cd desarroyo-form && npm run crm
```

**🔗 Luego ir a:** `http://localhost:3000/login.html`

**🔐 Credenciales:** `admin` / `admin123`

---

**✨ ¡Tu CRM con IA está a un comando de distancia! ✨** 