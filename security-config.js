const crypto = require('crypto');
const bcrypt = require('bcrypt');

/**
 * Configuración de Seguridad para DesArroyo.Tech CRM
 * Implementa múltiples capas de seguridad para datos sensibles
 */

class SecurityConfig {
    constructor() {
        this.algorithm = 'aes-256-cbc';
        this.secretKey = process.env.ENCRYPTION_KEY || crypto.randomBytes(32);
        this.iv = crypto.randomBytes(16);
    }

    // Encriptación AES-256 para datos sensibles
    encrypt(text) {
        const cipher = crypto.createCipher(this.algorithm, this.secretKey);
        let encrypted = cipher.update(text, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return encrypted;
    }

    // Desencriptación AES-256
    decrypt(encryptedText) {
        const decipher = crypto.createDecipher(this.algorithm, this.secretKey);
        let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    }

    // Hashing seguro para contraseñas
    async hashPassword(password) {
        const saltRounds = 12;
        return await bcrypt.hash(password, saltRounds);
    }

    // Verificación de contraseñas
    async verifyPassword(password, hash) {
        return await bcrypt.compare(password, hash);
    }

    // Generación de tokens seguros
    generateSecureToken() {
        return crypto.randomBytes(32).toString('hex');
    }

    // Validación de datos sensibles
    validateSensitiveData(data) {
        const patterns = {
            email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            phone: /^\+?[\d\s\-\(\)]{9,15}$/,
            dni: /^[0-9]{8}[A-Z]$/,
            nie: /^[A-Z][0-9]{7}[A-Z]$/,
            reference: /^[A-Z0-9]{20}$/
        };

        const validations = {};
        
        if (data.email) {
            validations.email = patterns.email.test(data.email);
        }
        
        if (data.phone) {
            validations.phone = patterns.phone.test(data.phone);
        }
        
        if (data.dni) {
            validations.dni = patterns.dni.test(data.dni.toUpperCase());
        }
        
        if (data.nie) {
            validations.nie = patterns.nie.test(data.nie.toUpperCase());
        }
        
        if (data.reference) {
            validations.reference = patterns.reference.test(data.reference);
        }

        return validations;
    }

    // Sanitización de inputs
    sanitizeInput(input) {
        if (typeof input !== 'string') return input;
        
        return input
            .replace(/[<>]/g, '') // Prevenir XSS básico
            .replace(/javascript:/gi, '') // Prevenir JS injection
            .trim();
    }

    // Log de auditoría
    logAuditEvent(userId, action, details) {
        const auditLog = {
            timestamp: new Date().toISOString(),
            userId,
            action,
            details,
            ip: details.ip || 'unknown',
            userAgent: details.userAgent || 'unknown'
        };

        // Aquí se guardaría en la base de datos
        console.log('🔒 AUDIT LOG:', auditLog);
        return auditLog;
    }
}

// 🔐 Configuración de Seguridad para DesArroyo.tech CRM
// Este archivo contiene configuraciones de seguridad para el sistema

const securityConfig = {
    // Configuración de autenticación
    auth: {
        // Contraseña del admin (cambiar en producción)
        adminPassword: process.env.ADMIN_PASSWORD || 'admin123',
        
        // Secret para JWT tokens
        jwtSecret: process.env.JWT_SECRET || 'desarroyo-secret-key-2024',
        
        // Tiempo de expiración del token (24 horas)
        tokenExpiration: '24h',
        
        // Intentos máximos de login
        maxLoginAttempts: 5,
        
        // Tiempo de bloqueo tras intentos fallidos (30 minutos)
        lockoutTime: 30 * 60 * 1000
    },

    // IPs con acceso premium (tu IP y otras autorizadas)
    authorizedIPs: [
        '5.224.13.147', // Tu IP actual
        '127.0.0.1',    // Localhost para desarrollo
        '::1'           // Localhost IPv6
    ],

    // Configuración de CORS
    cors: {
        origin: [
            'https://desarroyo.tech',
            'https://www.desarroyo.tech',
            'http://localhost:3000' // Para desarrollo
        ],
        credentials: true
    },

    // Configuración de rate limiting
    rateLimit: {
        windowMs: 15 * 60 * 1000, // 15 minutos
        max: 100 // máximo 100 requests por ventana
    },

    // Configuración de sesiones
    session: {
        secret: process.env.SESSION_SECRET || 'desarroyo-session-secret',
        resave: false,
        saveUninitialized: false,
        cookie: {
            secure: process.env.NODE_ENV === 'production',
            httpOnly: true,
            maxAge: 24 * 60 * 60 * 1000 // 24 horas
        }
    },

    // Configuración de logs
    logging: {
        enabled: true,
        level: 'info',
        file: './logs/security.log'
    },

    // Configuración de backup
    backup: {
        enabled: true,
        frequency: 'daily', // daily, weekly, monthly
        retention: 30, // días
        path: './backups/'
    }
};

// Función para verificar IP autorizada
function isAuthorizedIP(ip) {
    return securityConfig.authorizedIPs.includes(ip);
}

// Función para generar contraseña segura
function generateSecurePassword(length = 12) {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < length; i++) {
        password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    return password;
}

// Función para validar contraseña
function validatePassword(password) {
    const minLength = 8;
    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumbers = /\d/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChar;
}

// Función para registrar intentos de acceso
function logAccessAttempt(ip, success, username = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
        timestamp,
        ip,
        success,
        username,
        userAgent: 'CRM Access'
    };
    
    console.log(`🔐 Access Log: ${JSON.stringify(logEntry)}`);
    
    // Aquí podrías guardar en base de datos o archivo
    if (securityConfig.logging.enabled) {
        // Implementar logging a archivo
    }
}

module.exports = {
    securityConfig,
    isAuthorizedIP,
    generateSecurePassword,
    validatePassword,
    logAccessAttempt
}; 