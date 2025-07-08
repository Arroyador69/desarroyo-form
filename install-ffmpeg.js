#!/usr/bin/env node

const os = require('os');
const { exec } = require('child_process');
const VideoProcessor = require('./video-processor');

console.log('🎬 FFmpeg Installation Helper - DesArroyo.Tech');
console.log('================================================\n');

async function checkFFmpegInstallation() {
    const videoProcessor = new VideoProcessor();
    const isInstalled = await videoProcessor.checkFFmpegInstallation();
    
    if (isInstalled) {
        console.log('✅ FFmpeg ya está instalado y funcionando correctamente!\n');
        return true;
    } else {
        console.log('❌ FFmpeg no está instalado o no se encuentra en el PATH.\n');
        return false;
    }
}

function showInstallationInstructions() {
    const platform = os.platform();
    
    console.log('📋 Instrucciones de instalación por sistema operativo:\n');
    
    switch (platform) {
        case 'darwin': // macOS
            console.log('🍎 macOS:');
            console.log('   Opción 1 - Homebrew (recomendado):');
            console.log('   brew install ffmpeg');
            console.log('');
            console.log('   Opción 2 - MacPorts:');
            console.log('   sudo port install ffmpeg');
            console.log('');
            break;
            
        case 'linux':
            console.log('🐧 Linux:');
            console.log('   Ubuntu/Debian:');
            console.log('   sudo apt update');
            console.log('   sudo apt install ffmpeg');
            console.log('');
            console.log('   CentOS/RHEL/Fedora:');
            console.log('   sudo yum install ffmpeg  # CentOS/RHEL');
            console.log('   sudo dnf install ffmpeg  # Fedora');
            console.log('');
            break;
            
        case 'win32': // Windows
            console.log('🪟 Windows:');
            console.log('   Opción 1 - Chocolatey (recomendado):');
            console.log('   choco install ffmpeg');
            console.log('');
            console.log('   Opción 2 - Scoop:');
            console.log('   scoop install ffmpeg');
            console.log('');
            console.log('   Opción 3 - Descarga manual:');
            console.log('   1. Visita: https://ffmpeg.org/download.html#build-windows');
            console.log('   2. Descarga la versión estática');
            console.log('   3. Extrae el archivo y añade la carpeta bin al PATH');
            console.log('');
            break;
            
        default:
            console.log('❓ Sistema operativo no reconocido.');
            console.log('   Visita https://ffmpeg.org/download.html para instrucciones específicas.');
            console.log('');
    }
}

function showPostInstallationSteps() {
    console.log('🔄 Después de la instalación:');
    console.log('1. Reinicia tu terminal/consola');
    console.log('2. Ejecuta: node install-ffmpeg.js para verificar la instalación');
    console.log('3. Si todo está bien, ejecuta: npm start para iniciar el servidor');
    console.log('');
}

function showDockerInstructions() {
    console.log('🐳 Alternativa con Docker:');
    console.log('   Si prefieres usar Docker, puedes usar una imagen con FFmpeg preinstalado:');
    console.log('');
    console.log('   Dockerfile ejemplo:');
    console.log('   FROM node:18-alpine');
    console.log('   RUN apk add --no-cache ffmpeg');
    console.log('   WORKDIR /app');
    console.log('   COPY package*.json ./');
    console.log('   RUN npm install');
    console.log('   COPY . .');
    console.log('   EXPOSE 3000');
    console.log('   CMD ["npm", "start"]');
    console.log('');
}

async function main() {
    const isInstalled = await checkFFmpegInstallation();
    
    if (!isInstalled) {
        showInstallationInstructions();
        showPostInstallationSteps();
        showDockerInstructions();
        
        console.log('💡 Notas importantes:');
        console.log('   - FFmpeg es necesario para el sistema de fábrica de videos');
        console.log('   - Sin FFmpeg, solo podrás subir clips pero no procesarlos');
        console.log('   - La instalación puede tomar unos minutos dependiendo de tu sistema');
        console.log('');
        
        process.exit(1);
    } else {
        console.log('🚀 ¡Todo listo! Puedes usar el sistema de videos completo.');
        console.log('');
        console.log('📖 Próximos pasos:');
        console.log('1. Ejecuta: npm start');
        console.log('2. Ve al dashboard: http://localhost:3000/dashboard');
        console.log('3. Accede a la pestaña "Fábrica de Videos"');
        console.log('4. ¡Empieza a crear contenido automáticamente!');
        console.log('');
    }
}

if (require.main === module) {
    main().catch(console.error);
}

module.exports = { checkFFmpegInstallation, showInstallationInstructions }; 