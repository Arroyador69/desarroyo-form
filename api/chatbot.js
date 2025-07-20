/**
 * 🤖 API Chatbot Aura - DesArroyo.tech
 * Endpoint para el chatbot con DeepSeek y límites de uso
 */

const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Configuración
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;
const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';
const MAX_FREE_QUERIES = 10; // Límite para usuarios gratuitos
const PREMIUM_IPS = [
    '5.224.13.147',  // IP de desarrollo
    '127.0.0.1',     // Localhost
    '::1'            // Localhost IPv6
];

// Base de datos para tracking
const dbPath = path.join(__dirname, '../dashboard.db');
const db = new sqlite3.Database(dbPath);

// Inicializar tabla de tracking si no existe
db.serialize(() => {
    db.run(`CREATE TABLE IF NOT EXISTS chatbot_usage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip_address TEXT NOT NULL,
        user_agent TEXT,
        query_count INTEGER DEFAULT 0,
        last_query TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_premium BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )`);
});

// Base de conocimiento local de Aura
const auraKnowledge = [
    {
        keywords: ["hola", "saludos", "buenas", "hey", "hi"],
        answer: "¡Hola! 👋 Soy Aura, tu asistente personal de DesArroyo.Tech. Estoy aquí para ayudarte con automatizaciones, desarrollo web y dar vida a tus ideas digitales. ¿En qué puedo ayudarte hoy?"
    },
    {
        keywords: ["shortcuts", "iphone", "superpoderes", "atajos"],
        answer: "⚡ <strong>Shortcuts para iPhone</strong> son automatizaciones que te dan superpoderes tecnológicos. Puedes descargar los nuestros en la página de shortcuts. ¿Te gustaría que te explique alguno en particular?"
    },
    {
        keywords: ["telegram", "grupo", "tech hub", "comunidad"],
        answer: "💬 <strong>Tech Hub</strong> es nuestro grupo de Telegram gratuito donde compartimos las últimas novedades en tecnología, automatizaciones y trucos para iPhone. ¡Únete y forma parte de nuestra comunidad! 🚀"
    },
    {
        keywords: ["web", "pagina", "sitio", "html", "desarrollo"],
        answer: "🌐 <strong>Nuestras webs:</strong><br>• ⚡ Ultrarrápidas - Carga en menos de 2 segundos<br>• 📱 100% Responsive - Perfectas en móvil y desktop<br>• 🔍 SEO Optimizado - Posicionamiento en Google incluido<br>• 🎨 Diseño personalizado - Único para tu negocio<br>• 🚀 Hosting gratuito incluido<br><br>¡Desde 149€ y listas en 48 horas! ⏰<br><br>💡 <strong>¿Quieres crear tu web?</strong> Haz clic en 'Web Personalizada' en esta página para acceder al formulario."
    },
    {
        keywords: ["precio", "cuesta", "cuanto", "presupuesto"],
        answer: "💰 <strong>Precios y tiempos:</strong><br>• Webs HTML: desde 149€ (48h)<br>• Webs con Astro: desde 449€ (1 semana)<br>• Automatizaciones: desde 90€<br>• Proyectos personalizados: presupuesto a medida<br><br>📧 Escribe a <strong>alberto@desarroyo.tech</strong> para un presupuesto personalizado. ¡Nos encantan los retos! 🎯"
    },
    {
        keywords: ["formulario", "crear web", "encuesta", "48 horas"],
        answer: "🎯 <strong>¡Perfecto! Para crear tu web personalizada:</strong><br><br>1. Haz clic en 'Web Personalizada' en esta página<br>2. Completa la encuesta inteligente (5 minutos)<br>3. Recibe tu web en 48 horas<br>4. ¡Desde solo 149€!<br><br>⚡ <strong>El formulario te guiará paso a paso</strong> para crear la web perfecta para tu negocio. ¡Es súper fácil!"
    },
    {
        keywords: ["gracias", "adios", "chau", "bye", "hasta luego"],
        answer: "¡De nada! 😊 Ha sido un placer ayudarte. Si tienes más preguntas o quieres empezar un proyecto, no dudes en contactarnos. ¡Felices automatizaciones! 🚀✨"
    }
];

// Función para obtener IP del usuario
function getClientIP(req) {
    return req.headers['x-forwarded-for'] || 
           req.connection.remoteAddress || 
           req.socket.remoteAddress ||
           (req.connection.socket ? req.connection.socket.remoteAddress : null);
}

// Función para verificar si es IP premium
function isPremiumIP(ip) {
    return PREMIUM_IPS.includes(ip);
}

// Función para obtener o crear registro de uso
function getUserUsage(ip, userAgent) {
    return new Promise((resolve, reject) => {
        db.get(
            'SELECT * FROM chatbot_usage WHERE ip_address = ?',
            [ip],
            (err, row) => {
                if (err) {
                    reject(err);
                    return;
                }
                
                if (row) {
                    resolve(row);
                } else {
                    // Crear nuevo registro
                    const isPremium = isPremiumIP(ip);
                    db.run(
                        'INSERT INTO chatbot_usage (ip_address, user_agent, is_premium) VALUES (?, ?, ?)',
                        [ip, userAgent, isPremium],
                        function(err) {
                            if (err) {
                                reject(err);
                                return;
                            }
                            resolve({
                                id: this.lastID,
                                ip_address: ip,
                                user_agent: userAgent,
                                query_count: 0,
                                is_premium: isPremium
                            });
                        }
                    );
                }
            }
        );
    });
}

// Función para incrementar contador de consultas
function incrementQueryCount(ip) {
    return new Promise((resolve, reject) => {
        db.run(
            'UPDATE chatbot_usage SET query_count = query_count + 1, last_query = CURRENT_TIMESTAMP WHERE ip_address = ?',
            [ip],
            (err) => {
                if (err) reject(err);
                else resolve();
            }
        );
    });
}

// Función para buscar respuesta en conocimiento local
function findLocalAnswer(message) {
    const lowerMessage = message.toLowerCase();
    
    for (const item of auraKnowledge) {
        for (const keyword of item.keywords) {
            if (lowerMessage.includes(keyword)) {
                return item.answer;
            }
        }
    }
    
    return null;
}

// Función para consultar DeepSeek
async function queryDeepSeek(message, userContext = '') {
    if (!DEEPSEEK_API_KEY) {
        throw new Error('API key de DeepSeek no configurada');
    }

    const systemPrompt = `Eres Aura, un asistente especializado en tecnología, automatizaciones, desarrollo web y shortcuts para iPhone. 
    
Contexto del usuario: ${userContext}

Responde de forma amigable, profesional y siempre en español. Incluye emojis apropiados y formatea con HTML cuando sea necesario.
Mantén las respuestas concisas pero informativas. Si te preguntan sobre servicios de DesArroyo.Tech, menciona los precios y enlaces relevantes.`;

    try {
        const response = await axios.post(DEEPSEEK_URL, {
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: systemPrompt
                },
                {
                    role: 'user',
                    content: message
                }
            ],
            max_tokens: 300,
            temperature: 0.7
        }, {
            headers: {
                'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
                'Content-Type': 'application/json'
            },
            timeout: 15000
        });

        return response.data.choices[0].message.content;
    } catch (error) {
        console.error('Error en DeepSeek:', error.message);
        throw new Error('No pude procesar tu consulta en este momento. ¿Podrías intentarlo de nuevo?');
    }
}

// Endpoint principal del chatbot
async function handleChatbotRequest(req, res) {
    try {
        const { message } = req.body;
        
        if (!message || typeof message !== 'string') {
            return res.status(400).json({
                success: false,
                error: 'Mensaje requerido'
            });
        }

        const clientIP = getClientIP(req);
        const userAgent = req.headers['user-agent'] || 'Unknown';
        
        // Obtener información de uso del usuario
        const userUsage = await getUserUsage(clientIP, userAgent);
        
        // Verificar límites (excepto para IPs premium)
        if (!userUsage.is_premium && userUsage.query_count >= MAX_FREE_QUERIES) {
            return res.json({
                success: false,
                error: 'Límite de consultas alcanzado',
                message: `Has alcanzado el límite de ${MAX_FREE_QUERIES} consultas gratuitas. Para consultas ilimitadas, contacta con alberto@desarroyo.tech`,
                limitReached: true,
                currentCount: userUsage.query_count,
                maxQueries: MAX_FREE_QUERIES
            });
        }

        // Incrementar contador
        await incrementQueryCount(clientIP);

        // Primero intentar respuesta local
        const localAnswer = findLocalAnswer(message);
        
        if (localAnswer) {
            return res.json({
                success: true,
                message: localAnswer,
                source: 'local',
                queryCount: userUsage.query_count + 1,
                isPremium: userUsage.is_premium
            });
        }

        // Si no hay respuesta local, usar DeepSeek
        const deepseekAnswer = await queryDeepSeek(message, `IP: ${clientIP}, Consultas previas: ${userUsage.query_count}`);
        
        return res.json({
            success: true,
            message: deepseekAnswer,
            source: 'deepseek',
            queryCount: userUsage.query_count + 1,
            isPremium: userUsage.is_premium
        });

    } catch (error) {
        console.error('Error en chatbot:', error);
        
        return res.status(500).json({
            success: false,
            error: 'Error interno del servidor',
            message: 'Lo siento, estoy teniendo problemas técnicos. ¿Podrías intentarlo de nuevo en unos minutos?'
        });
    }
}

// Endpoint para obtener estadísticas de uso
function getUsageStats(req, res) {
    const clientIP = getClientIP(req);
    
    db.get(
        'SELECT query_count, is_premium, last_query FROM chatbot_usage WHERE ip_address = ?',
        [clientIP],
        (err, row) => {
            if (err) {
                return res.status(500).json({
                    success: false,
                    error: 'Error al obtener estadísticas'
                });
            }
            
            if (!row) {
                return res.json({
                    success: true,
                    stats: {
                        queryCount: 0,
                        isPremium: isPremiumIP(clientIP),
                        maxQueries: MAX_FREE_QUERIES,
                        remainingQueries: MAX_FREE_QUERIES
                    }
                });
            }
            
            const remainingQueries = row.is_premium ? '∞' : Math.max(0, MAX_FREE_QUERIES - row.query_count);
            
            return res.json({
                success: true,
                stats: {
                    queryCount: row.query_count,
                    isPremium: row.is_premium,
                    maxQueries: MAX_FREE_QUERIES,
                    remainingQueries: remainingQueries,
                    lastQuery: row.last_query
                }
            });
        }
    );
}

module.exports = {
    handleChatbotRequest,
    getUsageStats
}; 