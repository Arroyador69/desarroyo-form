/**
 * 🔧 Script para arreglar la tabla de shortcuts
 * Añade las columnas faltantes: file_path, download_url, install_count
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Conectar a la base de datos
const dbPath = path.join(__dirname, '..', 'dashboard.db');
const db = new sqlite3.Database(dbPath);

console.log('🔧 Iniciando reparación de tabla shortcuts...');

async function fixShortcutsTable() {
    return new Promise((resolve, reject) => {
        // Verificar estructura actual de la tabla
        db.all("PRAGMA table_info(shortcuts)", [], (err, columns) => {
            if (err) {
                console.error('❌ Error verificando tabla:', err);
                reject(err);
                return;
            }

            console.log('📋 Columnas actuales:');
            columns.forEach(col => {
                console.log(`   - ${col.name} (${col.type})`);
            });

            const columnNames = columns.map(col => col.name);
            const missingColumns = [];

            // Verificar columnas faltantes
            if (!columnNames.includes('file_path')) {
                missingColumns.push('file_path TEXT');
            }
            if (!columnNames.includes('download_url')) {
                missingColumns.push('download_url TEXT');
            }
            if (!columnNames.includes('install_count')) {
                missingColumns.push('install_count INTEGER DEFAULT 0');
            }

            if (missingColumns.length === 0) {
                console.log('✅ Todas las columnas necesarias ya existen');
                resolve();
                return;
            }

            console.log(`📝 Añadiendo columnas faltantes: ${missingColumns.join(', ')}`);

            // Añadir columnas faltantes una por una
            let addedCount = 0;
            const addNextColumn = () => {
                if (addedCount >= missingColumns.length) {
                    console.log('✅ Todas las columnas añadidas exitosamente');
                    resolve();
                    return;
                }

                const columnDef = missingColumns[addedCount];
                const columnName = columnDef.split(' ')[0];
                
                console.log(`   Añadiendo: ${columnName}`);
                db.run(`ALTER TABLE shortcuts ADD COLUMN ${columnDef}`, (err) => {
                    if (err) {
                        console.error(`❌ Error añadiendo ${columnName}:`, err);
                        // Continuar con la siguiente columna
                    } else {
                        console.log(`   ✅ ${columnName} añadida`);
                    }
                    addedCount++;
                    addNextColumn();
                });
            };

            addNextColumn();
        });
    });
}

// Ejecutar reparación
fixShortcutsTable()
    .then(() => {
        console.log('🎉 Reparación completada exitosamente');
        db.close();
    })
    .catch((error) => {
        console.error('💥 Error en reparación:', error);
        db.close();
        process.exit(1);
    }); 