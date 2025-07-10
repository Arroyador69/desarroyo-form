/**
 * 🔧 FIX DASHBOARD FRONTEND
 * Script para corregir problemas comunes del JavaScript del dashboard
 */

console.log('🔧 === INICIANDO FIX DASHBOARD FRONTEND ===');

// 1. UNIFICAR TOKENS
function unifyTokens() {
    console.log('🔑 Unificando tokens...');
    
    const dashboardToken = localStorage.getItem('dashboard_token');
    const token = localStorage.getItem('token');
    
    if (dashboardToken && !token) {
        localStorage.setItem('token', dashboardToken);
        console.log('✅ Token unificado: dashboard_token → token');
    } else if (token && !dashboardToken) {
        localStorage.setItem('dashboard_token', token);
        console.log('✅ Token unificado: token → dashboard_token');
    }
}

// 2. VERIFICAR AUTENTICACIÓN
function checkAuth() {
    console.log('🔐 Verificando autenticación...');
    
    const token = localStorage.getItem('dashboard_token');
    if (!token) {
        console.error('❌ No hay token de autenticación');
        return false;
    }
    
    console.log('✅ Token encontrado:', token.substring(0, 20) + '...');
    return true;
}

// 3. MEJORAR FETCH CON ERROR HANDLING
function createSafeFetch(url, options = {}) {
    const token = localStorage.getItem('dashboard_token');
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers
        },
        ...options
    };
    
    console.log(`🌐 Fetch seguro a: ${url}`);
    
    return fetch(url, defaultOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error(`❌ Error en ${url}:`, error);
            throw error;
        });
}

// 4. CORREGIR BOTONES PROBLEMÁTICOS
function fixButtons() {
    console.log('🔘 Corrigiendo botones...');
    
    // Buscar botones con @click que pueden tener problemas
    const buttons = document.querySelectorAll('button[x-text], button[x-show]');
    console.log(`🔍 Encontrados ${buttons.length} botones Alpine.js`);
    
    // Agregar event listeners de respaldo
    buttons.forEach((button, index) => {
        button.addEventListener('click', function(event) {
            console.log(`🔘 Click en botón ${index}:`, button.outerHTML.substring(0, 100));
        });
    });
}

// 5. DIAGNOSTICAR PROBLEMAS COMUNES
function diagnosticCommonIssues() {
    console.log('🔍 Diagnosticando problemas comunes...');
    
    // Alpine.js cargado?
    if (typeof Alpine === 'undefined') {
        console.error('❌ Alpine.js no está cargado');
    } else {
        console.log('✅ Alpine.js disponible');
    }
    
    // Dashboard data función existe?
    if (typeof dashboardData === 'undefined') {
        console.error('❌ Función dashboardData no definida');
    } else {
        console.log('✅ Función dashboardData disponible');
    }
    
    // Token válido?
    const token = localStorage.getItem('dashboard_token');
    if (!token) {
        console.error('❌ Token de dashboard faltante');
    } else {
        console.log('✅ Token de dashboard presente');
    }
}

// 6. INTERCEPTAR ERRORES
function setupErrorInterception() {
    console.log('🚨 Configurando interceptor de errores...');
    
    window.addEventListener('error', function(event) {
        console.error('🚨 ERROR JAVASCRIPT:', event.error);
        console.error('📍 Archivo:', event.filename);
        console.error('📍 Línea:', event.lineno);
    });
    
    window.addEventListener('unhandledrejection', function(event) {
        console.error('🚨 PROMISE RECHAZADA:', event.reason);
    });
}

// 7. HELPER PARA DEBUGGING
function debugDashboard() {
    console.log('🔍 === DEBUG DASHBOARD ===');
    console.log('🔑 Tokens:', {
        dashboard_token: localStorage.getItem('dashboard_token')?.substring(0, 20) + '...',
        token: localStorage.getItem('token')?.substring(0, 20) + '...',
        user: localStorage.getItem('dashboard_user') ? 'Presente' : 'Faltante'
    });
    
    console.log('🌐 Estado página:', {
        url: window.location.href,
        alpine: typeof Alpine !== 'undefined',
        dashboardData: typeof dashboardData !== 'undefined'
    });
}

// 8. EJECUTAR TODAS LAS CORRECCIONES
function runAllFixes() {
    try {
        unifyTokens();
        checkAuth();
        setupErrorInterception();
        diagnosticCommonIssues();
        debugDashboard();
        
        // Esperar a que Alpine.js esté listo
        document.addEventListener('alpine:init', () => {
            console.log('✅ Alpine.js inicializado');
            fixButtons();
        });
        
        console.log('✅ === FIX COMPLETADO ===');
    } catch (error) {
        console.error('❌ Error ejecutando fixes:', error);
    }
}

// EXPORTAR FUNCIONES PARA USO GLOBAL
window.dashboardFix = {
    unifyTokens,
    checkAuth,
    createSafeFetch,
    debugDashboard,
    runAllFixes
};

// EJECUTAR AUTOMÁTICAMENTE
runAllFixes(); 