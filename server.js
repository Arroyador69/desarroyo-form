const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const GestorComponentes = require('./bloques_html/componentes');
const axios = require('axios');
const stripe = require('stripe');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// Inicializar el gestor de componentes
const gestorComponentes = new GestorComponentes();

// Asegura que la carpeta 'respuestas' existe
const respuestasDir = path.join(__dirname, 'respuestas');
if (!fs.existsSync(respuestasDir)) {
  fs.mkdirSync(respuestasDir);
}

// Configuración de DeepSeek
const DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions';
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY;

// Configuración de Stripe
const stripeClient = stripe(process.env.STRIPE_SECRET_KEY);

// Almacenamiento de consultas por IP (en producción usar Redis o base de datos)
const userQueries = new Map();
const CONSULTAS_GRATUITAS = 10;

// IPs con acceso premium (tu IP y otras que quieras añadir)
const PREMIUM_IPS = [
    '5.224.13.147', // Tu IP actual
    '127.0.0.1',    // Localhost para desarrollo
    '::1'           // Localhost IPv6
];

// Función para obtener IP del usuario
function getClientIP(req) {
    return req.headers['x-forwarded-for'] || 
           req.connection.remoteAddress || 
           req.socket.remoteAddress ||
           (req.connection.socket ? req.connection.socket.remoteAddress : null);
}

// Función para verificar límite de consultas
function checkQueryLimit(ip) {
    // Si es una IP premium, acceso ilimitado
    if (PREMIUM_IPS.includes(ip)) {
        return {
            canQuery: true,
            remainingQueries: '∞',
            isPremium: true,
            totalQueries: 0
        };
    }
    
    const userData = userQueries.get(ip) || { count: 0, isPremium: false };
    return {
        canQuery: userData.count < CONSULTAS_GRATUITAS || userData.isPremium,
        remainingQueries: Math.max(0, CONSULTAS_GRATUITAS - userData.count),
        isPremium: userData.isPremium,
        totalQueries: userData.count
    };
}

// Función para incrementar contador de consultas
function incrementQueryCount(ip) {
    // No incrementar contador para IPs premium
    if (PREMIUM_IPS.includes(ip)) {
        return { count: 0, isPremium: true };
    }
    
    const userData = userQueries.get(ip) || { count: 0, isPremium: false };
    userData.count++;
    userQueries.set(ip, userData);
    return userData;
}

// Contexto del chatbot para DesArroyo.Tech
const SYSTEM_PROMPT = `Eres Aura, el asistente virtual de DesArroyo.Tech. Tu función es ayudar a los usuarios con:

SERVICIOS PRINCIPALES:
- Creación de webs HTML personalizadas (entrega en 48h)
- Generación de flujos de automatización con n8n
- Apps móviles híbridas (PWA/Capacitor)
- Bots de WhatsApp y Telegram
- Self-Check-in legal para Airbnb/Booking
- Automatizaciones con IA
- Servicios online + offline
- Prototipado IoT y wearables
- Generación automática de contenido

INFORMACIÓN DE LA EMPRESA:
- Fundador: Alberto Arroyo (Dos Hermanas, 1997)
- Actor, escritor y desarrollador
- Email: alberto@desarroyo.tech
- Filosofía: "Crea, automatiza, comparte… y vuelve a la playa a celebrar"

ESTILO DE COMUNICACIÓN:
- Amigable pero profesional
- Respuestas concisas pero informativas
- Usar emojis ocasionalmente para mantener el tono cercano
- Siempre ofrecer ayuda específica y concreta
- Si no sabes algo, ser honesto y redirigir al email de contacto

PRECIOS Y PLAZOS:
- Webs HTML: 48h de entrega
- Automatizaciones: Precio según complejidad
- Consultar precios específicos por email

IMPORTANTE: Si el usuario pregunta sobre precios específicos o proyectos complejos, siempre sugiere contactar por email a alberto@desarroyo.tech para una consulta personalizada.`;

// Endpoint para verificar límite de consultas
app.get('/api/query-limit', (req, res) => {
    const ip = getClientIP(req);
    const limitInfo = checkQueryLimit(ip);
    res.json(limitInfo);
});

// Endpoint para crear sesión de pago con Stripe
app.post('/api/create-payment-session', async (req, res) => {
    try {
        const session = await stripeClient.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: [
                {
                    price_data: {
                        currency: 'eur',
                        product_data: {
                            name: 'Acceso Premium Aura - DesArroyo.Tech',
                            description: 'Consultas ilimitadas con Aura + Acceso al grupo de Telegram exclusivo',
                        },
                        unit_amount: 999, // 9.99€ en céntimos
                    },
                    quantity: 1,
                },
            ],
            mode: 'payment',
            success_url: `${req.headers.origin}/success.html?session_id={CHECKOUT_SESSION_ID}`,
            cancel_url: `${req.headers.origin}/cancel.html`,
            metadata: {
                ip: getClientIP(req)
            }
        });

        res.json({ sessionId: session.id });
    } catch (error) {
        console.error('Error creando sesión de pago:', error);
        res.status(500).json({ error: 'Error creando sesión de pago' });
    }
});

// Endpoint para confirmar pago exitoso
app.post('/api/confirm-payment', async (req, res) => {
    try {
        const { sessionId } = req.body;
        const session = await stripeClient.checkout.sessions.retrieve(sessionId);
        
        if (session.payment_status === 'paid') {
            const ip = session.metadata.ip;
            const userData = userQueries.get(ip) || { count: 0, isPremium: false };
            userData.isPremium = true;
            userQueries.set(ip, userData);
            
            res.json({ 
                success: true, 
                message: '¡Pago confirmado! Ya tienes acceso premium a Aura.',
                telegramLink: 'https://t.me/desarroyo_tech_premium' // Tu grupo de Telegram
            });
        } else {
            res.status(400).json({ error: 'Pago no completado' });
        }
    } catch (error) {
        console.error('Error confirmando pago:', error);
        res.status(500).json({ error: 'Error confirmando pago' });
    }
});

// Endpoint para obtener información de componentes
app.get('/api/componentes', (req, res) => {
    try {
        const gestor = new GestorComponentes();
        const componentes = gestor.obtenerTodosLosComponentes();
        res.json(componentes);
    } catch (error) {
        console.error('Error al obtener componentes:', error);
        res.status(500).json({ error: 'Error al obtener componentes' });
    }
});

// Endpoint para guardar respuestas
app.post('/api/guardar-respuestas', (req, res) => {
    try {
        const { prompt, respuestas } = req.body;
        
        if (!prompt || !respuestas) {
            return res.status(400).json({ error: 'Faltan datos requeridos' });
        }

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const promptFile = path.join(respuestasDir, `prompt_${timestamp}.txt`);
        const respuestasFile = path.join(respuestasDir, `respuestas_${timestamp}.json`);

        fs.writeFileSync(promptFile, prompt);
        fs.writeFileSync(respuestasFile, JSON.stringify(respuestas, null, 2));

        res.json({ ok: true, mensaje: 'Respuestas y prompt guardados correctamente.' });
    } catch (error) {
        console.error('Error al guardar respuestas:', error);
        res.status(500).json({ error: 'Error al guardar respuestas' });
    }
});

// Endpoint para el chatbot (actualizado con límite)
app.post('/api/chat', async (req, res) => {
    try {
        const { message, context = 'general' } = req.body;
        const ip = getClientIP(req);
        
        // Verificar límite de consultas
        const limitInfo = checkQueryLimit(ip);
        
        if (!limitInfo.canQuery) {
            return res.json({
                response: `🚫 Has alcanzado el límite de ${CONSULTAS_GRATUITAS} consultas gratuitas.\n\n💎 **¡Desbloquea Aura Premium!**\n\n✅ Consultas ilimitadas\n✅ Acceso al grupo de Telegram exclusivo\n✅ Contenido premium sobre tech y automatizaciones\n✅ Soporte prioritario\n\n💳 **Solo 9.99€** - ¡Pago único!\n\nHaz clic en "Desbloquear Premium" para continuar.`,
                success: false,
                limitReached: true,
                remainingQueries: 0,
                isPremium: false
            });
        }

        if (!DEEPSEEK_API_KEY) {
            return res.status(500).json({
                error: 'API key de DeepSeek no configurada',
                fallback: 'Por favor, contacta con alberto@desarroyo.tech para obtener ayuda personalizada.'
            });
        }

        // Construir el mensaje con contexto
        const messages = [
            { role: 'system', content: SYSTEM_PROMPT },
            { role: 'user', content: message }
        ];

        // Llamada a DeepSeek
        const response = await axios.post(DEEPSEEK_API_URL, {
            model: 'deepseek-chat',
            messages: messages,
            max_tokens: 500,
            temperature: 0.7,
            stream: false
        }, {
            headers: {
                'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        const botResponse = response.data.choices[0].message.content;

        // Incrementar contador de consultas
        const userData = incrementQueryCount(ip);
        const newLimitInfo = checkQueryLimit(ip);

        res.json({
            response: botResponse,
            success: true,
            remainingQueries: newLimitInfo.remainingQueries,
            isPremium: newLimitInfo.isPremium,
            totalQueries: userData.count
        });

    } catch (error) {
        console.error('Error en el chatbot:', error);
        
        // Respuesta de fallback
        const fallbackResponses = {
            'precios': 'Para consultar precios específicos, te recomiendo contactar directamente con alberto@desarroyo.tech. Cada proyecto es único y merece una cotización personalizada.',
            'tecnico': 'Para consultas técnicas específicas, nuestro equipo puede ayudarte mejor por email. Contacta con alberto@desarroyo.tech',
            'general': 'Disculpa, estoy teniendo problemas técnicos. Por favor, contacta con alberto@desarroyo.tech para obtener ayuda inmediata.'
        };

        res.json({
            response: fallbackResponses[context] || fallbackResponses.general,
            success: false,
            error: 'Error de conexión con IA'
        });
    }
});

// Endpoint de salud
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        service: 'DesArroyo.Tech Chatbot',
        timestamp: new Date().toISOString()
    });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/generador_automatizaciones.html', (req, res) => {
    res.sendFile(__dirname + '/generador_automatizaciones.html');
});

// Manejo de errores
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Algo salió mal',
        message: 'Contacta con alberto@desarroyo.tech para ayuda'
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Servidor DesArroyo.Tech ejecutándose en puerto ${PORT}`);
    console.log(`🤖 Chatbot con DeepSeek activo`);
    console.log(`💳 Sistema de pagos con Stripe configurado`);
    console.log(`📧 Contacto: alberto@desarroyo.tech`);
}); 