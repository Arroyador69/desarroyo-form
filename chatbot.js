// DesArroyo.Tech - Chatbot "Aura"
// Este archivo contendrá toda la lógica para nuestro chatbot de ayuda.

// 1. Base de Conocimiento (Knowledge Base)
// Aquí definimos las preguntas y respuestas que el chatbot conocerá.
// Usamos "palabras clave" para que sea más flexible.

const knowledgeBase = [
    {
        keywords: ["hola", "saludos", "buenas"],
        answer: "¡Hola! Soy Aura, tu asistente personal de DesArroyo.Tech. Estoy aquí para ayudarte con tus dudas sobre automatizaciones, desarrollo web y cómo dar vida a tus ideas. ¿En qué puedo ayudarte?"
    },
    {
        keywords: ["n8n", "que es"],
        answer: "n8n es una herramienta de automatización de flujos de trabajo de código abierto. Te permite conectar diferentes aplicaciones y servicios para que trabajen juntos sin necesidad de escribir código. ¡Es como tener superpoderes para tus tareas diarias!"
    },
    {
        keywords: ["instalo", "importar", "flujo", "json"],
        answer: "Es muy fácil. Para instalar tu flujo, ve a tu panel de n8n, haz clic en 'Add workflow' y luego en 'Import from file'. Selecciona el archivo .json que generaste aquí y ¡listo para configurar!"
    },
    {
        keywords: ["credenciales", "conectar", "api", "clave"],
        answer: "Las credenciales son las 'llaves' que permiten a n8n acceder a tus apps (como Gmail o Telegram). En cada nodo de n8n, verás un campo 'Credential'. Haz clic en 'Create New' y sigue los pasos para conectar tu cuenta."
    },
    {
        keywords: ["cuanto", "cuesta", "tiempo", "web", "personalizada"],
        answer: "Una web 100% personalizada es un proyecto único. El coste y tiempo dependen de la complejidad, pero para darte una idea, una web estática como la que se describe en la página de inicio puede estar lista en 48 horas a un precio muy competitivo. Para proyectos más grandes (con Astro, bases de datos, etc.), lo mejor es que nos escribas a <strong>alberto@desarroyo.tech</strong> para darte un presupuesto a medida. ¡Nos encanta escuchar nuevas ideas!"
    },
    {
        keywords: ["servicios", "ofrecen"],
        answer: "Ofrecemos un abanico de soluciones: webs HTML ultrarrápidas, webs full-stack con Astro, bots para WhatsApp/Telegram, automatizaciones con IA, soluciones para check-in de alojamientos turísticos ¡y mucho más! Puedes ver la lista completa en la sección '¿Qué ofrecemos?' de la página de inicio."
    },
    {
        keywords: ["quien", "detras", "alberto"],
        answer: "Detrás de DesArroyo.Tech está <strong>Alberto Arroyo</strong>, un actor, escritor y artesano del código que fusiona su pasión por la narrativa con la tecnología para crear soluciones con alma. Puedes conocerle mejor en la sección 'Detrás del código' de la página de inicio."
    },
    {
        keywords: ["otra", "automatizacion", "no esta", "generador"],
        answer: "¡Por supuesto! El generador es un punto de partida. Si tienes una necesidad de automatización más compleja o específica, contáctanos en <strong>alberto@desarroyo.tech</strong>. Nos encantan los retos y crear soluciones a medida."
    },
    {
        keywords: ["superpoderes", "ejemplos", "ideas"],
        answer: "¡Claro! Aquí tienes algunos 'superpoderes' que puedes conseguir con n8n: <br>1. <strong>Sincronización automática:</strong> Guarda los archivos adjuntos de tus emails de Gmail directamente en Google Drive. <br>2. <strong>Notificador inteligente:</strong> Recibe un mensaje en Telegram cada vez que alguien complete tu formulario de Typeform. <br>3. <strong>Reportes automáticos:</strong> Crea un resumen diario de las ventas de Stripe y envíalo a una hoja de Google Sheets."
    },
    {
        keywords: ["gracias", "adios", "chau"],
        answer: "¡De nada! Si tienes más preguntas, no dudes en consultarme. ¡Felices automatizaciones!"
    }
];

// 2. Lógica del Chatbot

function getBotAnswer(userInput) {
    const lowerCaseInput = userInput.toLowerCase();

    // Buscar una respuesta en la base de conocimiento
    for (const item of knowledgeBase) {
        for (const keyword of item.keywords) {
            if (lowerCaseInput.includes(keyword)) {
                return item.answer;
            }
        }
    }

    // Respuesta por defecto si no se encuentra nada
    return "Lo siento, no he entendido esa pregunta. Prueba a usar los botones de sugerencia o reformula tu duda. Puedes preguntarme sobre 'servicios', 'coste de una web' o 'instalar un flujo'.";
} 