# DesArroyo.Tech - Plataforma Web Inteligente

🚀 **Generador de webs HTML personalizadas y automatizaciones con n8n, potenciado por IA**

## ✨ Características

- 🌐 **Generador de Webs HTML** - Encuesta inteligente para crear webs personalizadas en 48h
- ⚡ **Generador de Automatizaciones n8n** - Crea flujos de automatización con JSON descargable
- 🤖 **Chatbot Inteligente con DeepSeek** - Asistente virtual con IA avanzada
- 📱 **Diseño Responsive** - Funciona perfectamente en móviles y desktop
- 🎨 **Estilo Visual Consistente** - Efectos neón y animaciones modernas

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/Arroyador69/desarroyo-form.git
cd desarroyo-form
```

### 2. Instalar dependencias
```bash
npm install
```

### 3. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
# Configuración del servidor
PORT=3000

# API Key de DeepSeek (obtener en https://platform.deepseek.com/)
DEEPSEEK_API_KEY=tu_api_key_aqui

# Configuración adicional
NODE_ENV=development
```

### 4. Obtener API Key de DeepSeek
1. Ve a [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. Crea una cuenta gratuita
3. Ve a "API Keys" en tu dashboard
4. Crea una nueva API key
5. Copia la key y pégala en tu archivo `.env`

### 5. Ejecutar el servidor
```bash
# Desarrollo (con auto-reload)
npm run dev

# Producción
npm start
```

El servidor estará disponible en `http://localhost:3000`

## 🌐 Despliegue Online

### Opción 1: Render (Recomendado - Gratuito)
1. Conecta tu repositorio de GitHub a [Render](https://render.com/)
2. Crea un nuevo "Web Service"
3. Configura las variables de entorno en Render:
   - `DEEPSEEK_API_KEY`: Tu API key de DeepSeek
   - `PORT`: 10000 (Render usa este puerto)
4. Deploy automático

### Opción 2: Railway
1. Conecta tu repositorio a [Railway](https://railway.app/)
2. Añade las variables de entorno
3. Deploy automático

### Opción 3: Vercel
1. Conecta tu repositorio a [Vercel](https://vercel.com/)
2. Configura las variables de entorno
3. Deploy automático

### Opción 4: Heroku
1. Crea una cuenta en [Heroku](https://heroku.com/)
2. Conecta tu repositorio
3. Configura las variables de entorno
4. Deploy

## 🤖 Chatbot con DeepSeek

El chatbot utiliza DeepSeek para proporcionar respuestas inteligentes sobre:

- **Servicios de DesArroyo.Tech**
- **Precios y cotizaciones**
- **Ayuda técnica con n8n**
- **Información sobre automatizaciones**
- **Contacto y soporte**

### Características del Chatbot:
- ✅ Respuestas contextuales inteligentes
- ✅ Fallback a respuestas predefinidas si falla la IA
- ✅ Indicador de escritura
- ✅ Botones de respuesta rápida
- ✅ Manejo de errores robusto

## 📁 Estructura del Proyecto

```
desarroyo-form/
├── index.html                 # Página principal con encuesta de webs
├── generador_automatizaciones.html  # Generador de flujos n8n
├── server.js                  # Servidor Express con API del chatbot
├── chatbot.js                 # Lógica del chatbot frontend
├── package.json               # Dependencias y scripts
├── bloques_html/              # Componentes HTML reutilizables
├── img/                       # Imágenes y assets
└── respuestas/                # Respuestas guardadas
```

## 🔧 API Endpoints

- `GET /` - Página principal
- `GET /generador_automatizaciones.html` - Generador de automatizaciones
- `POST /api/chat` - Endpoint del chatbot con DeepSeek
- `GET /api/health` - Estado del servidor
- `POST /api/guardar-respuestas` - Guardar respuestas de la encuesta

## 🎨 Personalización

### Estilos Visuales
- Los estilos están en los archivos HTML
- Paleta de colores: `#00fff7` (cian), `#a259ff` (púrpura), `#10131a` (fondo)
- Efectos neón y animaciones CSS

### Chatbot
- Modifica `SYSTEM_PROMPT` en `server.js` para cambiar el comportamiento
- Ajusta `getFallbackResponse()` en `chatbot.js` para respuestas de respaldo

## 📞 Contacto

- **Email**: alberto@desarroyo.tech
- **GitHub**: [Arroyador69](https://github.com/Arroyador69)
- **Web**: [DesArroyo.Tech](https://desarroyo.tech)

## 📄 Licencia

ISC License - Desarrollado por Alberto Arroyo para DesArroyo.Tech

---

**"Crea, automatiza, comparte… y vuelve a la playa a celebrar"** 🏖️