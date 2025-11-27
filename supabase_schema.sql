-- ============================================
-- ESQUEMA DE BASE DE DATOS PARA DESARROYO.TECH
-- Supabase (PostgreSQL)
-- ============================================

-- ============================================
-- 1. TABLA DE CLIENTES
-- ============================================
-- Almacena información de contacto de los clientes
CREATE TABLE IF NOT EXISTS clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(50),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_consentimiento_rgpd TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fuente_descubrimiento VARCHAR(50),
    fuente_descubrimiento_otro TEXT,
    autoriza_portafolio BOOLEAN DEFAULT FALSE,
    publicar_testimonio BOOLEAN DEFAULT FALSE,
    notas_internas TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. TABLA DE PROYECTOS/ENCUESTAS
-- ============================================
-- Almacena cada encuesta enviada (un cliente puede tener múltiples proyectos)
CREATE TABLE IF NOT EXISTS proyectos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    
    -- Información básica del proyecto
    nombre_proyecto VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    sector_otro TEXT,
    
    -- Plan y presupuesto
    plan VARCHAR(50), -- 'rapida', 'escalable', 'pro'
    presupuesto_estimado VARCHAR(50),
    extras JSONB, -- Array de extras seleccionados: ["dominio", "hosting", "mantenimiento", "automatizacion"]
    
    -- Preferencias de diseño (arrays almacenados como JSONB)
    estilos JSONB, -- ["minimalista", "moderno", "corporativo", ...]
    colores JSONB, -- {"color1": "#000000", "color2": "#ffffff", "color3": "#cccccc"}
    fuentes JSONB, -- ["arial", "roboto", "montserrat", ...]
    
    -- Estructura y contenido
    secciones JSONB, -- ["Inicio", "Sobre mí", "Servicios", ...]
    secciones_extra TEXT,
    menu_estilo VARCHAR(50), -- 'menu1', 'menu2', ..., 'menu13'
    plantilla_estilo VARCHAR(50), -- 'estilo1', 'estilo2', ..., 'estilo13'
    footer_estilo VARCHAR(50), -- 'footer1', 'footer2', ..., 'footer13'
    
    -- Contenido adicional
    objetivo TEXT,
    redes_sociales TEXT,
    referencia_visual_1 TEXT,
    referencia_visual_2 TEXT,
    referencia_visual_3 TEXT,
    logo_idea TEXT,
    observaciones TEXT,
    
    -- Estado del proyecto
    estado VARCHAR(50) DEFAULT 'pendiente', 
    -- Estados posibles: 'pendiente', 'en_revision', 'en_desarrollo', 'muestra_enviada', 
    --                   'esperando_aprobacion', 'aprobado', 'en_produccion', 'completado', 'cancelado'
    
    fecha_entrega_deseada DATE,
    fecha_entrega_real DATE,
    
    -- Referencias y tracking
    referencia VARCHAR(100),
    cliente_categoria VARCHAR(100),
    
    -- Datos completos de la encuesta como JSONB (backup completo)
    datos_encuesta_completos JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 3. TABLA DE WEBS GENERADAS
-- ============================================
-- Almacena información sobre cada archivo HTML generado
CREATE TABLE IF NOT EXISTS webs_generadas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID NOT NULL REFERENCES proyectos(id) ON DELETE CASCADE,
    
    -- Información del archivo
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo TEXT NOT NULL,
    url_preview TEXT,
    url_absoluta TEXT,
    
    -- Versión
    version_numero INTEGER DEFAULT 1,
    es_version_final BOOLEAN DEFAULT FALSE,
    
    -- Estado
    estado VARCHAR(50) DEFAULT 'generada',
    -- Estados: 'generada', 'enviada_cliente', 'revisada', 'aprobada', 'rechazada'
    
    -- Metadatos
    fecha_generacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_envio_cliente TIMESTAMP WITH TIME ZONE,
    fecha_revision_cliente TIMESTAMP WITH TIME ZONE,
    
    -- Notas
    notas TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 4. TABLA DE VERSIONES DE WEB
-- ============================================
-- Historial de versiones de una web (si hay múltiples iteraciones)
CREATE TABLE IF NOT EXISTS versiones_web (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID NOT NULL REFERENCES proyectos(id) ON DELETE CASCADE,
    web_generada_id UUID REFERENCES webs_generadas(id) ON DELETE SET NULL,
    
    version_numero INTEGER NOT NULL,
    descripcion_cambios TEXT,
    cambios_solicitados TEXT,
    costo_version DECIMAL(10, 2),
    
    estado VARCHAR(50) DEFAULT 'pendiente',
    -- Estados: 'pendiente', 'en_desarrollo', 'completada', 'aprobada', 'rechazada'
    
    fecha_solicitud TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fecha_completada TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(proyecto_id, version_numero)
);

-- ============================================
-- 5. TABLA DE NOTAS Y COMENTARIOS
-- ============================================
-- Notas internas sobre proyectos y clientes
CREATE TABLE IF NOT EXISTS notas_proyecto (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID NOT NULL REFERENCES proyectos(id) ON DELETE CASCADE,
    cliente_id UUID REFERENCES clientes(id) ON DELETE CASCADE,
    
    tipo_nota VARCHAR(50) DEFAULT 'general',
    -- Tipos: 'general', 'llamada', 'email', 'reunion', 'recordatorio', 'problema', 'solucion'
    
    titulo VARCHAR(255),
    contenido TEXT NOT NULL,
    es_privada BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255), -- Usuario que creó la nota
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 6. TABLA DE PAGOS (OPCIONAL)
-- ============================================
-- Para tracking de pagos y facturación
CREATE TABLE IF NOT EXISTS pagos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    proyecto_id UUID NOT NULL REFERENCES proyectos(id) ON DELETE CASCADE,
    
    monto DECIMAL(10, 2) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'EUR',
    metodo_pago VARCHAR(50),
    estado_pago VARCHAR(50) DEFAULT 'pendiente',
    -- Estados: 'pendiente', 'procesando', 'completado', 'fallido', 'reembolsado'
    
    fecha_pago TIMESTAMP WITH TIME ZONE,
    fecha_vencimiento DATE,
    referencia_pago VARCHAR(255),
    notas TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- ÍNDICES PARA BÚSQUEDAS RÁPIDAS
-- ============================================

-- Índices en clientes
CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);
CREATE INDEX IF NOT EXISTS idx_clientes_nombre ON clientes(nombre_completo);
CREATE INDEX IF NOT EXISTS idx_clientes_fecha_registro ON clientes(fecha_registro);

-- Índices en proyectos
CREATE INDEX IF NOT EXISTS idx_proyectos_cliente_id ON proyectos(cliente_id);
CREATE INDEX IF NOT EXISTS idx_proyectos_nombre ON proyectos(nombre_proyecto);
CREATE INDEX IF NOT EXISTS idx_proyectos_sector ON proyectos(sector);
CREATE INDEX IF NOT EXISTS idx_proyectos_estado ON proyectos(estado);
CREATE INDEX IF NOT EXISTS idx_proyectos_plan ON proyectos(plan);
CREATE INDEX IF NOT EXISTS idx_proyectos_fecha_entrega ON proyectos(fecha_entrega_deseada);
CREATE INDEX IF NOT EXISTS idx_proyectos_created_at ON proyectos(created_at);

-- Índices en webs_generadas
CREATE INDEX IF NOT EXISTS idx_webs_proyecto_id ON webs_generadas(proyecto_id);
CREATE INDEX IF NOT EXISTS idx_webs_estado ON webs_generadas(estado);
CREATE INDEX IF NOT EXISTS idx_webs_version_final ON webs_generadas(es_version_final);

-- Índices en versiones_web
CREATE INDEX IF NOT EXISTS idx_versiones_proyecto_id ON versiones_web(proyecto_id);
CREATE INDEX IF NOT EXISTS idx_versiones_estado ON versiones_web(estado);

-- Índices en notas
CREATE INDEX IF NOT EXISTS idx_notas_proyecto_id ON notas_proyecto(proyecto_id);
CREATE INDEX IF NOT EXISTS idx_notas_cliente_id ON notas_proyecto(cliente_id);
CREATE INDEX IF NOT EXISTS idx_notas_tipo ON notas_proyecto(tipo_nota);

-- Índices en pagos
CREATE INDEX IF NOT EXISTS idx_pagos_proyecto_id ON pagos(proyecto_id);
CREATE INDEX IF NOT EXISTS idx_pagos_estado ON pagos(estado_pago);

-- ============================================
-- FUNCIONES Y TRIGGERS
-- ============================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar updated_at
CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_proyectos_updated_at BEFORE UPDATE ON proyectos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_webs_generadas_updated_at BEFORE UPDATE ON webs_generadas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_versiones_web_updated_at BEFORE UPDATE ON versiones_web
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_notas_proyecto_updated_at BEFORE UPDATE ON notas_proyecto
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_pagos_updated_at BEFORE UPDATE ON pagos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VISTAS ÚTILES (OPCIONAL)
-- ============================================

-- Vista: Resumen de proyectos con información del cliente
CREATE OR REPLACE VIEW vista_proyectos_completa AS
SELECT 
    p.id,
    p.nombre_proyecto,
    p.estado,
    p.plan,
    p.presupuesto_estimado,
    p.sector,
    p.fecha_entrega_deseada,
    p.created_at,
    c.nombre_completo AS cliente_nombre,
    c.email AS cliente_email,
    c.telefono AS cliente_telefono,
    COUNT(DISTINCT wg.id) AS total_webs_generadas,
    COUNT(DISTINCT vw.id) AS total_versiones
FROM proyectos p
LEFT JOIN clientes c ON p.cliente_id = c.id
LEFT JOIN webs_generadas wg ON p.id = wg.proyecto_id
LEFT JOIN versiones_web vw ON p.id = vw.proyecto_id
GROUP BY p.id, c.id;

-- Vista: Estadísticas por sector
CREATE OR REPLACE VIEW vista_estadisticas_sector AS
SELECT 
    COALESCE(sector, 'Sin especificar') AS sector,
    COUNT(*) AS total_proyectos,
    COUNT(CASE WHEN estado = 'completado' THEN 1 END) AS proyectos_completados,
    COUNT(CASE WHEN estado = 'pendiente' THEN 1 END) AS proyectos_pendientes,
    AVG(CASE WHEN presupuesto_estimado ~ '^[0-9]+' 
        THEN CAST(REGEXP_REPLACE(presupuesto_estimado, '[^0-9]', '', 'g') AS INTEGER) 
        ELSE NULL END) AS presupuesto_promedio
FROM proyectos
GROUP BY sector;

-- ============================================
-- COMENTARIOS EN TABLAS (DOCUMENTACIÓN)
-- ============================================

COMMENT ON TABLE clientes IS 'Información de contacto de los clientes';
COMMENT ON TABLE proyectos IS 'Proyectos/encuestas enviadas por los clientes';
COMMENT ON TABLE webs_generadas IS 'Archivos HTML generados para cada proyecto';
COMMENT ON TABLE versiones_web IS 'Historial de versiones de una web';
COMMENT ON TABLE notas_proyecto IS 'Notas internas sobre proyectos y clientes';
COMMENT ON TABLE pagos IS 'Tracking de pagos y facturación';

-- ============================================
-- FIN DEL ESQUEMA
-- ============================================

