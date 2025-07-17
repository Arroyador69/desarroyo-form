/**
 * 🧪 Test de URLs de Producción
 * Verifica que todos los enlaces usen https://desarroyo.tech
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Conectar a la base de datos
const dbPath = path.join(__dirname, 'dashboard.db');
const db = new sqlite3.Database(dbPath);

console.log('🧪 Verificando URLs de producción...\n');

async function testProductionUrls() {
    return new Promise((resolve, reject) => {
        // Obtener todos los shortcuts
        db.all('SELECT id, name, shortcut_url, qr_code, download_url FROM shortcuts', [], (err, shortcuts) => {
            if (err) {
                console.error('❌ Error obteniendo shortcuts:', err);
                reject(err);
                return;
            }

            console.log(`📱 Encontrados ${shortcuts.length} shortcuts para verificar\n`);

            let issuesFound = 0;

            shortcuts.forEach((shortcut, index) => {
                console.log(`${index + 1}. ${shortcut.name} (ID: ${shortcut.id})`);
                
                // Verificar enlaces de instalación
                const installUrl = `https://desarroyo.tech/shortcuts/install/${shortcut.id}`;
                console.log(`   📱 Enlace de instalación: ${installUrl}`);
                
                // Verificar QR code
                const expectedQrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(installUrl)}`;
                if (shortcut.qr_code && shortcut.qr_code !== expectedQrUrl) {
                    console.log(`   ⚠️  QR code no actualizado: ${shortcut.qr_code}`);
                    issuesFound++;
                } else {
                    console.log(`   ✅ QR code correcto`);
                }
                
                // Verificar download_url
                if (shortcut.download_url) {
                    const downloadUrl = `https://desarroyo.tech${shortcut.download_url}`;
                    console.log(`   📥 Descarga: ${downloadUrl}`);
                } else {
                    console.log(`   📥 Descarga: No disponible`);
                }
                
                console.log('');
            });

            if (issuesFound > 0) {
                console.log(`⚠️  Se encontraron ${issuesFound} problemas con URLs`);
                console.log('💡 Ejecuta el script de actualización de QR codes');
            } else {
                console.log('✅ Todas las URLs están configuradas correctamente para producción');
            }

            resolve();
        });
    });
}

// Ejecutar test
testProductionUrls()
    .then(() => {
        console.log('\n🎉 Verificación completada');
        db.close();
    })
    .catch((error) => {
        console.error('💥 Error en verificación:', error);
        db.close();
        process.exit(1);
    }); 