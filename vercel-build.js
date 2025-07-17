/**
 * Script de build para Vercel
 * Se ejecuta automáticamente al desplegar
 */

const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

console.log('🔧 Iniciando build para Vercel...');

// Crear directorio para la base de datos si no existe
const dbDir = path.join(__dirname, '.vercel/output/static');
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

// Crear directorio para shortcuts si no existe
const shortcutsDir = path.join(__dirname, 'shortcuts', 'files');
if (!fs.existsSync(shortcutsDir)) {
    fs.mkdirSync(shortcutsDir, { recursive: true });
}

console.log('✅ Directorios creados para Vercel');
console.log('🎉 Build completado exitosamente'); 