#!/usr/bin/env python3
"""
Script principal para análisis de grafos de citaciones y coocurrencia.

Este script integra:
1. Grafo de citaciones (Requerimiento 1)
2. Grafo de coocurrencia de términos (Requerimiento 2)
3. Análisis de conectividad y centralidad
4. Generación de reportes detallados

Autor: Proyecto Algoritmos UQ
"""

import os
import sys
import time
from datetime import datetime
import json

# Agregar el módulo de análisis de grafos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Graph_Analysis'))

from Graph_Analysis.citation_graph import CitationGraph
from Graph_Analysis.cooccurrence_graph import CooccurrenceGraph

def print_banner():
    """Imprime el banner del proyecto."""
    print("=" * 70)
    print("    SISTEMA DE ANÁLISIS DE GRAFOS DE CITACIONES Y COOCURRENCIA")
    print("    Proyecto Algoritmos - Universidad del Quindío")
    print("=" * 70)
    print()

def check_environment():
    """Verifica que el entorno esté configurado correctamente."""
    print("🔍 Verificando configuración del entorno...")
    
    # Verificar archivo de datos
    if not os.path.exists('Data/unificados.bib'):
        print("❌ Error: No se encontró el archivo Data/unificados.bib")
        print("   Ejecuta primero el script de unificación de datos")
        return False
    
    # Verificar dependencias
    try:
        import networkx
        import numpy
        print("✅ Dependencias de grafos encontradas")
    except ImportError as e:
        print(f"❌ Error: Dependencias faltantes - {e}")
        print("   Ejecuta: pip install networkx numpy nltk")
        return False
    
    print("✅ Entorno configurado correctamente")
    return True

def analyze_citation_graph():
    """Analizar grafo de citaciones (Requerimiento 1)."""
    print("\n" + "="*50)
    print("📚 ANÁLISIS DE GRAFO DE CITACIONES (Requerimiento 1)")
    print("="*50)
    
    # Crear instancia del grafo de citaciones
    citation_graph = CitationGraph()
    
    # Cargar artículos
    print("📖 Cargando artículos...")
    citation_graph.load_articles_from_bibtex("Data/unificados.bib")
    
    # Construir grafo
    print("🔗 Construyendo grafo de citaciones...")
    edges_added = citation_graph.build_citation_graph()
    
    if edges_added == 0:
        print("⚠️  No se encontraron relaciones de citación significativas")
        print("   Considera ajustar el umbral de similitud")
        return None
    
    # Obtener estadísticas
    stats = citation_graph.get_graph_statistics()
    print("\n📊 Estadísticas del grafo de citaciones:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Análisis de caminos mínimos
    print("\n🛤️  Análisis de caminos mínimos...")
    
    # Calcular algunos caminos de ejemplo
    nodes = list(citation_graph.graph.nodes())
    if len(nodes) >= 2:
        source = nodes[0]
        target = nodes[1]
        
        path, distance = citation_graph.dijkstra_shortest_path(source, target)
        if path:
            print(f"  Camino de {source} a {target}: {len(path)} pasos, distancia: {distance:.3f}")
        else:
            print(f"  No hay camino de {source} a {target}")
    
    # Encontrar componentes fuertemente conexas
    print("\n🔗 Buscando componentes fuertemente conexas...")
    scc = citation_graph.find_strongly_connected_components()
    
    if scc:
        scc_sizes = [len(component) for component in scc]
        print(f"  Componente más grande: {max(scc_sizes)} artículos")
        print(f"  Número de componentes: {len(scc)}")
    
    # Guardar grafo
    citation_graph.save_graph("Data/citation_graph.json")
    
    return citation_graph

def analyze_cooccurrence_graph():
    """Analizar grafo de coocurrencia (Requerimiento 2)."""
    print("\n" + "="*50)
    print("🔤 ANÁLISIS DE GRAFO DE COOCURRENCIA (Requerimiento 2)")
    print("="*50)
    
    # Crear instancia del grafo de coocurrencia
    cooccurrence_graph = CooccurrenceGraph(min_frequency=3, min_cooccurrence=2)
    
    # Cargar artículos
    print("📖 Cargando artículos...")
    cooccurrence_graph.load_articles_from_bibtex("Data/unificados.bib")
    
    # Construir matriz de coocurrencia
    print("🔢 Construyendo matriz de coocurrencia...")
    terms_count = cooccurrence_graph.build_cooccurrence_matrix()
    
    if terms_count == 0:
        print("⚠️  No se encontraron términos suficientes para el análisis")
        return None
    
    # Construir grafo
    print("🕸️  Construyendo grafo de coocurrencia...")
    edges_added = cooccurrence_graph.build_cooccurrence_graph()
    
    if edges_added == 0:
        print("⚠️  No se encontraron coocurrencias significativas")
        print("   Considera ajustar los umbrales de frecuencia y coocurrencia")
        return None
    
    # Obtener estadísticas
    stats = cooccurrence_graph.get_graph_statistics()
    print("\n📊 Estadísticas del grafo de coocurrencia:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Análisis de términos más conectados
    print("\n🔝 Términos más conectados:")
    top_terms = cooccurrence_graph.get_top_connected_terms(20)
    for i, (term, degree) in enumerate(top_terms, 1):
        print(f"  {i:2d}. {term}: {degree} conexiones")
    
    # Encontrar componentes conexas
    print("\n🔍 Buscando componentes conexas...")
    components = cooccurrence_graph.find_connected_components()
    
    # Analizar temas
    print("\n🎯 Análisis de temas:")
    themes = cooccurrence_graph.get_component_themes(components)
    
    print(f"  Temas identificados: {len(themes)}")
    for theme_id, theme_data in list(themes.items())[:5]:  # Mostrar solo los primeros 5
        print(f"    Tema {theme_id}: {theme_data['size']} términos")
        top_terms_str = [term for term, _ in theme_data['top_terms']]
        print(f"      Top términos: {', '.join(top_terms_str)}")
    
    # Calcular medidas de centralidad
    print("\n📊 Calculando medidas de centralidad...")
    centrality = cooccurrence_graph.calculate_centrality_measures()
    
    if centrality.get('degree'):
        top_degree = sorted(centrality['degree'].items(), key=lambda x: x[1], reverse=True)[:5]
        print("  Top 5 términos por grado de centralidad:")
        for term, score in top_degree:
            print(f"    {term}: {score:.4f}")
    
    # Guardar grafo
    cooccurrence_graph.save_graph("Data/cooccurrence_graph.json")
    
    return cooccurrence_graph

def generate_comprehensive_report(citation_graph, cooccurrence_graph):
    """Generar reporte comprensivo del análisis."""
    print("\n" + "="*50)
    print("📋 GENERANDO REPORTE COMPRENSIVO")
    print("="*50)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'citation_graph': {},
        'cooccurrence_graph': {},
        'summary': {}
    }
    
    # Estadísticas del grafo de citaciones
    if citation_graph:
        report['citation_graph'] = {
            'statistics': citation_graph.get_graph_statistics(),
            'strongly_connected_components': len(citation_graph.find_strongly_connected_components())
        }
    
    # Estadísticas del grafo de coocurrencia
    if cooccurrence_graph:
        report['cooccurrence_graph'] = {
            'statistics': cooccurrence_graph.get_graph_statistics(),
            'top_terms': cooccurrence_graph.get_top_connected_terms(10),
            'connected_components': len(cooccurrence_graph.find_connected_components())
        }
    
    # Resumen general
    report['summary'] = {
        'total_articles_analyzed': len(citation_graph.articles) if citation_graph else 0,
        'citation_relationships': citation_graph.graph.number_of_edges() if citation_graph else 0,
        'cooccurrence_relationships': cooccurrence_graph.graph.number_of_edges() if cooccurrence_graph else 0,
        'unique_terms': cooccurrence_graph.graph.number_of_nodes() if cooccurrence_graph else 0
    }
    
    # Guardar reporte
    with open('Data/graph_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ Reporte guardado en Data/graph_analysis_report.json")
    
    # Mostrar resumen
    print("\n📊 RESUMEN DEL ANÁLISIS:")
    print(f"  Artículos analizados: {report['summary']['total_articles_analyzed']}")
    print(f"  Relaciones de citación: {report['summary']['citation_relationships']}")
    print(f"  Relaciones de coocurrencia: {report['summary']['cooccurrence_relationships']}")
    print(f"  Términos únicos: {report['summary']['unique_terms']}")
    
    return report

def main():
    """Función principal."""
    print_banner()
    
    # Verificar entorno
    if not check_environment():
        sys.exit(1)
    
    start_time = time.time()
    
    # Análisis de grafo de citaciones
    citation_graph = analyze_citation_graph()
    
    # Análisis de grafo de coocurrencia
    cooccurrence_graph = analyze_cooccurrence_graph()
    
    # Generar reporte comprensivo
    report = generate_comprehensive_report(citation_graph, cooccurrence_graph)
    
    end_time = time.time()
    
    print(f"\n🎉 Análisis de grafos completado en {end_time - start_time:.2f} segundos")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
