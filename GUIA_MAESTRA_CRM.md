# 🚀 GUÍA MAESTRA - CRM DesArroyo.tech

## 📋 **ÍNDICE RÁPIDO**
1. [🚀 Iniciar el Sistema](#-iniciar-el-sistema)
2. [🔐 Acceso al CRM](#-acceso-al-crm)
3. [🎬 Sistema de Videos](#-sistema-de-videos)
4. [🎭 Generador de Guiones](#-generador-de-guiones)
5. [🤖 Chatbot con IA](#-chatbot-con-ia)
6. [👥 Gestión de Clientes](#-gestión-de-clientes)
7. [🔧 Solución de Problemas](#-solución-de-problemas)
8. [📞 Contacto y Ayuda](#-contacto-y-ayuda)

---

## 🚀 **INICIAR EL SISTEMA**

### **Paso 1: Abrir Terminal**
```bash
cd desarroyo-form
```

### **Paso 2: Iniciar Servidor**
```bash
npm start
```

### **Paso 3: Verificar que Funciona**
Deberías ver este mensaje:
```
🚀 Servidor DesArroyo.Tech ejecutándose en puerto 3000
🤖 Chatbot con DeepSeek activo
💳 Sistema de pagos con Stripe configurado
📊 Dashboard CRM disponible en /dashboard
```

---

## 🔐 **ACCESO AL CRM**

### **URLs Importantes**
- **Login**: `http://localhost:3000/login.html`
- **Dashboard**: `http://localhost:3000/dashboard`
- **Web Principal**: `http://localhost:3000`

### **Credenciales de Acceso**
```
👤 Usuario: admin
🔑 Contraseña: admin123
```

### **Si no puedes entrar:**
1. **Resetear contraseña**:
   ```bash
   node scripts/reset-admin-password.js
   ```
2. **Verificar usuario**:
   ```bash
   node scripts/reset-admin-password.js
   ```

---

## 🎬 **SISTEMA DE VIDEOS**

### **Dónde está**: Dashboard → Videos

### **Qué puedes hacer:**

#### 📂 **1. Clips (Subir Videos)**
- **Subir videos**: Arrastra archivos MP4
- **Configurar IA**: Análisis automático
- **Organizar**: Por tipo (intro, cuerpo, outro)
- **Editar**: Metadatos y descripciones

#### 🎨 **2. Plantillas**
- **Ver plantillas**: Educativo, Inspiracional, Promocional
- **🎭 Generar Guión**: Clic en botón morado
- **🚀 Usar plantilla**: Para crear videos
- **➕ Crear nueva**: Plantillas personalizadas

#### 🎬 **3. Videos Generados**
- **⚡ Generar Video**: Combinar clips automáticamente
- **👁️ Preview**: Ver resultado
- **🤖 IA Contenido**: Generar títulos y descripciones
- **📤 Publicar**: A redes sociales

### **Plantillas Disponibles:**
1. **📚 Superpoder Educativo**: Hook + Contenido + CTA
2. **💪 Inspiracional/Storytelling**: Historia personal + Motivación

---

## 🎭 **GENERADOR DE GUIONES**

### **Cómo acceder:**
1. **Dashboard** → **Videos** → **Plantillas**
2. **Seleccionar plantilla**
3. **Clic en 🎭 Guión**

### **Funcionalidades:**

#### 🎯 **Generar Guión Único**
- **Tema personalizado**: "Automatización para restaurantes"
- **Instrucciones adicionales**: Detalles específicos
- **🎭 Generar Guión**: Un guión profesional

#### 🎪 **Generar Múltiples Guiones**
- **🎪 Generar 3 Guiones**: Múltiples opciones
- **Variedad automática**: Diferentes enfoques
- **Comparar**: Elegir el mejor

#### 📋 **Gestionar Guiones**
- **📋 Ver Existentes**: Historial completo
- **✏️ Editar**: Modificar guiones
- **📋 Copiar**: Al portapapeles
- **🗑️ Eliminar**: Limpiar historial

### **Tipos de Guiones por Plantilla:**
- **📚 Educativo**: Hook + Contenido educativo + CTA
- **💪 Inspiracional**: Historia + Transformación + Motivación
- **📈 Promocional**: Problema + Solución + Venta
- **🎯 Tutorial**: Promesa + Pasos + Resultado

---

## 🤖 **CHATBOT CON IA**

### **Dónde está**: Página principal (`http://localhost:3000`)

### **Funcionalidades:**
- **DeepSeek IA**: Conversaciones inteligentes
- **Conocimiento DesArroyo.tech**: Servicios y precios
- **Límite gratuito**: 10 consultas por IP
- **Suscripción premium**: Acceso ilimitado

### **Temas que maneja:**
- Desarrollo web
- Automatizaciones
- Apps móviles
- Bots WhatsApp/Telegram
- Precios y servicios

---

## 👥 **GESTIÓN DE CLIENTES**

### **Dónde está**: Dashboard → Overview / Clientes

### **Funcionalidades:**
- **➕ Nuevo Cliente**: Registrar clientes
- **📊 Proyectos**: Seguimiento de avance
- **📧 Automatizaciones**: Email y WhatsApp
- **📈 Estadísticas**: Ingresos y métricas
- **📱 Actividad reciente**: Timeline de acciones

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### ❌ **"No puedo acceder al login"**
**Solución:**
```bash
# 1. Verificar servidor corriendo
npm start

# 2. Resetear contraseña admin
node scripts/reset-admin-password.js

# 3. Verificar en navegador
http://localhost:3000/login.html
```

### ❌ **"DeepSeek no funciona"**
**Solución:**
```bash
# Verificar variable de entorno
echo $DEEPSEEK_API_KEY

# Si está vacía, configurar:
export DEEPSEEK_API_KEY=tu_api_key_aqui
```

### ❌ **"Videos no se suben"**
**Solución:**
```bash
# Verificar carpetas
ls -la videos/
ls -la videos/clips/

# Si no existen, el servidor las crea automáticamente
```

### ❌ **"Error de base de datos"**
**Solución:**
```bash
# Verificar base de datos
ls -la dashboard.db

# Si hay problema, eliminar y reiniciar servidor
rm dashboard.db
npm start
```

### ❌ **"Puerto 3000 ocupado"**
**Solución:**
```bash
# Matar proceso en puerto 3000
kill -9 $(lsof -t -i:3000)

# Reiniciar
npm start
```

---

## 📊 **ESTRUCTURA DEL PROYECTO**

```
desarroyo-form/
├── 📄 server.js              # Servidor principal
├── 📄 dashboard.html         # Interface del CRM
├── 📄 login.html            # Página de login
├── 📄 index.html            # Web principal con chatbot
├── 📄 config.js             # Configuración
├── 📄 dashboard.db          # Base de datos SQLite
├── 📁 scripts/              # Scripts útiles
│   ├── reset-admin-password.js
│   ├── script-generator.js
│   └── generated-scripts/
├── 📁 videos/               # Sistema de videos
│   ├── clips/              # Videos subidos
│   ├── output/             # Videos generados
│   └── thumbnails/         # Miniaturas
└── 📁 bloques_html/        # Componentes web
```

---

## 🚀 **FLUJO DE TRABAJO RECOMENDADO**

### **Para Crear Contenido:**
1. **📂 Subir clips** → Videos → Clips → Arrastrar MP4
2. **🎨 Seleccionar plantilla** → Videos → Plantillas
3. **🎭 Generar guión** → Clic en "🎭 Guión"
4. **🎬 Crear video** → Videos → Generados → "⚡ Generar Video"
5. **🤖 Generar contenido** → "🤖 IA Contenido"
6. **📤 Publicar** → Redes sociales

### **Para Gestionar Clientes:**
1. **👥 Añadir cliente** → Dashboard → "➕ Nuevo Cliente"
2. **📊 Crear proyecto** → Asignar al cliente
3. **⚙️ Configurar automatización** → Email/WhatsApp
4. **📈 Seguimiento** → Dashboard Overview

---

## 🎯 **COMANDOS ÚTILES**

### **Desarrollo:**
```bash
# Iniciar servidor
npm start

# Ver logs en tiempo real
tail -f server.log

# Backup base de datos
cp dashboard.db dashboard.db.backup
```

### **Administración:**
```bash
# Listar plantillas
node scripts/script-generator.js list

# Generar guión desde terminal
node scripts/script-generator.js generate 1 "Mi tema"

# Cambiar contraseña admin
node scripts/reset-admin-password.js
```

---

## 📞 **CONTACTO Y AYUDA**

### **🆘 Si tienes problemas:**
1. **Consulta esta guía primero**
2. **Revisa la sección "Solución de Problemas"**
3. **Contacta**: alberto@desarroyo.tech

### **🔗 Enlaces Rápidos:**
- **Login**: http://localhost:3000/login.html
- **Dashboard**: http://localhost:3000/dashboard
- **API Docs**: http://localhost:3000/api/health
- **Chatbot**: http://localhost:3000

---

## 🎉 **¡LISTO PARA USAR!**

### **Proceso de Inicio Rápido:**
```bash
1. cd desarroyo-form
2. npm start
3. Ir a: http://localhost:3000/login.html
4. Login: admin / admin123
5. ¡Disfrutar del CRM! 🚀
```

### **Primera Vez Usando:**
1. **📂 Sube algunos videos** (3-5 clips)
2. **🎭 Genera tu primer guión** usando plantilla educativa
3. **🎬 Crea tu primer video** combinando clips
4. **🤖 Genera contenido viral** con IA
5. **👥 Añade tu primer cliente**

---

**✨ ¡Tu CRM con IA está listo para revolucionar tu negocio! ✨**

🚀 **DesArroyo.tech - Crea, Automatiza, Comparte... y vuelve a la playa a celebrar** 