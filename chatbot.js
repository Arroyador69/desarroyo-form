// DesArroyo.Tech - Chatbot "Aura" - Versión Mejorada
// Chatbot inteligente con mejor manejo de errores y respuestas más naturales

// 1. Base de Conocimiento Mejorada
const knowledgeBase = [
    {
        keywords: ["hola", "saludos", "buenas", "hey", "hi"],
        answer: "¡Hola! 👋 Soy Aura, tu asistente personal de DesArroyo.Tech. Estoy aquí para ayudarte con automatizaciones, desarrollo web y dar vida a tus ideas digitales. ¿En qué puedo ayudarte hoy?"
    },
    {
        keywords: ["n8n", "que es", "qué es"],
        answer: "🤖 <strong>n8n</strong> es una herramienta de automatización de flujos de trabajo de código abierto. Te permite conectar diferentes aplicaciones y servicios para que trabajen juntos automáticamente, sin necesidad de escribir código. ¡Es como tener superpoderes para tus tareas diarias! 🚀"
    },
    {
        keywords: ["instalo", "importar", "flujo", "json", "como instalar"],
        answer: "📥 <strong>Para instalar tu flujo:</strong><br>1. Ve a tu panel de n8n<br>2. Haz clic en 'Add workflow'<br>3. Selecciona 'Import from file'<br>4. Sube el archivo .json que generaste aquí<br>5. ¡Listo para configurar! ⚙️"
    },
    {
        keywords: ["credenciales", "conectar", "api", "clave", "configurar"],
        answer: "🔑 <strong>Las credenciales</strong> son las 'llaves' que permiten a n8n acceder a tus apps. En cada nodo de n8n, verás un campo 'Credential'. Haz clic en 'Create New' y sigue los pasos para conectar tu cuenta. ¡Es muy intuitivo! 💡"
    },
    {
        keywords: ["cuanto", "cuesta", "tiempo", "web", "personalizada", "precio"],
        answer: "💰 <strong>Precios y tiempos:</strong><br>• Webs HTML: desde 149€ (48h)<br>• Webs con Astro: desde 449€ (1 semana)<br>• Automatizaciones: desde 90€<br>• Proyectos personalizados: presupuesto a medida<br><br>📧 Escribe a <strong>alberto@desarroyo.tech</strong> para un presupuesto personalizado. ¡Nos encantan los retos! 🎯"
    },
    {
        keywords: ["servicios", "ofrecen", "que hacen"],
        answer: "🛠️ <strong>Nuestros servicios:</strong><br>• 🌐 Webs HTML ultrarrápidas<br>• ⚡ Webs full-stack con Astro<br>• 📱 Apps móviles híbridas<br>• 🤖 Bots de WhatsApp/Telegram<br>• 🔄 Automatizaciones con IA<br>• 🏨 Check-in automático para alojamientos<br>• 📊 Dashboards y CRMs<br><br>¡Todo con tecnología de vanguardia! 🚀"
    },
    {
        keywords: ["quien", "detras", "alberto", "equipo"],
        answer: "👨‍💻 <strong>Alberto Arroyo</strong> es actor, escritor y artesano del código. Fusiona su pasión por la narrativa con la tecnología para crear soluciones con alma. Ha publicado 4 libros para intérpretes y ahora canaliza esa creatividad en DesArroyo.Tech. ¡Conoce más en la sección 'Detrás del código'! 📚"
    },
    {
        keywords: ["otra", "automatizacion", "no esta", "generador", "personalizada"],
        answer: "🎯 ¡Por supuesto! El generador es solo el punto de partida. Si tienes una necesidad específica o más compleja, contáctanos en <strong>alberto@desarroyo.tech</strong>. Nos encantan los retos y crear soluciones a medida. ¡Cada proyecto es único! ✨"
    },
    {
        keywords: ["superpoderes", "ejemplos", "ideas", "casos de uso"],
        answer: "🦸‍♂️ <strong>Superpoderes con n8n:</strong><br>1. 📧 <strong>Sincronización automática:</strong> Guarda adjuntos de Gmail en Google Drive<br>2. 📱 <strong>Notificador inteligente:</strong> Telegram cuando alguien completa tu Typeform<br>3. 📊 <strong>Reportes automáticos:</strong> Resumen diario de ventas de Stripe a Google Sheets<br>4. 🤖 <strong>Chatbot personalizado:</strong> Atención al cliente 24/7<br>5. 📈 <strong>Análisis de datos:</strong> Procesamiento automático de información<br><br>¡Las posibilidades son infinitas! 🌟"
    },
    {
        keywords: ["gracias", "adios", "chau", "bye", "hasta luego"],
        answer: "¡De nada! 😊 Ha sido un placer ayudarte. Si tienes más preguntas o quieres empezar un proyecto, no dudes en contactarnos. ¡Felices automatizaciones! 🚀✨"
    },
    {
        keywords: ["error", "problema", "no funciona", "fallo"],
        answer: "🔧 <strong>Si tienes algún problema:</strong><br>1. Revisa que las credenciales estén bien configuradas<br>2. Verifica que los servicios estén conectados<br>3. Revisa los logs de n8n para errores específicos<br>4. Si persiste, escríbenos a <strong>alberto@desarroyo.tech</strong><br><br>¡Estamos aquí para ayudarte! 💪"
    },
    {
        keywords: ["web", "pagina", "sitio", "html"],
        answer: "🌐 <strong>Nuestras webs:</strong><br>• ⚡ <strong>Ultrarrápidas</strong> - Carga en menos de 2 segundos<br>• 📱 <strong>100% Responsive</strong> - Perfectas en móvil y desktop<br>• 🔍 <strong>SEO Optimizado</strong> - Posicionamiento en Google incluido<br>• 🎨 <strong>Diseño personalizado</strong> - Único para tu negocio<br>• 🚀 <strong>Hosting incluido</strong> - Sin costes ocultos<br><br>¡Desde 149€ y listas en 48 horas! ⏰"
    }
];

// 2. Configuración del Chatbot
let userLimitInfo = {
    remainingQueries: 10,
    isPremium: false,
    totalQueries: 0
};

let chatBody;
let isProcessing = false;
let retryCount = 0;
const maxRetries = 3;

// Variable para controlar si es la primera interacción
let isFirstInteraction = true;

// 3. Funciones Mejoradas

// Función para cargar el límite de consultas del usuario
async function loadUserLimit() {
    try {
        const response = await fetch('/api/query-limit', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 5000
        });
        
        if (response.ok) {
            userLimitInfo = await response.json();
            updateLimitDisplay();
        }
    } catch (error) {
        console.log('Usando límite por defecto:', error.message);
        // Usar límite por defecto si no hay conexión
        updateLimitDisplay();
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

// Función mejorada para obtener respuestas del chatbot
async function getBotAnswer(userInput) {
    if (isProcessing) {
        return "⏳ Estoy procesando tu mensaje anterior. Dame un momento...";
    }

    isProcessing = true;
    
    try {
        // Primero intentar con la base de conocimiento local
        const localAnswer = findLocalAnswer(userInput);
        if (localAnswer) {
            isProcessing = false;
            return localAnswer;
        }

        // Si no hay respuesta local y no es premium, verificar límite
        if (!userLimitInfo.isPremium && userLimitInfo.remainingQueries <= 0) {
            isProcessing = false;
            showPaymentButton();
            return "❌ Has alcanzado tu límite de consultas gratuitas. ¡Actualiza a Premium para consultas ilimitadas! 💎";
        }

        // Intentar con IA externa
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userInput,
                context: determineContext(userInput)
            }),
            timeout: 10000
        });

        if (response.ok) {
            const data = await response.json();
            
            if (data.success) {
                userLimitInfo.remainingQueries = data.remainingQueries;
                userLimitInfo.isPremium = data.isPremium;
                userLimitInfo.totalQueries = data.totalQueries;
                updateLimitDisplay();
                retryCount = 0;
                isProcessing = false;
                return data.response;
            } else {
                throw new Error(data.error || 'Error en la respuesta');
            }
        } else {
            throw new Error(`HTTP ${response.status}`);
        }

    } catch (error) {
        console.error('Error al obtener respuesta:', error);
        retryCount++;
        
        if (retryCount < maxRetries) {
            // Reintentar
            setTimeout(() => {
                isProcessing = false;
            }, 2000);
            return `🔄 Reintentando... (${retryCount}/${maxRetries})`;
        } else {
            // Usar respuesta de fallback
            retryCount = 0;
            isProcessing = false;
            return getFallbackResponse(userInput);
        }
    }
}

// Función para encontrar respuestas en la base de conocimiento local
function findLocalAnswer(userInput) {
    const lowerInput = userInput.toLowerCase();
    
    for (const item of knowledgeBase) {
        for (const keyword of item.keywords) {
            if (lowerInput.includes(keyword)) {
                return item.answer;
            }
        }
    }
    
    return null;
}

// Función para determinar el contexto de la pregunta
function determineContext(userInput) {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('precio') || lowerInput.includes('cuesta') || lowerInput.includes('coste')) {
        return 'precios';
    } else if (lowerInput.includes('n8n') || lowerInput.includes('flujo') || lowerInput.includes('automatización')) {
        return 'tecnico';
    } else if (lowerInput.includes('web') || lowerInput.includes('pagina') || lowerInput.includes('sitio')) {
        return 'web';
    } else if (lowerInput.includes('error') || lowerInput.includes('problema') || lowerInput.includes('fallo')) {
        return 'soporte';
    }
    
    return 'general';
}

// Función de fallback mejorada
function getFallbackResponse(userInput) {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('hola') || lowerInput.includes('saludos')) {
        return "¡Hola! 👋 Soy Aura, tu asistente de DesArroyo.Tech. ¿En qué puedo ayudarte hoy?";
    } else if (lowerInput.includes('web') || lowerInput.includes('pagina')) {
        return "🌐 <strong>Nuestras webs:</strong> Desde 149€, listas en 48 horas, 100% responsive y SEO optimizado. ¡Escribe a alberto@desarroyo.tech para más info!";
    } else if (lowerInput.includes('n8n') || lowerInput.includes('automatizacion')) {
        return "🤖 <strong>n8n</strong> es una herramienta de automatización que conecta apps sin código. ¡Perfecta para automatizar tareas!";
    } else {
        return "🤔 Interesante pregunta. Para darte la mejor respuesta, escríbenos a <strong>alberto@desarroyo.tech</strong>. ¡Estamos aquí para ayudarte! 💪";
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
    
    // Marcar que ya no es la primera interacción
    isFirstInteraction = false;
    
    // NO añadir botones de sugerencia después de la primera interacción
    // (las opciones rápidas solo aparecen al abrir el chat por primera vez)
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
    
    // Mostrar opciones rápidas solo la primera vez que se abre el chat
    if (isFirstInteraction) {
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
                // Resetear la variable para mostrar opciones al abrir el chat
                isFirstInteraction = true;
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