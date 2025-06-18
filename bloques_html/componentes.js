const fs = require('fs');
const path = require('path');

class GestorComponentes {
  constructor() {
    this.componentes = JSON.parse(fs.readFileSync(path.join(__dirname, 'componentes.json'), 'utf8'));
    this.footerBase = fs.readFileSync(path.join(__dirname, 'footers/footer_base.html'), 'utf8');
    this.menuBase = fs.readFileSync(path.join(__dirname, 'menus/menu_base.html'), 'utf8');
    this.estiloBase = fs.readFileSync(path.join(__dirname, 'estilos/estilo_base.html'), 'utf8');
  }

  // Obtener el HTML de un componente específico
  async obtenerHTML(tipo, id) {
    try {
      switch (tipo) {
        case 'footers':
          return this.personalizarFooter(id);
        case 'menus':
          return this.personalizarMenu(id);
        case 'estilos':
          return this.personalizarEstilo(id);
        default:
          const rutaHTML = this.componentes[tipo][id].html;
          return await fs.promises.readFile(rutaHTML, 'utf8');
      }
    } catch (error) {
      console.error(`Error al cargar el HTML de ${tipo}/${id}:`, error);
      return null;
    }
  }

  // Personalizar el footer según el estilo seleccionado
  personalizarFooter(id) {
    const footerInfo = this.componentes.footers[id];
    let footerHTML = this.footerBase;

    // Personalizar según el estilo
    switch (id) {
      case 'footer1':
        // Footer minimalista
        footerHTML = footerHTML.replace('background-color: #111', 'background-color: #0a0a0a');
        break;
      case 'footer2':
        // Footer con redes sociales
        footerHTML = footerHTML.replace('</div>', `
          <div class="social-links" style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem;">
            <a href="#" style="color: #ccc;"><i class="fab fa-facebook"></i></a>
            <a href="#" style="color: #ccc;"><i class="fab fa-twitter"></i></a>
            <a href="#" style="color: #ccc;"><i class="fab fa-instagram"></i></a>
            <a href="#" style="color: #ccc;"><i class="fab fa-linkedin"></i></a>
          </div>
        </div>`);
        break;
      case 'footer3':
        // Footer con newsletter
        footerHTML = footerHTML.replace('</div>', `
          <div class="newsletter" style="margin-top: 1rem; text-align: center;">
            <form style="display: flex; gap: 0.5rem; justify-content: center;">
              <input type="email" placeholder="Tu email" style="padding: 0.5rem; border: 1px solid #333; background: #222; color: white; border-radius: 4px;">
              <button type="submit" style="background: linear-gradient(90deg, #00fff7 0%, #00cfff 50%, #a259ff 100%); border: none; padding: 0.5rem 1rem; color: white; cursor: pointer; border-radius: 4px;">Suscribirse</button>
            </form>
          </div>
        </div>`);
        break;
    }

    return footerHTML;
  }

  // Personalizar el menú según el estilo seleccionado
  personalizarMenu(id) {
    const menuInfo = this.componentes.menus[id];
    let menuHTML = this.menuBase;

    switch (id) {
      case 'menu1':
        // Menú minimalista
        menuHTML = menuHTML.replace('background-color: #111', 'background-color: transparent');
        break;
      case 'menu2':
        // Menú con efecto hover
        menuHTML = menuHTML.replace('</style>', `
          .menu-links a {
            position: relative;
          }
          .menu-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--color-primary);
            transition: width 0.3s;
          }
          .menu-links a:hover::after {
            width: 100%;
          }
        </style>`);
        break;
      case 'menu3':
        // Menú con iconos
        menuHTML = menuHTML.replace('Inicio</a>', 'Inicio <i class="fas fa-home"></i></a>')
          .replace('Servicios</a>', 'Servicios <i class="fas fa-cogs"></i></a>')
          .replace('Sobre Nosotros</a>', 'Sobre Nosotros <i class="fas fa-info-circle"></i></a>')
          .replace('Contacto</a>', 'Contacto <i class="fas fa-envelope"></i></a>');
        break;
      case 'menu4':
        // Menú con submenús
        menuHTML = menuHTML.replace('</div>', `
          <div class="submenu" style="position: absolute; background: #111; padding: 1rem; display: none;">
            <a href="/submenu1" style="display: block; margin: 0.5rem 0;">Submenú 1</a>
            <a href="/submenu2" style="display: block; margin: 0.5rem 0;">Submenú 2</a>
          </div>
        </div>`);
        break;
    }

    return menuHTML;
  }

  // Personalizar el estilo según la selección
  personalizarEstilo(id) {
    const estiloInfo = this.componentes.estilos[id];
    let estiloHTML = this.estiloBase;

    switch (id) {
      case 'estilo1':
        // Legal Nomads - Estilo ilustrado y personal
        estiloHTML = estiloHTML.replace('--color-primary: #00fff7', '--color-primary: #ff6b6b')
          .replace('--color-secondary: #a259ff', '--color-secondary: #4ecdc4');
        break;
      case 'estilo2':
        // AngelList Talent - Minimalismo profesional
        estiloHTML = estiloHTML.replace('--color-background: #10131a', '--color-background: #ffffff')
          .replace('--color-text: #ffffff', '--color-text: #333333')
          .replace('--color-text-secondary: #cccccc', '--color-text-secondary: #666666');
        break;
      case 'estilo3':
        // TiendaNube - E-commerce limpio y moderno
        estiloHTML = estiloHTML.replace('</style>', `
          .product-card {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          }
        </style>`);
        break;
    }

    return estiloHTML;
  }

  // Obtener la información de un componente
  obtenerInfo(tipo, id) {
    return this.componentes[tipo][id];
  }

  // Obtener todos los componentes de un tipo
  obtenerComponentes(tipo) {
    return this.componentes[tipo];
  }

  // Verificar si un componente existe
  existeComponente(tipo, id) {
    return this.componentes[tipo] && this.componentes[tipo][id];
  }

  // Obtener la ruta de la imagen de un componente
  obtenerRutaImagen(tipo, id) {
    return this.componentes[tipo][id].imagen;
  }
}

module.exports = GestorComponentes; 