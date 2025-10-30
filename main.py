#!/usr/bin/env python3
"""
Script principal para ejecutar el proceso completo de descarga y unificación de bases de datos.

Este script:
1. Ejecuta los scrapers de ACM, IEEE y Sage
2. Unifica los resultados y detecta duplicados
3. Genera reportes de estadísticas

Autor: Proyecto Algoritmos UQ
"""

import os
import sys
import time
from datetime import datetime

# Agregar las carpetas del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Scraping'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Unificador_duplicador'))

def print_banner():
    """Imprime el banner del proyecto."""
    print("=" * 60)
    print("    SISTEMA DE DESCARGA Y UNIFICACIÓN DE BASES DE DATOS")
    print("    Proyecto Algoritmos - Universidad del Quindío")
    print("=" * 60)
    print()

def check_environment():
    """Verifica que el entorno esté configurado correctamente."""
    print("🔍 Verificando configuración del entorno...")
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("❌ Error: No se encontró el archivo .env")
        print("   Copia el archivo env.template como .env y configura tus credenciales")
        return False
    
    # Verificar dependencias
    try:
        import playwright
        from dotenv import load_dotenv
        print("✅ Dependencias encontradas")
    except ImportError as e:
        print(f"❌ Error: Dependencias faltantes - {e}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Entorno configurado correctamente")
    return True

def run_scrapers():
    """Ejecuta todos los scrapers."""
    print("\n📥 Iniciando descarga de bases de datos...")
    
    scrapers = [
        ("ACM Digital Library", "Scraping/ACM.py"),
        ("IEEE Xplore", "Scraping/IEE.py"),  # Nota: el archivo se llama IEE.py
        ("Sage Journals", "Scraping/Sage.py")
    ]
    
    for name, script_path in scrapers:
        print(f"\n🔄 Ejecutando scraper: {name}")
        start_time = time.time()
        
        try:
            # Importar y ejecutar el scraper
            if name == "ACM Digital Library":
                from Scraping.ACM import scrape_acm
                scrape_acm()
            elif name == "IEEE Xplore":
                from Scraping.IEE import scrape_ieee
                scrape_ieee()
            elif name == "Sage Journals":
                from Scraping.Sage import scrape_sage
                scrape_sage()
            
            elapsed_time = time.time() - start_time
            print(f"✅ {name} completado en {elapsed_time:.2f} segundos")
            
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
            return False
    
    return True

def unify_data():
    """Unifica los datos y detecta duplicados."""
    print("\n🔗 Unificando datos y detectando duplicados...")
    
    try:
        from Unificador_duplicador.Categorizacion import unify_results_from_files
        
        # Verificar que los archivos de datos existen
        data_files = [
            "Data/resultados_ACM.bib",
            "Data/resultados_ieee.bib", 
            "Data/resultados_Sage.bib"
        ]
        
        missing_files = [f for f in data_files if not os.path.exists(f)]
        if missing_files:
            print(f"❌ Archivos faltantes: {missing_files}")
            return False
        
        # Ejecutar unificación
        unify_results_from_files(*data_files)
        print("✅ Datos unificados correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en la unificación: {e}")
        return False

def generate_report():
    """Genera un reporte de estadísticas."""
    print("\n📊 Generando reporte de estadísticas...")
    
    try:
        # Contar artículos en cada archivo
        files_to_check = [
            ("ACM", "Data/resultados_ACM.bib"),
            ("IEEE", "Data/resultados_ieee.bib"),
            ("Sage", "Data/resultados_Sage.bib"),
            ("Unificados", "Data/unificados.bib"),
            ("Duplicados", "Data/duplicados.bib")
        ]
        
        print("\n" + "=" * 50)
        print("REPORTE DE ESTADÍSTICAS")
        print("=" * 50)
        
        total_articles = 0
        for name, filepath in files_to_check:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    count = content.count('@article{')
                    print(f"{name:12}: {count:>6} artículos")
                    if name != "Duplicados":
                        total_articles += count
            else:
                print(f"{name:12}: Archivo no encontrado")
        
        print("-" * 50)
        print(f"{'TOTAL':12}: {total_articles:>6} artículos únicos")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        return False

def main():
    """Función principal."""
    print_banner()
    
    # Verificar entorno
    if not check_environment():
        sys.exit(1)
    
    # Ejecutar scrapers
    if not run_scrapers():
        print("\n❌ Error en la descarga de datos")
        sys.exit(1)
    
    # Unificar datos
    if not unify_data():
        print("\n❌ Error en la unificación de datos")
        sys.exit(1)
    
    # Generar reporte
    if not generate_report():
        print("\n❌ Error generando reporte")
        sys.exit(1)
    
    print("\n🎉 ¡Proceso completado exitosamente!")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
