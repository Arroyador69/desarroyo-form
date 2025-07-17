#!/usr/bin/env node

/**
 * ⚡ Generador de Shortcuts para iPhone - DesArroyo.tech
 * Sistema para crear shortcuts automáticamente y generar enlaces directos
 */

const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const { config } = require('../config');

class ShortcutGenerator {
    constructor() {
        this.db = null;
        this.outputDir = './shortcuts/generated';
        
        // Asegurar que existe el directorio de salida
        if (!fs.existsSync(this.outputDir)) {
            fs.mkdirSync(this.outputDir, { recursive: true });
        }
    }

    async init() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(config.database.path, (err) => {
                if (err) {
                    console.error('❌ Error conectando a la base de datos:', err);
                    reject(err);
                } else {
                    console.log('✅ Conectado a la base de datos para shortcuts');
                    resolve();
                }
            });
        });
    }

    // 🎯 Generar shortcut para superpoder específico
    async generateSuperpowerShortcut(superpowerName, superpowerDescription, triggerType = 'voice', triggerPhrase = null) {
        try {
            console.log(`⚡ Generando shortcut para superpoder: ${superpowerName}`);

            // Definir acciones del shortcut basadas en el tipo de superpoder
            const actions = this.getActionsForSuperpower(superpowerName, superpowerDescription, triggerType);

            // Crear el contenido del shortcut
            const shortcutContent = {
                WFWorkflow: {
                    WFWorkflowClientVersion: "1200",
                    WFWorkflowClientRelease: "1230",
                    WFWorkflowIcon: {
                        WFIconStartColor: "blue",
                        WFIconGlyphNumber: "bolt"
                    },
                    WFWorkflowImportQuestions: [],
                    WFWorkflowTypes: ["WatchKit", "NCWidget"],
                    WFWorkflowInputContentItemClasses: ["WFStringContentItem"],
                    WFWorkflowActions: actions,
                    WFWorkflowOutputContentItemClasses: ["WFStringContentItem"]
                }
            };

            // Convertir a formato base64 para el enlace
            const shortcutData = Buffer.from(JSON.stringify(shortcutContent)).toString('base64');
            const shortcutUrl = `shortcuts://import-shortcut?url=data:text/plain;base64,${shortcutData}`;

            // Generar QR code
            const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(shortcutUrl)}`;

            // Guardar en base de datos
            const shortcutId = await this.saveShortcut({
                name: superpowerName,
                description: superpowerDescription,
                actions: JSON.stringify(actions),
                icon_color: 'blue',
                icon_glyph: 'bolt',
                shortcut_url: shortcutUrl,
                qr_code: qrCodeUrl,
                trigger_type: triggerType,
                trigger_phrase: triggerPhrase
            });

            // Guardar archivo local
            const fileName = `shortcut_${superpowerName.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}.json`;
            const filePath = path.join(this.outputDir, fileName);
            
            const shortcutInfo = {
                id: shortcutId,
                name: superpowerName,
                description: superpowerDescription,
                shortcut_url: shortcutUrl,
                qr_code: qrCodeUrl,
                trigger_type: triggerType,
                trigger_phrase: triggerPhrase,
                created_at: new Date().toISOString(),
                actions: actions
            };

            fs.writeFileSync(filePath, JSON.stringify(shortcutInfo, null, 2));

            console.log('✅ Shortcut generado exitosamente');
            console.log(`📁 Archivo guardado: ${filePath}`);
            console.log(`🔗 Enlace directo: ${shortcutUrl}`);

            return shortcutInfo;

        } catch (error) {
            console.error('❌ Error generando shortcut:', error);
            throw error;
        }
    }

    // 🎯 Obtener acciones específicas para cada superpoder
    getActionsForSuperpower(superpowerName, description, triggerType) {
        const baseActions = [
            {
                WFWorkflowActionIdentifier: "is.workflow.actions.showresult",
                WFWorkflowActionParameters: {
                    Text: `🎯 ${superpowerName} activado!\n\n${description}\n\n⚡ Generado por DesArroyo.tech`
                }
            }
        ];

        // Acciones específicas según el tipo de superpoder
        const superpowerActions = {
            'Scanner de Documentos': [
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.getfile",
                    WFWorkflowActionParameters: {
                        WFGetFileActionMode: "Get Latest Photos",
                        WFGetFileActionLimit: 1
                    }
                },
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.scanqr",
                    WFWorkflowActionParameters: {}
                }
            ],
            'Automatización de WhatsApp': [
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.geturl",
                    WFWorkflowActionParameters: {
                        URL: "https://wa.me/34600000000?text=Hola,%20me%20interesa%20tu%20servicio"
                    }
                },
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.openurl",
                    WFWorkflowActionParameters: {}
                }
            ],
            'Traductor Instantáneo': [
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.detect.language",
                    WFWorkflowActionParameters: {
                        WFLanguage: "es-ES"
                    }
                },
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.translate",
                    WFWorkflowActionParameters: {
                        WFTranslateTextTargetLanguage: "en"
                    }
                }
            ],
            'Calculadora Rápida': [
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.askforinput",
                    WFWorkflowActionParameters: {
                        WFInputPrompt: "Introduce la operación:",
                        WFInputType: "Number"
                    }
                },
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.calculate",
                    WFWorkflowActionParameters: {}
                }
            ],
            'Recordatorio por Voz': [
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.recordaudio",
                    WFWorkflowActionParameters: {
                        WFRecordingDuration: 30
                    }
                },
                {
                    WFWorkflowActionIdentifier: "is.workflow.actions.addreminder",
                    WFWorkflowActionParameters: {
                        WFReminderTitle: "Recordatorio por voz"
                    }
                }
            ]
        };

        // Buscar acciones específicas para el superpoder
        for (const [key, actions] of Object.entries(superpowerActions)) {
            if (superpowerName.toLowerCase().includes(key.toLowerCase()) || 
                key.toLowerCase().includes(superpowerName.toLowerCase())) {
                return [...actions, ...baseActions];
            }
        }

        // Si no hay acciones específicas, usar acciones genéricas
        return [
            {
                WFWorkflowActionIdentifier: "is.workflow.actions.showresult",
                WFWorkflowActionParameters: {
                    Text: `⚡ ${superpowerName}\n\n${description}\n\n🎯 Para activar este superpoder:\n1. Toca el shortcut\n2. Sigue las instrucciones\n3. ¡Disfruta del poder!\n\n💡 Creado por DesArroyo.tech`
                }
            },
            ...baseActions
        ];
    }

    // 💾 Guardar shortcut en base de datos
    async saveShortcut(shortcutData) {
        return new Promise((resolve, reject) => {
            const { name, description, actions, icon_color, icon_glyph, shortcut_url, qr_code, trigger_type, trigger_phrase } = shortcutData;
            
            this.db.run(
                'INSERT INTO shortcuts (name, description, actions, icon_color, icon_glyph, shortcut_url, qr_code, trigger_type, trigger_phrase, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [name, description, actions, icon_color, icon_glyph, shortcut_url, qr_code, trigger_type, trigger_phrase, new Date().toISOString()],
                function(err) {
                    if (err) {
                        console.error('Error guardando shortcut:', err);
                        reject(err);
                    } else {
                        resolve(this.lastID);
                    }
                }
            );
        });
    }

    // 📋 Obtener todos los shortcuts
    async getAllShortcuts() {
        return new Promise((resolve, reject) => {
            this.db.all('SELECT * FROM shortcuts ORDER BY created_at DESC', [], (err, shortcuts) => {
                if (err) {
                    console.error('Error obteniendo shortcuts:', err);
                    reject(err);
                } else {
                    resolve(shortcuts);
                }
            });
        });
    }

    // 🔍 Obtener shortcut por ID
    async getShortcutById(id) {
        return new Promise((resolve, reject) => {
            this.db.get('SELECT * FROM shortcuts WHERE id = ?', [id], (err, shortcut) => {
                if (err) {
                    console.error('Error obteniendo shortcut:', err);
                    reject(err);
                } else {
                    resolve(shortcut);
                }
            });
        });
    }

    // 🗑️ Eliminar shortcut
    async deleteShortcut(id) {
        return new Promise((resolve, reject) => {
            this.db.run('DELETE FROM shortcuts WHERE id = ?', [id], function(err) {
                if (err) {
                    console.error('Error eliminando shortcut:', err);
                    reject(err);
                } else {
                    resolve(this.changes > 0);
                }
            });
        });
    }

    // 📊 Generar reporte de shortcuts
    async generateReport() {
        try {
            const shortcuts = await this.getAllShortcuts();
            
            const report = {
                total_shortcuts: shortcuts.length,
                shortcuts_by_type: {},
                recent_shortcuts: shortcuts.slice(0, 5),
                created_at: new Date().toISOString()
            };

            // Agrupar por tipo de trigger
            shortcuts.forEach(shortcut => {
                const type = shortcut.trigger_type || 'manual';
                report.shortcuts_by_type[type] = (report.shortcuts_by_type[type] || 0) + 1;
            });

            return report;
        } catch (error) {
            console.error('Error generando reporte:', error);
            throw error;
        }
    }

    // 🔄 Cerrar conexión
    close() {
        if (this.db) {
            this.db.close((err) => {
                if (err) {
                    console.error('Error cerrando base de datos:', err);
                } else {
                    console.log('✅ Conexión a base de datos cerrada');
                }
            });
        }
    }
}

// 🚀 Función principal para testing
async function main() {
    const generator = new ShortcutGenerator();
    
    try {
        await generator.init();
        
        // Ejemplo de generación de shortcut
        const shortcut = await generator.generateSuperpowerShortcut(
            'Scanner de Documentos',
            'Escanea documentos automáticamente y los convierte en PDF',
            'voice',
            'Escanea documento'
        );
        
        console.log('✅ Shortcut creado:', shortcut);
        
        // Generar reporte
        const report = await generator.generateReport();
        console.log('📊 Reporte:', report);
        
    } catch (error) {
        console.error('❌ Error en main:', error);
    } finally {
        generator.close();
    }
}

// Exportar para uso en otros módulos
module.exports = ShortcutGenerator;

// Ejecutar si es el archivo principal
if (require.main === module) {
    main();
} 