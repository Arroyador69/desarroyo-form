#!/usr/bin/env node
/**
 * 🔗 Webhook que recibe POST del formulario y activa el workflow de GitHub Actions
 * Este script debe ejecutarse en un servidor que esté siempre activo
 * Alternativa: usar un servicio como n8n, Zapier, o un servidor simple
 */

require('dotenv').config();
const express = require('express');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3001;
const GITHUB_TOKEN = process.env.GH_TOKEN;
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'Arroyador69';
const GITHUB_REPO = process.env.GITHUB_REPO || 'desarroyo-form';

app.use(express.json());

// Endpoint que recibe el POST del formulario
app.post('/api/encuesta', async (req, res) => {
    try {
        const payload = req.body;

        console.log('📋 Encuesta recibida, activando workflow...');

        // Activar workflow de GitHub Actions usando repository_dispatch
        const response = await axios.post(
            `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/dispatches`,
            {
                event_type: 'encuesta-recibida',
                client_payload: {
                    encuesta_data: JSON.stringify(payload),
                    timestamp: new Date().toISOString()
                }
            },
            {
                headers: {
                    'Authorization': `token ${GITHUB_TOKEN}`,
                    'Accept': 'application/vnd.github.v3+json',
                    'Content-Type': 'application/json'
                }
            }
        );

        console.log('✅ Workflow activado correctamente');

        // Responder al formulario inmediatamente
        res.json({
            ok: true,
            message: 'Encuesta recibida. Estamos generando tu web HTML. Te notificaremos cuando esté lista.',
            workflow_triggered: true
        });

    } catch (error) {
        console.error('❌ Error activando workflow:', error.response?.data || error.message);
        
        res.status(500).json({
            ok: false,
            message: 'Error procesando la encuesta. Inténtalo de nuevo en unos minutos.'
        });
    }
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', service: 'webhook-activador' });
});

app.listen(PORT, () => {
    console.log(`🚀 Webhook activador corriendo en puerto ${PORT}`);
    console.log(`📡 Endpoint: http://localhost:${PORT}/api/encuesta`);
    console.log(`🔗 Este servidor debe estar siempre activo para recibir los POST del formulario`);
});

