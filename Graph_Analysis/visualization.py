#!/usr/bin/env python3
"""
Sistema de visualización de grafos de citaciones y coocurrencia.

Este módulo implementa:
1. Visualización de grafos de citaciones
2. Visualización de grafos de coocurrencia
3. Análisis visual de componentes conexas
4. Generación de gráficos y reportes visuales

Autor: Proyecto Algoritmos UQ
"""

import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import os

class GraphVisualizer:
    """Clase para visualizar grafos de citaciones y coocurrencia."""
    
    def __init__(self):
        """Inicializar el visualizador."""
        plt.style.use('seaborn-v0_8')
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def visualize_citation_graph(self, citation_graph, max_nodes: int = 100, 
                                save_path: str = "Data/citation_graph_visualization.png"):
        """Visualizar grafo de citaciones."""
        print("🎨 Generando visualización del grafo de citaciones...")
        
        # Crear subgrafo si el grafo es muy grande
        if citation_graph.graph.number_of_nodes() > max_nodes:
            # Seleccionar nodos con mayor grado
            degrees = dict(citation_graph.graph.degree())
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
            subgraph_nodes = [node for node, _ in top_nodes]
            G = citation_graph.graph.subgraph(subgraph_nodes)
            print(f"  Mostrando subgrafo con {len(subgraph_nodes)} nodos más conectados")
        else:
            G = citation_graph.graph
        
        # Configurar la figura
        plt.figure(figsize=(15, 12))
        
        # Calcular layout
        try:
            pos = nx.spring_layout(G, k=1, iterations=50)
        except:
            pos = nx.random_layout(G)
        
        # Dibujar nodos
        node_sizes = [G.degree(node) * 50 + 100 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                             node_color='lightblue', alpha=0.7)
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='gray', arrows=True, 
                              arrowsize=20, arrowstyle='->')
        
        # Dibujar etiquetas (solo para nodos importantes)
        important_nodes = [node for node in G.nodes() if G.degree(node) > np.mean(list(dict(G.degree()).values()))]
        labels = {node: node[:10] + '...' if len(node) > 10 else node 
                 for node in important_nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Grafo de Citaciones\n(Tamaño del nodo = grado de conexión)", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # Guardar visualización
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Visualización guardada en {save_path}")
    
    def visualize_cooccurrence_graph(self, cooccurrence_graph, max_nodes: int = 100,
                                   save_path: str = "Data/cooccurrence_graph_visualization.png"):
        """Visualizar grafo de coocurrencia."""
        print("🎨 Generando visualización del grafo de coocurrencia...")
        
        # Crear subgrafo si el grafo es muy grande
        if cooccurrence_graph.graph.number_of_nodes() > max_nodes:
            # Seleccionar nodos con mayor grado
            degrees = dict(cooccurrence_graph.graph.degree())
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:max_nodes]
            subgraph_nodes = [node for node, _ in top_nodes]
            G = cooccurrence_graph.graph.subgraph(subgraph_nodes)
            print(f"  Mostrando subgrafo con {len(subgraph_nodes)} términos más conectados")
        else:
            G = cooccurrence_graph.graph
        
        # Configurar la figura
        plt.figure(figsize=(15, 12))
        
        # Calcular layout
        try:
            pos = nx.spring_layout(G, k=1, iterations=50)
        except:
            pos = nx.random_layout(G)
        
        # Dibujar nodos
        node_sizes = [G.degree(node) * 30 + 50 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                             node_color='lightcoral', alpha=0.7)
        
        # Dibujar aristas
        nx.draw_networkx_edges(G, pos, alpha=0.6, edge_color='gray', width=0.5)
        
        # Dibujar etiquetas (solo para términos importantes)
        important_nodes = [node for node in G.nodes() if G.degree(node) > np.mean(list(dict(G.degree()).values()))]
        labels = {node: node for node in important_nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Grafo de Coocurrencia de Términos\n(Tamaño del nodo = grado de conexión)", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # Guardar visualización
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"✅ Visualización guardada en {save_path}")
    
    def plot_degree_distribution(self, graph, graph_name: str, 
                                save_path: str = None):
        """Graficar distribución de grados."""
        print(f"📊 Generando distribución de grados para {graph_name}...")
        
        degrees = [d for n, d in graph.degree()]
        
        plt.figure(figsize=(10, 6))
        
        # Histograma
        plt.subplot(1, 2, 1)
        plt.hist(degrees, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('Grado del nodo')
        plt.ylabel('Frecuencia')
        plt.title(f'Distribución de Grados - {graph_name}')
        plt.grid(True, alpha=0.3)
        
        # Log-log plot
        plt.subplot(1, 2, 2)
        degree_counts = {}
        for degree in degrees:
            degree_counts[degree] = degree_counts.get(degree, 0) + 1
        
        degrees_sorted = sorted(degree_counts.keys())
        counts = [degree_counts[d] for d in degrees_sorted]
        
        plt.loglog(degrees_sorted, counts, 'bo-', alpha=0.7)
        plt.xlabel('Grado del nodo (log)')
        plt.ylabel('Frecuencia (log)')
        plt.title(f'Distribución Log-Log - {graph_name}')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado en {save_path}")
        
        plt.show()
    
    def plot_component_sizes(self, components: List[List], graph_name: str,
                           save_path: str = None):
        """Graficar distribución de tamaños de componentes."""
        print(f"📊 Generando distribución de componentes para {graph_name}...")
        
        component_sizes = [len(component) for component in components]
        component_sizes.sort(reverse=True)
        
        plt.figure(figsize=(12, 6))
        
        # Gráfico de barras
        plt.subplot(1, 2, 1)
        plt.bar(range(len(component_sizes)), component_sizes, 
               color='lightgreen', alpha=0.7, edgecolor='black')
        plt.xlabel('Componente (ordenada por tamaño)')
        plt.ylabel('Tamaño de la componente')
        plt.title(f'Tamaños de Componentes - {graph_name}')
        plt.grid(True, alpha=0.3)
        
        # Histograma de tamaños
        plt.subplot(1, 2, 2)
        plt.hist(component_sizes, bins=20, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Tamaño de la componente')
        plt.ylabel('Frecuencia')
        plt.title(f'Distribución de Tamaños - {graph_name}')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado en {save_path}")
        
        plt.show()
    
    def plot_centrality_measures(self, centrality_data: Dict, graph_name: str,
                               save_path: str = None):
        """Graficar medidas de centralidad."""
        print(f"📊 Generando medidas de centralidad para {graph_name}...")
        
        if not centrality_data:
            print("⚠️  No hay datos de centralidad disponibles")
            return
        
        # Preparar datos
        measures = list(centrality_data.keys())
        n_measures = len(measures)
        
        if n_measures == 0:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.flatten()
        
        for i, (measure, values) in enumerate(centrality_data.items()):
            if i >= 4:  # Máximo 4 gráficos
                break
            
            if not values:
                continue
            
            # Obtener top 20 valores
            sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)[:20]
            terms, scores = zip(*sorted_values)
            
            axes[i].bar(range(len(terms)), scores, color=self.colors[i % len(self.colors)], alpha=0.7)
            axes[i].set_xlabel('Términos')
            axes[i].set_ylabel(f'Centralidad {measure}')
            axes[i].set_title(f'{measure.title()} Centrality - Top 20')
            axes[i].set_xticks(range(len(terms)))
            axes[i].set_xticklabels(terms, rotation=45, ha='right')
            axes[i].grid(True, alpha=0.3)
        
        # Ocultar subplots vacíos
        for i in range(n_measures, 4):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Gráfico guardado en {save_path}")
        
        plt.show()
    
    def generate_comprehensive_visualization(self, citation_graph=None, cooccurrence_graph=None):
        """Generar visualización comprensiva de ambos grafos."""
        print("🎨 Generando visualizaciones comprensivas...")
        
        # Crear directorio para visualizaciones
        os.makedirs("Data/visualizations", exist_ok=True)
        
        if citation_graph:
            # Visualizar grafo de citaciones
            self.visualize_citation_graph(
                citation_graph, 
                save_path="Data/visualizations/citation_graph.png"
            )
            
            # Distribución de grados
            self.plot_degree_distribution(
                citation_graph.graph,
                "Grafo de Citaciones",
                save_path="Data/visualizations/citation_degree_distribution.png"
            )
            
            # Componentes fuertemente conexas
            scc = citation_graph.find_strongly_connected_components()
            if scc:
                self.plot_component_sizes(
                    scc,
                    "Componentes Fuertemente Conexas",
                    save_path="Data/visualizations/citation_components.png"
                )
        
        if cooccurrence_graph:
            # Visualizar grafo de coocurrencia
            self.visualize_cooccurrence_graph(
                cooccurrence_graph,
                save_path="Data/visualizations/cooccurrence_graph.png"
            )
            
            # Distribución de grados
            self.plot_degree_distribution(
                cooccurrence_graph.graph,
                "Grafo de Coocurrencia",
                save_path="Data/visualizations/cooccurrence_degree_distribution.png"
            )
            
            # Componentes conexas
            components = cooccurrence_graph.find_connected_components()
            if components:
                self.plot_component_sizes(
                    components,
                    "Componentes Conexas",
                    save_path="Data/visualizations/cooccurrence_components.png"
                )
            
            # Medidas de centralidad
            centrality = cooccurrence_graph.calculate_centrality_measures()
            if centrality:
                self.plot_centrality_measures(
                    centrality,
                    "Grafo de Coocurrencia",
                    save_path="Data/visualizations/cooccurrence_centrality.png"
                )
        
        print("✅ Visualizaciones completadas")

def main():
    """Función principal para probar las visualizaciones."""
    print("🎨 Iniciando sistema de visualización...")
    
    # Cargar grafos existentes
    citation_graph = None
    cooccurrence_graph = None
    
    # Cargar grafo de citaciones
    if os.path.exists("Data/citation_graph.json"):
        from Graph_Analysis.citation_graph import CitationGraph
        citation_graph = CitationGraph()
        citation_graph.load_graph("Data/citation_graph.json")
        print("✅ Grafo de citaciones cargado")
    
    # Cargar grafo de coocurrencia
    if os.path.exists("Data/cooccurrence_graph.json"):
        from Graph_Analysis.cooccurrence_graph import CooccurrenceGraph
        cooccurrence_graph = CooccurrenceGraph()
        cooccurrence_graph.load_graph("Data/cooccurrence_graph.json")
        print("✅ Grafo de coocurrencia cargado")
    
    if not citation_graph and not cooccurrence_graph:
        print("❌ No se encontraron grafos para visualizar")
        print("   Ejecuta primero graph_analysis_main.py")
        return
    
    # Generar visualizaciones
    visualizer = GraphVisualizer()
    visualizer.generate_comprehensive_visualization(citation_graph, cooccurrence_graph)
    
    print("✅ Visualizaciones completadas")

if __name__ == "__main__":
    main()
