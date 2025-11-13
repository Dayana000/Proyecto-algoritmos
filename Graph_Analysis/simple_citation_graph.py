#!/usr/bin/env python3
"""
Versión simplificada del sistema de análisis de grafos de citaciones.
Funciona sin dependencias externas, usando solo librerías estándar de Python.

Autor: Proyecto Algoritmos UQ
"""

import json
import os
import re
import math
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Set, Optional

class SimpleCitationGraph:
    """Implementación ligera del grafo de citaciones sin dependencias externas."""
    
    def __init__(self):
        """Inicializa listas de adyacencia y parámetros base."""
        # Representamos el grafo como diccionario -> lista de vecinos para evitar usar networkx.
        self.graph: Dict[str, List[str]] = defaultdict(list)
        # Guardamos por separado el peso asociado a cada arista dirigida (similitud combinada).
        self.weights: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.articles: Dict[str, Dict[str, str]] = {}
        # Umbral de similitud mínimo: ligeramente más alto porque aquí no hay normalizaciones extra.
        self.similarity_threshold = 0.3
        
    def load_articles_from_bibtex(self, bibtex_file: str):
        """Carga artículos desde un BibTeX y los conserva en memoria para posteriores cálculos."""
        print(f"📖 Cargando artículos desde {bibtex_file}...")
        
        with open(bibtex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        articles = self._parse_bibtex(content)
        
        for article in articles:
            article_id = article.get('id', f"ref{len(self.articles)}")
            self.articles[article_id] = article
        
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
        """Construye el grafo dirigido comparando todos los pares con heurísticas básicas."""
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
                
                # Peso combinado
                combined_similarity = (
                    0.5 * title_sim + 
                    0.3 * author_sim + 
                    0.2 * abstract_sim
                )
                
                # Si la similitud supera el umbral, crear arista
                if combined_similarity > self.similarity_threshold:
                    year1 = int(article1.get('year', '0')) if article1.get('year', '0').isdigit() else 0
                    year2 = int(article2.get('year', '0')) if article2.get('year', '0').isdigit() else 0
                    
                    if year1 > year2:
                        # article1 cita a article2
                        self.graph[article1_id].append(article2_id)
                        self.weights[article1_id][article2_id] = combined_similarity
                        edges_added += 1
                    elif year2 > year1:
                        # article2 cita a article1
                        self.graph[article2_id].append(article1_id)
                        self.weights[article2_id][article1_id] = combined_similarity
                        edges_added += 1
        
        print(f"✅ Grafo construido con {len(self.articles)} nodos y {edges_added} aristas")
        return edges_added
    
    def dijkstra_shortest_path(self, source: str, target: str) -> Tuple[List, float]:
        """Implementación manual de Dijkstra sobre las estructuras listas de adyacencia."""
        if source not in self.articles or target not in self.articles:
            return [], float('inf')
        
        # Inicializar distancias
        distances = {node: float('inf') for node in self.articles}
        distances[source] = 0
        previous = {}
        visited = set()
        
        # Cola de prioridad simple (usando lista)
        queue = [(0, source)]
        
        while queue:
            current_distance, current_node = min(queue)
            queue.remove((current_distance, current_node))
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            if current_node == target:
                break
            
            # Explorar vecinos
            for neighbor in self.graph[current_node]:
                if neighbor in visited:
                    continue
                
                weight = self.weights[current_node].get(neighbor, 1.0)
                new_distance = current_distance + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    queue.append((new_distance, neighbor))
        
        # Reconstruir camino
        if target not in previous and source != target:
            return [], float('inf')
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = previous.get(current)
        
        path.reverse()
        return path, distances[target]
    
    def find_strongly_connected_components(self) -> List[List[str]]:
        """Encontrar componentes fuertemente conexas usando DFS."""
        print("🔍 Buscando componentes fuertemente conexas...")
        
        visited = set()
        finished = []
        
        def dfs1(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in self.graph[node]:
                dfs1(neighbor)
            finished.append(node)
        
        # Primera pasada DFS
        for node in self.articles:
            dfs1(node)
        
        # Crear grafo transpuesto
        transposed = defaultdict(list)
        for node in self.graph:
            for neighbor in self.graph[node]:
                transposed[neighbor].append(node)
        
        # Segunda pasada DFS en grafo transpuesto
        visited.clear()
        scc = []
        
        def dfs2(node, component):
            if node in visited:
                return
            visited.add(node)
            component.append(node)
            for neighbor in transposed[node]:
                dfs2(neighbor, component)
        
        for node in reversed(finished):
            if node not in visited:
                component = []
                dfs2(node, component)
                if component:
                    scc.append(component)
        
        print(f"✅ Encontradas {len(scc)} componentes fuertemente conexas")
        return scc
    
    def get_graph_statistics(self) -> Dict:
        """Obtener estadísticas del grafo."""
        total_edges = sum(len(neighbors) for neighbors in self.graph.values())
        
        # Calcular grados
        in_degrees = defaultdict(int)
        out_degrees = defaultdict(int)
        
        for node in self.graph:
            out_degrees[node] = len(self.graph[node])
            for neighbor in self.graph[node]:
                in_degrees[neighbor] += 1
        
        stats = {
            'nodes': len(self.articles),
            'edges': total_edges,
            'density': total_edges / (len(self.articles) * (len(self.articles) - 1)) if len(self.articles) > 1 else 0,
            'average_in_degree': sum(in_degrees.values()) / len(self.articles) if self.articles else 0,
            'average_out_degree': sum(out_degrees.values()) / len(self.articles) if self.articles else 0,
            'max_in_degree': max(in_degrees.values()) if in_degrees else 0,
            'max_out_degree': max(out_degrees.values()) if out_degrees else 0
        }
        
        return stats
    
    def save_graph(self, filename: str):
        """Guardar el grafo en formato JSON."""
        graph_data = {
            'nodes': list(self.articles.keys()),
            'edges': [{'source': source, 'target': target, 'weight': weight} for source in self.graph for target, weight in self.weights[source].items()],
            'statistics': self.get_graph_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Grafo guardado en {filename}")

def main():
    """Función principal para probar el grafo de citaciones."""
    print("🔬 Iniciando análisis de grafo de citaciones (versión simplificada)...")
    
    # Crear instancia del grafo
    citation_graph = SimpleCitationGraph()
    
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
    
    if scc:
        scc_sizes = [len(component) for component in scc]
        print(f"\n🔗 Componentes fuertemente conexas:")
        print(f"  Número de componentes: {len(scc)}")
        print(f"  Tamaño de la componente más grande: {max(scc_sizes)}")
        print(f"  Tamaños: {sorted(scc_sizes, reverse=True)[:10]}")
    
    # Probar algoritmo de Dijkstra
    nodes = list(citation_graph.articles.keys())
    if len(nodes) >= 2:
        source = nodes[0]
        target = nodes[1]
        path, distance = citation_graph.dijkstra_shortest_path(source, target)
        print(f"\n🛤️  Camino de {source} a {target}:")
        if path:
            print(f"  Distancia: {distance:.3f}")
            print(f"  Camino: {' -> '.join(path[:5])}{'...' if len(path) > 5 else ''}")
        else:
            print("  No hay camino disponible")
    
    # Guardar grafo
    citation_graph.save_graph("Data/simple_citation_graph.json")
    
    print("✅ Análisis de grafo de citaciones completado")

if __name__ == "__main__":
    main()
