# 🎭 Generador de Guiones IA - DesArroyo.tech

## 🚀 Funcionalidad Añadida al CRM

### ✅ **¿Qué se ha implementado?**

Hemos integrado completamente **DeepSeek** en tu CRM para generar **guiones automáticos** específicos para cada plantilla de video. ¡Es una funcionalidad súper potente!

## 🎯 **Características Principales**

### 📋 **1. Generación Inteligente por Plantilla**
- **Prompts específicos** para cada tipo de plantilla:
  - 📚 **Educativo**: Hook + Contenido + CTA
  - 💪 **Inspiracional**: Historia + Transformación + Motivación  
  - 📈 **Promocional**: Problema + Solución + Venta
  - 🎯 **Tutorial**: Promesa + Pasos + Resultado

### 🤖 **2. Personalización Avanzada**
- **Tema personalizado**: Especifica el tema del guión
- **Instrucciones adicionales**: Detalles específicos sobre clientes, productos, etc.
- **Contexto DesArroyo.tech**: Automáticamente incluye información de tu empresa

### 🎬 **3. Formato Profesional**
- **Estructura temporal**: Dividido en clips con tiempos específicos
- **Direcciones de video**: Qué hacer/mostrar en cada momento
- **Texto overlay**: Sugerencias para texto en pantalla
- **Duración optimizada**: Máximo 59 segundos (perfecto para redes)

## 🎭 **Cómo Usar el Generador**

### **Paso 1: Acceder al Generador**
1. Ve a **Dashboard** → **Videos** → **Plantillas**
2. Selecciona cualquier plantilla
3. Haz clic en **🎭 Guión**

### **Paso 2: Configurar el Guión**
```
🎯 Tema del guión: "Automatización para restaurantes"
📝 Instrucciones adicionales: "Menciona que ayudamos con reservas online"
```

### **Paso 3: Generar**
- **🎭 Generar Guión**: Un guión único
- **🎪 Generar 3 Guiones**: Múltiples opciones
- **📋 Ver Guiones Existentes**: Historial de guiones

### **Paso 4: Gestionar Guiones**
- ✏️ **Editar**: Modificar el guión
- 📋 **Copiar**: Al portapapeles
- 🗑️ **Eliminar**: Quitar guión

## 🛠️ **Configuración Técnica**

### **Variables de Entorno Necesarias**
```bash
# Añadir a tu archivo .env
DEEPSEEK_API_KEY=tu_api_key_de_deepseek
```

### **APIs Implementadas**
```
POST /api/dashboard/generate-script          # Generar un guión
POST /api/dashboard/generate-multiple-scripts # Generar múltiples guiones
GET  /api/dashboard/scripts/:template_id     # Obtener guiones de plantilla
GET  /api/dashboard/script/:script_id        # Obtener guión específico
PUT  /api/dashboard/script/:script_id        # Actualizar guión
DELETE /api/dashboard/script/:script_id      # Eliminar guión
```

## 🎬 **Ejemplo de Guión Generado**

### **Plantilla: Superpoder Educativo**
**Tema**: "Automatización para restaurantes"

```
[INTRO - 0:00-0:08]
Dirección: Apareces en pantalla con gesto de "problema"
Guión: "¿Tu restaurante pierde clientes porque no pueden reservar fácilmente?"
Texto overlay: "PROBLEMA COMÚN"

[BODY - 0:08-0:50]
Dirección: Mostrar pantalla con sistema de reservas
Guión: "En DesArroyo.tech automatizamos todo el proceso. WhatsApp, Instagram, web... Todo conectado. El cliente reserva, el sistema confirma automáticamente, y tú solo cocinas."
Texto overlay: "AUTOMATIZACIÓN TOTAL"

[OUTRO - 0:50-0:59]
Dirección: Mirando a cámara con sonrisa
Guión: "¿Quieres automatizar tu restaurante? Escríbeme a alberto@desarroyo.tech"
Texto overlay: "alberto@desarroyo.tech"
```

## 📊 **Temas por Defecto por Plantilla**

### 📚 **Educativo**
- Automatización para restaurantes
- Bots de WhatsApp para empresas  
- Webs HTML en 48 horas
- Apps móviles sin programar
- Automatizar Instagram con n8n

### 💪 **Inspiracional**
- De empleado a emprendedor tech
- Cómo automaticé mi negocio
- Mi primer cliente en 48 horas
- Del burnout al éxito digital
- Transformación digital personal

### 📈 **Promocional**
- Servicios DesArroyo.tech
- Automatización para tu negocio
- Webs profesionales rápidas
- Bots que venden 24/7
- Consultoría tech personalizada

## 💡 **Uso desde Línea de Comandos**

### **Script Independiente**
```bash
# Listar plantillas disponibles
node scripts/script-generator.js list

# Generar guión para plantilla específica
node scripts/script-generator.js generate 1 "Tema personalizado"

# Generar múltiples guiones
node scripts/script-generator.js multiple 1

# Ver guiones existentes
node scripts/script-generator.js scripts 1
```

## 🔧 **Solución de Problemas**

### ❌ **Error: "DeepSeek API no configurada"**
**Solución**: Configura `DEEPSEEK_API_KEY` en tu archivo `.env`

### ❌ **Error: "Plantilla no encontrada"**
**Solución**: Verifica que la plantilla exista en la base de datos

### ❌ **Guiones no se cargan**
**Solución**: Verifica que el usuario esté autenticado correctamente

## 🎯 **Próximas Mejoras**

- [ ] **Editor de guiones en tiempo real**
- [ ] **Plantillas de guiones personalizadas**
- [ ] **Análisis de efectividad de guiones**
- [ ] **Integración con generador de videos**
- [ ] **Exportación a formatos de producción**

## 🎉 **¡Listo para Usar!**

Tu CRM ya tiene la capacidad de generar **guiones automáticos** con IA para cualquier plantilla de video. ¡Es hora de crear contenido viral de forma automática!

### 🚀 **Para Probarlo Ahora:**
1. Inicia tu servidor: `npm start`
2. Ve a: `http://localhost:3000/dashboard`
3. Login: `admin` / `admin123`
4. Navega a **Videos** → **Plantillas**
5. ¡Haz clic en **🎭 Guión** en cualquier plantilla!

---
**✨ Creado por DesArroyo.tech - Automatización que transforma negocios** 