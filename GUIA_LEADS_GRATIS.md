# 🚀 SISTEMA DE LEADS GRATUITO - DESARROYO TECH

## ✅ **¡AHORRO TOTAL: $588/año!**

Hemos convertido el sistema de **$49/mes** en **100% GRATUITO** eliminando ScrapingBee y usando nuestro propio scraper.

---

## 📦 **INSTALACIÓN RÁPIDA**

```bash
# Ejecutar script de instalación
bash setup_leads_gratis.sh
```

---

## 🔧 **CONFIGURACIÓN MANUAL**

### 1. **Instalar Dependencias Python**
```bash
pip3 install requests beautifulsoup4 lxml selenium
```

### 2. **Configurar Variables de Entorno**
Edita el archivo `.env_leads_config`:

```bash
# APIs necesarias (las únicas que cuestan algo)
OPENAI_API_KEY=sk-tu_key_aqui          # ~$20/mes
TWILIO_ACCOUNT_SID=tu_sid_aqui         # ~$15/mes  
TWILIO_AUTH_TOKEN=tu_token_aqui
TWILIO_WHATSAPP_NUMBER=+1234567890
TELEGRAM_BOT_TOKEN=tu_bot_token_aqui   # GRATIS
TELEGRAM_CHAT_ID=tu_chat_id_aqui       # GRATIS

# Tu configuración
WEBSITE_URL=https://desarroyo.tech
BUSINESS_NAME=DesArroyo Tech
YOUR_NAME=Alberto
```

### 3. **Personalizar Búsquedas**
En el flujo de n8n, modifica los comandos:

```javascript
// Para Madrid + Restaurantes
python3 scripts/scraper_gratis.py Madrid restaurantes

// Para Barcelona + Peluquerías  
python3 scripts/scraper_gratis.py Barcelona peluquerias

// Para Valencia + Dentistas
python3 scripts/scraper_gratis.py Valencia dentistas
```

---

## 🎯 **CÓMO FUNCIONA EL SCRAPER GRATUITO**

### **Fuentes de Datos (GRATIS):**
1. **Google Search** - Busca "restaurantes Madrid sin página web"
2. **Páginas Amarillas** - Extrae listados de empresas
3. **Directorios locales** - APIs gratuitas de empresas

### **Características:**
- ✅ **Rotación de User-Agents** para evitar bloqueos
- ✅ **Delays aleatorios** entre peticiones
- ✅ **Reintentos automáticos** si falla
- ✅ **Filtrado inteligente** por sectores
- ✅ **Eliminación de duplicados**
- ✅ **Score automático** de leads

### **Sectores Configurados:**
- Restaurantes, cafés, bares, pizzerías
- Peluquerías, barberías, estéticas
- Dentistas, médicos, clínicas
- Abogados, notarios, asesores
- Hoteles, hostales, alojamientos
- Gimnasios, fitness, deportes
- Tiendas, comercios, negocios

---

## 🚀 **FLUJO COMPLETO**

### **Cada 6 horas automáticamente:**

1. **🔍 BÚSQUEDA** - Scraper encuentra 20-50 leads por ciudad
2. **🎯 FILTRADO** - AI filtra por sectores de alto valor
3. **📱 CONTACTO** - Envía WhatsApp personalizado con IA
4. **🤖 SEGUIMIENTO** - Responde automáticamente
5. **📋 ENCUESTA** - Envía formulario a interesados
6. **📊 REPORTE** - Notificaciones por Telegram

---

## 💰 **COMPARACIÓN DE COSTOS**

| Servicio | Antes | Ahora | Ahorro |
|----------|-------|-------|--------|
| ScrapingBee | $49/mes | **GRATIS** | $588/año |
| OpenAI | $20/mes | $20/mes | - |
| Twilio | $15/mes | $15/mes | - |
| Telegram | GRATIS | GRATIS | - |
| **TOTAL** | **$84/mes** | **$35/mes** | **$588/año** |

---

## 🛠 **PERSONALIZACIÓN AVANZADA**

### **Añadir Nuevas Ciudades:**
```python
# En el flujo n8n, cambia:
python3 scripts/scraper_gratis.py Sevilla restaurantes
python3 scripts/scraper_gratis.py Málaga peluquerias
```

### **Añadir Nuevos Sectores:**
```python
# Edita scripts/scraper_gratis.py línea 95:
sector_map = {
    'farmacia': 'farmacias',
    'veterinario': 'veterinarios',
    'inmobiliaria': 'inmobiliarias'
}
```

### **Modificar Frecuencia:**
En n8n, cambia el trigger de "cada 6 horas" a:
- Cada 4 horas (más agresivo)
- Cada 12 horas (más conservador)
- Solo días laborales

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Error: "No se encuentra python3"**
```bash
# Mac/Linux
brew install python3
# o
sudo apt install python3

# Windows
# Descargar de python.org
```

### **Error: "Módulo no encontrado"**
```bash
pip3 install requests beautifulsoup4 lxml
```

### **Error: "Permiso denegado"**
```bash
chmod +x scripts/scraper_gratis.py
```

### **Pocos resultados en scraping:**
- Las páginas cambian sus selectores CSS
- Añadir más fuentes en `scraper_gratis.py`
- Usar proxies si hay bloqueos

---

## ⚡ **OPTIMIZACIONES**

### **Para Mayor Volumen:**
1. **Múltiples ciudades paralelas** en n8n
2. **Proxies rotativos gratuitos**
3. **Base de datos local** para evitar duplicados
4. **APIs adicionales gratuitas**

### **Para Mayor Precisión:**
1. **Verificación de números** con APIs gratuitas
2. **Validación de direcciones** con Google Maps API
3. **Enriquecimiento social** con LinkedIn/Facebook

---

## 📞 **SOPORTE**

Si tienes problemas:
1. Revisa logs en n8n
2. Prueba manualmente: `python3 scripts/scraper_gratis.py Madrid restaurantes`
3. Verifica permisos de archivos
4. Consulta las variables de entorno

---

## 🎉 **¡YA ESTÁ LISTO!**

Tu sistema ahora genera leads **24/7 completamente gratis** con la misma calidad que antes, pero ahorrando **$588 al año**. 