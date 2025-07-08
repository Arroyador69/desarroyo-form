#!/usr/bin/env node

/**
 * 🔐 Reset Admin Password - DesArroyo.tech CRM
 * Script para resetear/crear usuario administrador
 */

const bcrypt = require('bcrypt');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');
const { config } = require('../config');

// Configuración desde archivo centralizado
const DEFAULT_USERNAME = config.admin.username;
const DEFAULT_PASSWORD = config.admin.password;
const DEFAULT_EMAIL = config.admin.email;
const DB_PATH = config.database.path;

class AdminPasswordManager {
    constructor() {
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(DB_PATH, (err) => {
                if (err) {
                    console.error('❌ Error conectando a la base de datos:', err.message);
                    reject(err);
                } else {
                    console.log('✅ Conectado a la base de datos SQLite');
                    resolve();
                }
            });
        });
    }

    async ensureUsersTable() {
        return new Promise((resolve, reject) => {
            const sql = `CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'admin',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )`;

            this.db.run(sql, (err) => {
                if (err) {
                    console.error('❌ Error creando tabla users:', err.message);
                    reject(err);
                } else {
                    console.log('✅ Tabla users verificada/creada');
                    resolve();
                }
            });
        });
    }

    async checkAdminExists() {
        return new Promise((resolve, reject) => {
            this.db.get('SELECT * FROM users WHERE username = ? OR role = ?', 
                [DEFAULT_USERNAME, 'admin'], (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    async deleteExistingAdmin() {
        return new Promise((resolve, reject) => {
            this.db.run('DELETE FROM users WHERE username = ? OR role = ?', 
                [DEFAULT_USERNAME, 'admin'], (err) => {
                if (err) {
                    reject(err);
                } else {
                    console.log('🗑️  Usuario admin anterior eliminado');
                    resolve();
                }
            });
        });
    }

    async createAdmin(username, password, email) {
        return new Promise(async (resolve, reject) => {
            try {
                // Hash de la contraseña
                const hashedPassword = await bcrypt.hash(password, 10);
                
                // Insertar usuario
                this.db.run(
                    'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                    [username, email, hashedPassword, 'admin'],
                    function(err) {
                        if (err) {
                            console.error('❌ Error creando usuario admin:', err.message);
                            reject(err);
                        } else {
                            console.log('✅ Usuario admin creado exitosamente');
                            console.log(`   👤 Usuario: ${username}`);
                            console.log(`   📧 Email: ${email}`);
                            console.log(`   🔑 Contraseña: ${password}`);
                            console.log(`   🆔 ID: ${this.lastID}`);
                            resolve(this.lastID);
                        }
                    }
                );
            } catch (err) {
                reject(err);
            }
        });
    }

    async verifyPassword(username, password) {
        return new Promise((resolve, reject) => {
            this.db.get('SELECT * FROM users WHERE username = ?', [username], async (err, user) => {
                if (err) {
                    reject(err);
                } else if (!user) {
                    resolve(false);
                } else {
                    try {
                        const isValid = await bcrypt.compare(password, user.password);
                        resolve(isValid);
                    } catch (err) {
                        reject(err);
                    }
                }
            });
        });
    }

    async listUsers() {
        return new Promise((resolve, reject) => {
            this.db.all('SELECT id, username, email, role, created_at FROM users', (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    close() {
        if (this.db) {
            this.db.close((err) => {
                if (err) {
                    console.error('❌ Error cerrando base de datos:', err.message);
                } else {
                    console.log('✅ Base de datos cerrada');
                }
            });
        }
    }
}

async function main() {
    const manager = new AdminPasswordManager();
    
    try {
        console.log('🚀 Iniciando reset de contraseña admin...\n');
        
        // Verificar si existe la base de datos
        if (!fs.existsSync(DB_PATH)) {
            console.log('⚠️  Base de datos no encontrada, se creará una nueva');
        }
        
        await manager.init();
        await manager.ensureUsersTable();
        
        // Verificar si existe admin
        const existingAdmin = await manager.checkAdminExists();
        if (existingAdmin) {
            console.log('🔍 Admin existente encontrado:');
            console.log(`   👤 Usuario: ${existingAdmin.username}`);
            console.log(`   📧 Email: ${existingAdmin.email}`);
            console.log(`   📅 Creado: ${existingAdmin.created_at}`);
            
            // Eliminar admin existente
            await manager.deleteExistingAdmin();
        }
        
        // Crear nuevo admin
        console.log('\n🔧 Creando nuevo usuario admin...');
        await manager.createAdmin(DEFAULT_USERNAME, DEFAULT_PASSWORD, DEFAULT_EMAIL);
        
        // Verificar que funciona
        console.log('\n🧪 Verificando credenciales...');
        const isValid = await manager.verifyPassword(DEFAULT_USERNAME, DEFAULT_PASSWORD);
        if (isValid) {
            console.log('✅ Credenciales verificadas correctamente');
        } else {
            console.log('❌ Error: Las credenciales no funcionan');
        }
        
        // Listar usuarios
        console.log('\n📋 Usuarios en la base de datos:');
        const users = await manager.listUsers();
        users.forEach((user, index) => {
            console.log(`   ${index + 1}. ${user.username} (${user.email}) - ${user.role}`);
        });
        
        console.log('\n🎉 ¡Proceso completado!');
        console.log('');
        console.log('🔐 CREDENCIALES DE ACCESO:');
        console.log('   URL: http://localhost:3000/login.html');
        console.log(`   Usuario: ${DEFAULT_USERNAME}`);
        console.log(`   Contraseña: ${DEFAULT_PASSWORD}`);
        console.log('');
        console.log('📝 Para cambiar la contraseña, edita las variables DEFAULT_PASSWORD en este script');
        
    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    } finally {
        manager.close();
    }
}

// Ejecutar si es llamado directamente
if (require.main === module) {
    main();
}

module.exports = AdminPasswordManager; 