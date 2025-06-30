#!/usr/bin/env node

const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const { generateSecurePassword, validatePassword } = require('../security-config');

class PasswordManager {
    constructor() {
        this.db = new sqlite3.Database('./dashboard.db');
    }

    async changeAdminPassword(newPassword) {
        try {
            console.log('🔐 Cambiando contraseña del administrador...');
            
            // Validar nueva contraseña
            if (!validatePassword(newPassword)) {
                console.error('❌ Error: La contraseña no cumple los requisitos de seguridad');
                console.log('📋 Requisitos:');
                console.log('   - Mínimo 8 caracteres');
                console.log('   - Al menos una mayúscula');
                console.log('   - Al menos una minúscula');
                console.log('   - Al menos un número');
                console.log('   - Al menos un carácter especial');
                process.exit(1);
            }

            // Encriptar nueva contraseña
            const saltRounds = 12;
            const hashedPassword = await bcrypt.hash(newPassword, saltRounds);
            
            // Actualizar en base de datos
            await this.updatePasswordInDB(hashedPassword);
            
            // Actualizar variable de entorno
            await this.updateEnvironmentVariable(newPassword);
            
            console.log('✅ Contraseña cambiada exitosamente');
            console.log('🔑 Nueva contraseña:', newPassword);
            console.log('⚠️  Guarda esta contraseña en un lugar seguro');
            
        } catch (error) {
            console.error('❌ Error cambiando contraseña:', error);
            process.exit(1);
        } finally {
            this.db.close();
        }
    }

    updatePasswordInDB(hashedPassword) {
        return new Promise((resolve, reject) => {
            this.db.run(
                'UPDATE users SET password = ? WHERE username = ?',
                [hashedPassword, 'admin'],
                function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        if (this.changes === 0) {
                            console.log('⚠️  Usuario admin no encontrado, creando...');
                            this.db.run(
                                'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                                ['admin', 'alberto@desarroyo.tech', hashedPassword, 'admin'],
                                function(err) {
                                    if (err) reject(err);
                                    else resolve();
                                }
                            );
                        } else {
                            resolve();
                        }
                    }
                }
            );
        });
    }

    async updateEnvironmentVariable(newPassword) {
        const fs = require('fs');
        const path = require('path');
        
        const envPath = path.join(__dirname, '../.env');
        let envContent = '';
        
        // Leer archivo .env si existe
        if (fs.existsSync(envPath)) {
            envContent = fs.readFileSync(envPath, 'utf8');
        }
        
        // Actualizar o añadir ADMIN_PASSWORD
        const passwordLine = `ADMIN_PASSWORD=${newPassword}`;
        
        if (envContent.includes('ADMIN_PASSWORD=')) {
            envContent = envContent.replace(/ADMIN_PASSWORD=.*/g, passwordLine);
        } else {
            envContent += `\n${passwordLine}\n`;
        }
        
        // Guardar archivo .env
        fs.writeFileSync(envPath, envContent);
        console.log('📝 Variable de entorno ADMIN_PASSWORD actualizada');
    }

    async generateSecurePassword() {
        const newPassword = generateSecurePassword(16);
        console.log('🔐 Generando contraseña segura...');
        console.log('🔑 Nueva contraseña generada:', newPassword);
        
        await this.changeAdminPassword(newPassword);
    }
}

// Ejecutar si se llama directamente
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('🔐 Gestor de Contraseñas - DesArroyo.tech CRM');
        console.log('============================================');
        console.log('');
        console.log('Uso:');
        console.log('  node scripts/change-admin-password.js <nueva_contraseña>');
        console.log('  node scripts/change-admin-password.js --generate');
        console.log('');
        console.log('Ejemplos:');
        console.log('  node scripts/change-admin-password.js "MiContraseña123!"');
        console.log('  node scripts/change-admin-password.js --generate');
        console.log('');
        console.log('⚠️  IMPORTANTE:');
        console.log('   - La contraseña debe tener al menos 8 caracteres');
        console.log('   - Incluir mayúsculas, minúsculas, números y símbolos');
        console.log('   - Guarda la contraseña en un lugar seguro');
        process.exit(1);
    }

    const passwordManager = new PasswordManager();
    
    if (args[0] === '--generate') {
        passwordManager.generateSecurePassword();
    } else {
        passwordManager.changeAdminPassword(args[0]);
    }
}

module.exports = PasswordManager; 