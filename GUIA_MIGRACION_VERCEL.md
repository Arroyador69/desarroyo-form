# 🚀 Guía Completa: Migración a Vercel

## 📚 Índice
1. [¿Qué es Vercel?](#qué-es-vercel)
2. [Arquitectura de Vercel](#arquitectura-de-vercel)
3. [Paso a Paso: Migración](#paso-a-paso-migración)
4. [Configuración de Variables](#configuración-de-variables)
5. [Configuración de Dominio](#configuración-de-dominio)
6. [Estructura de Archivos](#estructura-de-archivos)
7. [API Routes (Serverless Functions)](#api-routes-serverless-functions)
8. [Deploy y Testing](#deploy-y-testing)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 ¿Qué es Vercel?

**Vercel** es una plataforma de hosting/serverless que:
- ✅ Despliega automáticamente desde GitHub
- ✅ Proporciona funciones serverless (API routes)
- ✅ CDN global (rápido en todo el mundo)
- ✅ HTTPS automático
- ✅ Plan gratuito generoso

### **Conceptos Clave:**
- **Serverless Functions**: Funciones que se ejecutan solo cuando se llaman
- **API Routes**: Endpoints que funcionan como servidor backend
- **Edge Network**: CDN global para servir contenido rápido

---

## 🏗️ Arquitectura de Vercel

### **Estructura de Proyecto:**
```
tu-proyecto/
├── api/              # Serverless Functions (API routes)
│   ├── encuesta.js   # POST /api/encuesta
│   └── webhook.js    # POST /api/webhook
├── public/           # Archivos estáticos (opcional)
├── pages/            # Si usas Next.js (opcional)
├── server.js         # Servidor Express (si usas vercel.json)
├── vercel.json       # Configuración de Vercel
└── package.json      # Dependencias
```

### **Cómo Funciona:**
1. **Frontend** (HTML/JS) → Hace request a `/api/encuesta`
2. **Vercel** → Detecta que es una API route
3. **Serverless Function** → Se ejecuta (`api/encuesta.js`)
4. **Function** → Procesa la request y responde
5. **Frontend** → Recibe la respuesta

---

## 📋 Paso a Paso: Migración

### **PASO 1: Preparar el Proyecto**

#### 1.1. Verificar estructura
```bash
# Tu proyecto debe tener:
- package.json (con dependencias)
- vercel.json (configuración)
- api/ (carpeta para API routes)
```

#### 1.2. Instalar Vercel CLI (opcional pero útil)
```bash
npm install -g vercel
```

#### 1.3. Login en Vercel
```bash
vercel login
```

---

### **PASO 2: Crear API Route**

#### 2.1. Crear archivo API route
Crea `api/encuesta.js`:

```javascript
// api/encuesta.js
const axios = require('axios');

export default async function handler(req, res) {
  // Solo permitir POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const data = req.body;
    
    // Obtener token de variables de entorno (SEGURO)
    const GH_TOKEN = process.env.GH_TOKEN;
    const GITHUB_OWNER = process.env.GITHUB_OWNER || 'Arroyador69';
    const GITHUB_REPO = process.env.GITHUB_REPO || 'desarroyo-form';

    if (!GH_TOKEN) {
      return res.status(500).json({ 
        error: 'GH_TOKEN no configurado en variables de entorno' 
      });
    }

    // Activar workflow de GitHub Actions
    const response = await axios.post(
      `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/dispatches`,
      {
        event_type: 'encuesta-recibida',
        client_payload: {
          encuesta_data: JSON.stringify(data),
          timestamp: new Date().toISOString()
        }
      },
      {
        headers: {
          'Authorization': `token ${GH_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        }
      }
    );

    // Responder al frontend
    res.status(200).json({
      ok: true,
      message: 'Encuesta recibida. Estamos generando tu web HTML.',
      workflow_triggered: true
    });

  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    res.status(500).json({
      ok: false,
      error: error.response?.data?.message || 'Error procesando la encuesta'
    });
  }
}
```

#### 2.2. Alternativa: Usar Express (si ya tienes server.js)
Si ya tienes `server.js` con Express, puedes mantenerlo y usar `vercel.json`:

```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/server.js"
    },
    {
      "src": "/(.*)",
      "dest": "/server.js"
    }
  ]
}
```

---

### **PASO 3: Actualizar Frontend**

#### 3.1. Cambiar el formulario
En `index_conectado_n8n.html`, cambia:

```javascript
// ANTES (hardcodeado):
const GH_TOKEN = 'TU_TOKEN_AQUI';
const response = await fetch(`https://api.github.com/repos/...`, {
  headers: {
    'Authorization': `token ${GH_TOKEN}`, // ❌ Token expuesto
  }
});

// DESPUÉS (usando API de Vercel):
const response = await fetch('/api/encuesta', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(data)
});
// ✅ Token seguro en variables de entorno
```

---

### **PASO 4: Configurar Variables de Entorno**

#### 4.1. En Vercel Dashboard
1. Ve a: https://vercel.com/dashboard
2. Selecciona tu proyecto
3. Settings → Environment Variables
4. Añade:

```env
# GitHub
GH_TOKEN=ghp_tu_token_aqui
GITHUB_OWNER=Arroyador69
GITHUB_REPO=desarroyo-form

# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=tu_anon_key
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key

# Telegram
TELEGRAM_BOT_TOKEN=tu_bot_token
TELEGRAM_CHAT_ID=tu_chat_id

# Otros
PUBLIC_BASE_URL=https://desarroyo.tech
```

#### 4.2. Para cada entorno (opcional)
- **Production**: Variables para producción
- **Preview**: Variables para preview deployments
- **Development**: Variables para desarrollo local

#### 4.3. Variables sensibles
- ✅ **NUNCA** las subas a GitHub
- ✅ **SIEMPRE** úsalas desde Vercel Dashboard
- ✅ **ROTA** los tokens periódicamente

---

### **PASO 5: Configurar Dominio**

#### 5.1. Añadir dominio en Vercel
1. Ve a: Settings → Domains
2. Click en "Add Domain"
3. Escribe: `desarroyo.tech`
4. Sigue las instrucciones

#### 5.2. Configurar DNS
Vercel te dará registros DNS. Configúralos en tu proveedor de dominio:

```
Tipo: CNAME
Nombre: @ (o www)
Valor: cname.vercel-dns.com
```

O si usas A record:
```
Tipo: A
Nombre: @
Valor: 76.76.21.21 (IP de Vercel)
```

#### 5.3. Verificar SSL
- Vercel configura SSL automáticamente
- Espera 5-10 minutos
- Verifica en: https://desarroyo.tech

---

### **PASO 6: Deploy**

#### 6.1. Deploy automático desde GitHub
1. Conecta tu repo de GitHub a Vercel
2. Cada `git push` → Deploy automático
3. Vercel detecta cambios y despliega

#### 6.2. Deploy manual con CLI
```bash
# Desde tu proyecto
vercel

# Para producción
vercel --prod
```

#### 6.3. Verificar deploy
1. Ve a: Vercel Dashboard → Deployments
2. Verifica que el último deployment sea exitoso
3. Revisa los logs si hay errores

---

## 📁 Estructura de Archivos

### **Opción A: API Routes (Recomendado para funciones simples)**
```
proyecto/
├── api/
│   ├── encuesta.js      # POST /api/encuesta
│   └── webhook.js       # POST /api/webhook
├── index.html           # Frontend
└── vercel.json          # Config (opcional)
```

### **Opción B: Express Server (Si ya tienes server.js)**
```
proyecto/
├── server.js            # Servidor Express completo
├── api/                 # API routes adicionales (opcional)
├── index.html           # Frontend
└── vercel.json          # Config con @vercel/node
```

---

## 🔧 API Routes (Serverless Functions)

### **Estructura Básica:**
```javascript
// api/encuesta.js
export default async function handler(req, res) {
  // req.method: GET, POST, PUT, DELETE, etc.
  // req.body: Datos del body (si es POST)
  // req.query: Query parameters (?id=123)
  // req.headers: Headers de la request
  
  // Procesar request
  const data = req.body;
  
  // Hacer algo (llamar API, guardar en DB, etc.)
  const result = await hacerAlgo(data);
  
  // Responder
  res.status(200).json({ ok: true, data: result });
}
```

### **Ejemplo Completo:**
```javascript
// api/encuesta.js
const axios = require('axios');

export default async function handler(req, res) {
  // CORS headers (si necesitas)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Manejar OPTIONS (preflight)
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Solo POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Validar datos
    if (!req.body || !req.body.nombre_proyecto) {
      return res.status(400).json({ error: 'Datos incompletos' });
    }

    // Obtener variables de entorno
    const GH_TOKEN = process.env.GH_TOKEN;
    if (!GH_TOKEN) {
      return res.status(500).json({ error: 'Token no configurado' });
    }

    // Procesar
    const result = await procesarEncuesta(req.body, GH_TOKEN);

    // Responder
    res.status(200).json({
      ok: true,
      message: 'Encuesta procesada correctamente',
      data: result
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      ok: false,
      error: error.message || 'Error interno'
    });
  }
}
```

---

## 🚀 Deploy y Testing

### **1. Deploy Automático**
```bash
# Hacer cambios
git add .
git commit -m "feat: migrar a Vercel"
git push origin main

# Vercel detecta automáticamente y despliega
```

### **2. Verificar Deployment**
1. Ve a: Vercel Dashboard → Deployments
2. Verifica que el status sea "Ready"
3. Revisa los logs si hay errores

### **3. Testing Local (con Vercel CLI)**
```bash
# Instalar Vercel CLI
npm install -g vercel

# Ejecutar localmente
vercel dev

# Esto simula el entorno de Vercel localmente
# Accede a: http://localhost:3000
```

### **4. Testing en Producción**
```bash
# Probar endpoint
curl -X POST https://desarroyo.tech/api/encuesta \
  -H "Content-Type: application/json" \
  -d '{"nombre_proyecto": "Test"}'

# O desde el navegador
# Abre: https://desarroyo.tech
# Rellena el formulario y envía
```

---

## 🔍 Troubleshooting

### **Error: "Function not found"**
- ✅ Verifica que el archivo esté en `api/encuesta.js`
- ✅ Verifica que exporte `export default async function handler`

### **Error: "GH_TOKEN is not defined"**
- ✅ Ve a Vercel Dashboard → Settings → Environment Variables
- ✅ Añade `GH_TOKEN` con tu token
- ✅ Haz redeploy

### **Error: "CORS"**
- ✅ Añade headers CORS en la función:
```javascript
res.setHeader('Access-Control-Allow-Origin', '*');
```

### **Error: "Cold start" (lento primera vez)**
- ⚠️ Normal en serverless (1-2 segundos)
- ✅ Siguientes requests son rápidas
- ✅ Puedes usar "warm-up" functions

### **Error: "Timeout"**
- ⚠️ Plan gratuito: 10 segundos máximo
- ✅ Plan Pro: 60 segundos
- ✅ Si necesitas más tiempo, usa background jobs

---

## 📊 Comparación: Antes vs Después

### **ANTES (Frontend directo):**
```javascript
// ❌ Token expuesto
const GH_TOKEN = 'ghp_token_aqui';
fetch('https://api.github.com/...', {
  headers: { 'Authorization': `token ${GH_TOKEN}` }
});
```

### **DESPUÉS (Vercel API):**
```javascript
// ✅ Token seguro en variables de entorno
fetch('/api/encuesta', {
  method: 'POST',
  body: JSON.stringify(data)
});
```

---

## 🎯 Resumen de Pasos

1. ✅ **Crear API route** (`api/encuesta.js`)
2. ✅ **Actualizar frontend** (usar `/api/encuesta`)
3. ✅ **Configurar variables** en Vercel Dashboard
4. ✅ **Configurar dominio** en Vercel
5. ✅ **Deploy** (automático desde GitHub)
6. ✅ **Testing** (verificar que funciona)

---

## 💡 Tips y Mejores Prácticas

1. **Variables de Entorno:**
   - ✅ NUNCA hardcodees tokens
   - ✅ USA variables de entorno siempre
   - ✅ ROTA tokens periódicamente

2. **Logs:**
   - ✅ Usa `console.log()` para debugging
   - ✅ Ve logs en Vercel Dashboard → Functions → Logs

3. **Errores:**
   - ✅ Siempre maneja errores con try/catch
   - ✅ Responde con códigos HTTP apropiados
   - ✅ Incluye mensajes de error útiles

4. **Performance:**
   - ✅ Cachea resultados cuando sea posible
   - ✅ Usa conexiones persistentes (axios, etc.)
   - ✅ Optimiza el código (menos dependencias = más rápido)

5. **Seguridad:**
   - ✅ Valida todos los inputs
   - ✅ Usa HTTPS siempre (automático en Vercel)
   - ✅ Limita rate limiting si es necesario

---

## 📚 Recursos Adicionales

- **Documentación Vercel**: https://vercel.com/docs
- **API Routes**: https://vercel.com/docs/concepts/functions/serverless-functions
- **Variables de Entorno**: https://vercel.com/docs/concepts/projects/environment-variables
- **Dominios**: https://vercel.com/docs/concepts/projects/domains

---

**¿Tienes dudas sobre algún paso? ¡Pregunta!** 🚀

