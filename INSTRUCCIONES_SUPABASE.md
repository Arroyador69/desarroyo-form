# 📚 Instrucciones para Configurar Supabase

## 🚀 Paso 1: Crear las Tablas

1. Ve a tu proyecto en Supabase
2. Abre el **SQL Editor** (menú lateral izquierdo)
3. Copia y pega el contenido completo del archivo `supabase_schema.sql`
4. Haz clic en **Run** o presiona `Ctrl+Enter`
5. Deberías ver un mensaje de éxito: "Success. No rows returned"

## ✅ Verificar que se crearon las tablas

1. Ve a **Table Editor** en el menú lateral
2. Deberías ver estas tablas:
   - `clientes`
   - `proyectos`
   - `webs_generadas`
   - `versiones_web`
   - `notas_proyecto`
   - `pagos`

## 📊 Estructura de la Base de Datos

### Tabla: `clientes`
Almacena información de contacto de los clientes que llenan la encuesta.

**Campos principales:**
- `id` (UUID) - Identificador único
- `nombre_completo` - Nombre del cliente
- `email` - Email (único)
- `telefono` - Teléfono de contacto
- `fecha_registro` - Cuándo se registró
- `fuente_descubrimiento` - Cómo conoció DesArroyo.Tech

### Tabla: `proyectos`
Cada encuesta enviada se guarda como un proyecto.

**Campos principales:**
- `id` (UUID) - Identificador único
- `cliente_id` - Relación con la tabla `clientes`
- `nombre_proyecto` - Nombre del proyecto/marca
- `sector` - Sector del negocio
- `plan` - Plan seleccionado (rapida, escalable, pro)
- `estilos`, `colores`, `fuentes` - Preferencias (almacenadas como JSONB)
- `menu_estilo`, `plantilla_estilo`, `footer_estilo` - Selecciones de diseño
- `estado` - Estado del proyecto (pendiente, en_desarrollo, completado, etc.)
- `datos_encuesta_completos` - Backup completo de la encuesta (JSONB)

### Tabla: `webs_generadas`
Cada archivo HTML generado se registra aquí.

**Campos principales:**
- `id` (UUID) - Identificador único
- `proyecto_id` - Relación con `proyectos`
- `nombre_archivo` - Nombre del archivo HTML
- `ruta_archivo` - Ruta donde se guardó
- `url_preview` - URL para previsualizar
- `version_numero` - Número de versión
- `estado` - Estado (generada, enviada_cliente, aprobada, etc.)

### Tabla: `versiones_web`
Historial de versiones cuando hay múltiples iteraciones.

### Tabla: `notas_proyecto`
Notas internas sobre proyectos y clientes.

### Tabla: `pagos`
Tracking de pagos y facturación (opcional).

## 🔍 Queries Útiles

El archivo `supabase_queries_utiles.sql` contiene ejemplos de consultas comunes. Puedes copiar y pegar cualquiera de ellas en el SQL Editor.

### Ejemplos rápidos:

**Ver todos los proyectos:**
```sql
SELECT * FROM vista_proyectos_completa ORDER BY created_at DESC;
```

**Proyectos pendientes:**
```sql
SELECT * FROM proyectos WHERE estado = 'pendiente';
```

**Buscar cliente por email:**
```sql
SELECT * FROM clientes WHERE email = 'cliente@example.com';
```

## 🔐 Obtener Credenciales de Conexión

Para conectar tu aplicación Node.js a Supabase:

1. Ve a **Settings** → **API** en Supabase
2. Copia estos valores:
   - **Project URL** (ej: `https://xxxxx.supabase.co`)
   - **anon/public key** (para el cliente)
   - **service_role key** (para el servidor - ¡MANTÉN ESTO SECRETO!)

3. También necesitarás la **Database Password**:
   - Ve a **Settings** → **Database**
   - Copia la contraseña de la base de datos

📖 **Para más detalles sobre cómo configurar las variables de entorno en GitHub, consulta:**
👉 [`VARIABLES_ENTORNO_SUPABASE.md`](./VARIABLES_ENTORNO_SUPABASE.md)

## 📝 Próximos Pasos

1. ✅ Ejecutar el script `supabase_schema.sql` (ya hecho)
2. ⏳ Obtener las credenciales de conexión
3. ⏳ Modificar `server.js` para conectar con Supabase
4. ⏳ Actualizar el endpoint `/api/encuesta` para guardar en la BD

## 🎯 Estados de Proyecto

Los estados posibles para un proyecto son:
- `pendiente` - Encuesta recibida, esperando procesamiento
- `en_revision` - Revisando la encuesta
- `en_desarrollo` - Trabajando en la web
- `muestra_enviada` - Primera versión enviada al cliente
- `esperando_aprobacion` - Esperando respuesta del cliente
- `aprobado` - Cliente aprobó la versión
- `en_produccion` - Web en producción
- `completado` - Proyecto finalizado
- `cancelado` - Proyecto cancelado

## 💡 Tips

- Usa la vista `vista_proyectos_completa` para ver proyectos con información del cliente
- Los campos JSONB (`estilos`, `colores`, `fuentes`, etc.) permiten búsquedas flexibles
- El campo `datos_encuesta_completos` guarda toda la encuesta como backup
- Los timestamps se actualizan automáticamente gracias a los triggers

## 🆘 Solución de Problemas

**Error: "relation already exists"**
- Las tablas ya existen. Puedes eliminarlas primero o usar `DROP TABLE IF EXISTS nombre_tabla;`

**Error: "permission denied"**
- Asegúrate de estar usando el SQL Editor con permisos de administrador

**No veo las tablas**
- Refresca la página o ve a Table Editor y recarga

## 📞 Siguiente Paso

Una vez que tengas las tablas creadas, el siguiente paso es modificar `server.js` para que guarde los datos en Supabase en lugar de solo generar archivos HTML.

