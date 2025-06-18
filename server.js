const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const GestorComponentes = require('./bloques_html/componentes');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

// Inicializar el gestor de componentes
const gestorComponentes = new GestorComponentes();

// Asegura que la carpeta 'respuestas' existe
const respuestasDir = path.join(__dirname, 'respuestas');
if (!fs.existsSync(respuestasDir)) {
  fs.mkdirSync(respuestasDir);
}

// Endpoint para obtener información de componentes
app.get('/api/componentes/:tipo', (req, res) => {
  const tipo = req.params.tipo;
  const componentes = gestorComponentes.obtenerComponentes(tipo);
  if (componentes) {
    res.json(componentes);
  } else {
    res.status(404).json({ error: 'Tipo de componente no encontrado' });
  }
});

// Endpoint para obtener un componente específico
app.get('/api/componentes/:tipo/:id', async (req, res) => {
  const { tipo, id } = req.params;
  if (gestorComponentes.existeComponente(tipo, id)) {
    const html = await gestorComponentes.obtenerHTML(tipo, id);
    if (html) {
      res.json({ html, info: gestorComponentes.obtenerInfo(tipo, id) });
    } else {
      res.status(500).json({ error: 'Error al cargar el HTML del componente' });
    }
  } else {
    res.status(404).json({ error: 'Componente no encontrado' });
  }
});

app.post('/guardar', async (req, res) => {
  const data = req.body;
  const fecha = new Date().toISOString().replace(/[:.]/g, '-');
  const jsonPath = path.join(respuestasDir, `respuestas_${fecha}.json`);
  const txtPath = path.join(respuestasDir, `prompt_${fecha}.txt`);

  // Verificar que los componentes seleccionados existen
  const menuValido = gestorComponentes.existeComponente('menus', data.menu_seleccionado);
  const estiloValido = gestorComponentes.existeComponente('estilos', data.plantilla_seleccionada);
  const footerValido = gestorComponentes.existeComponente('footers', data.footer_seleccionado);

  if (!menuValido || !estiloValido || !footerValido) {
    return res.status(400).json({ 
      error: 'Componentes inválidos',
      detalles: {
        menu: menuValido ? 'válido' : 'inválido',
        estilo: estiloValido ? 'válido' : 'inválido',
        footer: footerValido ? 'válido' : 'inválido'
      }
    });
  }

  // Guardar JSON
  fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2), 'utf8');

  // Generar prompt
  const prompt = `# Especificaciones para el desarrollo web\n\n## Información básica\n- Nombre del proyecto: ${data.nombre_proyecto}\n- Sector: ${data.sector}${data.sector_otro ? ` (${data.sector_otro})` : ''}\n\n## Diseño\n- Estilos visuales: ${data.estilos ? data.estilos.join(', ') : 'No especificado'}\n- Colores principales: \n  ${data.color1_hex ? `- Color 1: ${data.color1_hex}` : ''}\n  ${data.color2_hex ? `- Color 2: ${data.color2_hex}` : ''}\n  ${data.color3_hex ? `- Color 3: ${data.color3_hex}` : ''}\n- Tipografías seleccionadas: ${data.fuentes ? data.fuentes.join(', ') : 'No especificado'}\n\n## Contenido\n- Logo: ${data.logo ? 'Sí' : 'No'}${data.logo_idea ? `\n  Descripción: ${data.logo_idea}` : ''}\n- Imagen de portada: ${data.portada ? 'Sí' : 'No'}\n\n## Estructura\n- Secciones seleccionadas: ${data.secciones ? data.secciones.join(', ') : 'No especificado'}\n${data.secciones_extra ? `- Secciones adicionales: ${data.secciones_extra}` : ''}\n- Estilo de menú: ${data.menu_estilo}\n\n## Objetivos y funcionalidades\n- Objetivo principal: ${data.objetivo}\n- Redes sociales: ${data.redes}\n- Referencias visuales:\n  ${data.ref1 ? `- ${data.ref1}` : ''}\n  ${data.ref2 ? `- ${data.ref2}` : ''}\n  ${data.ref3 ? `- ${data.ref3}` : ''}\n\n## Plantillas preferidas\n- Selección: ${data.plantilla1}\n\n## Observaciones adicionales\n${data.observaciones}\n\n## Presupuesto\n- Rango seleccionado: ${data.presupuesto}`;

  fs.writeFileSync(txtPath, prompt, 'utf8');

  res.json({ ok: true, mensaje: 'Respuestas y prompt guardados correctamente.' });
});

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
}); 