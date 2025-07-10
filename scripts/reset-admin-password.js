#!/usr/bin/env node
/**
 * 🔐 Script para resetear contraseña del administrador
 * Actualiza la contraseña en la base de datos SQLite
 */

const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');

// Nueva contraseña segura
const NUEVA_CONTRASEÑA = 'DesArroyo2024!Seguro';

async function resetearContraseña() {
    console.log('🔐 === RESETEANDO CONTRASEÑA ADMIN ===');
    console.log('📊 Contraseña nueva: DesArroyo2024!Seguro');
    
    // Conectar a la base de datos
    const db = new sqlite3.Database('./dashboard.db', (err) => {
        if (err) {
            console.error('❌ Error conectando a la base de datos:', err);
            process.exit(1);
        }
        console.log('✅ Conectado a la base de datos');
    });

    try {
        // Hashear la nueva contraseña
        console.log('🔨 Hasheando nueva contraseña...');
        const hashedPassword = await bcrypt.hash(NUEVA_CONTRASEÑA, 10);
        console.log('✅ Contraseña hasheada correctamente');

        // Actualizar en la base de datos
        db.run(
            'UPDATE users SET password = ? WHERE username = ?',
            [hashedPassword, 'admin'],
            function(err) {
                if (err) {
                    console.error('❌ Error actualizando contraseña:', err);
                    process.exit(1);
                }
                
                if (this.changes === 0) {
                    console.log('⚠️ Usuario admin no encontrado, creándolo...');
                    
                    // Crear usuario admin si no existe
                    db.run(
                        'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
                        ['admin', 'alberto@desarroyo.tech', hashedPassword, 'admin'],
                        function(err) {
                            if (err) {
                                console.error('❌ Error creando usuario admin:', err);
                                process.exit(1);
                            }
                            
                            console.log('✅ Usuario admin creado con nueva contraseña');
                            finalizarScript();
                        }
                    );
                } else {
                    console.log('✅ Contraseña actualizada correctamente');
                    finalizarScript();
                }
            }
        );

    } catch (error) {
        console.error('❌ Error hasheando contraseña:', error);
        process.exit(1);
    }

    function finalizarScript() {
        db.close((err) => {
            if (err) {
                console.error('❌ Error cerrando base de datos:', err);
            } else {
                console.log('✅ Base de datos cerrada');
            }
        });

        console.log('');
        console.log('🎯 === RESET COMPLETADO ===');
        console.log('👤 Usuario: admin');
        console.log('🔑 Contraseña: DesArroyo2024!Seguro');
        console.log('📍 Puedes acceder en:');
        console.log('   🏠 Local: http://localhost:3000/login.html');
        console.log('   🌐 Online: https://desarroyo.tech/login.html');
        console.log('');
        console.log('⚠️ IMPORTANTE: También actualiza ADMIN_PASSWORD en Vercel');
        process.exit(0);
    }
}

// Ejecutar script
resetearContraseña(); 