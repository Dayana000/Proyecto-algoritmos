#!/usr/bin/env python3
"""
Versión simplificada del sistema de análisis de grafos de coocurrencia.
Funciona sin dependencias externas, usando solo librerías estándar de Python.

Autor: Proyecto Algoritmos UQ
"""

import json
import os
import re
import math
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set, Optional

class SimpleCooccurrenceGraph:
    """Clase simplificada para manejar el grafo de coocurrencia de términos."""
    
    def __init__(self, min_frequency: int = 2, min_cooccurrence: int = 1):
        """Inicializar el grafo de coocurrencia."""
        self.graph = defaultdict(list)  # Lista de adyacencia
        self.weights = defaultdict(dict)  # Pesos de las aristas
        self.term_frequencies = Counter()
        self.cooccurrence_matrix = defaultdict(int)
        self.articles = {}
        self.min_frequency = min_frequency
        self.min_cooccurrence = min_cooccurrence
        
        # Lista de stop words en inglés (simplificada)
        self.stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'these', 'they', 'them',
            'their', 'there', 'then', 'than', 'or', 'but', 'not', 'no',
            'all', 'any', 'can', 'could', 'do', 'does', 'did', 'have',
            'had', 'has', 'having', 'if', 'into', 'more', 'most', 'other',
            'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too',
            'very', 'what', 'when', 'where', 'which', 'who', 'why', 'how'
        }
    
    def load_articles_from_bibtex(self, bibtex_file: str):
        """Cargar artículos desde archivo BibTeX."""
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
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocesar texto para extraer términos."""
        if not text:
            return []
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales y números
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        
        # Tokenizar (separar por espacios)
        tokens = text.split()
        
        # Filtrar stop words y palabras muy cortas
        tokens = [
            token for token in tokens 
            if len(token) > 2 and token not in self.stop_words
        ]
        
        return tokens
    
    def _extract_terms_from_article(self, article: Dict) -> Set[str]:
        """Extraer términos relevantes de un artículo."""
        terms = set()
        
        # Extraer de título
        title_terms = self._preprocess_text(article.get('title', ''))
        terms.update(title_terms)
        
        # Extraer de abstract
        abstract_terms = self._preprocess_text(article.get('abstract', ''))
        terms.update(abstract_terms)
        
        # Extraer de journal (para términos específicos del dominio)
        journal_terms = self._preprocess_text(article.get('journal', ''))
        terms.update(journal_terms)
        
        return terms
    
    def build_cooccurrence_matrix(self):
        """Construir matriz de coocurrencia de términos."""
        print("🔗 Construyendo matriz de coocurrencia...")
        
        # Primero, extraer todos los términos y contar frecuencias
        print("  Extrayendo términos de todos los artículos...")
        for article_id, article in self.articles.items():
            terms = self._extract_terms_from_article(article)
            for term in terms:
                self.term_frequencies[term] += 1
        
        # Filtrar términos por frecuencia mínima
        filtered_terms = {
            term: freq for term, freq in self.term_frequencies.items() 
            if freq >= self.min_frequency
        }
        
        print(f"  Términos únicos: {len(self.term_frequencies)}")
        print(f"  Términos filtrados (freq >= {self.min_frequency}): {len(filtered_terms)}")
        
        # Construir matriz de coocurrencia
        print("  Construyendo matriz de coocurrencia...")
        for article_id, article in self.articles.items():
            terms = self._extract_terms_from_article(article)
            # Solo considerar términos que pasaron el filtro
            filtered_article_terms = [term for term in terms if term in filtered_terms]
            
            # Contar coocurrencias
            for i, term1 in enumerate(filtered_article_terms):
                for j, term2 in enumerate(filtered_article_terms):
                    if i != j:
                        # Ordenar para evitar duplicados
                        pair = tuple(sorted([term1, term2]))
                        self.cooccurrence_matrix[pair] += 1
        
        print(f"  Pares de coocurrencia únicos: {len(self.cooccurrence_matrix)}")
        return len(filtered_terms)
    
    def build_cooccurrence_graph(self):
        """Construir el grafo de coocurrencia."""
        print("🕸️  Construyendo grafo de coocurrencia...")
        
        # Limpiar grafo existente
        self.graph.clear()
        self.weights.clear()
        
        # Agregar nodos (términos)
        for term, freq in self.term_frequencies.items():
            if freq >= self.min_frequency:
                self.graph[term] = []  # Inicializar lista de vecinos
        
        # Agregar aristas (coocurrencias)
        edges_added = 0
        for (term1, term2), cooccurrence_count in self.cooccurrence_matrix.items():
            if cooccurrence_count >= self.min_cooccurrence:
                # Calcular peso basado en coocurrencia y frecuencias individuales
                freq1 = self.term_frequencies[term1]
                freq2 = self.term_frequencies[term2]
                
                # Peso normalizado (Jaccard-like)
                denominator = freq1 + freq2 - cooccurrence_count
                weight = cooccurrence_count / denominator if denominator > 0 else 0
                
                # Agregar arista en ambas direcciones (grafo no dirigido)
                self.graph[term1].append(term2)
                self.graph[term2].append(term1)
                self.weights[term1][term2] = weight
                self.weights[term2][term1] = weight
                edges_added += 1
        
        print(f"✅ Grafo construido con {len(self.graph)} nodos y {edges_added} aristas")
        return edges_added
    
    def get_node_degrees(self) -> Dict[str, int]:
        """Obtener grado de cada nodo."""
        degrees = {term: len(neighbors) for term, neighbors in self.graph.items()}
        return degrees
    
    def get_top_connected_terms(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Obtener los términos más conectados."""
        degrees = self.get_node_degrees()
        sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_degrees[:top_n]
    
    def find_connected_components(self) -> List[List[str]]:
        """Encontrar componentes conexas del grafo usando DFS."""
        print("🔍 Buscando componentes conexas...")
        
        visited = set()
        components = []
        
        def dfs(node, component):
            if node in visited:
                return
            visited.add(node)
            component.append(node)
            for neighbor in self.graph[node]:
                dfs(neighbor, component)
        
        for node in self.graph:
            if node not in visited:
                component = []
                dfs(node, component)
                if component:
                    components.append(component)
        
        component_sizes = [len(component) for component in components]
        
        print(f"✅ Encontradas {len(components)} componentes conexas")
        print(f"   Tamaños: {sorted(component_sizes, reverse=True)[:10]}...")
        
        return components
    
    def get_component_themes(self, components: List[List[str]]) -> Dict[int, Dict]:
        """Analizar temas de las componentes conexas."""
        themes = {}
        
        for i, component in enumerate(components):
            if len(component) < 3:  # Solo analizar componentes con al menos 3 términos
                continue
            
            # Obtener términos más frecuentes en la componente
            component_frequencies = {
                term: self.term_frequencies[term] for term in component
            }
            
            # Obtener términos más conectados en la componente
            component_degrees = {term: len(self.graph[term]) for term in component}
            
            # Términos más importantes (combinación de frecuencia y conectividad)
            term_importance = {}
            for term in component:
                freq_score = component_frequencies[term]
                degree_score = component_degrees[term]
                importance = freq_score * math.log(degree_score + 1)
                term_importance[term] = importance
            
            top_terms = sorted(term_importance.items(), key=lambda x: x[1], reverse=True)[:5]
            
            themes[i] = {
                'size': len(component),
                'top_terms': top_terms,
                'terms': list(component)
            }
        
        return themes
    
    def get_graph_statistics(self) -> Dict:
        """Obtener estadísticas del grafo."""
        total_edges = sum(len(neighbors) for neighbors in self.graph.values()) // 2  # Dividir por 2 porque es no dirigido
        
        degrees = [len(neighbors) for neighbors in self.graph.values()]
        
        stats = {
            'nodes': len(self.graph),
            'edges': total_edges,
            'density': (2 * total_edges) / (len(self.graph) * (len(self.graph) - 1)) if len(self.graph) > 1 else 0,
            'average_degree': sum(degrees) / len(degrees) if degrees else 0,
            'max_degree': max(degrees) if degrees else 0,
            'min_degree': min(degrees) if degrees else 0
        }
        
        return stats
    
    def save_graph(self, filename: str):
        """Guardar el grafo en formato JSON."""
        graph_data = {
            'nodes': list(self.graph.keys()),
            'edges': [{'source': source, 'target': target, 'weight': weight} for source in self.graph for target, weight in self.weights[source].items() if source < target],  # Solo una dirección para grafo no dirigido
            'statistics': self.get_graph_statistics(),
            'term_frequencies': dict(self.term_frequencies),
            'cooccurrence_matrix': {f"{pair[0]}_{pair[1]}": count for pair, count in self.cooccurrence_matrix.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Grafo guardado en {filename}")

def main():
    """Función principal para probar el grafo de coocurrencia."""
    print("🔬 Iniciando análisis de grafo de coocurrencia (versión simplificada)...")
    
    # Crear instancia del grafo
    cooccurrence_graph = SimpleCooccurrenceGraph(min_frequency=3, min_cooccurrence=2)
    
    # Cargar artículos
    bibtex_file = "Data/unificados.bib"
    if not os.path.exists(bibtex_file):
        print(f"❌ Archivo no encontrado: {bibtex_file}")
        return
    
    cooccurrence_graph.load_articles_from_bibtex(bibtex_file)
    
    # Construir matriz de coocurrencia
    cooccurrence_graph.build_cooccurrence_matrix()
    
    # Construir grafo
    cooccurrence_graph.build_cooccurrence_graph()
    
    # Obtener estadísticas
    stats = cooccurrence_graph.get_graph_statistics()
    print("\n📊 Estadísticas del grafo:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Obtener términos más conectados
    top_terms = cooccurrence_graph.get_top_connected_terms(20)
    print(f"\n🔝 Top 20 términos más conectados:")
    for i, (term, degree) in enumerate(top_terms, 1):
        print(f"  {i:2d}. {term}: {degree} conexiones")
    
    # Encontrar componentes conexas
    components = cooccurrence_graph.find_connected_components()
    
    # Analizar temas
    print(f"\n🎯 Análisis de temas:")
    themes = cooccurrence_graph.get_component_themes(components)
    
    print(f"  Temas identificados: {len(themes)}")
    for theme_id, theme_data in list(themes.items())[:5]:  # Mostrar solo los primeros 5
        print(f"    Tema {theme_id}: {theme_data['size']} términos")
        top_terms_str = [term for term, _ in theme_data['top_terms']]
        print(f"      Top términos: {', '.join(top_terms_str)}")
    
    # Guardar grafo
    cooccurrence_graph.save_graph("Data/simple_cooccurrence_graph.json")
    
    print("✅ Análisis de grafo de coocurrencia completado")

if __name__ == "__main__":
    main()
