# Configuración del Webhook de Stripe

## Paso 1: Acceder al Dashboard de Stripe
1. Ve a https://dashboard.stripe.com
2. Inicia sesión con tu cuenta
3. Ve a **Developers** > **Webhooks**

## Paso 2: Crear el Webhook
1. Haz clic en **"Add endpoint"**
2. URL del endpoint: `https://arroyo805.app.n8n.cloud/webhook/webhook-pago-confirmado`
3. Selecciona los eventos:
   - `checkout.session.completed`
4. Haz clic en **"Add endpoint"**

## Paso 3: Configurar los Metadatos en el Flujo 1
En el flujo 1 (`1_0_desarroyo_form.json`), en el nodo "8 HTTP Request" (crear sesión de Stripe), asegúrate de que los metadatos incluyan:

```json
{
  "metadata": {
    "original_html": "{{$node['3. AI Agent (Genera Web v1)'].json.output}}",
    "client_email": "{{$node['2. Generar Prompt'].json.email}}",
    "client_name": "{{$node['2. Generar Prompt'].json.nombre}}"
  }
}
```

## Paso 4: Verificar la Configuración
1. El webhook debe estar activo en Stripe
2. El flujo 2 debe estar activo en n8n
3. Los metadatos deben pasar correctamente

## Flujo Completo:
1. Cliente paga → Stripe envía webhook → Flujo 2 se activa
2. Flujo 2 procesa los datos y envía email de entrega v1
3. Cliente puede solicitar mejora desde el email
4. Mejora se procesa y se envía versión final 