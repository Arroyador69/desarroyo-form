/**
 * 🔄 Script de Migración - Contador de Instalaciones
 * Añade la columna install_count a la tabla de shortcuts existente
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Conectar a la base de datos
const dbPath = path.join(__dirname, '..', 'dashboard.db');
const db = new sqlite3.Database(dbPath);

console.log('🔄 Iniciando migración de contador de instalaciones...');

async function migrateInstallCount() {
    return new Promise((resolve, reject) => {
        // Verificar si la columna install_count ya existe
        db.get("PRAGMA table_info(shortcuts)", [], (err, rows) => {
            if (err) {
                console.error('❌ Error verificando estructura de tabla:', err);
                reject(err);
                return;
            }

            // Verificar si la columna install_count existe
            db.all("PRAGMA table_info(shortcuts)", [], (err, columns) => {
                if (err) {
                    console.error('❌ Error obteniendo columnas:', err);
                    reject(err);
                    return;
                }

                const hasInstallCount = columns.some(col => col.name === 'install_count');
                
                if (hasInstallCount) {
                    console.log('✅ La columna install_count ya existe');
                    resolve();
                    return;
                }

                // Añadir la columna install_count
                console.log('📝 Añadiendo columna install_count...');
                db.run('ALTER TABLE shortcuts ADD COLUMN install_count INTEGER DEFAULT 0', (err) => {
                    if (err) {
                        console.error('❌ Error añadiendo columna:', err);
                        reject(err);
                        return;
                    }

                    console.log('✅ Columna install_count añadida exitosamente');
                    
                    // Actualizar todos los shortcuts existentes para tener install_count = 0
                    db.run('UPDATE shortcuts SET install_count = 0 WHERE install_count IS NULL', (err) => {
                        if (err) {
                            console.error('❌ Error actualizando shortcuts existentes:', err);
                            reject(err);
                            return;
                        }

                        console.log('✅ Shortcuts existentes actualizados con install_count = 0');
                        resolve();
                    });
                });
            });
        });
    });
}

// Ejecutar migración
migrateInstallCount()
    .then(() => {
        console.log('🎉 Migración completada exitosamente');
        db.close();
    })
    .catch((error) => {
        console.error('💥 Error en migración:', error);
        db.close();
        process.exit(1);
    }); 