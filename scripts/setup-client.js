#!/usr/bin/env node

/**
 * Script para configurar nuevos clientes en el sistema DesArroyo.Tech
 * 
 * Uso: node scripts/setup-client.js --name "Juan Pérez" --email "juan@ejemplo.com" --project "Web de Restaurante"
 */

const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

// Configuración
const DB_PATH = path.join(__dirname, '../dashboard.db');

class ClientSetup {
    constructor() {
        this.db = new sqlite3.Database(DB_PATH);
    }

    async setupClient(clientData) {
        try {
            console.log('🚀 Configurando nuevo cliente...');
            
            // 1. Crear cliente en la base de datos
            const clientId = await this.createClient(clientData);
            console.log(`✅ Cliente creado con ID: ${clientId}`);
            
            // 2. Crear proyecto asociado
            const projectId = await this.createProject(clientId, clientData);
            console.log(`✅ Proyecto creado con ID: ${projectId}`);
            
            // 3. Configurar automatizaciones básicas
            await this.setupAutomations(clientId, clientData);
            console.log('✅ Automatizaciones configuradas');
            
            // 4. Generar configuración de n8n
            await this.generateN8nConfig(clientId, clientData);
            console.log('✅ Configuración n8n generada');
            
            // 5. Crear acceso al mini-CRM
            const crmUrl = await this.createCRMAccess(clientId, clientData);
            console.log(`✅ Mini-CRM disponible en: ${crmUrl}`);
            
            // 6. Generar documentación del cliente
            await this.generateClientDocs(clientId, clientData);
            console.log('✅ Documentación generada');
            
            // 7. Generar código de integración para la web del cliente
            await this.generateIntegrationCode(clientId, clientData);
            console.log('✅ Código de integración generado');
            
            console.log('\n🎉 Cliente configurado exitosamente!');
            this.printSummary(clientId, clientData, crmUrl);
            
        } catch (error) {
            console.error('❌ Error configurando cliente:', error);
            process.exit(1);
        } finally {
            this.db.close();
        }
    }

    async createClient(clientData) {
        return new Promise((resolve, reject) => {
            const { name, email, phone, company, project_name, domain } = clientData;
            
            this.db.run(
                `INSERT INTO clients (name, email, phone, company, project_name, domain, status) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)`,
                [name, email, phone, company, project_name, domain, 'active'],
                function(err) {
                    if (err) reject(err);
                    else resolve(this.lastID);
                }
            );
        });
    }

    async createProject(clientId, clientData) {
        return new Promise((resolve, reject) => {
            this.db.run(
                `INSERT INTO projects (client_id, name, description, domain, status, progress) 
                 VALUES (?, ?, ?, ?, ?, ?)`,
                [clientId, clientData.project_name, `Proyecto web para ${clientData.name}`, clientData.domain, 'active', 0],
                function(err) {
                    if (err) reject(err);
                    else resolve(this.lastID);
                }
            );
        });
    }

    async setupAutomations(clientId, clientData) {
        const automations = [
            {
                name: 'Email de Bienvenida',
                description: 'Envío automático de email de bienvenida a nuevos leads',
                type: 'email_welcome',
                config: JSON.stringify({
                    template: 'welcome_email',
                    subject: '¡Bienvenido a ' + clientData.project_name + '!'
                })
            },
            {
                name: 'Notificación de Lead',
                description: 'Notificación por Telegram cuando se capture un nuevo lead',
                type: 'telegram_notification',
                config: JSON.stringify({
                    chat_id: process.env.TELEGRAM_CHAT_ID,
                    message_template: 'Nuevo lead en ' + clientData.project_name
                })
            },
            {
                name: 'Recordatorio de Contacto',
                description: 'Recordatorio automático para contactar leads no respondidos',
                type: 'reminder',
                config: JSON.stringify({
                    delay_days: 3,
                    message: 'Recordatorio: Contactar lead de ' + clientData.project_name
                })
            }
        ];

        for (const automation of automations) {
            await new Promise((resolve, reject) => {
                this.db.run(
                    `INSERT INTO automations (client_id, name, description, type, config, active) 
                     VALUES (?, ?, ?, ?, ?, ?)`,
                    [clientId, automation.name, automation.description, automation.type, automation.config, 1],
                    function(err) {
                        if (err) reject(err);
                        else resolve(this.lastID);
                    }
                );
            });
        }
    }

    async generateN8nConfig(clientId, clientData) {
        const n8nConfig = {
            name: `Cliente ${clientData.name} - Automatizaciones`,
            description: `Automatizaciones para ${clientData.project_name}`,
            version: '1.0.0',
            client_id: clientId,
            workflows: [
                {
                    name: 'Captura de Lead',
                    description: 'Procesa nuevos leads del formulario web',
                    nodes: [
                        {
                            type: 'webhook',
                            name: 'Webhook Nuevo Lead',
                            config: {
                                path: `/api/webhooks/${clientId}/new-lead`,
                                method: 'POST'
                            }
                        },
                        {
                            type: 'email',
                            name: 'Email de Confirmación',
                            config: {
                                to: '{{lead.email}}',
                                subject: 'Gracias por contactar con ' + clientData.project_name,
                                template: 'lead_confirmation'
                            }
                        },
                        {
                            type: 'telegram',
                            name: 'Notificación Telegram',
                            config: {
                                chat_id: process.env.TELEGRAM_CHAT_ID,
                                message: `🎯 Nuevo lead en ${clientData.project_name}:\n👤 ${clientData.name}\n📧 {{lead.email}}\n📞 {{lead.phone}}`
                            }
                        },
                        {
                            type: 'database',
                            action: 'save_lead',
                            config: {
                                table: 'leads',
                                data: {
                                    client_id: clientId,
                                    name: '{{lead.name}}',
                                    email: '{{lead.email}}',
                                    phone: '{{lead.phone}}',
                                    status: 'new'
                                }
                            }
                        }
                    ]
                }
            ]
        };

        // Crear directorio para configuraciones de n8n
        const n8nDir = path.join(__dirname, '../n8n-configs');
        if (!fs.existsSync(n8nDir)) {
            fs.mkdirSync(n8nDir, { recursive: true });
        }

        // Guardar configuración
        const configPath = path.join(n8nDir, `client-${clientId}.json`);
        fs.writeFileSync(configPath, JSON.stringify(n8nConfig, null, 2));
        
        console.log(`📁 Configuración n8n guardada en: ${configPath}`);
    }

    async createCRMAccess(clientId, clientData) {
        // Generar URL del mini-CRM
        const crmUrl = `https://desarroyo.tech/client-crm.html?client_id=${clientId}`;
        
        // Crear archivo de configuración del cliente
        const clientConfig = {
            client_id: clientId,
            name: clientData.name,
            email: clientData.email,
            project_name: clientData.project_name,
            domain: clientData.domain,
            crm_url: crmUrl,
            created_at: new Date().toISOString()
        };

        // Guardar configuración del cliente
        const clientsDir = path.join(__dirname, '../client-configs');
        if (!fs.existsSync(clientsDir)) {
            fs.mkdirSync(clientsDir, { recursive: true });
        }

        const configPath = path.join(clientsDir, `client-${clientId}.json`);
        fs.writeFileSync(configPath, JSON.stringify(clientConfig, null, 2));

        return crmUrl;
    }

    async generateClientDocs(clientId, clientData) {
        const docsDir = path.join(__dirname, '../client-docs');
        if (!fs.existsSync(docsDir)) {
            fs.mkdirSync(docsDir, { recursive: true });
        }

        const docContent = `# Documentación del Cliente: ${clientData.name}

## Información General
- **ID del Cliente**: ${clientId}
- **Nombre**: ${clientData.name}
- **Email**: ${clientData.email}
- **Proyecto**: ${clientData.project_name}
- **Dominio**: ${clientData.domain}

## URLs Importantes
- **Mini-CRM**: https://desarroyo.tech/client-crm.html?client_id=${clientId}
- **Dashboard Admin**: https://desarroyo.tech/dashboard

## Automatizaciones Configuradas
1. Email de Bienvenida
2. Notificación de Lead por Telegram
3. Recordatorio de Contacto

## Webhooks n8n
- Nuevo Lead: /api/webhooks/${clientId}/new-lead
- Lead Convertido: /api/webhooks/${clientId}/lead-converted
- Actualización de Proyecto: /api/webhooks/${clientId}/project-update

## Configuración
- Estado: Activo
- Fecha de Creación: ${new Date().toLocaleDateString('es-ES')}

---
Generado automáticamente por DesArroyo.Tech
`;

        const docPath = path.join(docsDir, `client-${clientId}.md`);
        fs.writeFileSync(docPath, docContent);
    }

    async generateIntegrationCode(clientId, clientData) {
        const integrationDir = path.join(__dirname, '../client-integrations');
        if (!fs.existsSync(integrationDir)) {
            fs.mkdirSync(integrationDir, { recursive: true });
        }

        // Código HTML para integrar en la web del cliente
        const htmlCode = `<!-- Código de integración para ${clientData.project_name} -->
<!-- Colocar este código en la web del cliente para integrar el mini-CRM -->

<!-- Opción 1: Iframe embebido -->
<iframe src="https://desarroyo.tech/client-crm.html?client_id=${clientId}" 
        width="100%" 
        height="800px" 
        frameborder="0"
        style="border: none; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</iframe>

<!-- Opción 2: Enlace directo -->
<a href="https://desarroyo.tech/client-crm.html?client_id=${clientId}" 
   target="_blank"
   style="display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold;">
   🚀 Acceder al Panel de Administración
</a>

<!-- Opción 3: Formulario de contacto integrado -->
<form id="contact-form-${clientId}" style="max-width: 500px; margin: 20px auto;">
    <h3>Contacta con ${clientData.project_name}</h3>
    <input type="text" name="name" placeholder="Tu nombre" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
    <input type="email" name="email" placeholder="Tu email" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
    <input type="tel" name="phone" placeholder="Tu teléfono" style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;">
    <textarea name="message" placeholder="Tu mensaje" rows="4" required style="width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px;"></textarea>
    <button type="submit" style="width: 100%; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 5px; cursor: pointer;">
        Enviar Mensaje
    </button>
</form>

<script>
// JavaScript para manejar el formulario
document.getElementById('contact-form-${clientId}').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        client_id: ${clientId},
        name: formData.get('name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        message: formData.get('message'),
        source: '${clientData.domain}'
    };
    
    try {
        const response = await fetch('https://desarroyo.tech/api/webhooks/${clientId}/new-lead', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('¡Gracias por contactar! Te responderemos pronto.');
            this.reset();
        } else {
            alert('Error al enviar el mensaje. Inténtalo de nuevo.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al enviar el mensaje. Inténtalo de nuevo.');
    }
});
</script>`;

        // Código JavaScript para webhooks
        const jsCode = `// Código JavaScript para ${clientData.project_name}
// Integrar en la web del cliente para capturar leads

class LeadCapture {
    constructor(clientId) {
        this.clientId = clientId;
        this.webhookUrl = \`https://desarroyo.tech/api/webhooks/\${clientId}/new-lead\`;
    }

    async captureLead(leadData) {
        try {
            const response = await fetch(this.webhookUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    client_id: this.clientId,
                    ...leadData,
                    source: window.location.hostname,
                    timestamp: new Date().toISOString()
                })
            });

            return response.ok;
        } catch (error) {
            console.error('Error capturando lead:', error);
            return false;
        }
    }

    // Método para capturar desde formulario
    captureFromForm(formElement) {
        formElement.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(formElement);
            const leadData = {
                name: formData.get('name'),
                email: formData.get('email'),
                phone: formData.get('phone'),
                message: formData.get('message')
            };

            const success = await this.captureLead(leadData);
            
            if (success) {
                alert('¡Gracias por contactar! Te responderemos pronto.');
                formElement.reset();
            } else {
                alert('Error al enviar el mensaje. Inténtalo de nuevo.');
            }
        });
    }
}

// Inicializar captura de leads
const leadCapture = new LeadCapture(${clientId});

// Ejemplo de uso con formulario existente
// leadCapture.captureFromForm(document.getElementById('contact-form'));
`;

        // Guardar archivos
        const htmlPath = path.join(integrationDir, `client-${clientId}-integration.html`);
        const jsPath = path.join(integrationDir, `client-${clientId}-capture.js`);
        
        fs.writeFileSync(htmlPath, htmlCode);
        fs.writeFileSync(jsPath, jsCode);
        
        console.log(`📁 Código de integración guardado en:`);
        console.log(`   - ${htmlPath}`);
        console.log(`   - ${jsPath}`);
    }

    printSummary(clientId, clientData, crmUrl) {
        console.log('\n📋 RESUMEN DE CONFIGURACIÓN');
        console.log('========================');
        console.log(`👤 Cliente: ${clientData.name}`);
        console.log(`📧 Email: ${clientData.email}`);
        console.log(`🏢 Proyecto: ${clientData.project_name}`);
        console.log(`🌐 Dominio: ${clientData.domain}`);
        console.log(`🆔 ID: ${clientId}`);
        console.log(`🔗 Mini-CRM: ${crmUrl}`);
        console.log('\n📁 Archivos Generados:');
        console.log(`   - n8n-configs/client-${clientId}.json`);
        console.log(`   - client-configs/client-${clientId}.json`);
        console.log(`   - client-docs/client-${clientId}.md`);
        console.log(`   - client-integrations/client-${clientId}-integration.html`);
        console.log(`   - client-integrations/client-${clientId}-capture.js`);
        console.log('\n🎯 Próximos Pasos:');
        console.log('   1. Importar configuración en n8n');
        console.log('   2. Configurar webhooks en la web del cliente');
        console.log('   3. Probar automatizaciones');
        console.log('   4. Entregar acceso al mini-CRM al cliente');
        console.log('   5. Integrar código en la web del cliente');
    }
}

// Ejecutar si se llama directamente
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.length < 4) {
        console.log('Uso: node setup-client.js <nombre> <email> <proyecto> <dominio> [telefono] [empresa]');
        console.log('Ejemplo: node setup-client.js "Juan Pérez" "juan@ejemplo.com" "Web de Restaurante" "restaurantejuan.com" "+34600000000" "Restaurante Juan"');
        process.exit(1);
    }

    const clientData = {
        name: args[0],
        email: args[1],
        project_name: args[2],
        domain: args[3],
        phone: args[4] || '',
        company: args[5] || ''
    };

    const setup = new ClientSetup();
    setup.setupClient(clientData);
}

module.exports = ClientSetup; 