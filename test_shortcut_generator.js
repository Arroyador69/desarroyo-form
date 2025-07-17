#!/usr/bin/env node

/**
 * 🧪 Test del Generador de Shortcuts - DesArroyo.tech
 * Script para probar la generación de shortcuts de iPhone
 */

require('dotenv').config();
const ShortcutGenerator = require('./scripts/shortcut-generator');

async function testShortcutGenerator() {
    console.log('🧪 Iniciando test del generador de shortcuts...\n');
    
    const generator = new ShortcutGenerator();
    
    try {
        await generator.init();
        console.log('✅ Generador inicializado correctamente\n');
        
        // Test 1: Scanner de Documentos
        console.log('📱 Test 1: Scanner de Documentos');
        const scannerShortcut = await generator.generateSuperpowerShortcut(
            'Scanner de Documentos',
            'Escanea documentos automáticamente y los convierte en PDF. Perfecto para facturas, contratos y cualquier documento importante.',
            'voice',
            'Escanea documento'
        );
        
        console.log('✅ Scanner shortcut creado:');
        console.log(`   Nombre: ${scannerShortcut.name}`);
        console.log(`   Enlace: ${scannerShortcut.shortcut_url}`);
        console.log(`   QR Code: ${scannerShortcut.qr_code}\n`);
        
        // Test 2: Traductor Instantáneo
        console.log('🌍 Test 2: Traductor Instantáneo');
        const translatorShortcut = await generator.generateSuperpowerShortcut(
            'Traductor Instantáneo',
            'Traduce texto instantáneamente entre múltiples idiomas. Ideal para viajes y comunicación internacional.',
            'voice',
            'Traduce esto'
        );
        
        console.log('✅ Traductor shortcut creado:');
        console.log(`   Nombre: ${translatorShortcut.name}`);
        console.log(`   Enlace: ${translatorShortcut.shortcut_url}`);
        console.log(`   QR Code: ${translatorShortcut.qr_code}\n`);
        
        // Test 3: Calculadora Rápida
        console.log('🧮 Test 3: Calculadora Rápida');
        const calculatorShortcut = await generator.generateSuperpowerShortcut(
            'Calculadora Rápida',
            'Realiza cálculos complejos con solo tu voz. Perfecto para matemáticas rápidas y conversiones.',
            'voice',
            'Calcula'
        );
        
        console.log('✅ Calculadora shortcut creado:');
        console.log(`   Nombre: ${calculatorShortcut.name}`);
        console.log(`   Enlace: ${calculatorShortcut.shortcut_url}`);
        console.log(`   QR Code: ${calculatorShortcut.qr_code}\n`);
        
        // Test 4: Recordatorio por Voz
        console.log('🎤 Test 4: Recordatorio por Voz');
        const reminderShortcut = await generator.generateSuperpowerShortcut(
            'Recordatorio por Voz',
            'Crea recordatorios rápidos usando solo tu voz. Nunca más olvides una tarea importante.',
            'voice',
            'Recuérdame'
        );
        
        console.log('✅ Recordatorio shortcut creado:');
        console.log(`   Nombre: ${reminderShortcut.name}`);
        console.log(`   Enlace: ${reminderShortcut.shortcut_url}`);
        console.log(`   QR Code: ${reminderShortcut.qr_code}\n`);
        
        // Generar reporte final
        console.log('📊 Generando reporte final...');
        const report = await generator.generateReport();
        
        console.log('📈 Reporte de Shortcuts:');
        console.log(`   Total creados: ${report.total_shortcuts}`);
        console.log(`   Por tipo: ${JSON.stringify(report.shortcuts_by_type, null, 2)}`);
        console.log(`   Recientes: ${report.recent_shortcuts.length} shortcuts\n`);
        
        // Mostrar todos los shortcuts
        console.log('📋 Lista completa de shortcuts:');
        const allShortcuts = await generator.getAllShortcuts();
        allShortcuts.forEach((shortcut, index) => {
            console.log(`   ${index + 1}. ${shortcut.name}`);
            console.log(`      Descripción: ${shortcut.description}`);
            console.log(`      Enlace: ${shortcut.shortcut_url}`);
            console.log(`      Creado: ${new Date(shortcut.created_at).toLocaleString()}\n`);
        });
        
        console.log('🎉 ¡Todos los tests completados exitosamente!');
        console.log('\n📱 Para usar los shortcuts:');
        console.log('   1. Copia el enlace del shortcut');
        console.log('   2. Ábrelo en tu iPhone');
        console.log('   3. Confirma la instalación');
        console.log('   4. ¡Disfruta del superpoder!\n');
        
        console.log('🔗 Enlaces directos para copiar:');
        allShortcuts.forEach((shortcut, index) => {
            console.log(`   ${index + 1}. ${shortcut.name}:`);
            console.log(`      ${shortcut.shortcut_url}`);
        });
        
    } catch (error) {
        console.error('❌ Error en el test:', error);
    } finally {
        generator.close();
        console.log('\n✅ Test finalizado');
    }
}

// Ejecutar el test
testShortcutGenerator(); 