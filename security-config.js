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

module.exports = SecurityConfig; 