# 🚀 Guía de Acceso al CRM - DesArroyo.tech

## 📋 Instrucciones para Acceder al CRM

### ✅ Paso 1: Iniciar el Servidor

```bash
# Asegúrate de estar en el directorio del proyecto
cd desarroyo-form

# Instalar dependencias si es necesario
npm install

# Iniciar el servidor
npm start
```

### ✅ Paso 2: Acceder al Login

1. **Abre tu navegador web**
2. **Ve a la URL**: `http://localhost:3000/login.html`
3. **Usa las credenciales**:
   - **Usuario**: `admin`
   - **Contraseña**: `admin123`

### ✅ Paso 3: Acceso al Dashboard

Una vez logueado, serás redirigido automáticamente a:
- **Dashboard Principal**: `http://localhost:3000/dashboard`

## 🔧 Solución de Problemas

### ❌ Error: "Usuario no encontrado"

**Solución**: Ejecuta el script de reset de contraseña:

```bash
node scripts/reset-admin-password.js
```

### ❌ Error: "Token inválido"

**Solución**: Borra el localStorage del navegador:

```javascript
// En la consola del navegador
localStorage.clear();
```

### ❌ Error: "Base de datos no encontrada"

**Solución**: El script de reset creará la base de datos automáticamente:

```bash
node scripts/reset-admin-password.js
```

### ❌ Servidor no inicia

**Solución**: Verifica que el puerto esté libre:

```bash
# Matar procesos en puerto 3000
lsof -ti:3000 | xargs kill -9

# Reiniciar servidor
npm start
```

## 🔐 Cambiar Credenciales

### Método 1: Editar config.js

```javascript
// En el archivo config.js
const config = {
    admin: {
        username: 'tu_usuario',
        password: 'tu_contraseña',
        email: 'tu_email@ejemplo.com'
    },
    // ... resto de configuración
};
```

### Método 2: Variables de Entorno

```bash
# Crear archivo .env
ADMIN_USERNAME=tu_usuario
ADMIN_PASSWORD=tu_contraseña
ADMIN_EMAIL=tu_email@ejemplo.com
```

### Método 3: Script Personalizado

```javascript
// Modificar scripts/reset-admin-password.js
const DEFAULT_USERNAME = 'nuevo_usuario';
const DEFAULT_PASSWORD = 'nueva_contraseña';
const DEFAULT_EMAIL = 'nuevo_email@ejemplo.com';
```

## 📱 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Login** | `http://localhost:3000/login.html` | Página de inicio de sesión |
| **Dashboard** | `http://localhost:3000/dashboard` | Panel principal de administración |
| **Mini-CRM** | `http://localhost:3000/client-crm.html?client_id=X` | Panel para clientes |
| **API Docs** | `http://localhost:3000/api/` | Documentación de APIs |

## 🌐 Despliegue en Producción

### Para GitHub Pages o Hosting:

1. **Cambiar credenciales**:
   ```javascript
   // config.js
   admin: {
       username: 'admin_seguro',
       password: 'contraseña_muy_segura_123',
       email: 'admin@desarroyo.tech'
   }
   ```

2. **Configurar variables de entorno**:
   ```bash
   JWT_SECRET=tu_secret_muy_seguro
   SESSION_SECRET=otro_secret_seguro
   ```

3. **Subir a GitHub**:
   ```bash
   git add .
   git commit -m "Configuración CRM lista"
   git push origin main
   ```

## 🎯 Funcionalidades Disponibles

### 📊 Dashboard Principal
- ✅ Estadísticas generales
- ✅ Gestión de clientes
- ✅ Gestión de proyectos
- ✅ Automatizaciones
- ✅ Sistema de videos
- ✅ Analíticas

### 👥 Gestión de Clientes
- ✅ Crear/editar/eliminar clientes
- ✅ Asignar proyectos
- ✅ Generar mini-CRM personalizado
- ✅ Configurar automatizaciones

### 🎬 Sistema de Videos
- ✅ Subir clips de video
- ✅ Crear plantillas
- ✅ Generar videos automáticamente
- ✅ Subtítulos con IA
- ✅ Publicación en redes sociales

### 🤖 Automatizaciones
- ✅ Flujos de n8n
- ✅ Webhooks
- ✅ Notificaciones
- ✅ Integraciones con APIs

## 📞 Soporte

Si tienes problemas, contacta:
- **Email**: alberto@desarroyo.tech
- **WhatsApp**: +34 600 000 000
- **Telegram**: @desarroyotech

## 🔄 Actualizaciones

Para mantener el sistema actualizado:

```bash
# Obtener últimos cambios
git pull origin main

# Reinstalar dependencias
npm install

# Resetear admin si es necesario
node scripts/reset-admin-password.js

# Reiniciar servidor
npm start
```

---

**🎉 ¡Disfruta de tu CRM completo!**

> Desarrollado con ❤️ por Alberto Arroyo - DesArroyo.tech 