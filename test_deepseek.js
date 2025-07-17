#!/usr/bin/env node
/**
 * 🧪 TEST DEEPSEEK API - Verificar configuración
 * Prueba que la API key de DeepSeek funcione correctamente
 */

const axios = require('axios');
require('dotenv').config();

async function testDeepSeekAPI() {
    console.log('🧪 TESTING DEEPSEEK API...\n');
    
    // Verificar que la API key esté configurada
    const apiKey = process.env.DEEPSEEK_API_KEY;
    
    if (!apiKey) {
        console.log('❌ ERROR: DEEPSEEK_API_KEY no está configurada');
        console.log('📝 Por favor, configura la API key en el archivo .env');
        process.exit(1);
    }
    
    if (apiKey === 'tu_api_key_deepseek' || apiKey === 'REEMPLAZA_CON_TU_API_KEY_REAL_AQUI') {
        console.log('❌ ERROR: DEEPSEEK_API_KEY tiene un valor placeholder');
        console.log('📝 Por favor, reemplaza con tu API key real de DeepSeek');
        console.log('🔗 Obtén tu API key en: https://platform.deepseek.com/');
        process.exit(1);
    }
    
    console.log('✅ API Key configurada correctamente');
    console.log(`🔑 API Key: ${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`);
    
    // Test de conexión
    try {
        console.log('\n🔄 Probando conexión con DeepSeek...');
        
        const response = await axios.post('https://api.deepseek.com/v1/chat/completions', {
            model: 'deepseek-chat',
            messages: [
                {
                    role: 'system',
                    content: 'Eres un asistente útil.'
                },
                {
                    role: 'user',
                    content: 'Responde solo con: "¡DeepSeek funciona correctamente!"'
                }
            ],
            max_tokens: 50,
            temperature: 0.7
        }, {
            headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
            },
            timeout: 10000
        });
        
        const botResponse = response.data.choices[0].message.content;
        
        console.log('✅ CONEXIÓN EXITOSA!');
        console.log(`🤖 Respuesta de DeepSeek: ${botResponse}`);
        console.log('\n🎉 ¡El generador de guiones ya debería funcionar!');
        console.log('🔗 Ve a: http://localhost:3000/dashboard');
        console.log('📝 Prueba generar un guión desde Videos → Plantillas → 🎭 Guión');
        
    } catch (error) {
        console.log('❌ ERROR DE CONEXIÓN:');
        
        if (error.response) {
            console.log(`📊 Status: ${error.response.status}`);
            console.log(`📝 Error: ${error.response.data.error?.message || 'Error desconocido'}`);
            
            if (error.response.status === 401) {
                console.log('\n🔧 SOLUCIÓN:');
                console.log('1. Verifica que la API key sea correcta');
                console.log('2. Ve a https://platform.deepseek.com/');
                console.log('3. Genera una nueva API key');
                console.log('4. Reemplaza en el archivo .env');
            }
        } else {
            console.log(`📝 Error: ${error.message}`);
        }
        
        process.exit(1);
    }
}

// Ejecutar test
testDeepSeekAPI(); 