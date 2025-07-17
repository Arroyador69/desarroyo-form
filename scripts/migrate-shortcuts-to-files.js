const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

// Conectar a la base de datos
const db = new sqlite3.Database('./dashboard.db');

// Crear directorio para shortcuts si no existe
const shortcutsDir = path.join(__dirname, '..', 'shortcuts', 'files');
if (!fs.existsSync(shortcutsDir)) {
    fs.mkdirSync(shortcutsDir, { recursive: true });
}

async function migrateShortcuts() {
    console.log('🔄 Migrando shortcuts existentes a archivos físicos...');
    
    return new Promise((resolve, reject) => {
        db.all('SELECT * FROM shortcuts WHERE file_path IS NULL OR file_path = ""', [], async (err, shortcuts) => {
            if (err) {
                console.error('Error obteniendo shortcuts:', err);
                reject(err);
                return;
            }

        console.log(`📱 Encontrados ${shortcuts.length} shortcuts para migrar`);

        for (const shortcut of shortcuts) {
            try {
                // Parsear las acciones del shortcut
                const actions = JSON.parse(shortcut.actions);
                
                // Crear el contenido del shortcut
                const shortcutContent = {
                    WFWorkflow: {
                        WFWorkflowClientVersion: "1200",
                        WFWorkflowClientRelease: "1230",
                        WFWorkflowIcon: {
                            WFIconStartColor: shortcut.icon_color || "blue",
                            WFIconGlyphNumber: shortcut.icon_glyph || "bolt"
                        },
                        WFWorkflowImportQuestions: [],
                        WFWorkflowTypes: ["WatchKit", "NCWidget"],
                        WFWorkflowInputContentItemClasses: ["WFStringContentItem"],
                        WFWorkflowActions: actions,
                        WFWorkflowOutputContentItemClasses: ["WFStringContentItem"]
                    }
                };

                // Generar nombre de archivo único
                const timestamp = Date.now();
                const safeName = shortcut.name.replace(/[^a-zA-Z0-9]/g, '_');
                const fileName = `${safeName}_${timestamp}.shortcut`;
                const filePath = path.join(shortcutsDir, fileName);

                // Guardar archivo físico .shortcut
                fs.writeFileSync(filePath, JSON.stringify(shortcutContent, null, 2));

                // Crear URL para descargar el archivo físico
                const downloadUrl = `/api/dashboard/download-shortcut/${fileName}`;

                // Actualizar la base de datos
                db.run(
                    'UPDATE shortcuts SET file_path = ?, download_url = ? WHERE id = ?',
                    [filePath, downloadUrl, shortcut.id],
                    function(err) {
                        if (err) {
                            console.error(`Error actualizando shortcut ${shortcut.name}:`, err);
                        } else {
                            console.log(`✅ Migrado: ${shortcut.name} -> ${fileName}`);
                        }
                    }
                );

            } catch (error) {
                console.error(`Error procesando shortcut ${shortcut.name}:`, error);
            }
        }

        console.log('🎉 Migración completada');
        resolve();
    });
    });
}

// Ejecutar migración
migrateShortcuts()
    .then(() => {
        console.log('✅ Todos los shortcuts han sido migrados exitosamente');
        process.exit(0);
    })
    .catch((error) => {
        console.error('❌ Error en la migración:', error);
        process.exit(1);
    }); 