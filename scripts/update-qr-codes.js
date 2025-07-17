/**
 * 🔄 Script para actualizar QR codes existentes
 * Actualiza todos los QR codes para que apunten a los enlaces de instalación correctos
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Conectar a la base de datos
const dbPath = path.join(__dirname, '..', 'dashboard.db');
const db = new sqlite3.Database(dbPath);

console.log('🔄 Actualizando QR codes para enlaces de instalación...\n');

async function updateQrCodes() {
    return new Promise((resolve, reject) => {
        // Obtener todos los shortcuts
        db.all('SELECT id, name FROM shortcuts', [], (err, shortcuts) => {
            if (err) {
                console.error('❌ Error obteniendo shortcuts:', err);
                reject(err);
                return;
            }

            console.log(`📱 Encontrados ${shortcuts.length} shortcuts para actualizar\n`);

            let updatedCount = 0;
            let errorCount = 0;

            // Actualizar cada shortcut
            const updateNext = (index) => {
                if (index >= shortcuts.length) {
                    console.log(`\n📊 Resumen:`);
                    console.log(`   ✅ Actualizados: ${updatedCount}`);
                    console.log(`   ❌ Errores: ${errorCount}`);
                    resolve();
                    return;
                }

                const shortcut = shortcuts[index];
                const installUrl = `https://desarroyo.tech/shortcuts/install/${shortcut.id}`;
                const newQrCode = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(installUrl)}`;

                console.log(`${index + 1}. Actualizando: ${shortcut.name} (ID: ${shortcut.id})`);
                console.log(`   📱 Nuevo QR: ${newQrCode}`);

                db.run('UPDATE shortcuts SET qr_code = ? WHERE id = ?', 
                       [newQrCode, shortcut.id], function(err) {
                    if (err) {
                        console.error(`   ❌ Error actualizando ${shortcut.name}:`, err);
                        errorCount++;
                    } else {
                        console.log(`   ✅ ${shortcut.name} actualizado`);
                        updatedCount++;
                    }
                    
                    updateNext(index + 1);
                });
            };

            updateNext(0);
        });
    });
}

// Ejecutar actualización
updateQrCodes()
    .then(() => {
        console.log('\n🎉 Actualización de QR codes completada');
        db.close();
    })
    .catch((error) => {
        console.error('💥 Error en actualización:', error);
        db.close();
        process.exit(1);
    }); 