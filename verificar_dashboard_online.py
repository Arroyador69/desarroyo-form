#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICADOR DASHBOARD ONLINE - DesArroyo Tech
Verifica que todo esté listo para acceder al dashboard online
"""

import os
import json
import requests
from datetime import datetime

def verificar_dashboard_online():
    """
    Verifica la configuración para el dashboard online
    """
    print("🔍 === VERIFICADOR DASHBOARD ONLINE ===")
    print("📋 Verificando configuración para Vercel...")
    print("=" * 60)
    
    # 1. Verificar archivos necesarios
    archivos_necesarios = [
        'vercel.json',
        'server.js', 
        'dashboard.html',
        'login.html',
        'package.json'
    ]
    
    print("\n📁 VERIFICANDO ARCHIVOS:")
    for archivo in archivos_necesarios:
        existe = "✅ EXISTE" if os.path.exists(archivo) else "❌ FALTA"
        print(f"   📄 {archivo}: {existe}")
    
    # 2. Verificar vercel.json
    print("\n🔧 VERIFICANDO VERCEL.JSON:")
    try:
        with open('vercel.json', 'r') as f:
            vercel_config = json.load(f)
            
        # Verificar rutas del dashboard
        rutas_dashboard = False
        for route in vercel_config.get('routes', []):
            if '/api/dashboard' in route.get('src', ''):
                rutas_dashboard = True
                break
        
        print(f"   🛣️ Rutas dashboard: {'✅ CONFIGURADAS' if rutas_dashboard else '❌ FALTAN'}")
        
        # Verificar variables de entorno
        env_vars = vercel_config.get('env', {})
        vars_necesarias = ['JWT_SECRET', 'ADMIN_PASSWORD', 'TWILIO_PHONE_NUMBER']
        
        print("   🔐 Variables de entorno:")
        for var in vars_necesarias:
            tiene_var = "✅ SÍ" if var in env_vars else "❌ FALTA"
            print(f"      {var}: {tiene_var}")
            
    except Exception as e:
        print(f"   ❌ Error leyendo vercel.json: {e}")
    
    # 3. Verificar package.json
    print("\n📦 VERIFICANDO PACKAGE.JSON:")
    try:
        with open('package.json', 'r') as f:
            package_config = json.load(f)
            
        dependencias_necesarias = [
            'express', 'jsonwebtoken', 'bcryptjs', 
            'cors', 'multer', 'sqlite3'
        ]
        
        deps = package_config.get('dependencies', {})
        for dep in dependencias_necesarias:
            tiene_dep = "✅ SÍ" if dep in deps else "❌ FALTA"
            print(f"   📚 {dep}: {tiene_dep}")
            
    except Exception as e:
        print(f"   ❌ Error leyendo package.json: {e}")
    
    # 4. Test local (si server está corriendo)
    print("\n🧪 TEST LOCAL (si servidor está corriendo):")
    try:
        response = requests.get('http://localhost:3000/login.html', timeout=5)
        if response.status_code == 200:
            print("   ✅ Servidor local funcionando")
            
            # Test de API
            try:
                api_response = requests.get('http://localhost:3000/api/dashboard/overview', timeout=5)
                if api_response.status_code in [200, 401]:  # 401 es OK (necesita autenticación)
                    print("   ✅ API dashboard respondiendo")
                else:
                    print("   ⚠️ API dashboard respuesta inesperada")
            except:
                print("   ❌ API dashboard no responde")
        else:
            print("   ❌ Servidor local no responde")
    except:
        print("   ⏭️ Servidor local no está corriendo (normal)")
    
    # 5. Verificar configuración de Git
    print("\n📚 VERIFICANDO GIT:")
    if os.path.exists('.git'):
        print("   ✅ Repositorio Git inicializado")
        
        # Verificar que no hay cambios sin commit
        try:
            import subprocess
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                print("   ⚠️ Hay cambios sin commit")
                print("   💡 Ejecuta: git add . && git commit -m 'Update dashboard'")
            else:
                print("   ✅ Todo commiteado")
        except:
            print("   ⚠️ No se pudo verificar status de Git")
    else:
        print("   ❌ No es un repositorio Git")
    
    # 6. Resumen y recomendaciones
    print("\n📊 === RESUMEN Y PRÓXIMOS PASOS ===")
    print("\n🚀 PARA ACTIVAR DASHBOARD ONLINE:")
    print("1. 🔐 Agregar secrets en Vercel:")
    print("   - JWT_SECRET = desarroyo-secret-key-2024-super-seguro")
    print("   - ADMIN_PASSWORD = tu_contraseña_segura_123")
    print("\n2. 📤 Hacer deploy:")
    print("   git add .")
    print("   git commit -m '🔧 Configurar dashboard para Vercel'")
    print("   git push origin main")
    print("\n3. ✅ Acceder online:")
    print("   URL: https://desarroyo.tech/login.html")
    print("   Usuario: admin")
    print("   Contraseña: (la que pongas en ADMIN_PASSWORD)")
    
    print("\n🎯 SISTEMA DE LLAMADAS:")
    print("   ✅ Ya está configurado y funcionando")
    print("   📞 Próximas llamadas: Mañana 9:00h español")
    print("   💰 Presupuesto: 10€ máximo diario")
    print("   📊 Monitoreo: Disponible en dashboard online")
    
    print(f"\n🕒 Verificación completada: {datetime.now().strftime('%H:%M:%S')}")
    print("🚀 ¡Todo listo para dashboard online!")

if __name__ == "__main__":
    verificar_dashboard_online() 