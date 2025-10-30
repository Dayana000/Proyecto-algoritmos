#!/usr/bin/env python3
"""
Sistema de análisis de grafos de citaciones.

Este módulo implementa:
1. Construcción de grafo de citaciones basado en similitud de títulos, autores y palabras clave
2. Algoritmos de caminos mínimos (Dijkstra y Floyd-Warshall)
3. Detección de componentes fuertemente conexas
4. Análisis de conectividad en la red

Autor: Proyecto Algoritmos UQ
"""

import networkx as nx
import numpy as np
from collections import defaultdict
import re
import math
from typing import Dict, List, Tuple, Set, Optional
import json
import os

class CitationGraph:
    """Clase para manejar el grafo de citaciones."""
    
    def __init__(self):
        """Inicializar el grafo de citaciones."""
        self.graph = nx.DiGraph()
        self.articles = {}
        self.similarity_threshold = 0.3  # Umbral de similitud para considerar citación
        
    def load_articles_from_bibtex(self, bibtex_file: str):
        """Cargar artículos desde archivo BibTeX."""
        print(f"📖 Cargando artículos desde {bibtex_file}...")
        
        with open(bibtex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parsear artículos del archivo BibTeX
        articles = self._parse_bibtex(content)
        
        for article in articles:
            article_id = article.get('id', f"ref{len(self.articles)}")
            self.articles[article_id] = article
            self.graph.add_node(article_id, **article)
        
        print(f"✅ Cargados {len(self.articles)} artículos")
        return len(self.articles)
    
    def _parse_bibtex(self, content: str) -> List[Dict]:
        """Parsear contenido BibTeX."""
        articles = []
        current_article = {}
        in_article = False
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('@article{'):
                if current_article:
                    articles.append(current_article)
                current_article = {'id': line.split('{')[1].split(',')[0]}
                in_article = True
            elif line == '}' and in_article:
                if current_article:
                    articles.append(current_article)
                current_article = {}
                in_article = False
            elif '=' in line and in_article:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('{}').strip(',').strip()
                current_article[key] = value
        
        return articles
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calcular similitud entre dos textos usando Jaccard."""
        if not text1 or not text2:
            return 0.0
        
        # Normalizar textos
        text1 = re.sub(r'[^\w\s]', '', text1.lower())
        text2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        # Obtener conjuntos de palabras
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Calcular similitud de Jaccard
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_author_similarity(self, authors1: str, authors2: str) -> float:
        """Calcular similitud entre listas de autores."""
        if not authors1 or not authors2:
            return 0.0
        
        # Normalizar nombres de autores
        def normalize_authors(authors_str):
            authors = [author.strip().lower() for author in authors_str.split(',')]
            return set(authors)
        
        authors1_set = normalize_authors(authors1)
        authors2_set = normalize_authors(authors2)
        
        if not authors1_set or not authors2_set:
            return 0.0
        
        intersection = len(authors1_set.intersection(authors2_set))
        union = len(authors1_set.union(authors2_set))
        
        return intersection / union if union > 0 else 0.0
    
    def build_citation_graph(self):
        """Construir el grafo de citaciones basado en similitud."""
        print("🔗 Construyendo grafo de citaciones...")
        
        article_ids = list(self.articles.keys())
        edges_added = 0
        
        for i, article1_id in enumerate(article_ids):
            if i % 100 == 0:
                print(f"  Procesando artículo {i+1}/{len(article_ids)}")
            
            article1 = self.articles[article1_id]
            
            for j, article2_id in enumerate(article_ids):
                if i == j:
                    continue
                
                article2 = self.articles[article2_id]
                
                # Calcular similitudes
                title_sim = self._calculate_text_similarity(
                    article1.get('title', ''), 
                    article2.get('title', '')
                )
                
                author_sim = self._calculate_author_similarity(
                    article1.get('author', ''), 
                    article2.get('author', '')
                )
                
                abstract_sim = self._calculate_text_similarity(
                    article1.get('abstract', ''), 
                    article2.get('abstract', '')
                )
                
                # Peso combinado (título tiene más peso)
                combined_similarity = (
                    0.5 * title_sim + 
                    0.3 * author_sim + 
                    0.2 * abstract_sim
                )
                
                # Si la similitud supera el umbral, crear arista
                if combined_similarity > self.similarity_threshold:
                    # Determinar dirección basada en año (artículo más reciente cita al más antiguo)
                    year1 = int(article1.get('year', '0')) if article1.get('year', '0').isdigit() else 0
                    year2 = int(article2.get('year', '0')) if article2.get('year', '0').isdigit() else 0
                    
                    if year1 > year2:
                        # article1 cita a article2
                        self.graph.add_edge(article1_id, article2_id, 
                                         weight=combined_similarity,
                                         similarity=combined_similarity)
                        edges_added += 1
                    elif year2 > year1:
                        # article2 cita a article1
                        self.graph.add_edge(article2_id, article1_id, 
                                         weight=combined_similarity,
                                         similarity=combined_similarity)
                        edges_added += 1
        
        print(f"✅ Grafo construido con {self.graph.number_of_nodes()} nodos y {edges_added} aristas")
        return edges_added
    
    def dijkstra_shortest_path(self, source: str, target: str) -> Tuple[List, float]:
        """Calcular camino mínimo usando algoritmo de Dijkstra."""
        try:
            path = nx.shortest_path(self.graph, source, target, weight='weight')
            distance = nx.shortest_path_length(self.graph, source, target, weight='weight')
            return path, distance
        except nx.NetworkXNoPath:
            return [], float('inf')
        except nx.NodeNotFound:
            return [], float('inf')
    
    def floyd_warshall_all_pairs(self) -> Dict[Tuple[str, str], Tuple[List, float]]:
        """Calcular todos los caminos mínimos usando Floyd-Warshall."""
        print("🔄 Calculando todos los caminos mínimos (Floyd-Warshall)...")
        
        # Usar NetworkX para Floyd-Warshall
        try:
            distances = dict(nx.all_pairs_shortest_path_length(self.graph, weight='weight'))
            paths = dict(nx.all_pairs_shortest_path(self.graph, weight='weight'))
            
            result = {}
            for source in distances:
                for target in distances[source]:
                    if source != target:
                        path = paths.get((source, target), [])
                        distance = distances[source][target]
                        result[(source, target)] = (path, distance)
            
            print(f"✅ Calculados caminos para {len(result)} pares de nodos")
            return result
        except Exception as e:
            print(f"❌ Error en Floyd-Warshall: {e}")
            return {}
    
    def find_strongly_connected_components(self) -> List[List[str]]:
        """Encontrar componentes fuertemente conexas."""
        print("🔍 Buscando componentes fuertemente conexas...")
        
        try:
            scc = list(nx.strongly_connected_components(self.graph))
            scc_sizes = [len(component) for component in scc]
            
            print(f"✅ Encontradas {len(scc)} componentes fuertemente conexas")
            print(f"   Tamaños: {sorted(scc_sizes, reverse=True)[:10]}...")
            
            return scc
        except Exception as e:
            print(f"❌ Error buscando componentes: {e}")
            return []
    
    def get_graph_statistics(self) -> Dict:
        """Obtener estadísticas del grafo."""
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph.to_undirected()),
            'is_strongly_connected': nx.is_strongly_connected(self.graph),
            'is_weakly_connected': nx.is_weakly_connected(self.graph),
            'number_of_scc': len(list(nx.strongly_connected_components(self.graph))),
            'number_of_wcc': len(list(nx.weakly_connected_components(self.graph)))
        }
        
        if self.graph.number_of_edges() > 0:
            in_degrees = [d for n, d in self.graph.in_degree()]
            out_degrees = [d for n, d in self.graph.out_degree()]
            
            stats.update({
                'average_in_degree': np.mean(in_degrees),
                'average_out_degree': np.mean(out_degrees),
                'max_in_degree': max(in_degrees),
                'max_out_degree': max(out_degrees)
            })
        
        return stats
    
    def save_graph(self, filename: str):
        """Guardar el grafo en formato JSON."""
        graph_data = {
            'nodes': list(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True)),
            'statistics': self.get_graph_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Grafo guardado en {filename}")
    
    def load_graph(self, filename: str):
        """Cargar grafo desde archivo JSON."""
        with open(filename, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        self.graph.clear()
        
        # Agregar nodos
        for node, data in graph_data['nodes']:
            self.graph.add_node(node, **data)
        
        # Agregar aristas
        for source, target, data in graph_data['edges']:
            self.graph.add_edge(source, target, **data)
        
        print(f"📂 Grafo cargado desde {filename}")
        return len(self.graph.nodes())

def main():
    """Función principal para probar el grafo de citaciones."""
    print("🔬 Iniciando análisis de grafo de citaciones...")
    
    # Crear instancia del grafo
    citation_graph = CitationGraph()
    
    # Cargar artículos
    bibtex_file = "Data/unificados.bib"
    if not os.path.exists(bibtex_file):
        print(f"❌ Archivo no encontrado: {bibtex_file}")
        return
    
    citation_graph.load_articles_from_bibtex(bibtex_file)
    
    # Construir grafo
    citation_graph.build_citation_graph()
    
    # Obtener estadísticas
    stats = citation_graph.get_graph_statistics()
    print("\n📊 Estadísticas del grafo:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Encontrar componentes fuertemente conexas
    scc = citation_graph.find_strongly_connected_components()
    
    # Guardar grafo
    citation_graph.save_graph("Data/citation_graph.json")
    
    print("✅ Análisis de grafo de citaciones completado")

if __name__ == "__main__":
    main()
