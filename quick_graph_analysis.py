#!/usr/bin/env python3
"""
Script rápido para análisis de grafos con muestra limitada.
Ideal para pruebas y demostraciones.

Autor: Proyecto Algoritmos UQ
"""

import os
import sys
import time
from datetime import datetime
import json

# Agregar el módulo de análisis de grafos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Graph_Analysis'))

from Graph_Analysis.simple_citation_graph import SimpleCitationGraph
from Graph_Analysis.simple_cooccurrence_graph import SimpleCooccurrenceGraph

def print_banner():
    """Imprime el banner del proyecto."""
    print("=" * 70)
    print("    ANÁLISIS RÁPIDO DE GRAFOS (MUESTRA LIMITADA)")
    print("    Proyecto Algoritmos - Universidad del Quindío")
    print("=" * 70)
    print()

def analyze_sample_citation_graph(sample_size: int = 100):
    """Analizar grafo de citaciones con muestra limitada."""
    print(f"\n📚 ANÁLISIS DE GRAFO DE CITACIONES (Muestra de {sample_size} artículos)")
    print("="*60)
    
    # Crear instancia del grafo de citaciones
    citation_graph = SimpleCitationGraph()
    citation_graph.similarity_threshold = 0.4  # Aumentar umbral para muestra pequeña
    
    # Cargar artículos
    print("📖 Cargando artículos...")
    citation_graph.load_articles_from_bibtex("Data/unificados.bib")
    
    # Limitar a una muestra
    article_ids = list(citation_graph.articles.keys())[:sample_size]
    citation_graph.articles = {aid: citation_graph.articles[aid] for aid in article_ids}
    print(f"✅ Muestra limitada a {len(citation_graph.articles)} artículos")
    
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
    nodes = list(citation_graph.articles.keys())
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
        print(f"  Tamaños: {sorted(scc_sizes, reverse=True)[:10]}")
    
    # Guardar grafo
    citation_graph.save_graph("Data/quick_citation_graph.json")
    
    return citation_graph

def analyze_sample_cooccurrence_graph(sample_size: int = 200):
    """Analizar grafo de coocurrencia con muestra limitada."""
    print(f"\n🔤 ANÁLISIS DE GRAFO DE COOCURRENCIA (Muestra de {sample_size} artículos)")
    print("="*60)
    
    # Crear instancia del grafo de coocurrencia
    cooccurrence_graph = SimpleCooccurrenceGraph(min_frequency=2, min_cooccurrence=1)
    
    # Cargar artículos
    print("📖 Cargando artículos...")
    cooccurrence_graph.load_articles_from_bibtex("Data/unificados.bib")
    
    # Limitar a una muestra
    article_ids = list(cooccurrence_graph.articles.keys())[:sample_size]
    cooccurrence_graph.articles = {aid: cooccurrence_graph.articles[aid] for aid in article_ids}
    print(f"✅ Muestra limitada a {len(cooccurrence_graph.articles)} artículos")
    
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
        return None
    
    # Obtener estadísticas
    stats = cooccurrence_graph.get_graph_statistics()
    print("\n📊 Estadísticas del grafo de coocurrencia:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Análisis de términos más conectados
    print("\n🔝 Términos más conectados:")
    top_terms = cooccurrence_graph.get_top_connected_terms(15)
    for i, (term, degree) in enumerate(top_terms, 1):
        print(f"  {i:2d}. {term}: {degree} conexiones")
    
    # Encontrar componentes conexas
    print("\n🔍 Buscando componentes conexas...")
    components = cooccurrence_graph.find_connected_components()
    
    # Analizar temas
    print("\n🎯 Análisis de temas:")
    themes = cooccurrence_graph.get_component_themes(components)
    
    print(f"  Temas identificados: {len(themes)}")
    for theme_id, theme_data in list(themes.items())[:3]:  # Mostrar solo los primeros 3
        print(f"    Tema {theme_id}: {theme_data['size']} términos")
        top_terms_str = [term for term, _ in theme_data['top_terms']]
        print(f"      Top términos: {', '.join(top_terms_str)}")
    
    # Guardar grafo
    cooccurrence_graph.save_graph("Data/quick_cooccurrence_graph.json")
    
    return cooccurrence_graph

def generate_quick_report(citation_graph, cooccurrence_graph):
    """Generar reporte rápido del análisis."""
    print("\n📋 GENERANDO REPORTE RÁPIDO")
    print("="*40)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'sample_analysis': True,
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
        'citation_relationships': sum(len(neighbors) for neighbors in citation_graph.graph.values()) if citation_graph else 0,
        'cooccurrence_relationships': sum(len(neighbors) for neighbors in cooccurrence_graph.graph.values()) // 2 if cooccurrence_graph else 0,
        'unique_terms': len(cooccurrence_graph.graph) if cooccurrence_graph else 0
    }
    
    # Guardar reporte
    with open('Data/quick_graph_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("✅ Reporte guardado en Data/quick_graph_analysis_report.json")
    
    # Mostrar resumen
    print("\n📊 RESUMEN DEL ANÁLISIS RÁPIDO:")
    print(f"  Artículos analizados: {report['summary']['total_articles_analyzed']}")
    print(f"  Relaciones de citación: {report['summary']['citation_relationships']}")
    print(f"  Relaciones de coocurrencia: {report['summary']['cooccurrence_relationships']}")
    print(f"  Términos únicos: {report['summary']['unique_terms']}")
    
    return report

def main():
    """Función principal."""
    print_banner()
    
    # Verificar entorno
    if not os.path.exists('Data/unificados.bib'):
        print("❌ Error: No se encontró el archivo Data/unificados.bib")
        print("   Ejecuta primero el script de unificación de datos")
        return
    
    start_time = time.time()
    
    # Análisis de grafo de citaciones (muestra pequeña)
    citation_graph = analyze_sample_citation_graph(50)
    
    # Análisis de grafo de coocurrencia (muestra pequeña)
    cooccurrence_graph = analyze_sample_cooccurrence_graph(100)
    
    # Generar reporte rápido
    report = generate_quick_report(citation_graph, cooccurrence_graph)
    
    end_time = time.time()
    
    print(f"\n🎉 Análisis rápido completado en {end_time - start_time:.2f} segundos")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n💡 Para análisis completo, ejecuta: python simple_graph_analysis.py")

if __name__ == "__main__":
    main()
