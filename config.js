/**
 * 🔧 Configuración Principal - DesArroyo.tech CRM
 * Archivo de configuración para el sistema de gestión
 */

const config = {
    // 🔐 Credenciales de Administrador
    admin: {
        username: 'admin',
        password: 'DesArroyo2024!',
        email: 'alberto@desarroyo.tech'
    },

    // 🌐 Servidor
    server: {
        port: process.env.PORT || 3000,
        host: process.env.HOST || 'localhost',
        environment: process.env.NODE_ENV || 'development'
    },

    // 🔑 Seguridad
    security: {
        jwtSecret: process.env.JWT_SECRET || 'desarroyo-secret-key-2024',
        sessionSecret: process.env.SESSION_SECRET || 'desarroyo-session-secret',
        tokenExpiration: process.env.TOKEN_EXPIRATION || '24h',
        maxLoginAttempts: parseInt(process.env.MAX_LOGIN_ATTEMPTS) || 5,
        lockoutTime: parseInt(process.env.LOCKOUT_TIME) || 1800000, // 30 minutos
        saltRounds: 10
    },

    // 🗄️ Base de Datos
    database: {
        path: process.env.DATABASE_PATH || './dashboard.db',
        backupEnabled: process.env.BACKUP_ENABLED === 'true',
        backupPath: process.env.BACKUP_PATH || './backups/',
        backupFrequency: process.env.BACKUP_FREQUENCY || 'daily'
    },

    // 🤖 APIs Externas
    apis: {
        deepseek: {
            apiKey: process.env.DEEPSEEK_API_KEY || '',
            baseURL: 'https://api.deepseek.com/v1/chat/completions'
        },
        stripe: {
            secretKey: process.env.STRIPE_SECRET_KEY || '',
            publicKey: process.env.STRIPE_PUBLIC_KEY || '',
            webhookSecret: process.env.STRIPE_WEBHOOK_SECRET || ''
        },
        telegram: {
            botToken: process.env.TELEGRAM_BOT_TOKEN || '',
            chatId: process.env.TELEGRAM_CHAT_ID || ''
        }
    },

    // 📧 Email
    email: {
        service: 'zoho',
        user: process.env.ZOHO_EMAIL || '',
        password: process.env.ZOHO_PASSWORD || ''
    },

    // 🔒 CORS
    cors: {
        allowedOrigins: process.env.ALLOWED_ORIGINS 
            ? process.env.ALLOWED_ORIGINS.split(',') 
            : ['http://localhost:3000', 'https://desarroyo.tech', 'https://www.desarroyo.tech'],
        credentials: true
    },

    // 📊 Límites y Cuotas
    limits: {
        freeQueries: 10,
        premiumIPs: [
            '5.224.13.147',  // IP de desarrollo
            '127.0.0.1',     // Localhost
            '::1'            // Localhost IPv6
        ],
        fileUpload: {
            maxSize: 100 * 1024 * 1024, // 100MB
            allowedTypes: ['video/mp4', 'video/mov', 'video/avi', 'video/quicktime']
        }
    },

    // 🎬 Video Processing
    video: {
        clipPath: './videos/clips/',
        outputPath: './videos/output/',
        thumbnailPath: './videos/thumbnails/',
        tempPath: './videos/temp/',
        maxDuration: 59, // segundos
        defaultResolution: '1080x1920'
    },

    // 📝 Logs
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        file: process.env.LOG_FILE || './logs/app.log',
        maxSize: '10m',
        maxFiles: 5
    },

    // 🌍 Localización
    locale: {
        default: 'es',
        timezone: 'Europe/Madrid',
        currency: 'EUR'
    },

    // 🔄 Automatizaciones
    automation: {
        n8nWebhookBase: process.env.N8N_WEBHOOK_BASE || '',
        retryAttempts: 3,
        retryDelay: 1000
    }
};

// 🛡️ Validación de configuración crítica
function validateConfig() {
    const errors = [];

    // Validar credenciales admin
    if (!config.admin.username || !config.admin.password) {
        errors.push('❌ Credenciales de administrador incompletas');
    }

    // Validar JWT Secret
    if (!config.security.jwtSecret || config.security.jwtSecret === 'desarroyo-secret-key-2024') {
        console.warn('⚠️  Usando JWT Secret por defecto. Cambia esto en producción.');
    }

    // Validar rutas de archivos
    const requiredDirs = [
        config.video.clipPath,
        config.video.outputPath,
        config.video.thumbnailPath,
        config.video.tempPath
    ];

    requiredDirs.forEach(dir => {
        const fs = require('fs');
        if (!fs.existsSync(dir)) {
            try {
                fs.mkdirSync(dir, { recursive: true });
                console.log(`✅ Directorio creado: ${dir}`);
            } catch (err) {
                errors.push(`❌ No se pudo crear directorio: ${dir}`);
            }
        }
    });

    if (errors.length > 0) {
        console.error('🚨 Errores de configuración:');
        errors.forEach(error => console.error(error));
        process.exit(1);
    }

    console.log('✅ Configuración validada correctamente');
    return true;
}

// 🔧 Función para obtener configuración con validación
function getConfig() {
    validateConfig();
    return config;
}

// 📝 Función para mostrar configuración actual
function showConfig() {
    console.log('🔧 Configuración actual:');
    console.log('');
    
    console.log('🔐 Admin:');
    console.log(`   Usuario: ${config.admin.username}`);
    console.log(`   Email: ${config.admin.email}`);
    console.log(`   Contraseña: ${'*'.repeat(config.admin.password.length)}`);
    console.log('');
    
    console.log('🌐 Servidor:');
    console.log(`   Puerto: ${config.server.port}`);
    console.log(`   Host: ${config.server.host}`);
    console.log(`   Entorno: ${config.server.environment}`);
    console.log('');
    
    console.log('🗄️  Base de Datos:');
    console.log(`   Ruta: ${config.database.path}`);
    console.log(`   Backup: ${config.database.backupEnabled ? 'Activado' : 'Desactivado'}`);
    console.log('');
    
    console.log('🤖 APIs configuradas:');
    console.log(`   DeepSeek: ${config.apis.deepseek.apiKey ? 'Configurada' : 'No configurada'}`);
    console.log(`   Stripe Secret: ${config.apis.stripe.secretKey ? 'Configurada' : 'No configurada'}`);
    console.log(`   Stripe Public: ${config.apis.stripe.publicKey ? 'Configurada' : 'No configurada'}`);
    console.log(`   Telegram: ${config.apis.telegram.botToken ? 'Configurada' : 'No configurada'}`);
}

// 🔐 Función para cambiar contraseña de admin
function changeAdminPassword(newPassword) {
    if (!newPassword || newPassword.length < 6) {
        console.error('❌ La contraseña debe tener al menos 6 caracteres');
        return false;
    }
    
    config.admin.password = newPassword;
    console.log('✅ Contraseña de admin actualizada');
    console.log('⚠️  Recuerda ejecutar el script de reset para aplicar los cambios');
    return true;
}

module.exports = {
    config,
    getConfig,
    validateConfig,
    showConfig,
    changeAdminPassword
};

// Si es ejecutado directamente, mostrar configuración
if (require.main === module) {
    showConfig();
} 