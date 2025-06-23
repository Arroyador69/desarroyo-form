# 🤖 Aura Bot - Configuración Completa

## 📋 Descripción del Flujo

Aura Bot es un sistema de automatización inteligente que publica contenido en Telegram usando IA de DeepSeek. El flujo incluye **3 triggers diferentes** que se ejecutan automáticamente:

### 🕐 Horarios de Publicación
- **8:00 AM** - Noticias tecnológicas con IA
- **12:00 PM** - Superpoderes de n8n
- **4:00 PM** - Shortcuts iPhone vs Android

## 🚀 Instalación y Configuración

### 1. Importar el Flujo en n8n

1. Abre tu instancia de n8n
2. Ve a "Workflows" → "Import from file"
3. Selecciona el archivo `aura_bot_flujo_completo.json`
4. Haz clic en "Import"

### 2. Configurar Variables de Entorno

En n8n, ve a **Settings** → **Variables** y añade:

```env
# API Key de DeepSeek (obtener en https://platform.deepseek.com/)
DEEPSEEK_API_KEY=tu_api_key_deepseek_aqui

# API Key de NewsAPI (obtener en https://newsapi.org/)
NEWS_API_KEY=tu_api_key_newsapi_aqui

# ID del grupo de Telegram donde publicar
TELEGRAM_GROUP_ID=-1001234567890
```

### 3. Obtener las API Keys

#### DeepSeek API Key:
1. Ve a [https://platform.deepseek.com/](https://platform.deepseek.com/)
2. Crea una cuenta gratuita
3. Ve a "API Keys" en tu dashboard
4. Crea una nueva API key
5. Copia la key

#### NewsAPI Key:
1. Ve a [https://newsapi.org/](https://newsapi.org/)
2. Regístrate gratuitamente
3. Copia tu API key del dashboard

#### Telegram Group ID:
1. Añade tu bot al grupo de Telegram
2. Envía un mensaje al grupo
3. Ve a: `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
4. Busca el `chat.id` del grupo (será un número negativo)

### 4. Configurar Credenciales en n8n

#### DeepSeek:
1. Ve a **Credentials** → **Add Credential**
2. Selecciona "DeepSeek API"
3. Nombre: "DeepSeek account"
4. API Key: tu clave de DeepSeek

#### Telegram:
1. Ve a **Credentials** → **Add Credential**
2. Selecciona "Telegram API"
3. Nombre: "Telegram account"
4. Access Token: tu token del bot de Telegram

## 🔧 Funcionalidades del Flujo

### 📰 Trigger 1: Noticias Tecnológicas (8:00 AM)

**Qué hace:**
- Obtiene las 5 noticias más relevantes de tecnología en español
- Usa IA de DeepSeek para crear un resumen inteligente
- Publica en Telegram con formato atractivo
- Incluye referencias a las fuentes originales

**Ejemplo de publicación:**
```
📰 Las Noticias Tech Más Importantes de Hoy

🤖 OpenAI presenta GPT-5 con capacidades multimodales revolucionarias
💻 Microsoft lanza Windows 12 con IA integrada
📱 Apple anuncia iPhone 16 con pantalla plegable

🔗 Referencias:
1. https://ejemplo1.com
2. https://ejemplo2.com
3. https://ejemplo3.com
```

### ⚡ Trigger 2: Superpoderes de n8n (12:00 PM)

**Qué hace:**
- Selecciona aleatoriamente un "superpoder" de n8n
- Usa IA para explicar por qué es útil
- Incluye tiempo de implementación y dificultad
- Motiva a los usuarios a aprender más

**Ejemplo de publicación:**
```
⚡ Agendar Llamadas Automáticamente

¿Te imaginas que tu calendario se sincronice automáticamente con WhatsApp? 
Con n8n puedes crear este superpoder en solo 5 minutos.

🎯 ¿Por qué es útil?
- Ahorra tiempo manual
- Reduce errores de programación
- Mejora la experiencia del cliente
- Automatiza tareas repetitivas

⏱️ Tiempo: 5 min | 🎯 Dificultad: Fácil

💡 ¿Quieres aprender más sobre automatizaciones? ¡Pregúntame!
```

### 📱 Trigger 3: Shortcuts iPhone vs Android (4:00 PM)

**Qué hace:**
- Compara shortcuts de iPhone y Android
- Usa IA para crear contenido educativo
- Incluye comandos prácticos
- Fomenta la participación

**Ejemplo de publicación:**
```
📱 Automatización Móvil: iPhone vs Android

Descubre cómo ambos sistemas te pueden hacer la vida más fácil con automatizaciones inteligentes.

🍎 iPhone - Agenda Rápida:
Agenda eventos con Siri en segundos
Comando: "Hey Siri, agenda llamada con Juan mañana a las 10"

🤖 Android - Bixby Routines:
Automatiza tu día completo
Comando: Configura rutinas para trabajo, casa y viajes

💡 Tip: Ambos sistemas son potentes, elige el que mejor se adapte a tu flujo de trabajo.

¿Cuál prefieres? ¡Comenta tu experiencia!
```

## 🎛️ Personalización

### Cambiar Horarios
Para modificar los horarios de publicación, edita los nodos "Cron":

1. **Trigger Noticias**: Cambia `hoursInterval: 8` por el intervalo deseado
2. **Trigger Superpoderes**: Cambia `hoursInterval: 12` por el intervalo deseado  
3. **Trigger Shortcuts**: Cambia `hoursInterval: 16` por el intervalo deseado

### Añadir Más Superpoderes
Edita el nodo "6. Procesar Superpoderes" y añade más elementos al array `superpoderes`:

```javascript
{
  titulo: 'Nuevo Superpoder',
  descripcion: 'Descripción del nuevo superpoder',
  dificultad: 'Fácil/Media/Difícil',
  tiempo: 'X min'
}
```

### Cambiar Fuentes de Noticias
Modifica el nodo "4. Obtener Noticias Tech" para cambiar la API o parámetros:

```javascript
// Para noticias en inglés
url: "https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={{$env.NEWS_API_KEY}}&pageSize=5"

// Para más noticias
url: "https://newsapi.org/v2/top-headlines?country=es&category=technology&apiKey={{$env.NEWS_API_KEY}}&pageSize=10"
```

## 🔍 Monitoreo y Logs

El flujo incluye nodos de logging que registran:
- ✅ Cuándo se envía cada publicación
- 📊 Tipo de contenido publicado
- 🕐 Timestamp de la ejecución
- 📝 Mensajes de éxito/error

Puedes ver los logs en:
- **n8n Execution Logs**: En la interfaz de n8n
- **Console**: Si ejecutas n8n desde terminal

## 🚨 Solución de Problemas

### Error: "DeepSeek API Key not found"
- Verifica que la variable `DEEPSEEK_API_KEY` esté configurada
- Asegúrate de que las credenciales de DeepSeek estén correctas

### Error: "Telegram chat not found"
- Verifica que el `TELEGRAM_GROUP_ID` sea correcto
- Asegúrate de que el bot esté añadido al grupo
- Confirma que el bot tenga permisos para enviar mensajes

### Error: "NewsAPI quota exceeded"
- La versión gratuita de NewsAPI tiene límites
- Considera actualizar a un plan de pago
- O cambia a otra API de noticias

### Las publicaciones no se envían
- Verifica que el workflow esté activado
- Revisa los logs de ejecución
- Confirma que los triggers cron estén configurados correctamente

## 🎯 Próximas Mejoras

### Funcionalidades que se pueden añadir:
- 📊 Estadísticas de engagement
- 🎨 Templates personalizables
- 🔄 Integración con más redes sociales
- 📈 Análisis de tendencias
- 🤖 Respuestas automáticas a comentarios
- 📅 Calendario de contenido programado

## 📞 Soporte

Si tienes problemas con la configuración:
- 📧 Email: alberto@desarroyo.tech
- 💬 Telegram: @Arroyador69
- 🌐 Web: [DesArroyo.Tech](https://desarroyo.tech)

---

**"Aura Bot: Tu asistente IA para contenido automático"** 🤖✨ 