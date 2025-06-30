const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const GestorComponentes = require('./bloques_html/componentes');
const axios = require('axios');
const stripe = require('stripe');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const sqlite3 = require('sqlite3').verbose();
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// Inicializar el gestor de componentes
const gestorComponentes = new GestorComponentes();

// Inicializar base de datos SQLite
const db = new sqlite3.Database('./dashboard.db', (err) => {
    if (err) {
        console.error('Error conectando a la base de datos:', err);
    } else {
        console.log('✅ Base de datos SQLite conectada');
        initDatabase();
    }
});

// Inicializar tablas de la base de datos
function initDatabase() {
    // Tabla de usuarios (admin)
    db.run(`CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'admin',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Tabla de clientes
    db.run(`CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        company TEXT,
        project_name TEXT,
        domain TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Tabla de proyectos
    db.run(`CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        domain TEXT,
        status TEXT DEFAULT 'pending',
        progress INTEGER DEFAULT 0,
        budget REAL,
        start_date DATE,
        end_date DATE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )`);

    // Tabla de automatizaciones
    db.run(`CREATE TABLE IF NOT EXISTS automations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        type TEXT,
        config TEXT,
        active BOOLEAN DEFAULT 1,
        executions INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )`);

    // Tabla de leads
    db.run(`CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        company TEXT,
        notes TEXT,
        source TEXT DEFAULT 'manual',
        status TEXT DEFAULT 'new',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )`);

    // Tabla de actividad
    db.run(`CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        description TEXT,
        entity_type TEXT,
        entity_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`);

    // Crear usuario admin por defecto si no existe
    const adminPassword = process.env.ADMIN_PASSWORD || 'admin123';
    bcrypt.hash(adminPassword, 10, (err, hash) => {
        if (err) {
            console.error('Error hasheando contraseña admin:', err);
            return;
        }
        
        db.run(`INSERT OR IGNORE INTO users (username, email, password, role) VALUES (?, ?, ?, ?)`,
            ['admin', 'alberto@desarroyo.tech', hash, 'admin'],
            (err) => {
                if (err) {
                    console.error('Error creando usuario admin:', err);
                } else {
                    console.log('✅ Usuario admin creado/verificado');
                }
            }
        );
    });
}

// Middleware de autenticación JWT
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Token de acceso requerido' });
    }

    jwt.verify(token, process.env.JWT_SECRET || 'desarroyo-secret-key', (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Token inválido' });
        }
        req.user = user;
        next();
    });
}

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

// ===== RUTAS DEL DASHBOARD =====

// Ruta del dashboard
app.get('/dashboard', (req, res) => {
    res.sendFile(path.join(__dirname, 'dashboard.html'));
});

// Ruta del login
app.get('/login.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'login.html'));
});

// Login del dashboard
app.post('/api/dashboard/login', (req, res) => {
    const { username, password } = req.body;
    
    db.get('SELECT * FROM users WHERE username = ?', [username], (err, user) => {
        if (err) {
            return res.status(500).json({ error: 'Error en la base de datos' });
        }
        
        if (!user) {
            return res.status(401).json({ error: 'Usuario no encontrado' });
        }
        
        bcrypt.compare(password, user.password, (err, isMatch) => {
            if (err) {
                return res.status(500).json({ error: 'Error verificando contraseña' });
            }
            
            if (!isMatch) {
                return res.status(401).json({ error: 'Contraseña incorrecta' });
            }
            
            const token = jwt.sign(
                { id: user.id, username: user.username, role: user.role },
                process.env.JWT_SECRET || 'desarroyo-secret-key',
                { expiresIn: '24h' }
            );
            
            res.json({
                success: true,
                token,
                user: {
                    id: user.id,
                    username: user.username,
                    email: user.email,
                    role: user.role
                }
            });
        });
    });
});

// Obtener datos del dashboard
app.get('/api/dashboard/overview', authenticateToken, (req, res) => {
    const overview = {};
    
    // Contar clientes
    db.get('SELECT COUNT(*) as count FROM clients', (err, result) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo datos' });
        }
        overview.totalClients = result.count;
        
        // Contar proyectos activos
        db.get('SELECT COUNT(*) as count FROM projects WHERE status = "active"', (err, result) => {
            if (err) {
                return res.status(500).json({ error: 'Error obteniendo datos' });
            }
            overview.activeProjects = result.count;
            
            // Contar automatizaciones
            db.get('SELECT COUNT(*) as count FROM automations WHERE active = 1', (err, result) => {
                if (err) {
                    return res.status(500).json({ error: 'Error obteniendo datos' });
                }
                overview.activeAutomations = result.count;
                
                // Calcular ingresos (simulado por ahora)
                overview.monthlyRevenue = 2499;
                
                res.json(overview);
            });
        });
    });
});

// Obtener clientes
app.get('/api/dashboard/clients', authenticateToken, (req, res) => {
    db.all('SELECT * FROM clients ORDER BY created_at DESC', (err, clients) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo clientes' });
        }
        res.json(clients);
    });
});

// Crear nuevo cliente
app.post('/api/dashboard/clients', authenticateToken, (req, res) => {
    const { name, email, phone, company, project_name, domain } = req.body;
    
    db.run(
        'INSERT INTO clients (name, email, phone, company, project_name, domain) VALUES (?, ?, ?, ?, ?, ?)',
        [name, email, phone, company, project_name, domain],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error creando cliente' });
            }
            
            // Registrar actividad
            db.run(
                'INSERT INTO activity_log (user_id, action, description, entity_type, entity_id) VALUES (?, ?, ?, ?, ?)',
                [req.user.id, 'CREATE', `Cliente creado: ${name}`, 'client', this.lastID]
            );
            
            res.json({ 
                success: true, 
                id: this.lastID,
                message: 'Cliente creado exitosamente' 
            });
        }
    );
});

// Actualizar cliente
app.put('/api/dashboard/clients/:id', authenticateToken, (req, res) => {
    const { id } = req.params;
    const { name, email, phone, company, project_name, domain, status } = req.body;
    
    db.run(
        'UPDATE clients SET name = ?, email = ?, phone = ?, company = ?, project_name = ?, domain = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
        [name, email, phone, company, project_name, domain, status, id],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error actualizando cliente' });
            }
            
            if (this.changes === 0) {
                return res.status(404).json({ error: 'Cliente no encontrado' });
            }
            
            res.json({ success: true, message: 'Cliente actualizado exitosamente' });
        }
    );
});

// Eliminar cliente
app.delete('/api/dashboard/clients/:id', authenticateToken, (req, res) => {
    const { id } = req.params;
    
    db.run('DELETE FROM clients WHERE id = ?', [id], function(err) {
        if (err) {
            return res.status(500).json({ error: 'Error eliminando cliente' });
        }
        
        if (this.changes === 0) {
            return res.status(404).json({ error: 'Cliente no encontrado' });
        }
        
        res.json({ success: true, message: 'Cliente eliminado exitosamente' });
    });
});

// Obtener proyectos
app.get('/api/dashboard/projects', authenticateToken, (req, res) => {
    db.all(`
        SELECT p.*, c.name as client_name 
        FROM projects p 
        LEFT JOIN clients c ON p.client_id = c.id 
        ORDER BY p.created_at DESC
    `, (err, projects) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo proyectos' });
        }
        res.json(projects);
    });
});

// Crear nuevo proyecto
app.post('/api/dashboard/projects', authenticateToken, (req, res) => {
    const { client_id, name, description, domain, budget, start_date, end_date } = req.body;
    
    db.run(
        'INSERT INTO projects (client_id, name, description, domain, budget, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?, ?)',
        [client_id, name, description, domain, budget, start_date, end_date],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error creando proyecto' });
            }
            
            res.json({ 
                success: true, 
                id: this.lastID,
                message: 'Proyecto creado exitosamente' 
            });
        }
    );
});

// Obtener automatizaciones
app.get('/api/dashboard/automations', authenticateToken, (req, res) => {
    db.all(`
        SELECT a.*, c.name as client_name 
        FROM automations a 
        LEFT JOIN clients c ON a.client_id = c.id 
        ORDER BY a.created_at DESC
    `, (err, automations) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo automatizaciones' });
        }
        res.json(automations);
    });
});

// Obtener actividad reciente
app.get('/api/dashboard/activity', authenticateToken, (req, res) => {
    db.all(`
        SELECT al.*, u.username 
        FROM activity_log al 
        LEFT JOIN users u ON al.user_id = u.id 
        ORDER BY al.created_at DESC 
        LIMIT 20
    `, (err, activity) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo actividad' });
        }
        res.json(activity);
    });
});

// ===== RUTAS EXISTENTES =====

// Endpoint para verificar límite de consultas
app.get('/api/query-limit', (req, res) => {
    const ip = getClientIP(req);
    const limitInfo = checkQueryLimit(ip);
    res.json(limitInfo);
});

// Endpoint para crear sesión de pago con Stripe (actualizado a suscripción)
app.post('/api/create-payment-session', async (req, res) => {
    try {
        const session = await stripeClient.checkout.sessions.create({
            payment_method_types: ['card'],
            line_items: [
                {
                    price_data: {
                        currency: 'eur',
                        product_data: {
                            name: 'Suscripción DesArroyo.Tech Hub',
                            description: 'Acceso completo a la comunidad y herramientas de DesArroyo.Tech.',
                        },
                        unit_amount: 999, // 9.99€ en céntimos
                        recurring: {
                            interval: 'month', // Cobro mensual
                        },
                    },
                    quantity: 1,
                },
            ],
            mode: 'subscription', // Cambiado a modo suscripción
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
                telegramLink: 'https://t.me/+rAtJXuHGH8o4NzRk' // Enlace actualizado
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
                response: `🚫 **Has alcanzado el límite de consultas gratuitas.**\n\n💎 **Únete a DesArroyo.Tech Hub por 9,99€/mes y obtén:**\n\n✅ **Chatbot Ilimitado:** Habla con Aura siempre que quieras.\n✅ **Acceso Anticipado:** Prueba nuevos productos y herramientas antes que nadie.\n✅ **Descuentos Exclusivos:** Ofertas especiales en todos nuestros servicios.\n✅ **Comunidad Privada:** Acceso al grupo de Telegram para networking y soporte.\n\n👇 **Haz clic para unirte ahora.**`,
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

// API endpoints para mini-CRM de clientes
app.get('/api/client/:clientId/info', (req, res) => {
    const { clientId } = req.params;
    
    db.get('SELECT * FROM clients WHERE id = ?', [clientId], (err, client) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo información del cliente' });
        }
        
        if (!client) {
            return res.status(404).json({ error: 'Cliente no encontrado' });
        }
        
        res.json({
            id: client.id,
            name: client.name,
            email: client.email,
            project_name: client.project_name,
            domain: client.domain,
            status: client.status
        });
    });
});

app.get('/api/client/:clientId/leads', (req, res) => {
    const { clientId } = req.params;
    
    db.all('SELECT * FROM leads WHERE client_id = ? ORDER BY created_at DESC', [clientId], (err, leads) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo leads' });
        }
        
        res.json(leads || []);
    });
});

app.post('/api/client/:clientId/leads', (req, res) => {
    const { clientId } = req.params;
    const { name, email, phone, company, notes, source } = req.body;
    
    if (!name || !email) {
        return res.status(400).json({ error: 'Nombre y email son requeridos' });
    }
    
    db.run(
        'INSERT INTO leads (client_id, name, email, phone, company, notes, source, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
        [clientId, name, email, phone, company, notes, source, 'new'],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error creando lead' });
            }
            
            // Registrar actividad
            db.run(
                'INSERT INTO activity_log (action, description, entity_type, entity_id) VALUES (?, ?, ?, ?)',
                ['CREATE', `Nuevo lead: ${name}`, 'lead', this.lastID]
            );
            
            res.json({ 
                success: true, 
                id: this.lastID,
                message: 'Lead creado exitosamente' 
            });
        }
    );
});

app.put('/api/client/:clientId/leads/:leadId', (req, res) => {
    const { clientId, leadId } = req.params;
    const { name, email, phone, company, notes, status } = req.body;
    
    db.run(
        'UPDATE leads SET name = ?, email = ?, phone = ?, company = ?, notes = ?, status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND client_id = ?',
        [name, email, phone, company, notes, status, leadId, clientId],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error actualizando lead' });
            }
            
            if (this.changes === 0) {
                return res.status(404).json({ error: 'Lead no encontrado' });
            }
            
            res.json({ success: true, message: 'Lead actualizado exitosamente' });
        }
    );
});

app.delete('/api/client/:clientId/leads/:leadId', (req, res) => {
    const { clientId, leadId } = req.params;
    
    db.run(
        'DELETE FROM leads WHERE id = ? AND client_id = ?',
        [leadId, clientId],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error eliminando lead' });
            }
            
            if (this.changes === 0) {
                return res.status(404).json({ error: 'Lead no encontrado' });
            }
            
            res.json({ success: true, message: 'Lead eliminado exitosamente' });
        }
    );
});

app.get('/api/client/:clientId/automations', (req, res) => {
    const { clientId } = req.params;
    
    db.all('SELECT * FROM automations WHERE client_id = ? ORDER BY created_at DESC', [clientId], (err, automations) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo automatizaciones' });
        }
        
        res.json(automations || []);
    });
});

app.put('/api/client/:clientId/automations/:automationId', (req, res) => {
    const { clientId, automationId } = req.params;
    const { active } = req.body;
    
    db.run(
        'UPDATE automations SET active = ? WHERE id = ? AND client_id = ?',
        [active ? 1 : 0, automationId, clientId],
        function(err) {
            if (err) {
                return res.status(500).json({ error: 'Error actualizando automatización' });
            }
            
            if (this.changes === 0) {
                return res.status(404).json({ error: 'Automatización no encontrada' });
            }
            
            res.json({ success: true, message: 'Automatización actualizada exitosamente' });
        }
    );
});

app.get('/api/client/:clientId/stats', (req, res) => {
    const { clientId } = req.params;
    
    // Obtener estadísticas del cliente
    db.get('SELECT COUNT(*) as total_leads FROM leads WHERE client_id = ?', [clientId], (err, leadsResult) => {
        if (err) {
            return res.status(500).json({ error: 'Error obteniendo estadísticas' });
        }
        
        db.get('SELECT COUNT(*) as converted_leads FROM leads WHERE client_id = ? AND status = "converted"', [clientId], (err, convertedResult) => {
            if (err) {
                return res.status(500).json({ error: 'Error obteniendo estadísticas' });
            }
            
            db.get('SELECT COUNT(*) as active_automations FROM automations WHERE client_id = ? AND active = 1', [clientId], (err, automationsResult) => {
                if (err) {
                    return res.status(500).json({ error: 'Error obteniendo estadísticas' });
                }
                
                res.json({
                    total_leads: leadsResult.total_leads,
                    converted_leads: convertedResult.converted_leads,
                    active_automations: automationsResult.active_automations,
                    conversion_rate: leadsResult.total_leads > 0 ? 
                        Math.round((convertedResult.converted_leads / leadsResult.total_leads) * 100) : 0
                });
            });
        });
    });
});

// Webhook para captura de leads desde webs de clientes
app.post('/api/webhooks/:clientId/new-lead', (req, res) => {
    const { clientId } = req.params;
    const { name, email, phone, company, message, source } = req.body;
    
    if (!name || !email) {
        return res.status(400).json({ error: 'Nombre y email son requeridos' });
    }
    
    // Verificar que el cliente existe
    db.get('SELECT id FROM clients WHERE id = ? AND status = "active"', [clientId], (err, client) => {
        if (err || !client) {
            return res.status(404).json({ error: 'Cliente no encontrado o inactivo' });
        }
        
        // Crear el lead
        db.run(
            'INSERT INTO leads (client_id, name, email, phone, company, notes, source, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)',
            [clientId, name, email, phone, company, message, source, 'new'],
            function(err) {
                if (err) {
                    return res.status(500).json({ error: 'Error creando lead' });
                }
                
                // Registrar actividad
                db.run(
                    'INSERT INTO activity_log (action, description, entity_type, entity_id) VALUES (?, ?, ?, ?)',
                    ['WEBHOOK', `Lead capturado desde ${source}: ${name}`, 'lead', this.lastID]
                );
                
                // Aquí podrías activar automatizaciones n8n
                // triggerN8nAutomation(clientId, 'new_lead', { lead_id: this.lastID, ...req.body });
                
                res.json({ 
                    success: true, 
                    id: this.lastID,
                    message: 'Lead capturado exitosamente' 
                });
            }
        );
    });
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
    console.log(`📊 Dashboard CRM disponible en /dashboard`);
    console.log(`📧 Contacto: alberto@desarroyo.tech`);
}); 