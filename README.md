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

## ⚙️ Gestión y Mantenimiento

### Cómo Cambiar el Precio de la Web

El precio de la web se configura directamente en el flujo de n8n que crea el enlace de pago de Stripe.

1.  **Abre el Flujo 1 en n8n**: Carga el workflow desde el archivo `1.1_desarroyo_form.json`.
2.  **Localiza el Nodo de Pago**: Busca el nodo llamado `8 HTTP Request`. Este es el que se comunica con la API de Stripe.
3.  **Edita los Parámetros del Body**:
    *   Dentro del nodo, ve a la sección "Body Parameters".
    *   Busca el parámetro llamado `line_items[0][price_data][unit_amount]`.
4.  **Cambia el Valor**:
    *   El precio debe estar en **céntimos**. Por ejemplo:
        *   Para **99€**, el valor debe ser `9900`.
        *   Para **149€**, el valor debe ser `14900`.
        *   Para **49.50€**, el valor debe ser `4950`.
5.  **Guarda el Flujo**: Una vez cambiado el valor, guarda los cambios en tu workflow de n8n.

¡Y listo! El próximo cliente que rellene el formulario recibirá un enlace de pago con el nuevo precio.

---

### Cómo Implementar Múltiples Opciones de Precios (Ej: Básico, Estándar, Premium)

Si en el futuro deseas ofrecer varios planes, el sistema se puede adaptar. Esto requiere modificar tanto la página web como el flujo de n8n.

#### Paso 1: Modificar la Página Web (`index.html`)

Deberás añadir un campo en el formulario para que el cliente seleccione su plan. La forma más sencilla es con `radio buttons`.

**Ejemplo de código para añadir en `index.html`:**

```html
<!-- Añade esta sección antes del botón de enviar -->
<h4>Selecciona tu Plan:</h4>
<div class="plan-selector">
  <label>
    <input type="radio" name="plan" value="basico" checked>
    <strong>Plan Básico (49€)</strong> - Web sencilla y funcional.
  </label>
  <label>
    <input type="radio" name="plan" value="estandar">
    <strong>Plan Estándar (99€)</strong> - Diseño avanzado y más secciones.
  </label>
  <label>
    <input type="radio" name="plan" value="premium">
    <strong>Plan Premium (199€)</strong> - Funcionalidades extra y soporte prioritario.
  </label>
</div>
```

Este código enviará un campo `plan` con el valor `basico`, `estandar` o `premium` junto con el resto de los datos del formulario.

#### Paso 2: Modificar el Flujo 1 de n8n

El cambio principal es usar un nodo **Switch** para establecer el precio según el plan elegido.

**Diagrama del flujo modificado:**
`Webhook -> Switch (evalúa plan) -> Set Price (ruta para cada plan) -> HTTP Request`

**Pasos en n8n:**

1.  **Webhook**: No necesita cambios. Ya recibirá el campo `plan` del formulario.

2.  **Añadir un Nodo `Switch`**: Colócalo justo después del nodo `2. Generar Prompt`.
    *   **Propiedad a Evaluar**: `{{$json.body.plan}}`
    *   **Rutas de Salida**:
        *   **Ruta 0**: `basico`
        *   **Ruta 1**: `estandar`
        *   **Ruta 2**: `premium`

3.  **Añadir Nodos `Set` para cada ruta**:
    *   **En la ruta "basico"**: Añade un nodo `Set` para crear una variable `precio`.
        *   Nombre: `precio`, Valor: `4900`
    *   **En la ruta "estandar"**: Añade otro nodo `Set`.
        *   Nombre: `precio`, Valor: `9900`
    *   **En la ruta "premium"**: Añade un tercer nodo `Set`.
        *   Nombre: `precio`, Valor: `19900`

4.  **Conectar los Nodos `Set` al Nodo `8 HTTP Request`**: Los tres nodos `Set` deben conectarse al nodo que crea el pago en Stripe.

5.  **Modificar el Nodo `8 HTTP Request`**:
    *   Busca el parámetro `line_items[0][price_data][unit_amount]`.
    *   Cambia el valor fijo (ej: `9900`) por la variable que acabas de crear: `{{$json.precio}}`.
    *   De esta forma, el precio que se envía a Stripe será dinámico según la elección del cliente.

6.  **Guarda el Flujo**: ¡No olvides guardar los cambios!

Con estos pasos, tu sistema estará preparado para manejar múltiples planes de precios de forma totalmente automática.

---

**"Crea, automatiza, comparte… y vuelve a la playa a celebrar"** 🏖️