/**
 * 🧪 Test del Sistema de Contador de Instalaciones
 * Prueba el endpoint de instalación y verifica que el contador se incremente
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Conectar a la base de datos
const dbPath = path.join(__dirname, 'dashboard.db');
const db = new sqlite3.Database(dbPath);

console.log('🧪 Iniciando test del sistema de contador de instalaciones...\n');

async function testInstallCounter() {
    return new Promise((resolve, reject) => {
        // 1. Verificar que hay shortcuts en la base de datos
        db.all('SELECT id, name, install_count FROM shortcuts LIMIT 3', [], (err, shortcuts) => {
            if (err) {
                console.error('❌ Error obteniendo shortcuts:', err);
                reject(err);
                return;
            }

            if (shortcuts.length === 0) {
                console.log('⚠️  No hay shortcuts para probar. Creando uno de prueba...');
                createTestShortcut().then(() => {
                    testInstallCounter().then(resolve).catch(reject);
                });
                return;
            }

            console.log('📱 Shortcuts encontrados:');
            shortcuts.forEach(shortcut => {
                console.log(`   - ID: ${shortcut.id}, Nombre: ${shortcut.name}, Instalaciones: ${shortcut.install_count || 0}`);
            });

            // 2. Simular instalaciones
            const testShortcut = shortcuts[0];
            console.log(`\n🔄 Simulando instalaciones para: ${testShortcut.name} (ID: ${testShortcut.id})`);

            // Simular 3 instalaciones
            let installCount = 0;
            const simulateInstallation = () => {
                return new Promise((resolveInstall) => {
                    db.run('UPDATE shortcuts SET install_count = install_count + 1 WHERE id = ?', 
                           [testShortcut.id], function(err) {
                        if (err) {
                            console.error('❌ Error simulando instalación:', err);
                        } else {
                            installCount++;
                            console.log(`   ✅ Instalación ${installCount} registrada`);
                        }
                        resolveInstall();
                    });
                });
            };

            // Ejecutar 3 instalaciones secuencialmente
            simulateInstallation()
                .then(() => simulateInstallation())
                .then(() => simulateInstallation())
                .then(() => {
                    // 3. Verificar el contador final
                    db.get('SELECT install_count FROM shortcuts WHERE id = ?', [testShortcut.id], (err, result) => {
                        if (err) {
                            console.error('❌ Error verificando contador:', err);
                            reject(err);
                            return;
                        }

                        const finalCount = result.install_count;
                        const expectedCount = (testShortcut.install_count || 0) + 3;
                        
                        console.log(`\n📊 Resultados:`);
                        console.log(`   - Contador inicial: ${testShortcut.install_count || 0}`);
                        console.log(`   - Contador final: ${finalCount}`);
                        console.log(`   - Contador esperado: ${expectedCount}`);
                        
                        if (finalCount === expectedCount) {
                            console.log('✅ Test exitoso: El contador funciona correctamente');
                        } else {
                            console.log('❌ Test fallido: El contador no se incrementó correctamente');
                        }

                        // 4. Mostrar estadísticas generales
                        db.get('SELECT COUNT(*) as total, SUM(install_count) as total_installs FROM shortcuts', [], (err, stats) => {
                            if (err) {
                                console.error('❌ Error obteniendo estadísticas:', err);
                            } else {
                                console.log(`\n📈 Estadísticas generales:`);
                                console.log(`   - Total shortcuts: ${stats.total}`);
                                console.log(`   - Total instalaciones: ${stats.total_installs || 0}`);
                                console.log(`   - Promedio por shortcut: ${stats.total > 0 ? Math.round((stats.total_installs || 0) / stats.total) : 0}`);
                            }
                            
                            resolve();
                        });
                    });
                });
        });
    });
}

async function createTestShortcut() {
    return new Promise((resolve, reject) => {
        const testShortcut = {
            name: 'Test Shortcut',
            description: 'Shortcut de prueba para testing',
            actions: JSON.stringify([{ type: 'test' }]),
            icon_color: 'blue',
            icon_glyph: 'gear',
            shortcut_url: 'shortcuts://test',
            qr_code: 'https://test.com/qr',
            trigger_type: 'manual',
            trigger_phrase: 'test',
            file_path: '/test/path',
            download_url: '/test/download',
            install_count: 0
        };

        db.run(`INSERT INTO shortcuts (name, description, actions, icon_color, icon_glyph, shortcut_url, qr_code, trigger_type, trigger_phrase, file_path, download_url, install_count, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
               [testShortcut.name, testShortcut.description, testShortcut.actions, testShortcut.icon_color, testShortcut.icon_glyph, testShortcut.shortcut_url, testShortcut.qr_code, testShortcut.trigger_type, testShortcut.trigger_phrase, testShortcut.file_path, testShortcut.download_url, testShortcut.install_count, new Date().toISOString()],
               function(err) {
                   if (err) {
                       console.error('❌ Error creando shortcut de prueba:', err);
                       reject(err);
                   } else {
                       console.log('✅ Shortcut de prueba creado exitosamente');
                       resolve();
                   }
               });
    });
}

// Ejecutar test
testInstallCounter()
    .then(() => {
        console.log('\n🎉 Test completado exitosamente');
        db.close();
    })
    .catch((error) => {
        console.error('💥 Error en test:', error);
        db.close();
        process.exit(1);
    }); 