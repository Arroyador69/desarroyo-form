#!/usr/bin/env node

/**
 * 🎬 Generador de Guiones para Videos - DesArroyo.tech
 * Sistema inteligente para crear guiones específicos para cada plantilla
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const { config } = require('../config');

class ScriptGenerator {
    constructor() {
        this.deepseekApiKey = process.env.DEEPSEEK_API_KEY;
        this.deepseekApiUrl = 'https://api.deepseek.com/v1/chat/completions';
        this.db = null;
        this.outputDir = './scripts/generated-scripts';
        
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
                    console.log('✅ Conectado a la base de datos');
                    resolve();
                }
            });
        });
    }

    // 🎭 Prompts específicos para cada tipo de plantilla
    getPromptForTemplate(templateType, templateName, templateDescription, customTopic = null) {
        const baseContext = `
Eres el escritor de guiones para DesArroyo.tech, empresa de desarrollo y automatización dirigida por Alberto Arroyo.

INFORMACIÓN DE LA EMPRESA:
- Servicios: Webs HTML (48h), automatizaciones n8n, apps móviles, bots WhatsApp/Telegram
- Público: Emprendedores, pequeñas empresas, desarrolladores
- Estilo: Profesional pero cercano, enfocado en resultados
- Contact: alberto@desarroyo.tech
- Filosofía: "Crea, automatiza, comparte… y vuelve a la playa a celebrar"

INSTRUCCIONES:
- Genera un guión específico para la plantilla "${templateName}"
- Duración máxima: 59 segundos (aprox. 150-180 palabras)
- Incluye calls-to-action naturales hacia DesArroyo.tech
- Usa un tono profesional pero amigable
- Estructura clara con momentos clave
- Incluye direcciones específicas para cada clip/momento
        `;

        const prompts = {
            'educativo': `${baseContext}

PLANTILLA: ${templateName}
TIPO: Educativo/Tutorial
DESCRIPCIÓN: ${templateDescription}

ESTRUCTURA REQUERIDA:
1. INTRO (5-8 segundos): Hook potente que capture atención
2. BODY (40-45 segundos): Contenido educativo valioso y actionable
3. OUTRO (8-10 segundos): CTA claro hacia DesArroyo.tech

TEMA: ${customTopic || 'Automatización para emprendedores'}

GENERA UN GUIÓN QUE INCLUYA:
- Hook impactante sobre el problema/oportunidad
- 3-5 consejos prácticos súper valiosos
- Llamada a la acción natural hacia alberto@desarroyo.tech
- Direcciones específicas para cada clip (qué mostrar, gestos, etc.)
- Texto overlay sugerido para cada momento

FORMATO:
[INTRO - 0:00-0:08]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[BODY - 0:08-0:50]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[OUTRO - 0:50-0:59]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."`,

            'inspiracional': `${baseContext}

PLANTILLA: ${templateName}
TIPO: Inspiracional/Storytelling
DESCRIPCIÓN: ${templateDescription}

ESTRUCTURA REQUERIDA:
1. INTRO (5-8 segundos): Hook emocional
2. DESARROLLO (20-25 segundos): Historia/problema personal
3. CLÍMAX (15-20 segundos): Momento de transformación
4. RESOLUCIÓN (8-10 segundos): CTA inspiracional

TEMA: ${customTopic || 'Transformación digital para emprendedores'}

GENERA UN GUIÓN QUE INCLUYA:
- Historia personal/testimonio real
- Momento de crisis/desafío
- Solución/transformación clara
- Inspiración para la audiencia
- CTA emocional hacia DesArroyo.tech

FORMATO:
[INTRO - 0:00-0:08]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[DESARROLLO - 0:08-0:33]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[CLÍMAX - 0:33-0:50]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[RESOLUCIÓN - 0:50-0:59]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."`,

            'promocional': `${baseContext}

PLANTILLA: ${templateName}
TIPO: Promocional/Ventas
DESCRIPCIÓN: ${templateDescription}

ESTRUCTURA REQUERIDA:
1. PROBLEMA (8-12 segundos): Identifica dolor específico
2. SOLUCIÓN (35-40 segundos): Presenta servicios DesArroyo.tech
3. CTA (8-10 segundos): Llamada a la acción directa

TEMA: ${customTopic || 'Servicios de automatización DesArroyo.tech'}

GENERA UN GUIÓN QUE INCLUYA:
- Problema específico que resuelve DesArroyo.tech
- Beneficios claros de los servicios
- Casos de uso concretos
- CTA directo y persuasivo

FORMATO:
[PROBLEMA - 0:00-0:12]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[SOLUCIÓN - 0:12-0:50]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[CTA - 0:50-0:59]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."`,

            'tutorial': `${baseContext}

PLANTILLA: ${templateName}
TIPO: Tutorial/Paso a paso
DESCRIPCIÓN: ${templateDescription}

ESTRUCTURA REQUERIDA:
1. INTRO (5-8 segundos): Qué van a aprender
2. PASOS (40-45 segundos): Tutorial paso a paso
3. RESULTADO (8-10 segundos): Beneficio + CTA

TEMA: ${customTopic || 'Cómo automatizar procesos empresariales'}

GENERA UN GUIÓN QUE INCLUYA:
- Promesa clara de aprendizaje
- Pasos específicos y actionables
- Resultado tangible
- CTA hacia más recursos en DesArroyo.tech

FORMATO:
[INTRO - 0:00-0:08]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[PASOS - 0:08-0:50]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."

[RESULTADO - 0:50-0:59]
Dirección: (describe qué hacer/mostrar)
Guión: "..."
Texto overlay: "..."`
        };

        return prompts[templateType] || prompts['educativo'];
    }

    // 🤖 Generar guión con DeepSeek
    async generateScript(templateId, customTopic = null, additionalInstructions = '') {
        try {
            console.log(`🎬 Generando guión para plantilla ID: ${templateId}`);

            // Obtener información de la plantilla
            const template = await this.getTemplate(templateId);
            if (!template) {
                throw new Error('Plantilla no encontrada');
            }

            // Preparar el prompt
            const prompt = this.getPromptForTemplate(
                template.type, 
                template.name, 
                template.description, 
                customTopic
            );

            const fullPrompt = `${prompt}

${additionalInstructions ? `\nINSTRUCCIONES ADICIONALES: ${additionalInstructions}` : ''}

RECUERDA: 
- Máximo 59 segundos total
- Incluye direcciones específicas para cada clip
- Menciona DesArroyo.tech naturalmente
- Texto overlay debe ser corto y impactante
- Tono profesional pero cercano`;

            console.log('🤖 Enviando petición a DeepSeek...');

            // Llamada a DeepSeek
            const response = await axios.post(this.deepseekApiUrl, {
                model: 'deepseek-chat',
                messages: [
                    {
                        role: 'system',
                        content: 'Eres un escritor de guiones experto en contenido viral para redes sociales, especializado en videos educativos y promocionales para empresas de tecnología.'
                    },
                    {
                        role: 'user',
                        content: fullPrompt
                    }
                ],
                max_tokens: 2000,
                temperature: 0.7
            }, {
                headers: {
                    'Authorization': `Bearer ${this.deepseekApiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.data.choices || response.data.choices.length === 0) {
                throw new Error('No se recibió respuesta de DeepSeek');
            }

            const generatedScript = response.data.choices[0].message.content;

            // Guardar en base de datos
            const scriptId = await this.saveScript(templateId, generatedScript, customTopic, additionalInstructions);

            // Guardar archivo de texto
            const fileName = `script_${templateId}_${Date.now()}.txt`;
            const filePath = path.join(this.outputDir, fileName);
            
            const scriptContent = `# Guión Generado - ${template.name}
## Plantilla: ${template.name} (${template.type})
## Tema: ${customTopic || 'Tema por defecto'}
## Generado: ${new Date().toLocaleString()}

${generatedScript}

---
Generado por DesArroyo.tech Script Generator
`;

            fs.writeFileSync(filePath, scriptContent);

            console.log('✅ Guión generado exitosamente');
            console.log(`📁 Archivo guardado: ${filePath}`);
            console.log(`🆔 ID en base de datos: ${scriptId}`);

            return {
                id: scriptId,
                template_id: templateId,
                template_name: template.name,
                template_type: template.type,
                script: generatedScript,
                topic: customTopic,
                file_path: filePath,
                created_at: new Date().toISOString()
            };

        } catch (error) {
            console.error('❌ Error generando guión:', error);
            throw error;
        }
    }

    // 🗄️ Obtener plantilla de la base de datos
    async getTemplate(templateId) {
        return new Promise((resolve, reject) => {
            this.db.get(
                'SELECT * FROM video_templates WHERE id = ?',
                [templateId],
                (err, row) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(row);
                    }
                }
            );
        });
    }

    // 💾 Guardar guión en la base de datos
    async saveScript(templateId, script, topic, additionalInstructions) {
        return new Promise((resolve, reject) => {
            // Primero crear la tabla si no existe
            this.db.run(`CREATE TABLE IF NOT EXISTS video_scripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id INTEGER,
                script TEXT NOT NULL,
                topic TEXT,
                additional_instructions TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES video_templates (id)
            )`, (err) => {
                if (err) {
                    console.error('Error creando tabla video_scripts:', err);
                }
                
                // Insertar el guión
                this.db.run(
                    'INSERT INTO video_scripts (template_id, script, topic, additional_instructions) VALUES (?, ?, ?, ?)',
                    [templateId, script, topic, additionalInstructions],
                    function(err) {
                        if (err) {
                            reject(err);
                        } else {
                            resolve(this.lastID);
                        }
                    }
                );
            });
        });
    }

    // 📋 Obtener todos los guiones de una plantilla
    async getScriptsForTemplate(templateId) {
        return new Promise((resolve, reject) => {
            this.db.all(
                `SELECT s.*, t.name as template_name, t.type as template_type 
                 FROM video_scripts s 
                 JOIN video_templates t ON s.template_id = t.id 
                 WHERE s.template_id = ? 
                 ORDER BY s.created_at DESC`,
                [templateId],
                (err, rows) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(rows);
                    }
                }
            );
        });
    }

    // 📊 Listar todas las plantillas disponibles
    async listTemplates() {
        return new Promise((resolve, reject) => {
            this.db.all(
                'SELECT id, name, type, description FROM video_templates ORDER BY name',
                (err, rows) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(rows);
                    }
                }
            );
        });
    }

    // 🎯 Generar múltiples guiones para una plantilla
    async generateMultipleScripts(templateId, topics = [], count = 3) {
        const scripts = [];
        
        if (topics.length === 0) {
            // Temas por defecto según el tipo de plantilla
            const template = await this.getTemplate(templateId);
            const defaultTopics = this.getDefaultTopics(template.type);
            topics = defaultTopics.slice(0, count);
        }

        for (const topic of topics) {
            try {
                console.log(`🎬 Generando guión para tema: ${topic}`);
                const script = await this.generateScript(templateId, topic);
                scripts.push(script);
                
                // Pequeña pausa para evitar rate limiting
                await this.sleep(1000);
            } catch (error) {
                console.error(`❌ Error generando guión para tema "${topic}":`, error);
            }
        }

        return scripts;
    }

    // 🎭 Temas por defecto según el tipo de plantilla
    getDefaultTopics(templateType) {
        const topicsByType = {
            'educativo': [
                'Automatización para restaurantes',
                'Bots de WhatsApp para empresas',
                'Webs HTML en 48 horas',
                'Apps móviles sin programar',
                'Automatizar Instagram con n8n'
            ],
            'inspiracional': [
                'De empleado a emprendedor tech',
                'Cómo automaticé mi negocio',
                'Mi primer cliente en 48 horas',
                'Del burnout al éxito digital',
                'Transformación digital personal'
            ],
            'promocional': [
                'Servicios DesArroyo.tech',
                'Automatización para tu negocio',
                'Webs profesionales rápidas',
                'Bots que venden 24/7',
                'Consultoría tech personalizada'
            ],
            'tutorial': [
                'Configurar bot de WhatsApp',
                'Crear formulario de contacto',
                'Automatizar redes sociales',
                'Integrar Stripe en tu web',
                'Configurar n8n básico'
            ]
        };

        return topicsByType[templateType] || topicsByType['educativo'];
    }

    // 💤 Función auxiliar para pausas
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // 🔄 Cerrar conexión
    close() {
        if (this.db) {
            this.db.close((err) => {
                if (err) {
                    console.error('❌ Error cerrando base de datos:', err);
                } else {
                    console.log('✅ Base de datos cerrada');
                }
            });
        }
    }
}

// 🚀 Función principal para uso desde línea de comandos
async function main() {
    const args = process.argv.slice(2);
    const generator = new ScriptGenerator();

    try {
        await generator.init();

        if (args.length === 0) {
            console.log('📋 Uso del Script Generator:');
            console.log('');
            console.log('node script-generator.js list                    # Listar plantillas');
            console.log('node script-generator.js generate <template_id>  # Generar guión');
            console.log('node script-generator.js generate <template_id> "tema personalizado"');
            console.log('node script-generator.js multiple <template_id> # Generar múltiples guiones');
            console.log('node script-generator.js scripts <template_id>  # Ver guiones de una plantilla');
            console.log('');
            return;
        }

        const command = args[0];

        switch (command) {
            case 'list':
                const templates = await generator.listTemplates();
                console.log('📋 Plantillas disponibles:');
                templates.forEach((template, index) => {
                    console.log(`   ${index + 1}. ID: ${template.id} - ${template.name} (${template.type})`);
                    console.log(`      ${template.description}`);
                    console.log('');
                });
                break;

            case 'generate':
                if (args.length < 2) {
                    console.log('❌ Uso: node script-generator.js generate <template_id> [topic]');
                    return;
                }
                
                const templateId = parseInt(args[1]);
                const topic = args[2] || null;
                
                const script = await generator.generateScript(templateId, topic);
                console.log('🎬 Guión generado:');
                console.log('');
                console.log(script.script);
                break;

            case 'multiple':
                if (args.length < 2) {
                    console.log('❌ Uso: node script-generator.js multiple <template_id>');
                    return;
                }
                
                const multiTemplateId = parseInt(args[1]);
                const scripts = await generator.generateMultipleScripts(multiTemplateId);
                
                console.log(`🎬 Generados ${scripts.length} guiones:`);
                scripts.forEach((script, index) => {
                    console.log(`\n--- Guión ${index + 1}: ${script.topic} ---`);
                    console.log(script.script);
                });
                break;

            case 'scripts':
                if (args.length < 2) {
                    console.log('❌ Uso: node script-generator.js scripts <template_id>');
                    return;
                }
                
                const scriptsTemplateId = parseInt(args[1]);
                const existingScripts = await generator.getScriptsForTemplate(scriptsTemplateId);
                
                console.log(`📋 Guiones existentes para plantilla ID ${scriptsTemplateId}:`);
                existingScripts.forEach((script, index) => {
                    console.log(`\n--- Guión ${index + 1} ---`);
                    console.log(`Tema: ${script.topic || 'Sin tema'}`);
                    console.log(`Creado: ${script.created_at}`);
                    console.log(`Plantilla: ${script.template_name} (${script.template_type})`);
                    console.log('');
                    console.log(script.script.substring(0, 200) + '...');
                });
                break;

            default:
                console.log('❌ Comando no reconocido');
                console.log('Usa: list, generate, multiple, scripts');
        }

    } catch (error) {
        console.error('❌ Error:', error.message);
        process.exit(1);
    } finally {
        generator.close();
    }
}

// Ejecutar si es llamado directamente
if (require.main === module) {
    if (!process.env.DEEPSEEK_API_KEY) {
        console.error('❌ Error: DEEPSEEK_API_KEY no configurada');
        console.log('💡 Configurar en archivo .env o como variable de entorno');
        process.exit(1);
    }
    
    main();
}

module.exports = ScriptGenerator; 