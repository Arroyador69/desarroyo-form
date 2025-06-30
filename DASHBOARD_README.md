# 🚀 Dashboard CRM - DesArroyo.Tech

## 📋 Descripción

Sistema de gestión CRM completo para DesArroyo.Tech que incluye:

- **Dashboard Principal**: Panel de administración para gestionar todos los clientes y proyectos
- **Mini-CRM para Clientes**: Panel personalizado que cada cliente puede usar en su web
- **Base de Datos Centralizada**: SQLite para almacenar toda la información
- **Autenticación Segura**: JWT para proteger el acceso
- **API REST**: Endpoints para conectar con n8n y otros servicios

## 🏗️ Arquitectura

```
desarroyo.tech/
├── /dashboard          # Panel principal (admin)
├── /login.html         # Página de login
├── /client-crm.html    # Plantilla mini-CRM para clientes
└── /api/dashboard/*    # APIs del dashboard
```

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias

```bash
npm install
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Configuración del servidor
PORT=3000

# API Keys
DEEPSEEK_API_KEY=tu_api_key_de_deepseek
STRIPE_SECRET_KEY=tu_stripe_secret_key

# Configuración del Dashboard
JWT_SECRET=tu_jwt_secret_super_seguro
ADMIN_PASSWORD=admin123
```

### 3. Iniciar el Servidor

```bash
npm start
```

El servidor se iniciará en `http://localhost:3000`

## 🔐 Acceso al Dashboard

### Credenciales por Defecto

- **Usuario**: `admin`
- **Contraseña**: `admin123` (o la que configures en ADMIN_PASSWORD)

### URLs de Acceso

- **Dashboard Principal**: `http://localhost:3000/dashboard`
- **Login**: `http://localhost:3000/login.html`

## 📊 Funcionalidades del Dashboard Principal

### 1. Visión General
- Estadísticas de clientes, proyectos y automatizaciones
- Actividad reciente
- Ingresos mensuales
- Métricas clave

### 2. Gestión de Clientes
- Lista completa de clientes
- Crear, editar y eliminar clientes
- Filtros por estado y búsqueda
- Información detallada de cada cliente

### 3. Gestión de Proyectos
- Vista de todos los proyectos
- Progreso de cada proyecto
- Asignación de clientes
- Estados y fechas

### 4. Automatizaciones
- Lista de automatizaciones activas
- Control de activación/desactivación
- Estadísticas de ejecución
- Configuración de flujos

### 5. Analíticas
- Gráficos de ingresos
- Métricas de clientes
- Reportes de actividad

### 6. Configuración
- Configuración general del sistema
- Gestión de usuarios
- Configuración de integraciones

## 👥 Mini-CRM para Clientes

### Características

- **Panel Personalizado**: Cada cliente tiene su propio espacio
- **Gestión de Leads**: Captura y gestión de contactos
- **Automatizaciones**: Control de flujos automáticos
- **Soporte**: Acceso directo al soporte técnico
- **Configuración**: Personalización del panel

### Integración en Webs de Clientes

Para integrar el mini-CRM en la web de un cliente:

1. **Subdominio**: `cliente.desarroyo.tech/admin`
2. **Subdirectorio**: `micliente.com/admin`
3. **Iframe**: Integración embebida en la web del cliente

### Ejemplo de Integración

```html
<!-- En la web del cliente -->
<iframe src="https://desarroyo.tech/client-crm.html?client_id=123" 
        width="100%" 
        height="800px" 
        frameborder="0">
</iframe>
```

## 🔌 APIs Disponibles

### Autenticación
- `POST /api/dashboard/login` - Login de administrador

### Dashboard
- `GET /api/dashboard/overview` - Datos generales
- `GET /api/dashboard/clients` - Lista de clientes
- `POST /api/dashboard/clients` - Crear cliente
- `PUT /api/dashboard/clients/:id` - Actualizar cliente
- `DELETE /api/dashboard/clients/:id` - Eliminar cliente

### Proyectos
- `GET /api/dashboard/projects` - Lista de proyectos
- `POST /api/dashboard/projects` - Crear proyecto

### Automatizaciones
- `GET /api/dashboard/automations` - Lista de automatizaciones

### Actividad
- `GET /api/dashboard/activity` - Log de actividad

## 🗄️ Base de Datos

### Tablas Principales

#### users
- Administradores del sistema
- Autenticación y permisos

#### clients
- Información de clientes
- Proyectos asociados
- Estados y fechas

#### projects
- Detalles de proyectos
- Progreso y presupuestos
- Relación con clientes

#### automations
- Configuración de automatizaciones
- Estados y ejecuciones
- Relación con clientes

#### activity_log
- Registro de actividad
- Auditoría del sistema

## 🔗 Integración con n8n

### Webhooks Disponibles

```javascript
// Ejemplo de webhook para nuevo cliente
POST /api/webhooks/new-client
{
  "client_id": 123,
  "name": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "project": "Web de Restaurante"
}
```

### Automatizaciones Sugeridas

1. **Nuevo Cliente**:
   - Envío de email de bienvenida
   - Creación de acceso al mini-CRM
   - Notificación por Telegram
   - Creación de proyecto en n8n

2. **Lead Capturado**:
   - Email de confirmación
   - Notificación al cliente
   - Actualización de estadísticas

3. **Proyecto Completado**:
   - Email de entrega
   - Generación de factura
   - Solicitud de feedback

## 🛠️ Desarrollo

### Estructura de Archivos

```
├── server.js              # Servidor principal
├── dashboard.html         # Dashboard admin
├── login.html            # Página de login
├── client-crm.html       # Mini-CRM para clientes
├── dashboard.db          # Base de datos SQLite
├── package.json          # Dependencias
└── .env                  # Variables de entorno
```

### Comandos de Desarrollo

```bash
# Modo desarrollo con auto-reload
npm run dev

# Iniciar servidor de producción
npm start

# Ver logs
npm run logs
```

## 🔒 Seguridad

### Autenticación
- JWT tokens con expiración de 24h
- Contraseñas encriptadas con bcrypt
- Middleware de autenticación en todas las rutas protegidas

### Validación
- Validación de entrada en todos los endpoints
- Sanitización de datos
- Protección contra SQL injection

### CORS
- Configuración de CORS para APIs
- Dominios permitidos configurados

## 📈 Escalabilidad

### Optimizaciones Futuras

1. **Base de Datos**:
   - Migrar a PostgreSQL para mayor escalabilidad
   - Implementar índices optimizados
   - Backup automático

2. **Caché**:
   - Redis para caché de sesiones
   - Caché de consultas frecuentes

3. **Microservicios**:
   - Separar APIs por dominio
   - Load balancer
   - Docker containers

4. **Monitoreo**:
   - Logs centralizados
   - Métricas de rendimiento
   - Alertas automáticas

## 🆘 Soporte

### Contacto
- **Email**: alberto@desarroyo.tech
- **WhatsApp**: +34 600 000 000
- **Telegram**: @desarroyotech

### Documentación Adicional
- [API Documentation](./API_DOCS.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

## 📝 Changelog

### v1.0.0 (2024-01-XX)
- ✅ Dashboard principal funcional
- ✅ Sistema de autenticación
- ✅ Gestión de clientes y proyectos
- ✅ Mini-CRM para clientes
- ✅ Base de datos SQLite
- ✅ APIs REST completas

### Próximas Versiones
- 🔄 Integración con n8n
- 🔄 Sistema de facturación
- 🔄 Reportes avanzados
- 🔄 App móvil
- 🔄 Multi-idioma

---

**Desarrollado con ❤️ por Alberto Arroyo - DesArroyo.Tech** 