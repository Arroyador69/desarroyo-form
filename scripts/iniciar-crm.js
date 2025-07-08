#!/usr/bin/env node

/**
 * 🚀 Script de Inicio Automático - CRM DesArroyo.tech
 * Configura y inicia todo el sistema automáticamente
 */

const fs = require('fs');
const path = require('path');
const { spawn, exec } = require('child_process');

console.log('🚀 INICIANDO CRM DESARROYO.TECH...\n');

// Colores para la consola
const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
    reset: '\x1b[0m',
    bright: '\x1b[1m'
};

function log(message, color = 'cyan') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function success(message) {
    console.log(`${colors.green}✅ ${message}${colors.reset}`);
}

function error(message) {
    console.log(`${colors.red}❌ ${message}${colors.reset}`);
}

function info(message) {
    console.log(`${colors.blue}ℹ️  ${message}${colors.reset}`);
}

function warning(message) {
    console.log(`${colors.yellow}⚠️  ${message}${colors.reset}`);
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function runCommand(command, description) {
    return new Promise((resolve, reject) => {
        info(`Ejecutando: ${description}`);
        
        exec(command, (error, stdout, stderr) => {
            if (error) {
                error(`Error en: ${description}`);
                console.log(`Error: ${error.message}`);
                reject(error);
            } else {
                success(`Completado: ${description}`);
                if (stdout) console.log(stdout);
                resolve(stdout);
            }
        });
    });
}

async function checkAndCreateFiles() {
    log('\n📁 VERIFICANDO ARCHIVOS PRINCIPALES...');
    
    const requiredFiles = [
        'server.js',
        'dashboard.html', 
        'login.html',
        'index.html',
        'package.json'
    ];
    
    for (const file of requiredFiles) {
        if (fs.existsSync(file)) {
            success(`Archivo encontrado: ${file}`);
        } else {
            error(`Archivo faltante: ${file}`);
            return false;
        }
    }
    
    return true;
}

async function checkAndCreateDirectories() {
    log('\n📂 VERIFICANDO DIRECTORIOS...');
    
    const requiredDirs = [
        'scripts',
        'videos',
        'videos/clips',
        'videos/output', 
        'videos/thumbnails',
        'videos/temp',
        'respuestas'
    ];
    
    for (const dir of requiredDirs) {
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
            success(`Directorio creado: ${dir}`);
        } else {
            success(`Directorio existe: ${dir}`);
        }
    }
}

async function resetDatabase() {
    log('\n🗄️ CONFIGURANDO BASE DE DATOS...');
    
    if (fs.existsSync('dashboard.db')) {
        warning('Base de datos existente encontrada');
        info('Manteniendo datos existentes');
    } else {
        info('Creando nueva base de datos');
    }
}

async function resetAdminUser() {
    log('\n👤 CONFIGURANDO USUARIO ADMINISTRADOR...');
    
    try {
        if (fs.existsSync('scripts/reset-admin-password.js')) {
            await runCommand('node scripts/reset-admin-password.js', 'Configurando usuario admin');
        } else {
            warning('Script de reset no encontrado, el servidor creará el usuario automáticamente');
        }
    } catch (error) {
        warning('No se pudo ejecutar reset, continuando...');
    }
}

async function killExistingProcess() {
    log('\n🔄 LIMPIANDO PROCESOS ANTERIORES...');
    
    try {
        // Intentar matar procesos en puerto 3000
        await runCommand('kill -9 $(lsof -t -i:3000) 2>/dev/null || true', 'Liberando puerto 3000');
        await sleep(2000); // Esperar 2 segundos
    } catch (error) {
        info('No hay procesos anteriores en puerto 3000');
    }
}

async function installDependencies() {
    log('\n📦 VERIFICANDO DEPENDENCIAS...');
    
    if (!fs.existsSync('node_modules')) {
        await runCommand('npm install', 'Instalando dependencias');
    } else {
        success('Dependencias ya instaladas');
    }
}

async function startServer() {
    log('\n🚀 INICIANDO SERVIDOR...');
    
    return new Promise((resolve, reject) => {
        const server = spawn('npm', ['start'], {
            stdio: 'pipe',
            detached: false
        });
        
        let serverStarted = false;
        
        server.stdout.on('data', (data) => {
            const output = data.toString();
            console.log(output);
            
            if (output.includes('ejecutándose en puerto 3000') && !serverStarted) {
                serverStarted = true;
                resolve(server);
            }
        });
        
        server.stderr.on('data', (data) => {
            console.error(data.toString());
        });
        
        server.on('error', (error) => {
            error('Error iniciando servidor');
            reject(error);
        });
        
        // Timeout después de 30 segundos
        setTimeout(() => {
            if (!serverStarted) {
                error('Timeout iniciando servidor');
                reject(new Error('Timeout'));
            }
        }, 30000);
    });
}

async function displaySuccessInfo() {
    log('\n' + '='.repeat(60));
    log('🎉 ¡CRM DESARROYO.TECH INICIADO CORRECTAMENTE!', 'green');
    log('='.repeat(60));
    
    console.log(`
${colors.bright}${colors.cyan}📊 INFORMACIÓN DE ACCESO:${colors.reset}

${colors.green}🔗 URLs Importantes:${colors.reset}
   • Login:     http://localhost:3000/login.html
   • Dashboard: http://localhost:3000/dashboard
   • Web:       http://localhost:3000

${colors.green}🔐 Credenciales:${colors.reset}
   • Usuario:    admin
   • Contraseña: admin123

${colors.green}🎬 Funcionalidades Disponibles:${colors.reset}
   • ✅ Sistema completo de videos con IA
   • ✅ Generador de guiones automático 
   • ✅ Chatbot inteligente con DeepSeek
   • ✅ Gestión de clientes y proyectos
   • ✅ Automatizaciones y reportes

${colors.green}🚀 Próximos Pasos:${colors.reset}
   1. Abre tu navegador
   2. Ve a: http://localhost:3000/login.html  
   3. Login con: admin / admin123
   4. ¡Explora tu CRM!

${colors.yellow}💡 Tip: Presiona Ctrl+C para detener el servidor${colors.reset}
`);
}

async function main() {
    try {
        // Verificar archivos principales
        const filesOk = await checkAndCreateFiles();
        if (!filesOk) {
            error('Archivos principales faltantes. Verifica que estás en el directorio correcto.');
            process.exit(1);
        }
        
        // Crear directorios necesarios
        await checkAndCreateDirectories();
        
        // Limpiar procesos anteriores
        await killExistingProcess();
        
        // Instalar dependencias si es necesario
        await installDependencies();
        
        // Configurar base de datos
        await resetDatabase();
        
        // Configurar usuario admin
        await resetAdminUser();
        
        // Iniciar servidor
        const serverProcess = await startServer();
        
        // Mostrar información de éxito
        await displaySuccessInfo();
        
        // Manejar cierre del proceso
        process.on('SIGINT', () => {
            log('\n🛑 Cerrando servidor...');
            serverProcess.kill();
            process.exit(0);
        });
        
        // Mantener el proceso vivo
        serverProcess.on('close', (code) => {
            if (code !== 0) {
                error(`Servidor cerrado con código: ${code}`);
            }
            process.exit(code);
        });
        
    } catch (error) {
        error(`Error en la inicialización: ${error.message}`);
        console.error(error);
        process.exit(1);
    }
}

// Ejecutar script principal
main(); 