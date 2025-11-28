# 🚀 Sistema de Procesamiento de Encuestas con GitHub Actions

## 📋 ¿Cómo funciona?

1. **Usuario rellena el formulario** → El formulario activa directamente el workflow de GitHub Actions
2. **GitHub Actions se ejecuta** → Genera HTML, guarda en Supabase, envía a Telegram
3. **Usuario recibe confirmación** → La web está lista

## 🔧 Configuración Requerida

### 1. Variables de Entorno en GitHub Secrets

Ya las tienes configuradas:
- ✅ `SUPABASE_URL`
- ✅ `SUPABASE_ANON_KEY`
- ✅ `SUPABASE_SERVICE_ROLE_KEY`
- ✅ `TELEGRAM_BOT_TOKEN`
- ✅ `TELEGRAM_CHAT_ID`

### 2. Token de GitHub para activar workflows desde el frontend

**⚠️ IMPORTANTE:** Para que el formulario active el workflow directamente, necesitas un token de GitHub.

**Opción A: Token con permisos limitados (Recomendado para desarrollo)**

1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre: `workflow-activator-frontend`
4. Selecciona el scope: `repo` (permiso completo)
5. Genera el token y **cópialo**

6. **Configurar el token en el formulario:**
   - Edita `index_conectado_n8n.html`
   - Busca la línea: `const GITHUB_TOKEN = window.GITHUB_TOKEN || prompt(...);`
   - Cámbiala por: `const GITHUB_TOKEN = 'tu_token_aqui';`
   - **⚠️ ADVERTENCIA:** Esto expone el token en el frontend. Solo para desarrollo o con permisos muy limitados.

**Opción B: GitHub App (Recomendado para producción)**

Para producción, considera usar un GitHub App con permisos limitados en lugar de un token personal.

### 3. Actualizar el Formulario

El formulario ya está configurado para activar el workflow directamente. Solo necesitas:

1. Añadir el token de GitHub en `index_conectado_n8n.html` (línea ~1218)
2. El formulario llamará directamente a la GitHub API para activar el workflow

## 🎯 Flujo Completo

```
Usuario → Formulario HTML
    ↓
GitHub API (repository_dispatch) → Activa workflow "procesar-encuesta"
    ↓
GitHub Actions → Ejecuta procesar-encuesta.js
    ↓
Genera HTML → Guarda en Supabase → Envía a Telegram
    ↓
✅ ¡Listo!
```

## 📝 Archivos

1. **`scripts/procesar-encuesta.js`** - Script que hace todo el trabajo
2. **`.github/workflows/procesar-encuesta.yml`** - Workflow de GitHub Actions
3. **`index_conectado_n8n.html`** - Formulario que activa el workflow directamente

## ✅ Verificación

1. Configura el token de GitHub en el formulario
2. Rellena el formulario y envía
3. Ve a GitHub → Actions → Deberías ver el workflow ejecutándose
4. Revisa Telegram → Deberías recibir el HTML generado

## 🔍 Troubleshooting

### El workflow no se activa
- Verifica que el token tenga permisos `repo`
- Verifica que el token esté correctamente configurado en el formulario
- Revisa la consola del navegador para ver errores

### Error 401 (Unauthorized)
- El token no tiene permisos suficientes
- El token ha expirado
- Verifica que el token esté correctamente configurado

### Error en Supabase
- Verifica que las variables estén en GitHub Secrets
- Verifica que el schema de Supabase esté creado

### No llega a Telegram
- Verifica `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en GitHub Secrets
- Verifica que el bot tenga permisos para enviar archivos

## 💡 Notas

- **Seguridad:** Exponer un token en el frontend no es ideal. Para producción, considera usar un GitHub App o un servicio intermedio.
- Los HTMLs generados se guardan en `webs_generadas/` y también se suben como artifacts en GitHub Actions
- El workflow se ejecuta en GitHub Actions, no requiere servidor adicional
