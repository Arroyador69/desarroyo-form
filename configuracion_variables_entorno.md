# Configuración de Variables de Entorno - Sistema de Prospección Automatizada

## Variables Requeridas para n8n

### 1. APIs de Scraping
```bash
SCRAPINGBEE_API_KEY=tu_api_key_de_scrapingbee
```

### 2. OpenAI (AI Chatbot)
```bash
OPENAI_API_KEY=tu_api_key_de_openai
```

### 3. Twilio (WhatsApp)
```bash
TWILIO_ACCOUNT_SID=tu_account_sid_de_twilio
TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
TWILIO_WHATSAPP_NUMBER=+1234567890
```

### 4. Telegram (Reportes)
```bash
TELEGRAM_BOT_TOKEN=tu_bot_token_de_telegram
TELEGRAM_CHAT_ID=tu_chat_id_personal
```

### 5. Configuración Web
```bash
WEBSITE_URL=https://tu-dominio.com
```

## Cómo Configurar en n8n

1. **Ir a Settings > Variables**
2. **Agregar cada variable** con su valor correspondiente
3. **Guardar** la configuración

## URLs de Webhook para Integrar

### Webhook para Respuestas de Clientes
```
https://tu-instancia-n8n.com/webhook/respuesta-cliente
```

### Webhook para Encuestas Completadas
```
https://tu-instancia-n8n.com/webhook/encuesta-completada
```

## Configuración de Twilio WhatsApp

1. **Comprar número** en Twilio con capacidad WhatsApp
2. **Configurar webhook** para recibir respuestas
3. **Verificar número** en WhatsApp Business API

## Configuración de Telegram Bot

1. **Crear bot** con @BotFather
2. **Obtener token** del bot
3. **Obtener chat_id** personal
4. **Configurar** en variables de entorno

## Sectores Objetivo Configurados

- Restaurantes y cafés
- Peluquerías y estética
- Dentistas y médicos
- Abogados y asesores
- Tiendas y comercios
- Hoteles y alojamientos
- Gimnasios y deportes
- Autoescuelas y talleres

## Frecuencia de Ejecución

- **Búsqueda de leads**: Cada 6 horas
- **Reportes**: Diarios a las 20:00
- **Seguimiento**: Automático según respuestas

## Métricas que Genera

- Leads encontrados por día
- Tasa de respuesta
- Conversiones a encuestas
- Leads calientes
- Mejores sectores/fuentes
- ROI de la automatización 