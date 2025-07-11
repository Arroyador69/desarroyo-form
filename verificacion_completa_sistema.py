#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 VERIFICACIÓN COMPLETA DEL SISTEMA
Diagnóstico exhaustivo de todos los componentes
"""

import os
import sqlite3
import json
import requests
import subprocess
import time
from datetime import datetime

def verificar_sistema_completo():
    """
    Verificación exhaustiva de todos los componentes
    """
    print("🔍 === VERIFICACIÓN COMPLETA DEL SISTEMA ===")
    print("📋 Revisando TODOS los componentes...")
    print("=" * 70)
    
    errores = []
    warnings = []
    
    # 1. VERIFICAR ARCHIVOS CRÍTICOS
    print("\n📄 === ARCHIVOS CRÍTICOS ===")
    archivos_criticos = {
        'package.json': 'Dependencias Node.js',
        'server.js': 'Servidor principal',
        'config.js': 'Configuración',
        'login.html': 'Página de login',
        'dashboard.html': 'Dashboard principal',
        'dashboard.db': 'Base de datos SQLite'
    }
    
    for archivo, descripcion in archivos_criticos.items():
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo)
            print(f"   ✅ {archivo}: {tamaño} bytes - {descripcion}")
        else:
            print(f"   ❌ {archivo}: FALTA - {descripcion}")
            errores.append(f"Archivo crítico faltante: {archivo}")
    
    # 2. VERIFICAR BASE DE DATOS
    print("\n🗄️ === BASE DE DATOS ===")
    if os.path.exists('dashboard.db'):
        try:
            conn = sqlite3.connect('dashboard.db')
            cursor = conn.cursor()
            
            # Verificar tabla users
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if cursor.fetchone():
                print("   ✅ Tabla 'users' existe")
                
                # Verificar usuario admin
                cursor.execute("SELECT username, email FROM users WHERE username='admin'")
                admin_user = cursor.fetchone()
                if admin_user:
                    print(f"   ✅ Usuario admin existe: {admin_user[0]} ({admin_user[1]})")
                else:
                    print("   ❌ Usuario admin NO existe")
                    errores.append("Usuario admin no encontrado en la base de datos")
            else:
                print("   ❌ Tabla 'users' NO existe")
                errores.append("Tabla users no existe en la base de datos")
            
            conn.close()
        except Exception as e:
            print(f"   ❌ Error accediendo a la base de datos: {e}")
            errores.append(f"Error base de datos: {e}")
    else:
        print("   ❌ dashboard.db NO existe")
        errores.append("Base de datos no existe")
    
    # 3. VERIFICAR DEPENDENCIAS NODE.JS
    print("\n📦 === DEPENDENCIAS NODE.JS ===")
    if os.path.exists('node_modules'):
        print("   ✅ Carpeta node_modules existe")
        
        # Verificar dependencias críticas
        deps_criticas = [
            'express', 'sqlite3', 'bcryptjs', 'jsonwebtoken', 
            'cors', 'multer', 'dotenv'
        ]
        
        for dep in deps_criticas:
            dep_path = f"node_modules/{dep}"
            if os.path.exists(dep_path):
                print(f"   ✅ {dep}: Instalado")
            else:
                print(f"   ❌ {dep}: FALTA")
                errores.append(f"Dependencia faltante: {dep}")
    else:
        print("   ❌ node_modules NO existe")
        errores.append("Dependencias no instaladas")
    
    # 4. VERIFICAR SERVIDOR
    print("\n🖥️ === ESTADO DEL SERVIDOR ===")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        print(f"   ✅ Servidor responde: {response.status_code}")
        
        # Test específico del login
        try:
            login_response = requests.get('http://localhost:3000/login.html', timeout=5)
            if login_response.status_code == 200:
                print("   ✅ Página login accesible")
                
                # Test del endpoint de login
                try:
                    api_response = requests.post(
                        'http://localhost:3000/api/dashboard/login',
                        json={'username': 'admin', 'password': 'DesArroyo2024!Seguro'},
                        timeout=5
                    )
                    print(f"   ✅ API login responde: {api_response.status_code}")
                    
                    if api_response.status_code == 200:
                        data = api_response.json()
                        if data.get('success'):
                            print("   ✅ Login API funciona correctamente")
                        else:
                            print(f"   ❌ Login falló: {data.get('error', 'Error desconocido')}")
                            errores.append(f"Login API error: {data.get('error')}")
                    else:
                        print(f"   ❌ Login API error HTTP: {api_response.status_code}")
                        try:
                            error_data = api_response.json()
                            print(f"       Error: {error_data}")
                        except:
                            print(f"       Error text: {api_response.text[:200]}")
                        errores.append(f"Login API HTTP {api_response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error probando login API: {e}")
                    errores.append(f"Login API error: {e}")
            else:
                print(f"   ❌ Página login error: {login_response.status_code}")
                errores.append(f"Login page HTTP {login_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error accediendo a login: {e}")
            errores.append(f"Login page error: {e}")
            
    except Exception as e:
        print(f"   ❌ Servidor NO responde: {e}")
        errores.append("Servidor no está corriendo")
    
    # 5. VERIFICAR PROCESOS
    print("\n⚙️ === PROCESOS ACTIVOS ===")
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        node_processes = [line for line in result.stdout.split('\n') if 'node' in line.lower() and 'server.js' in line]
        
        if node_processes:
            print(f"   ✅ Encontrados {len(node_processes)} procesos Node.js:")
            for proc in node_processes[:3]:  # Mostrar máximo 3
                print(f"       {proc.strip()}")
        else:
            print("   ⚠️ No se encontraron procesos Node.js con server.js")
            warnings.append("No hay procesos Node.js activos")
            
    except Exception as e:
        print(f"   ❌ Error verificando procesos: {e}")
    
    # 6. VERIFICAR PUERTOS
    print("\n🔌 === PUERTOS ===")
    try:
        result = subprocess.run(['lsof', '-i', ':3000'], capture_output=True, text=True)
        if result.stdout:
            print("   ✅ Puerto 3000 en uso:")
            for line in result.stdout.split('\n')[1:3]:  # Primeras 2 líneas después del header
                if line.strip():
                    print(f"       {line.strip()}")
        else:
            print("   ❌ Puerto 3000 NO está en uso")
            errores.append("Puerto 3000 no está ocupado")
    except Exception as e:
        print(f"   ⚠️ Error verificando puertos: {e}")
    
    # 7. VERIFICAR LOGS DE ERROR
    print("\n📝 === LOGS DEL SISTEMA ===")
    log_files = ['npm-debug.log', 'error.log', 'app.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    content = f.read()[-500:]  # Últimas 500 caracteres
                    if content.strip():
                        print(f"   ⚠️ {log_file} contiene errores:")
                        print(f"       ...{content[-100:]}")  # Últimas 100 chars
                        warnings.append(f"Errores en {log_file}")
            except Exception as e:
                print(f"   ❌ Error leyendo {log_file}: {e}")
    
    # 8. VERIFICAR CONFIGURACIÓN
    print("\n🔧 === CONFIGURACIÓN ===")
    try:
        with open('config.js', 'r') as f:
            config_content = f.read()
            
        if 'DesArroyo2024!Seguro' in config_content:
            print("   ✅ Contraseña segura configurada en config.js")
        else:
            print("   ❌ Contraseña segura NO encontrada en config.js")
            errores.append("Contraseña no actualizada en config.js")
            
        if 'admin' in config_content:
            print("   ✅ Usuario admin configurado")
        else:
            print("   ❌ Usuario admin NO configurado")
            errores.append("Usuario admin no configurado")
            
    except Exception as e:
        print(f"   ❌ Error leyendo config.js: {e}")
    
    # 9. TEST DE INICIO COMPLETO
    print("\n🚀 === TEST DE INICIO ===")
    print("   🔄 Intentando iniciar servidor...")
    
    try:
        # Verificar que npm start funciona
        result = subprocess.run(['npm', 'run', 'check'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ npm check exitoso")
        else:
            print(f"   ⚠️ npm check warning: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("   ⚠️ npm check timeout")
    except Exception as e:
        print(f"   ⚠️ Error npm check: {e}")
    
    # RESUMEN FINAL
    print("\n" + "=" * 70)
    print("🎯 === RESUMEN DIAGNÓSTICO ===")
    
    if not errores:
        print("✅ ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("🎯 Deberías poder acceder sin problemas")
    else:
        print(f"❌ ENCONTRADOS {len(errores)} ERRORES CRÍTICOS:")
        for i, error in enumerate(errores, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print(f"\n⚠️ {len(warnings)} ADVERTENCIAS:")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    # SOLUCIONES AUTOMÁTICAS
    print("\n🔧 === SOLUCIONES AUTOMÁTICAS ===")
    
    if not os.path.exists('node_modules'):
        print("🔄 Instalando dependencias...")
        subprocess.run(['npm', 'install'], check=False)
    
    if not os.path.exists('dashboard.db'):
        print("🔄 Inicializando base de datos...")
        subprocess.run(['node', 'scripts/reset-admin-password.js'], check=False)
    
    print(f"\n🕒 Diagnóstico completado: {datetime.now().strftime('%H:%M:%S')}")
    
    # INSTRUCCIONES ESPECÍFICAS
    print("\n📋 === INSTRUCCIONES ESPECÍFICAS ===")
    print("1. 🖥️ Abrir terminal y ejecutar: npm start")
    print("2. 🌐 Abrir navegador: http://localhost:3000/login.html")
    print("3. 🔑 Login: admin / DesArroyo2024!Seguro")
    print("4. 📱 Si no funciona, envía captura del error exacto")

if __name__ == "__main__":
    verificar_sistema_completo() 