# 🚀 Desplegar Webhook Activador en la Nube

Este documento explica cómo desplegar el webhook activador en Railway o Render.

## 📋 Opciones de Despliegue

### Opción 1: Railway (Recomendado - Más fácil)

1. **Crear cuenta en Railway:**
   - Ve a: https://railway.app
   - Conecta con GitHub

2. **Crear nuevo proyecto:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Elige el repositorio `desarroyo-form`

3. **Configurar el servicio:**
   - Railway detectará automáticamente el `Procfile`
   - O configura manualmente:
     - **Start Command:** `npm run webhook`
     - **Root Directory:** `/` (raíz del repo)

4. **Configurar variables de entorno:**
   - Ve a Variables → Add Variable
   - Añade:
     - `GH_TOKEN` = (tu token de GitHub)
     - `GITHUB_OWNER` = `Arroyador69`
     - `GITHUB_REPO` = `desarroyo-form`
     - `PORT` = `3001` (Railway lo asigna automáticamente, pero por si acaso)

5. **Obtener la URL:**
   - Railway te dará una URL como: `https://webhook-activador.up.railway.app`
   - Copia esta URL

6. **Actualizar el formulario:**
   - Edita `index_conectado_n8n.html`
   - Cambia la línea con `WEBHOOK_URL`:
     ```javascript
     const WEBHOOK_URL = 'https://tu-url-railway.up.railway.app/api/encuesta';
     ```

---

### Opción 2: Render

1. **Crear cuenta en Render:**
   - Ve a: https://render.com
   - Conecta con GitHub

2. **Crear nuevo Web Service:**
   - Click en "New +" → "Web Service"
   - Conecta el repositorio `desarroyo-form`

3. **Configurar el servicio:**
   - **Name:** `webhook-activador`
   - **Environment:** `Node`
   - **Build Command:** `npm install`
   - **Start Command:** `npm run webhook`
   - **Plan:** Free (o el que prefieras)

4. **Configurar variables de entorno:**
   - En la sección "Environment Variables":
     - `GH_TOKEN` = (tu token de GitHub)
     - `GITHUB_OWNER` = `Arroyador69`
     - `GITHUB_REPO` = `desarroyo-form`
     - `PORT` = `3001`

5. **Desplegar:**
   - Click en "Create Web Service"
   - Render desplegará automáticamente

6. **Obtener la URL:**
   - Render te dará una URL como: `https://webhook-activador.onrender.com`
   - Copia esta URL

7. **Actualizar el formulario:**
   - Edita `index_conectado_n8n.html`
   - Cambia la línea con `WEBHOOK_URL`:
     ```javascript
     const WEBHOOK_URL = 'https://webhook-activador.onrender.com/api/encuesta';
     ```

---

## ✅ Verificación

1. **Probar el health check:**
   - Visita: `https://tu-url.com/health`
   - Deberías ver: `{"status":"ok","service":"webhook-activador"}`

2. **Probar el endpoint:**
   - Puedes usar Postman o curl:
     ```bash
     curl -X POST https://tu-url.com/api/encuesta \
       -H "Content-Type: application/json" \
       -d '{"test": "data"}'
     ```

3. **Probar desde el formulario:**
   - Rellena el formulario y envía
   - Deberías ver el workflow ejecutándose en GitHub Actions

---

## 🔧 Troubleshooting

### El webhook no responde
- Verifica que el servicio esté "Running" en Railway/Render
- Revisa los logs del servicio
- Verifica que las variables de entorno estén configuradas

### Error 401 al activar workflow
- Verifica que `GH_TOKEN` tenga permisos `repo`
- Verifica que el token no haya expirado

### El workflow no se activa
- Revisa los logs del webhook activador
- Verifica que el evento `repository_dispatch` esté configurado en el workflow
- Verifica que el repositorio y owner sean correctos

---

## 📝 Notas Importantes

- **Railway:** El plan gratuito tiene límites, pero es suficiente para empezar
- **Render:** El plan gratuito puede "dormir" después de inactividad, pero se despierta automáticamente
- **Costo:** Ambos tienen planes gratuitos que deberían ser suficientes para empezar
- **Siempre activo:** El webhook debe estar siempre corriendo para recibir los POST del formulario

---

## 🎯 Siguiente Paso

Una vez desplegado, actualiza el formulario con la URL del webhook y ¡listo! 🚀

