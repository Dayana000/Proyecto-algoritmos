#!/usr/bin/env python3
"""
Script de verificación de instalación y configuración del proyecto.

Este script verifica:
1. Versión de Python
2. Dependencias instaladas
3. Playwright y navegadores
4. Recursos de NLTK
5. Archivo .env y credenciales
6. Estructura de carpetas

Autor: Proyecto Algoritmos UQ
"""

import sys
import os

def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Verifica la versión de Python."""
    print_header("VERIFICANDO PYTHON")
    version = sys.version_info
    print(f"Versión de Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Versión de Python compatible (3.7+)")
        return True
    else:
        print("❌ Versión de Python incompatible. Se requiere Python 3.7+")
        return False

def check_dependencies():
    """Verifica que las dependencias estén instaladas."""
    print_header("VERIFICANDO DEPENDENCIAS")
    
    dependencies = {
        'playwright': 'Playwright',
        'dotenv': 'python-dotenv',
        'networkx': 'NetworkX',
        'nltk': 'NLTK',
        'matplotlib': 'Matplotlib',
        'seaborn': 'Seaborn'
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} instalado")
        except ImportError:
            print(f"❌ {name} NO instalado")
            all_ok = False
    
    return all_ok

def check_playwright():
    """Verifica que Playwright y los navegadores estén instalados."""
    print_header("VERIFICANDO PLAYWRIGHT")
    
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright instalado")
        
        # Verificar navegadores
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=True)
                    browser.close()
                    print("✅ Chromium instalado y funcionando")
                    return True
                except Exception as e:
                    print(f"⚠️  Chromium instalado pero hay un problema: {e}")
                    print("   Ejecuta: playwright install")
                    return False
        except Exception as e:
            print(f"❌ Error al verificar Chromium: {e}")
            print("   Ejecuta: playwright install chromium")
            return False
    except ImportError:
        print("❌ Playwright NO instalado")
        print("   Ejecuta: pip install playwright")
        print("   Luego: playwright install")
        return False

def check_nltk_resources():
    """Verifica que los recursos de NLTK estén descargados."""
    print_header("VERIFICANDO RECURSOS DE NLTK")
    
    try:
        import nltk
        
        resources = ['stopwords', 'punkt']
        all_ok = True
        
        for resource in resources:
            try:
                if resource == 'stopwords':
                    from nltk.corpus import stopwords
                    stopwords.words('english')
                    print(f"✅ Recurso '{resource}' disponible")
                elif resource == 'punkt':
                    from nltk.tokenize import word_tokenize
                    word_tokenize("test")
                    print(f"✅ Recurso '{resource}' disponible")
            except LookupError:
                print(f"❌ Recurso '{resource}' NO disponible")
                print(f"   Ejecuta: python -c \"import nltk; nltk.download('{resource}')\"")
                all_ok = False
        
        return all_ok
    except ImportError:
        print("❌ NLTK NO instalado")
        return False

def check_env_file():
    """Verifica que el archivo .env exista y tenga las credenciales."""
    print_header("VERIFICANDO ARCHIVO .env")
    
    if not os.path.exists('.env'):
        print("❌ Archivo .env NO encontrado")
        print("   Copia env.template como .env y configura tus credenciales")
        return False
    
    print("✅ Archivo .env encontrado")
    
    # Verificar contenido
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if not email_user or email_user == 'tu_email@ejemplo.com':
            print("⚠️  EMAIL_USER no configurado o usa valor por defecto")
            print("   Edita el archivo .env y configura tu email institucional")
        else:
            print(f"✅ EMAIL_USER configurado: {email_user[:20]}...")
        
        if not email_password or email_password == 'tu_contraseña_de_aplicacion':
            print("⚠️  EMAIL_PASSWORD no configurado o usa valor por defecto")
            print("   Edita el archivo .env y configura tu contraseña de aplicación de Google")
        else:
            print("✅ EMAIL_PASSWORD configurado")
        
        if email_user and email_password and email_user != 'tu_email@ejemplo.com' and email_password != 'tu_contraseña_de_aplicacion':
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️  Error al leer .env: {e}")
        return False

def check_folder_structure():
    """Verifica que la estructura de carpetas esté correcta."""
    print_header("VERIFICANDO ESTRUCTURA DE CARPETAS")
    
    required_folders = ['Scraping', 'Unificador_duplicador', 'Graph_Analysis', 'Data']
    all_ok = True
    
    for folder in required_folders:
        if os.path.exists(folder):
            print(f"✅ Carpeta '{folder}' existe")
        else:
            print(f"⚠️  Carpeta '{folder}' NO existe (se creará automáticamente)")
    
    return True

def check_data_files():
    """Verifica si existen archivos de datos."""
    print_header("VERIFICANDO ARCHIVOS DE DATOS")
    
    data_files = [
        'Data/resultados_ACM.bib',
        'Data/resultados_ieee.bib',
        'Data/resultados_Sage.bib',
        'Data/unificados.bib'
    ]
    
    found_files = []
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} existe ({size:,} bytes)")
            found_files.append(file)
        else:
            print(f"ℹ️  {file} no existe (se generará al ejecutar el scraping)")
    
    if found_files:
        print(f"\n📊 Se encontraron {len(found_files)} archivo(s) de datos")
        return True
    else:
        print("\n💡 Ejecuta 'python main.py' para generar los archivos de datos")
        return True

def main():
    """Función principal de verificación."""
    print("\n" + "=" * 60)
    print("  VERIFICACIÓN DE INSTALACIÓN Y CONFIGURACIÓN")
    print("  Proyecto Algoritmos - Universidad del Quindío")
    print("=" * 60)
    
    results = {
        'Python': check_python_version(),
        'Dependencias': check_dependencies(),
        'Playwright': check_playwright(),
        'NLTK': check_nltk_resources(),
        'Archivo .env': check_env_file(),
        'Estructura': check_folder_structure(),
        'Datos': check_data_files()
    }
    
    # Resumen final
    print_header("RESUMEN")
    
    all_ok = all(results.values())
    passed = sum(results.values())
    total = len(results)
    
    for check, result in results.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    print(f"\n{'=' * 60}")
    print(f"Resultado: {passed}/{total} verificaciones pasadas")
    
    if all_ok:
        print("\n🎉 ¡Todo está configurado correctamente!")
        print("💡 Puedes ejecutar: python main.py")
    else:
        print("\n⚠️  Hay problemas que debes resolver antes de ejecutar el proyecto")
        print("💡 Revisa los mensajes anteriores y sigue las instrucciones")
        print("\n📖 Consulta GUIA_INSTALACION.md para más detalles")
    
    print("=" * 60 + "\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())

