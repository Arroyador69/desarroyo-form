# 🔐 Variables de Entorno para Supabase

## 📋 Variables Necesarias

Para conectar tu aplicación Node.js con Supabase, necesitas estas variables de entorno:

### Variables de Supabase

```bash
# URL del proyecto Supabase
SUPABASE_URL=https://xxxxx.supabase.co

# Clave pública (anon key) - Para operaciones del cliente
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Clave de servicio (service_role key) - Para operaciones del servidor
# ⚠️ IMPORTANTE: Esta clave tiene permisos completos, ¡MANTÉNLA SECRETA!
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# (Opcional) Si usas conexión directa a PostgreSQL
SUPABASE_DB_HOST=db.xxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=tu_contraseña_aqui
```

## 🐙 Configurar en GitHub Secrets

### Opción 1: GitHub Secrets (Recomendado para producción)

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** (Configuración)
3. En el menú lateral, haz clic en **Secrets and variables** → **Actions**
4. Haz clic en **New repository secret**
5. Añade cada variable una por una:

| Nombre del Secret | Valor |
|-------------------|-------|
| `SUPABASE_URL` | `https://xxxxx.supabase.co` |
| `SUPABASE_ANON_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

### Opción 2: GitHub Environment Variables (Para diferentes entornos)

Si tienes múltiples entornos (desarrollo, staging, producción):

1. Ve a **Settings** → **Environments**
2. Crea un nuevo environment (ej: `production`)
3. Añade las variables de entorno allí
4. En tu workflow de GitHub Actions, especifica el environment:

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v2
      # ... resto de pasos
```

## 💻 Usar en GitHub Actions Workflow

Ejemplo de `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Deploy
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
          SUPABASE_SERVICE_ROLE_KEY: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          PORT: ${{ secrets.PORT }}
        run: npm start
```

## 🏠 Configurar para Desarrollo Local

Crea un archivo `.env` en la raíz del proyecto `desarroyo-form/`:

```bash
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Telegram (ya existentes)
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui

# Otros
PUBLIC_BASE_URL=http://localhost:3000
PORT=3000
```

**⚠️ IMPORTANTE:**
- Añade `.env` a tu `.gitignore` para que no se suba al repositorio
- Nunca subas las claves a GitHub
- Usa GitHub Secrets para producción

## 📝 Código en server.js

Ejemplo de cómo usar las variables en tu código:

```javascript
// Al inicio del archivo server.js
require('dotenv').config();

// Variables de Supabase
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

// Verificar que las variables estén configuradas
if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    console.error('❌ Error: Variables de Supabase no configuradas');
    console.error('   Asegúrate de tener SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en .env');
}

// Usar con el cliente de Supabase
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY // Usa service_role para operaciones del servidor
);
```

## 🔍 Dónde Encontrar las Credenciales en Supabase

### 1. Project URL y API Keys

1. Ve a tu proyecto en Supabase
2. Haz clic en el icono de **Settings** (⚙️) en el menú lateral
3. Haz clic en **API**
4. Encontrarás:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon public**: Esta es tu `SUPABASE_ANON_KEY`
   - **service_role**: Esta es tu `SUPABASE_SERVICE_ROLE_KEY` ⚠️ (SECRETO)

### 2. Database Password (Solo si usas conexión directa)

1. Ve a **Settings** → **Database**
2. Busca **Database password**
3. Si no la tienes, haz clic en **Reset database password**
4. Copia la contraseña (solo se muestra una vez)

## ✅ Verificar que Funciona

Crea un script de prueba `test-supabase.js`:

```javascript
require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
    process.env.SUPABASE_URL,
    process.env.SUPABASE_SERVICE_ROLE_KEY
);

// Probar conexión
async function testConnection() {
    try {
        const { data, error } = await supabase
            .from('clientes')
            .select('count')
            .limit(1);
        
        if (error) throw error;
        console.log('✅ Conexión a Supabase exitosa!');
    } catch (error) {
        console.error('❌ Error conectando a Supabase:', error.message);
    }
}

testConnection();
```

Ejecuta: `node test-supabase.js`

## 🎯 Resumen de Nombres de Variables

| Variable | Descripción | Dónde encontrarla |
|----------|-------------|-------------------|
| `SUPABASE_URL` | URL del proyecto | Settings → API → Project URL |
| `SUPABASE_ANON_KEY` | Clave pública | Settings → API → anon public |
| `SUPABASE_SERVICE_ROLE_KEY` | Clave de servicio (SECRETO) | Settings → API → service_role |

## 🚨 Seguridad

- ✅ **SÍ**: Usa `SUPABASE_ANON_KEY` en el frontend/cliente
- ✅ **SÍ**: Usa `SUPABASE_SERVICE_ROLE_KEY` solo en el servidor
- ❌ **NO**: Nunca expongas `SUPABASE_SERVICE_ROLE_KEY` en el frontend
- ❌ **NO**: No subas `.env` al repositorio
- ✅ **SÍ**: Usa GitHub Secrets para producción

## 📦 Instalar Cliente de Supabase

Si aún no lo tienes instalado:

```bash
npm install @supabase/supabase-js
```

## 🔄 Actualizar .gitignore

Asegúrate de que tu `.gitignore` incluya:

```
.env
.env.local
.env.production
```

