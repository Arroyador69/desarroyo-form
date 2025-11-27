-- ============================================
-- QUERIES ÚTILES PARA DESARROYO.TECH
-- Ejemplos de consultas comunes
-- ============================================

-- ============================================
-- 1. INSERTAR UN CLIENTE NUEVO
-- ============================================
INSERT INTO clientes (nombre_completo, email, telefono, fuente_descubrimiento, autoriza_portafolio)
VALUES (
    'Juan Pérez',
    'juan@example.com',
    '+34612345678',
    'instagram',
    true
)
RETURNING *;

-- ============================================
-- 2. INSERTAR UNA ENCUESTA/PROYECTO
-- ============================================
INSERT INTO proyectos (
    cliente_id,
    nombre_proyecto,
    sector,
    plan,
    presupuesto_estimado,
    estilos,
    colores,
    fuentes,
    secciones,
    menu_estilo,
    plantilla_estilo,
    footer_estilo,
    objetivo,
    datos_encuesta_completos
) VALUES (
    'UUID_DEL_CLIENTE', -- Reemplazar con el UUID real
    'Mi Tienda Online',
    'ecommerce',
    'escalable',
    '1200 €',
    '["minimalista", "moderno"]'::jsonb,
    '{"color1": "#000000", "color2": "#ffffff", "color3": "#cccccc"}'::jsonb,
    '["roboto", "montserrat"]'::jsonb,
    '["Inicio", "Productos", "Contacto"]'::jsonb,
    'menu3',
    'estilo5',
    'footer2',
    'Vender productos online',
    '{"todos": "los", "datos": "de la encuesta"}'::jsonb
)
RETURNING *;

-- ============================================
-- 3. INSERTAR UNA WEB GENERADA
-- ============================================
INSERT INTO webs_generadas (
    proyecto_id,
    nombre_archivo,
    ruta_archivo,
    url_preview,
    url_absoluta,
    version_numero,
    estado
) VALUES (
    'UUID_DEL_PROYECTO', -- Reemplazar con el UUID real
    'mi-tienda-1234567890.html',
    '/webs_generadas/mi-tienda-1234567890.html',
    '/webs_generadas/mi-tienda-1234567890.html',
    'https://desarroyo.tech/webs_generadas/mi-tienda-1234567890.html',
    1,
    'generada'
)
RETURNING *;

-- ============================================
-- 4. BUSCAR CLIENTE POR EMAIL
-- ============================================
SELECT * FROM clientes WHERE email = 'juan@example.com';

-- ============================================
-- 5. LISTAR TODOS LOS PROYECTOS CON INFO DEL CLIENTE
-- ============================================
SELECT 
    p.id,
    p.nombre_proyecto,
    p.estado,
    p.plan,
    p.created_at,
    c.nombre_completo,
    c.email,
    c.telefono
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
ORDER BY p.created_at DESC;

-- ============================================
-- 6. PROYECTOS PENDIENTES
-- ============================================
SELECT 
    p.nombre_proyecto,
    p.fecha_entrega_deseada,
    c.nombre_completo,
    c.email
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
WHERE p.estado = 'pendiente'
ORDER BY p.fecha_entrega_deseada ASC NULLS LAST;

-- ============================================
-- 7. PROYECTOS POR SECTOR
-- ============================================
SELECT 
    sector,
    COUNT(*) as total,
    COUNT(CASE WHEN estado = 'completado' THEN 1 END) as completados
FROM proyectos
GROUP BY sector
ORDER BY total DESC;

-- ============================================
-- 8. PROYECTOS POR PLAN
-- ============================================
SELECT 
    plan,
    COUNT(*) as total,
    AVG(CASE WHEN presupuesto_estimado ~ '^[0-9]+' 
        THEN CAST(REGEXP_REPLACE(presupuesto_estimado, '[^0-9]', '', 'g') AS INTEGER) 
        ELSE NULL END) as presupuesto_promedio
FROM proyectos
WHERE plan IS NOT NULL
GROUP BY plan;

-- ============================================
-- 9. WEBS GENERADAS DE UN PROYECTO
-- ============================================
SELECT 
    wg.nombre_archivo,
    wg.url_preview,
    wg.version_numero,
    wg.estado,
    wg.fecha_generacion
FROM webs_generadas wg
WHERE wg.proyecto_id = 'UUID_DEL_PROYECTO'
ORDER BY wg.version_numero DESC;

-- ============================================
-- 10. CLIENTES CON MÚLTIPLES PROYECTOS
-- ============================================
SELECT 
    c.nombre_completo,
    c.email,
    COUNT(p.id) as total_proyectos
FROM clientes c
LEFT JOIN proyectos p ON c.id = p.cliente_id
GROUP BY c.id, c.nombre_completo, c.email
HAVING COUNT(p.id) > 1
ORDER BY total_proyectos DESC;

-- ============================================
-- 11. PROYECTOS QUE NECESITAN ATENCIÓN
-- ============================================
SELECT 
    p.nombre_proyecto,
    p.estado,
    p.fecha_entrega_deseada,
    c.nombre_completo,
    c.email,
    CASE 
        WHEN p.fecha_entrega_deseada < CURRENT_DATE THEN 'VENCIDO'
        WHEN p.fecha_entrega_deseada < CURRENT_DATE + INTERVAL '3 days' THEN 'URGENTE'
        ELSE 'NORMAL'
    END as prioridad
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
WHERE p.estado IN ('pendiente', 'en_revision', 'en_desarrollo')
ORDER BY 
    CASE 
        WHEN p.fecha_entrega_deseada < CURRENT_DATE THEN 1
        WHEN p.fecha_entrega_deseada < CURRENT_DATE + INTERVAL '3 days' THEN 2
        ELSE 3
    END,
    p.fecha_entrega_deseada ASC;

-- ============================================
-- 12. ESTADÍSTICAS GENERALES
-- ============================================
SELECT 
    (SELECT COUNT(*) FROM clientes) as total_clientes,
    (SELECT COUNT(*) FROM proyectos) as total_proyectos,
    (SELECT COUNT(*) FROM proyectos WHERE estado = 'completado') as proyectos_completados,
    (SELECT COUNT(*) FROM webs_generadas) as total_webs_generadas,
    (SELECT COUNT(*) FROM proyectos WHERE estado = 'pendiente') as proyectos_pendientes;

-- ============================================
-- 13. BUSCAR PROYECTOS POR TÉRMINO
-- ============================================
SELECT 
    p.nombre_proyecto,
    p.sector,
    p.estado,
    c.nombre_completo,
    c.email
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
WHERE 
    p.nombre_proyecto ILIKE '%tienda%' OR
    c.nombre_completo ILIKE '%tienda%' OR
    c.email ILIKE '%tienda%'
ORDER BY p.created_at DESC;

-- ============================================
-- 14. ACTUALIZAR ESTADO DE UN PROYECTO
-- ============================================
UPDATE proyectos
SET 
    estado = 'muestra_enviada',
    updated_at = NOW()
WHERE id = 'UUID_DEL_PROYECTO'
RETURNING *;

-- ============================================
-- 15. MARCAR WEB COMO ENVIADA AL CLIENTE
-- ============================================
UPDATE webs_generadas
SET 
    estado = 'enviada_cliente',
    fecha_envio_cliente = NOW(),
    updated_at = NOW()
WHERE id = 'UUID_DE_LA_WEB'
RETURNING *;

-- ============================================
-- 16. AÑADIR NOTA A UN PROYECTO
-- ============================================
INSERT INTO notas_proyecto (
    proyecto_id,
    tipo_nota,
    titulo,
    contenido
) VALUES (
    'UUID_DEL_PROYECTO',
    'llamada',
    'Llamada con el cliente',
    'Cliente quiere cambios en el menú. Prefiere estilo más minimalista.'
)
RETURNING *;

-- ============================================
-- 17. OBTENER TODAS LAS NOTAS DE UN PROYECTO
-- ============================================
SELECT 
    np.titulo,
    np.tipo_nota,
    np.contenido,
    np.created_at,
    np.created_by
FROM notas_proyecto np
WHERE np.proyecto_id = 'UUID_DEL_PROYECTO'
ORDER BY np.created_at DESC;

-- ============================================
-- 18. PROYECTOS POR MES
-- ============================================
SELECT 
    DATE_TRUNC('month', created_at) as mes,
    COUNT(*) as total_proyectos,
    COUNT(CASE WHEN estado = 'completado' THEN 1 END) as completados
FROM proyectos
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY mes DESC;

-- ============================================
-- 19. TOP ESTILOS MÁS SOLICITADOS
-- ============================================
SELECT 
    estilo,
    COUNT(*) as veces_solicitado
FROM (
    SELECT jsonb_array_elements_text(estilos) as estilo
    FROM proyectos
    WHERE estilos IS NOT NULL
) subquery
GROUP BY estilo
ORDER BY veces_solicitado DESC;

-- ============================================
-- 20. PROYECTOS CON EXTRAS SELECCIONADOS
-- ============================================
SELECT 
    p.nombre_proyecto,
    c.nombre_completo,
    p.extras
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
WHERE p.extras IS NOT NULL 
  AND jsonb_array_length(p.extras) > 0
ORDER BY jsonb_array_length(p.extras) DESC;

-- ============================================
-- 21. EXPORTAR DATOS DE UN PROYECTO COMPLETO
-- ============================================
SELECT 
    p.*,
    c.nombre_completo as cliente_nombre,
    c.email as cliente_email,
    c.telefono as cliente_telefono,
    json_agg(DISTINCT jsonb_build_object(
        'id', wg.id,
        'nombre_archivo', wg.nombre_archivo,
        'url_preview', wg.url_preview,
        'version_numero', wg.version_numero,
        'estado', wg.estado
    )) as webs_generadas
FROM proyectos p
JOIN clientes c ON p.cliente_id = c.id
LEFT JOIN webs_generadas wg ON p.id = wg.proyecto_id
WHERE p.id = 'UUID_DEL_PROYECTO'
GROUP BY p.id, c.id;

-- ============================================
-- 22. ELIMINAR UN PROYECTO (CASCADE eliminará webs y versiones)
-- ============================================
-- CUIDADO: Esto eliminará también las webs generadas y versiones relacionadas
-- DELETE FROM proyectos WHERE id = 'UUID_DEL_PROYECTO';

-- ============================================
-- 23. DESACTIVAR UN CLIENTE (SOFT DELETE)
-- ============================================
UPDATE clientes
SET activo = false
WHERE id = 'UUID_DEL_CLIENTE'
RETURNING *;

-- ============================================
-- 24. REACTIVAR UN CLIENTE
-- ============================================
UPDATE clientes
SET activo = true
WHERE id = 'UUID_DEL_CLIENTE'
RETURNING *;

-- ============================================
-- 25. CLIENTES ACTIVOS CON PROYECTOS
-- ============================================
SELECT 
    c.nombre_completo,
    c.email,
    COUNT(p.id) as proyectos_activos
FROM clientes c
LEFT JOIN proyectos p ON c.id = p.cliente_id AND p.estado != 'cancelado'
WHERE c.activo = true
GROUP BY c.id, c.nombre_completo, c.email
HAVING COUNT(p.id) > 0
ORDER BY proyectos_activos DESC;

