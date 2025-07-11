// WEBHOOK SIMPLE PARA RESPUESTAS AUTOMÁTICAS WHATSAPP
// Vercel Serverless Function

const twilio = require('twilio');

export default async function handler(req, res) {
    // Solo acepta POST
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Método no permitido' });
    }

    try {
        // Datos de Twilio WhatsApp
        const fromPhone = req.body.From || '';
        const mensaje = req.body.Body || '';
        
        console.log(`📥 Respuesta recibida de ${fromPhone}: ${mensaje}`);
        
        if (!fromPhone || !mensaje) {
            return res.status(400).json({ error: 'Datos incompletos' });
        }

        // Generar respuesta automática inteligente
        const respuesta = generarRespuestaAutomatica(mensaje);
        
        // Enviar respuesta por WhatsApp
        if (process.env.TWILIO_ACCOUNT_SID && process.env.TWILIO_AUTH_TOKEN) {
            const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
            
            await client.messages.create({
                from: `whatsapp:${process.env.TWILIO_WHATSAPP_NUMBER}`,
                to: fromPhone,
                body: respuesta
            });
            
            console.log(`✅ Respuesta enviada a ${fromPhone}`);
        }

        // Notificar por Telegram (opcional)
        if (process.env.TELEGRAM_BOT_TOKEN && process.env.TELEGRAM_CHAT_ID) {
            await notificarTelegram(fromPhone, mensaje, respuesta);
        }

        return res.status(200).json({ 
            status: 'success', 
            message: 'Respuesta enviada automáticamente' 
        });

    } catch (error) {
        console.error('❌ Error webhook:', error);
        return res.status(500).json({ error: error.message });
    }
}

function generarRespuestaAutomatica(mensaje) {
    const msg = mensaje.toLowerCase();
    
    // Respuestas por palabras clave
    if (msg.includes('precio') || msg.includes('cuanto') || msg.includes('cuesta') || msg.includes('tarifa')) {
        return `¡Perfecto! 💰 Tenemos 3 planes adaptados a cada necesidad:

🟢 **Plan Rápida: 149€**
✅ 1 página profesional
✅ Entrega en 72 horas
✅ Optimizada para móviles

🟡 **Plan Escalable: 449€**
✅ Hasta 5 páginas completas
✅ SEO básico incluido
✅ Animaciones profesionales

🔴 **Plan Pro Digital: 999€**
✅ Hasta 10 páginas
✅ Dashboard personalizado
✅ Integración avanzada

ROI garantizado: recuperas la inversión en 2-4 semanas.

¿Vemos cuál se adapta mejor a tu negocio?
https://desarroyo.tech/generador_automatizaciones.html`;
    }
    
    if (msg.includes('si') || msg.includes('sí') || msg.includes('vale') || msg.includes('ok') || msg.includes('interesa')) {
        return `¡Excelente! 🎯 Me alegra saber que te interesa.

Para crear tu web perfecta, necesito conocer mejor tu negocio. 

Completa esta encuesta estratégica (solo 2 minutos):
https://desarroyo.tech/generador_automatizaciones.html

Con estos datos podremos hacer una propuesta 100% personalizada.

Entrega garantizada en máximo 48 horas. ¿Empezamos? 🚀`;
    }
    
    if (msg.includes('no') || msg.includes('gracias')) {
        return `Entiendo perfectamente. No hay problema. 😊

Si en algún momento cambias de opinión o tienes alguna pregunta, no dudes en escribirme.

Nuestros clientes ven resultados desde la primera semana:
• Restaurantes: +40% en ventas
• Clínicas: +3x más citas
• Negocios locales: +200% visibilidad online

¡Que tengas un excelente día!

Agente comercial de DesArroyo Tech 🚀`;
    }
    
    // Respuesta general
    return `¡Hola! 👋 Gracias por tu mensaje.

Entiendo que puedas tener dudas. Es normal cuando se trata de invertir en el crecimiento de tu negocio.

Nuestros clientes ven resultados reales desde la primera semana:
🍽️ Restaurantes aumentan ventas 40%
🏥 Clínicas triplican las citas
🏪 Negocios locales duplican su visibilidad

¿Vemos tu caso específico? Solo 2 minutos:
https://desarroyo.tech/generador_automatizaciones.html

¿En qué más puedo ayudarte?

Agente comercial de DesArroyo Tech 🚀`;
}

async function notificarTelegram(phone, mensaje, respuesta) {
    try {
        const texto = `🤖 **RESPUESTA AUTOMÁTICA ENVIADA**

📱 **Cliente:** ${phone}
💬 **Pregunta:** ${mensaje}
🤖 **Respuesta:** ${respuesta.substring(0, 200)}...

⏰ ${new Date().toLocaleString('es-ES')}`;

        const url = `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/sendMessage`;
        
        await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: process.env.TELEGRAM_CHAT_ID,
                text: texto,
                parse_mode: 'Markdown'
            })
        });
    } catch (error) {
        console.error('Error Telegram:', error);
    }
} 