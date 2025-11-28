#!/usr/bin/env node
/**
 * 🚀 Script para procesar encuesta y generar HTML
 * Se ejecuta desde GitHub Actions cuando se recibe una encuesta
 */

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');
const { Pool } = require('pg');

// Variables de entorno
const DATABASE_URL = process.env.DATABASE_URL || process.env.NEON_DATABASE_URL;
const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;
const PUBLIC_BASE_URL = process.env.PUBLIC_BASE_URL || 'https://desarroyo.tech';

// Inicializar Neon (PostgreSQL)
let dbPool = null;
if (DATABASE_URL) {
    try {
        dbPool = new Pool({
            connectionString: DATABASE_URL,
            ssl: {
                rejectUnauthorized: false // Neon requiere SSL
            },
            max: 1 // En serverless, mantener solo 1 conexión
        });
        console.log('✅ Cliente de Neon (PostgreSQL) inicializado correctamente.');
    } catch (error) {
        console.error('❌ Error inicializando Neon:', error.message);
        dbPool = null;
    }
} else {
    console.log('⏸️  Neon no se ha inicializado. Solo se generarán los HTMLs locales.');
}

// Helper functions
const stringOrNull = (value) => (value && String(value).trim()) || null;
const parseBooleanField = (value) => {
    if (typeof value === 'boolean') return value;
    if (typeof value === 'number') return value === 1;
    if (typeof value === 'string') {
        const lower = value.toLowerCase().trim();
        return lower === 'true' || lower === '1' || lower === 'yes' || lower === 'on';
    }
    return false;
};
const toArray = (value) => {
    if (Array.isArray(value)) return value.filter(Boolean);
    if (typeof value === 'string') return value.split(',').map(s => s.trim()).filter(Boolean);
    return value ? [value] : [];
};
const escapeHtml = (text) => {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
};
const slugify = (text) => {
    if (!text) return 'proyecto';
    return String(text)
        .toLowerCase()
        .trim()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_-]+/g, '-')
        .replace(/^-+|-+$/g, '')
        .substring(0, 50);
};
const isHexColor = (str) => /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(str);
const sanitizeUrl = (value) => {
    if (!value) return '';
    const trimmed = value.trim();
    if (!trimmed) return '';
    if (/^https?:\/\//i.test(trimmed)) return trimmed;
    return `https://${trimmed}`;
};
const formatMultiline = (text) => {
    if (!text) return '';
    return String(text)
        .split('\n')
        .map(line => `<p>${escapeHtml(line.trim())}</p>`)
        .join('');
};

const getColorsFromData = (data = {}) => {
    const candidates = [
        data.color1_hex,
        data.color2_hex,
        data.color3_hex,
        data.color1,
        data.color2,
        data.color3
    ].filter((color) => typeof color === 'string' && isHexColor(color));

    if (!candidates.length) {
        return ['#6366f1', '#0f172a', '#facc15'];
    }

    return candidates.slice(0, 3);
};

const buildColorPalette = (data = {}) => {
    const colors = getColorsFromData(data);
    return colors.length ? colors : null;
};

// Funciones de Neon (PostgreSQL)
const neonDisponible = () => Boolean(dbPool);

const upsertClienteNeon = async (payload = {}) => {
    if (!neonDisponible() || !payload.email) return null;

    try {
        const query = `
            INSERT INTO clientes (
                nombre_completo, email, telefono, fuente_descubrimiento,
                fuente_descubrimiento_otro, autoriza_portafolio, publicar_testimonio
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (email) 
            DO UPDATE SET
                nombre_completo = EXCLUDED.nombre_completo,
                telefono = EXCLUDED.telefono,
                fuente_descubrimiento = EXCLUDED.fuente_descubrimiento,
                fuente_descubrimiento_otro = EXCLUDED.fuente_descubrimiento_otro,
                autoriza_portafolio = EXCLUDED.autoriza_portafolio,
                publicar_testimonio = EXCLUDED.publicar_testimonio,
                updated_at = NOW()
            RETURNING id
        `;
        
        const result = await dbPool.query(query, [
            stringOrNull(payload.nombre_completo),
            payload.email,
            stringOrNull(payload.telefono),
            stringOrNull(payload.fuente_descubrimiento),
            stringOrNull(payload.fuente_descubrimiento_otro),
            parseBooleanField(payload.autoriza_portafolio),
            parseBooleanField(payload.publicar_testimonio)
        ]);

        return result.rows[0]?.id || null;
    } catch (error) {
        throw new Error(`Neon clientes: ${error.message}`);
    }
};

const crearProyectoNeon = async (payload = {}, clienteId) => {
    if (!neonDisponible() || !clienteId) return null;

    try {
        const query = `
            INSERT INTO proyectos (
                cliente_id, nombre_proyecto, sector, sector_otro, plan, presupuesto_estimado,
                extras, estilos, colores, fuentes, secciones, secciones_extra,
                menu_estilo, plantilla_estilo, footer_estilo, objetivo, redes_sociales,
                referencia_visual_1, referencia_visual_2, referencia_visual_3,
                logo_idea, observaciones, estado, fecha_entrega_deseada, referencia,
                cliente_categoria, datos_encuesta_completos
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27)
            RETURNING id
        `;
        
        const result = await dbPool.query(query, [
            clienteId,
            stringOrNull(payload.nombre_proyecto) || stringOrNull(payload.nombre_completo) || 'Proyecto sin nombre',
            stringOrNull(payload.sector),
            stringOrNull(payload.sector_otro),
            stringOrNull(payload.plan),
            stringOrNull(payload.presupuesto),
            toArray(payload.extras).length ? JSON.stringify(toArray(payload.extras)) : null,
            toArray(payload.estilos).length ? JSON.stringify(toArray(payload.estilos)) : null,
            buildColorPalette(payload) ? JSON.stringify(buildColorPalette(payload)) : null,
            toArray(payload.fuentes).length ? JSON.stringify(toArray(payload.fuentes)) : null,
            toArray(payload.secciones).length ? JSON.stringify(toArray(payload.secciones)) : null,
            stringOrNull(payload.secciones_extra),
            stringOrNull(payload.menu_seleccionado),
            stringOrNull(payload.plantilla_seleccionada),
            stringOrNull(payload.footer_seleccionado),
            stringOrNull(payload.objetivo),
            stringOrNull(payload.redes),
            stringOrNull(payload.ref1),
            stringOrNull(payload.ref2),
            stringOrNull(payload.ref3),
            stringOrNull(payload.logo_idea),
            stringOrNull(payload.observaciones),
            'pendiente',
            stringOrNull(payload.fecha_entrega_deseada),
            stringOrNull(payload.referencia),
            stringOrNull(payload.cliente_categoria),
            JSON.stringify(payload)
        ]);

        return result.rows[0]?.id || null;
    } catch (error) {
        throw new Error(`Neon proyectos: ${error.message}`);
    }
};

const registrarWebGeneradaNeon = async (
    proyectoId,
    { fileName, previewUrl, absoluteUrl, relativeFilePath }
) => {
    if (!neonDisponible() || !proyectoId) return null;

    try {
        const query = `
            INSERT INTO webs_generadas (
                proyecto_id, nombre_archivo, ruta_archivo, url_preview, url_absoluta,
                version_numero, estado
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
        `;
        
        const result = await dbPool.query(query, [
            proyectoId,
            fileName,
            relativeFilePath || fileName,
            previewUrl,
            absoluteUrl,
            1,
            'generada'
        ]);

        return result.rows[0]?.id || null;
    } catch (error) {
        throw new Error(`Neon webs_generadas: ${error.message}`);
    }
};

const persistSurveyInNeon = async (payload, metadata = {}) => {
    if (!neonDisponible()) return null;

    const clienteId = await upsertClienteNeon(payload);
    const proyectoId = await crearProyectoNeon(payload, clienteId);
    const webId = await registrarWebGeneradaNeon(proyectoId, metadata);

    return { clienteId, proyectoId, webId };
};

// Función para generar HTML (simplificada del server.js)
const buildQuickLandingHTML = (data = {}) => {
    const colors = getColorsFromData(data);
    const [primaryColor, secondaryColor, accentColor] = [
        colors[0] || '#6366f1',
        colors[1] || '#0f172a',
        colors[2] || '#facc15'
    ];

    const styles = toArray(data.estilos).map(escapeHtml);
    const fonts = toArray(data.fuentes).map(escapeHtml);
    const extras = toArray(data.extras).map(escapeHtml);
    const sections = toArray(data.secciones).map(escapeHtml);
    if (data.secciones_extra) sections.push(escapeHtml(data.secciones_extra));

    const redes = (data.redes || '')
        .split(/,|\n/)
        .map((item) => item.trim())
        .filter(Boolean)
        .map((url) => ({
            text: escapeHtml(url),
            href: sanitizeUrl(url)
        }));

    const referencias = [data.ref1, data.ref2, data.ref3]
        .filter(Boolean)
        .map((url) => ({
            text: escapeHtml(url),
            href: sanitizeUrl(url)
        }));

    const catalogoSecciones =
        sections.length > 0
            ? sections.map((section) => `<li>${section}</li>`).join('')
            : '<li>Secciones por definir</li>';

    const estilosHTML = styles.length
        ? styles.map((style) => `<span class="chip">${style}</span>`).join('')
        : '<span class="chip">Personalizar</span>';

    const fuentesHTML = fonts.length
        ? fonts.map((font) => `<span class="chip">${font}</span>`).join('')
        : '<span class="chip">Fuentes a definir</span>';

    const extrasHTML = extras.length
        ? extras.map((extra) => `<li>${extra}</li>`).join('')
        : '<li>Sin extras seleccionados</li>';

    const redesHTML = redes.length
        ? redes
              .map(
                  (item, index) =>
                      `<li><a href="${item.href}" target="_blank" rel="noopener noreferrer">Red ${index + 1}</a> — ${item.text}</li>`
              )
              .join('')
        : '<li>El cliente no dejó redes sociales</li>';

    const referenciasHTML = referencias.length
        ? referencias
              .map(
                  (item, index) =>
                      `<li><a href="${item.href}" target="_blank" rel="noopener noreferrer">Referencia ${index + 1}</a></li>`
              )
              .join('')
        : '<li>Sin referencias enviadas</li>';

    const paletteHTML = colors
        .map(
            (color) =>
                `<span class="color-pill" style="background:${color};">${color.toUpperCase()}</span>`
        )
        .join('');

    const descripcionProyecto = formatMultiline(data.observaciones || 'Este espacio está listo para añadir una historia breve del proyecto, tono de voz y mensajes clave.');

    return `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${escapeHtml(
      data.nombre_proyecto || 'Concepto digital'
  )} · Borrador generado automáticamente</title>
  <style>
    :root {
      --primary: ${primaryColor};
      --secondary: ${secondaryColor};
      --accent: ${accentColor};
      --bg: #f8fafc;
      --text: #0f172a;
    }
    * { box-sizing: border-box; }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      margin: 0;
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
    }
    header {
      background: linear-gradient(135deg, var(--primary), var(--secondary));
      color: #fff;
      padding: 4rem 2rem;
      text-align: center;
    }
    header h1 {
      margin: 0;
      font-size: clamp(2rem, 5vw, 3.5rem);
    }
    main {
      max-width: 960px;
      margin: -80px auto 3rem;
      padding: 2rem;
      background: #fff;
      border-radius: 24px;
      box-shadow: 0 30px 80px rgba(15, 23, 42, 0.15);
    }
    section {
      margin-bottom: 2.5rem;
    }
    section h2 {
      font-size: 1.5rem;
      margin-bottom: 0.75rem;
      color: var(--secondary);
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1.5rem;
    }
    .card {
      border: 1px solid rgba(15, 23, 42, 0.08);
      border-radius: 18px;
      padding: 1.5rem;
      background: #fff;
      box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
    }
    .chip {
      display: inline-block;
      padding: 0.35rem 0.8rem;
      border-radius: 999px;
      background: rgba(99, 102, 241, 0.12);
      color: var(--primary);
      font-weight: 600;
      margin: 0.25rem;
      font-size: 0.9rem;
    }
    .color-pill {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.5rem 1rem;
      border-radius: 999px;
      font-weight: 600;
      color: #fff;
      margin: 0.25rem;
      border: 1px solid rgba(255,255,255,0.2);
      min-width: 130px;
    }
    ul {
      padding-left: 1.2rem;
      margin: 0;
    }
    .cta {
      background: var(--secondary);
      color: #fff;
      padding: 2rem;
      border-radius: 18px;
      text-align: center;
      box-shadow: inset 0 0 0 2px rgba(255,255,255,0.2);
    }
    .cta a {
      color: #fff;
      text-decoration: none;
      font-weight: 600;
      border-bottom: 1px solid rgba(255,255,255,0.4);
    }
    footer {
      text-align: center;
      color: rgba(15, 23, 42, 0.5);
      font-size: 0.9rem;
      margin-top: 2rem;
    }
    @media (max-width: 600px) {
      main { padding: 1.5rem; margin-top: -60px; }
      header { padding: 3rem 1.5rem; }
    }
  </style>
</head>
<body>
  <header>
    <p style="font-weight:600; letter-spacing:0.1em;">Concepto generado automáticamente</p>
    <h1>${escapeHtml(
        data.nombre_proyecto || data.nombre_completo || 'Web sin título'
    )}</h1>
    <p style="max-width:720px; margin: 1rem auto 0; font-size:1.2rem;">${escapeHtml(
        data.objetivo || 'Creamos experiencias digitales memorables en 48 horas.'
    )}</p>
  </header>
  <main>
    <section class="grid">
      <div class="card">
        <h2>Cliente</h2>
        <p><strong>Nombre:</strong> ${escapeHtml(data.nombre_completo || 'No especificado')}</p>
        <p><strong>Sector:</strong> ${escapeHtml(data.sector_otro || data.sector || 'General')}</p>
        <p><strong>Plan elegido:</strong> ${escapeHtml(data.plan || 'Sin plan')}</p>
        <p><strong>Extras:</strong></p>
        <ul>${extrasHTML}</ul>
      </div>
      <div class="card">
        <h2>Estética</h2>
        <p><strong>Estilos preferidos:</strong></p>
        <div>${estilosHTML}</div>
        <p><strong>Fuentes:</strong></p>
        <div>${fuentesHTML}</div>
      </div>
      <div class="card">
        <h2>Componentes seleccionados</h2>
        <p><strong>Menú:</strong> ${escapeHtml(data.menu_seleccionado || 'Por definir')}</p>
        <p><strong>Plantilla:</strong> ${escapeHtml(data.plantilla_seleccionada || 'Por definir')}</p>
        <p><strong>Footer:</strong> ${escapeHtml(data.footer_seleccionado || 'Por definir')}</p>
      </div>
    </section>

    <section>
      <h2>Paleta sugerida</h2>
      ${paletteHTML}
    </section>

    <section class="grid">
      <div class="card">
        <h2>Estructura</h2>
        <ul>${catalogoSecciones}</ul>
      </div>
      <div class="card">
        <h2>Historial y notas</h2>
        <p>${descripcionProyecto}</p>
      </div>
    </section>

    <section class="grid">
      <div class="card">
        <h2>Redes sociales</h2>
        <ul>${redesHTML}</ul>
      </div>
      <div class="card">
        <h2>Referencias visuales</h2>
        <ul>${referenciasHTML}</ul>
      </div>
    </section>

    <section class="cta">
      <h2>Contacto directo</h2>
      <p>📧 ${escapeHtml(data.email || 'Sin correo')}</p>
      <p>📞 ${escapeHtml(data.telefono || 'Sin teléfono')}</p>
      <p style="margin-top:1rem;">Este borrador se genera automáticamente con los datos de la encuesta inteligente. Nos sirve como punto de partida para trabajar la versión profesional.</p>
    </section>
  </main>
  <footer>
    <p>Generado automáticamente el ${new Date().toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    })}</p>
    <p>DesArroyo.Tech · Borrador interno</p>
  </footer>
</body>
</html>`;
};

// Función para enviar a Telegram
const sendLandingToTelegram = async (filePath, data, previewUrl) => {
    if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) {
        console.warn('⚠️ Telegram no configurado. Skipping notification.');
        return;
    }

    try {
        const form = new FormData();
        form.append('chat_id', TELEGRAM_CHAT_ID);

        const absoluteLink =
            previewUrl && PUBLIC_BASE_URL ? new URL(previewUrl, PUBLIC_BASE_URL).href : null;

        const captionLines = [
            '🚀 Nueva encuesta completada',
            `👤 ${data.nombre_completo || 'Sin nombre'}`,
            `📧 ${data.email || 'Sin correo'}`,
            `📱 ${data.telefono || 'Sin teléfono'}`,
            `🏷️ Proyecto: ${data.nombre_proyecto || 'Sin título'}`,
            `🎯 Objetivo: ${data.objetivo || 'Sin objetivo'}`,
            absoluteLink ? `🌐 Vista previa: ${absoluteLink}` : null
        ].filter(Boolean);

        form.append('caption', captionLines.join('\n').slice(0, 1024));
        form.append('document', fs.createReadStream(filePath));

        await axios.post(
            `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendDocument`,
            form,
            { headers: form.getHeaders() }
        );
        
        console.log('✅ Enviado a Telegram correctamente');
    } catch (error) {
        console.error('❌ Error enviando a Telegram:', error.message);
    }
};

// Función principal
async function procesarEncuesta() {
    try {
        // Leer datos del payload desde stdin o variable de entorno
        const payloadJson = process.env.ENCUESTA_DATA || process.stdin.read();
        if (!payloadJson) {
            throw new Error('No se recibieron datos de la encuesta');
        }

        const payload = typeof payloadJson === 'string' ? JSON.parse(payloadJson) : payloadJson;

        console.log('📋 Procesando encuesta...');
        console.log(`👤 Cliente: ${payload.nombre_completo || 'Sin nombre'}`);
        console.log(`📧 Email: ${payload.email || 'Sin email'}`);

        // Crear directorio si no existe
        const GENERATED_SITES_DIR = path.join(__dirname, '..', 'webs_generadas');
        if (!fs.existsSync(GENERATED_SITES_DIR)) {
            fs.mkdirSync(GENERATED_SITES_DIR, { recursive: true });
        }

        // Generar nombre de archivo
        const slugBase = slugify(payload.nombre_proyecto || payload.nombre_completo || 'proyecto');
        const fileName = `${slugBase}-${Date.now()}.html`;
        const filePath = path.join(GENERATED_SITES_DIR, fileName);
        const relativeFilePath = path.relative(path.join(__dirname, '..'), filePath);

        // Generar HTML
        console.log('🎨 Generando HTML...');
        const htmlContent = buildQuickLandingHTML(payload);
        fs.writeFileSync(filePath, htmlContent, 'utf-8');
        console.log(`✅ HTML generado: ${fileName}`);

        const previewUrl = `/webs_generadas/${fileName}`;
        const absoluteUrl = PUBLIC_BASE_URL
            ? new URL(previewUrl, PUBLIC_BASE_URL).href
            : null;

        // Guardar en Neon (PostgreSQL)
        if (neonDisponible()) {
            try {
                console.log('💾 Guardando en Neon...');
                await persistSurveyInNeon(payload, {
                    fileName,
                    previewUrl,
                    absoluteUrl,
                    relativeFilePath
                });
                console.log('✅ Datos guardados en Neon');
            } catch (dbError) {
                console.error('⚠️ Error guardando datos en Neon:', dbError.message || dbError);
            }
        } else {
            console.log('⏸️ Neon no configurado, saltando persistencia');
        }

        // Enviar a Telegram
        console.log('📤 Enviando a Telegram...');
        await sendLandingToTelegram(filePath, payload, previewUrl);

        console.log('🎉 ¡Proceso completado exitosamente!');
        console.log(`🌐 URL: ${absoluteUrl || previewUrl}`);

        // Output para GitHub Actions
        if (process.env.GITHUB_ACTIONS) {
            console.log(`::set-output name=file_name::${fileName}`);
            console.log(`::set-output name=preview_url::${previewUrl}`);
            console.log(`::set-output name=absolute_url::${absoluteUrl || ''}`);
        }

        process.exit(0);
    } catch (error) {
        console.error('❌ Error procesando encuesta:', error);
        process.exit(1);
    }
}

// Ejecutar si se llama directamente
if (require.main === module) {
    procesarEncuesta();
}

module.exports = { procesarEncuesta };

