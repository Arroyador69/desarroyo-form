# 🚀 Sistema de Procesamiento de Encuestas con GitHub Actions

## 📋 ¿Cómo funciona?

1. **Usuario rellena el formulario** → Envía POST a `/api/encuesta`
2. **Webhook activador recibe el POST** → Activa workflow de GitHub Actions
3. **GitHub Actions ejecuta el script** → Genera HTML, guarda en Supabase, envía a Telegram
4. **Usuario recibe confirmación** → La web está lista

## 🔧 Configuración Requerida

### 1. Variables de Entorno en GitHub Secrets

Ya las tienes configuradas:
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_ANON_KEY`
- ✅ `SUPABASE_SERVICE_ROLE_KEY`
- ✅ `TELEGRAM_BOT_TOKEN`
- ✅ `TELEGRAM_CHAT_ID`

### 2. Token de GitHub para activar workflows

Necesitas crear un **Personal Access Token** con permisos para activar workflows:

1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre: `workflow-activator`
4. Selecciona el scope: `repo` (permiso completo)
5. Genera el token y **cópialo** (solo se muestra una vez)

### 3. Configurar el Webhook Activador

Tienes 2 opciones:

#### Opción A: Servidor Simple (Recomendado)

Ejecuta el webhook activador en tu PC o servidor:

```bash
cd desarroyo-form
npm install express axios
```

Crea un archivo `.env` con:
```env
GH_TOKEN=tu_token_de_github_aqui
GITHUB_OWNER=Arroyador69
GITHUB_REPO=desarroyo-form
PORT=3001
```

Ejecuta:
```bash
node scripts/webhook-activador.js
```

**⚠️ IMPORTANTE:** Este servidor debe estar **siempre corriendo** para recibir los POST del formulario.

#### Opción B: Servicio en la Nube (Railway, Render, etc.)

1. Despliega `scripts/webhook-activador.js` en Railway/Render
2. Configura las variables de entorno
3. Obtén la URL pública (ej: `https://tu-webhook.railway.app`)
4. Actualiza el formulario para que apunte a esa URL

### 4. Actualizar el Formulario

En `index_conectado_n8n.html`, cambia la línea 1257:

```javascript
// ANTES:
const response = await fetch('/api/encuesta', {

// DESPUÉS (si usas servidor local):
const response = await fetch('http://localhost:3001/api/encuesta', {

// O (si usas servicio en la nube):
const response = await fetch('https://tu-webhook.railway.app/api/encuesta', {
```

## 🎯 Flujo Completo

```
Usuario → Formulario HTML
    ↓
POST /api/encuesta → Webhook Activador (siempre activo)
    ↓
GitHub API → Activa workflow "procesar-encuesta"
    ↓
GitHub Actions → Ejecuta procesar-encuesta.js
    ↓
Genera HTML → Guarda en Supabase → Envía a Telegram
    ↓
✅ ¡Listo!
```

## 📝 Archivos Creados

1. **`scripts/procesar-encuesta.js`** - Script que hace todo el trabajo
2. **`.github/workflows/procesar-encuesta.yml`** - Workflow de GitHub Actions
3. **`scripts/webhook-activador.js`** - Servidor que recibe POST y activa workflow

## ✅ Verificación

1. Inicia el webhook activador: `node scripts/webhook-activador.js`
2. Rellena el formulario y envía
3. Ve a GitHub → Actions → Deberías ver el workflow ejecutándose
4. Revisa Telegram → Deberías recibir el HTML generado

## 🔍 Troubleshooting

### El workflow no se activa
- Verifica que el `GH_TOKEN` tenga permisos `repo`
- Verifica que el webhook activador esté corriendo
- Revisa los logs del webhook activador

### Error en Supabase
- Verifica que las variables estén en GitHub Secrets
- Verifica que el schema de Supabase esté creado

### No llega a Telegram
- Verifica `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID`
- Verifica que el bot tenga permisos para enviar archivos

## 💡 Notas

- El webhook activador **debe estar siempre activo** (24/7)
- Si se cae, las encuestas no se procesarán
- Considera usar un servicio en la nube (Railway, Render) para mayor estabilidad
- Los HTMLs generados se guardan en `webs_generadas/` y también se suben como artifacts en GitHub Actions

