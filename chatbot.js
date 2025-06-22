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

// Variables globales para el estado del usuario
let userLimitInfo = {
    remainingQueries: 10,
    isPremium: false,
    totalQueries: 0
};
let chatBody; // Variable global para el cuerpo del chat

// Función para cargar el límite de consultas del usuario
async function loadUserLimit() {
    try {
        const response = await fetch('/api/query-limit');
        if (response.ok) {
            userLimitInfo = await response.json();
            updateLimitDisplay();
        }
    } catch (error) {
        console.error('Error cargando límite de usuario:', error);
    }
}

// Función para actualizar la visualización del límite
function updateLimitDisplay() {
    const limitDisplay = document.getElementById('limit-display');
    if (limitDisplay) {
        if (userLimitInfo.isPremium) {
            limitDisplay.innerHTML = '💎 <strong>Premium</strong> - Consultas ilimitadas';
            limitDisplay.className = 'limit-display premium';
        } else {
            limitDisplay.innerHTML = `🔢 Consultas restantes: <strong>${userLimitInfo.remainingQueries}</strong>`;
            limitDisplay.className = 'limit-display';
        }
    }
}

// Función para crear sesión de pago con Stripe
async function createPaymentSession() {
    try {
        const response = await fetch('/api/create-payment-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Error creando sesión de pago');
        }

        const { sessionId } = await response.json();
        
        // Redirigir a Stripe Checkout
        const stripe = Stripe('pk_live_51RGg0AGayGuUgznnZ1FfHOEfSlHEdiSAhSGKO41ckEowveEs4aojJVdEcrx3MpJUp4dmfLeZ84ybN9iCe5ClzU3p00bKSWKKWR'); // Tu Stripe publishable key
        stripe.redirectToCheckout({
            sessionId: sessionId
        });

    } catch (error) {
        console.error('Error creando sesión de pago:', error);
        alert('Error procesando el pago. Por favor, intenta de nuevo.');
    }
}

// Función para confirmar pago exitoso
async function confirmPayment(sessionId) {
    try {
        const response = await fetch('/api/confirm-payment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sessionId })
        });

        if (response.ok) {
            const result = await response.json();
            if (result.success) {
                userLimitInfo.isPremium = true;
                userLimitInfo.remainingQueries = '∞';
                updateLimitDisplay();
                
                // Mostrar mensaje de éxito
                addMessage(`🎉 ¡Pago confirmado! Ya tienes acceso premium a Aura.\n\n📱 Únete a nuestro grupo de Telegram exclusivo: ${result.telegramLink}`, 'bot-message', true);
                
                // Limpiar URL
                window.history.replaceState({}, document.title, window.location.pathname);
            }
        }
    } catch (error) {
        console.error('Error confirmando pago:', error);
    }
}

// Función para obtener respuestas del chatbot con DeepSeek
async function getBotAnswer(userInput) {
    try {
        // Determinar el contexto basado en la pregunta
        let context = 'general';
        const lowerInput = userInput.toLowerCase();
        
        if (lowerInput.includes('precio') || lowerInput.includes('cuesta') || lowerInput.includes('coste')) {
            context = 'precios';
        } else if (lowerInput.includes('n8n') || lowerInput.includes('flujo') || lowerInput.includes('automatización') || lowerInput.includes('instalar')) {
            context = 'tecnico';
        }

        // Llamada al servidor
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userInput,
                context: context
            })
        });

        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }

        const data = await response.json();
        
        // Actualizar información del usuario
        if (data.success) {
            userLimitInfo.remainingQueries = data.remainingQueries;
            userLimitInfo.isPremium = data.isPremium;
            userLimitInfo.totalQueries = data.totalQueries;
            updateLimitDisplay();
            return data.response;
        } else {
            // Si hay error o límite alcanzado
            if (data.limitReached) {
                // Mostrar botón de pago
                setTimeout(() => {
                    showPaymentButton();
                }, 1000);
            }
            return data.response || getFallbackResponse(userInput);
        }

    } catch (error) {
        console.error('Error al obtener respuesta del chatbot:', error);
        return getFallbackResponse(userInput);
    }
}

// Función para mostrar botón de pago
function showPaymentButton() {
    const paymentButton = document.createElement('button');
    paymentButton.className = 'payment-btn';
    paymentButton.innerHTML = '💎 Unirme a DesArroyo.Tech Hub - 9,99€/mes';
    paymentButton.onclick = createPaymentSession;
    
    const chatBody = document.getElementById('chat-body');
    chatBody.appendChild(paymentButton);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Respuestas de fallback (mantener las existentes como respaldo)
function getFallbackResponse(userInput) {
    const lowerInput = userInput.toLowerCase();
    
    // Respuestas específicas para preguntas comunes
    if (lowerInput.includes('precio') || lowerInput.includes('cuesta') || lowerInput.includes('coste')) {
        return "Los precios varían según la complejidad del proyecto. Para una cotización personalizada, contacta con alberto@desarroyo.tech. ¡Cada proyecto es único! 💰";
    }
    
    if (lowerInput.includes('n8n') || lowerInput.includes('flujo') || lowerInput.includes('automatización')) {
        return "Para automatizaciones con n8n, primero genera tu flujo con nuestra herramienta, luego sigue los pasos de instalación. Si necesitas ayuda específica, contacta con alberto@desarroyo.tech 🔧";
    }
    
    if (lowerInput.includes('web') || lowerInput.includes('sitio')) {
        return "Creamos webs HTML personalizadas en 48h. Responde nuestra encuesta inteligente y tendrás tu web lista en tiempo récord! 🌐";
    }
    
    if (lowerInput.includes('tiempo') || lowerInput.includes('días') || lowerInput.includes('entrega')) {
        return "Webs HTML: 48h. Automatizaciones: 1-3 días. Apps móviles: 1-2 semanas. ¡Siempre más rápido de lo esperado! ⚡";
    }
    
    if (lowerInput.includes('contacto') || lowerInput.includes('email') || lowerInput.includes('hablar')) {
        return "¡Perfecto! Escribe a alberto@desarroyo.tech para cualquier consulta. Te responderemos en menos de 24h 📧";
    }
    
    if (lowerInput.includes('servicios') || lowerInput.includes('ofrecen') || lowerInput.includes('hacen')) {
        return "Ofrecemos: webs HTML, automatizaciones n8n, apps móviles, bots de WhatsApp/Telegram, IoT, y mucho más. ¡Somos tu taller digital completo! 🛠️";
    }
    
    if (lowerInput.includes('superpoderes') || lowerInput.includes('ejemplos')) {
        return "Ejemplos de 'superpoderes': automatizar reservas de Airbnb, bots que responden consultas 24/7, apps que funcionan offline, sensores que alertan por Telegram... ¡La tecnología al servicio de tu vida! 🦸‍♂️";
    }
    
    // Respuesta genérica
    return "¡Hola! Soy Aura, tu asistente de DesArroyo.Tech. Puedo ayudarte con webs, automatizaciones, apps móviles y más. ¿En qué puedo asistirte? 🤖";
}

// Función para manejar la entrada del usuario (actualizada)
async function handleUserInput(userInput) {
    addMessage(userInput, 'user-message');
    
    // Mostrar indicador de "Pensando..."
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'chat-message bot-message typing-indicator';
    typingIndicator.innerHTML = 'Pensando... <div class="loader"></div>';
    chatBody.appendChild(typingIndicator);
    chatBody.scrollTop = chatBody.scrollHeight;
    
    // Obtener la respuesta de la IA (sin temporizador)
    const botResponse = await getBotAnswer(userInput);
    
    // Quitar el indicador de "Pensando..."
    typingIndicator.remove();
    
    // Mostrar la respuesta del bot
    addMessage(botResponse, 'bot-message', true);
    
    // Añadir botones de sugerencia (si no es premium)
    if (!userLimitInfo.isPremium) {
        setTimeout(() => {
            addQuickReplies();
        }, 500);
    }
}

// Función para añadir mensajes al chat (mantener la existente)
function addMessage(message, className, isHTML = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${className}`;
    if (isHTML) {
        messageDiv.innerHTML = message;
    } else {
        messageDiv.textContent = message;
    }
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Función para añadir botones de respuesta rápida (mantener la existente)
function addQuickReplies() {
    const repliesContainer = document.createElement('div');
    repliesContainer.className = 'quick-replies';
    
    const quickReplies = [
        '¿Cómo instalo el flujo en n8n?',
        '¿Cuánto cuesta una web personalizada?',
        '¿Qué otros servicios ofrecen?',
        '¿Puedo pedir una automatización a medida?',
        'Dame ejemplos de "superpoderes"'
    ];
    
    quickReplies.forEach(replyText => {
        const replyBtn = document.createElement('button');
        replyBtn.className = 'quick-reply-btn';
        replyBtn.textContent = replyText;
        replyBtn.onclick = () => {
            handleUserInput(replyText);
            // Eliminar botones tras el uso
            const allReplies = document.querySelectorAll('.quick-replies');
            allReplies.forEach(r => r.remove());
        };
        repliesContainer.appendChild(replyBtn);
    });
    chatBody.appendChild(repliesContainer);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Función para inicializar el chat (actualizada)
async function initializeChat() {
    // Cargar límite de usuario al inicializar
    await loadUserLimit();
    
    addMessage("¡Hola! Soy Aura, tu asistente personal de DesArroyo.Tech. ¿En qué puedo ayudarte?", 'bot-message', true);
    
    // Mostrar opciones rápidas solo a usuarios no premium
    if (!userLimitInfo.isPremium) {
        addQuickReplies();
    }
}

// Verificar si hay pago exitoso en la URL
function checkForSuccessfulPayment() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session_id');
    
    if (sessionId) {
        confirmPayment(sessionId);
    }
}

// Exportar funciones para uso global
window.chatbot = {
    handleUserInput,
    addMessage,
    addQuickReplies,
    initializeChat,
    getBotAnswer,
    loadUserLimit,
    createPaymentSession
};

// --- INICIALIZACIÓN DEL CHATBOT Y MANEJO DE EVENTOS ---
document.addEventListener('DOMContentLoaded', () => {
    const chatButton = document.getElementById('chat-button');
    const chatWidget = document.getElementById('chat-widget');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    chatBody = document.getElementById('chat-body');

    console.log('🔍 Verificando elementos del chatbot...');
    console.log('Elementos encontrados:', {
        chatButton: !!chatButton,
        chatWidget: !!chatWidget,
        chatInput: !!chatInput,
        sendButton: !!sendButton,
        chatBody: !!chatBody
    });

    if (chatButton && chatWidget && chatInput && sendButton && chatBody) {
        console.log('✅ Todos los elementos encontrados, inicializando chatbot...');

        // 1. Abrir y cerrar el widget
        chatButton.addEventListener('click', async () => {
            console.log('🔄 Abriendo/cerrando chat...');
            chatWidget.classList.toggle('open');
            
            if (chatWidget.classList.contains('open') && chatBody.children.length === 0) {
                console.log('🚀 Inicializando chat por primera vez...');
                await initializeChat();
            }
            
            if (chatWidget.classList.contains('open')) {
                setTimeout(() => {
                    chatInput.focus();
                    console.log('📝 Input enfocado');
                }, 300);
            }
        });

        // 2. Función para enviar mensaje
        async function sendMessage() {
            console.log('Función sendMessage ejecutada');
            const message = chatInput.value.trim();
            console.log('Mensaje a enviar:', message);
            
            if (message !== '') {
                const allReplies = document.querySelectorAll('.quick-replies');
                allReplies.forEach(r => r.remove());
                
                await handleUserInput(message);
                chatInput.value = '';
                chatInput.style.height = 'auto'; // Resetear altura
                
                // Actualizar estado del botón
                sendButton.style.opacity = '0.5';
                sendButton.style.cursor = 'default';
                
                console.log('✅ Mensaje enviado correctamente');
            } else {
                console.log('❌ Mensaje vacío, no se envía');
            }
        }

        // 3. Enviar mensaje con la tecla Enter
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                console.log('Enter presionado');
                sendMessage();
            }
        });

        // 4. Enviar mensaje con el botón
        console.log('🧪 Añadiendo test directo al botón...');
        sendButton.onclick = function(e) {
            e.preventDefault();
            console.log('🧪 Test directo: Botón clickeado!');
            sendMessage();
        };

        // 5. Auto-resize del textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 100) + 'px';
        });

        // 6. Habilitar/deshabilitar botón según contenido
        chatInput.addEventListener('input', function() {
            const hasContent = this.value.trim() !== '';
            sendButton.style.opacity = hasContent ? '1' : '0.5';
            sendButton.style.cursor = hasContent ? 'pointer' : 'default';
        });

        // 7. Verificar pago exitoso
        checkForSuccessfulPayment();

        console.log('🎉 Chatbot inicializado correctamente');

    } else {
        console.error('❌ Elementos faltantes del chatbot:', {
            chatButton: !chatButton,
            chatWidget: !chatWidget,
            chatInput: !chatInput,
            sendButton: !sendButton,
            chatBody: !chatBody
        });
    }
}); 