#!/usr/bin/env python3
"""
Sistema de análisis de grafos de coocurrencia de términos.

Este módulo implementa:
1. Construcción de grafo de coocurrencia basado en términos de abstracts
2. Cálculo del grado de cada nodo (término)
3. Detección de componentes conexas para identificar temas
4. Análisis de centralidad y conectividad

Autor: Proyecto Algoritmos UQ
"""

import networkx as nx
from collections import defaultdict, Counter
import re
import math
from typing import Dict, List, Tuple, Set, Optional
import json
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

class CooccurrenceGraph:
    """Clase para manejar el grafo de coocurrencia de términos."""
    
    def __init__(self, min_frequency: int = 2, min_cooccurrence: int = 1):
        """Inicializar el grafo de coocurrencia."""
        self.graph = nx.Graph()
        self.term_frequencies = Counter()
        self.cooccurrence_matrix = defaultdict(int)
        self.articles = {}
        self.min_frequency = min_frequency
        self.min_cooccurrence = min_cooccurrence
        self.stemmer = PorterStemmer()
        
        # Descargar recursos de NLTK si no están disponibles
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
        
        try:
            word_tokenize("test")
        except LookupError:
            nltk.download('punkt')
    
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
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Filtrar stop words y palabras muy cortas
        tokens = [
            self.stemmer.stem(token) for token in tokens 
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
        print("🕸️ Construyendo grafo de coocurrencia...")
        
        # Limpiar grafo existente
        self.graph.clear()
        
        # Agregar nodos (términos)
        for term, freq in self.term_frequencies.items():
            if freq >= self.min_frequency:
                self.graph.add_node(term, frequency=freq)
        
        # Agregar aristas (coocurrencias)
        edges_added = 0
        for (term1, term2), cooccurrence_count in self.cooccurrence_matrix.items():
            if cooccurrence_count >= self.min_cooccurrence:
                # Calcular peso basado en coocurrencia y frecuencias individuales
                freq1 = self.term_frequencies[term1]
                freq2 = self.term_frequencies[term2]
                
                # Peso normalizado (Jaccard-like)
                weight = cooccurrence_count / (freq1 + freq2 - cooccurrence_count)
                
                self.graph.add_edge(term1, term2, 
                                 weight=weight,
                                 cooccurrence_count=cooccurrence_count)
                edges_added += 1
        
        print(f"✅ Grafo construido con {self.graph.number_of_nodes()} nodos y {edges_added} aristas")
        return edges_added
    
    def get_node_degrees(self) -> Dict[str, int]:
        """Obtener grado de cada nodo."""
        degrees = dict(self.graph.degree())
        return degrees
    
    def get_top_connected_terms(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Obtener los términos más conectados."""
        degrees = self.get_node_degrees()
        sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return sorted_degrees[:top_n]
    
    def find_connected_components(self) -> List[List[str]]:
        """Encontrar componentes conexas del grafo."""
        print("🔍 Buscando componentes conexas...")
        
        try:
            components = list(nx.connected_components(self.graph))
            component_sizes = [len(component) for component in components]
            
            print(f"✅ Encontradas {len(components)} componentes conexas")
            print(f"   Tamaños: {sorted(component_sizes, reverse=True)[:10]}...")
            
            return components
        except Exception as e:
            print(f"❌ Error buscando componentes: {e}")
            return []
    
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
            subgraph = self.graph.subgraph(component)
            component_degrees = dict(subgraph.degree())
            
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
    
    def calculate_centrality_measures(self) -> Dict[str, Dict]:
        """Calcular medidas de centralidad."""
        print("📊 Calculando medidas de centralidad...")
        
        try:
            # Degree centrality
            degree_centrality = nx.degree_centrality(self.graph)
            
            # Betweenness centrality (solo para grafos no muy grandes)
            if self.graph.number_of_nodes() < 1000:
                betweenness_centrality = nx.betweenness_centrality(self.graph)
            else:
                betweenness_centrality = {}
            
            # Closeness centrality (solo para grafos no muy grandes)
            if self.graph.number_of_nodes() < 1000:
                closeness_centrality = nx.closeness_centrality(self.graph)
            else:
                closeness_centrality = {}
            
            # Eigenvector centrality
            try:
                eigenvector_centrality = nx.eigenvector_centrality(self.graph, max_iter=1000)
            except:
                eigenvector_centrality = {}
            
            centrality_measures = {
                'degree': degree_centrality,
                'betweenness': betweenness_centrality,
                'closeness': closeness_centrality,
                'eigenvector': eigenvector_centrality
            }
            
            print("✅ Medidas de centralidad calculadas")
            return centrality_measures
            
        except Exception as e:
            print(f"❌ Error calculando centralidad: {e}")
            return {}
    
    def get_graph_statistics(self) -> Dict:
        """Obtener estadísticas del grafo."""
        stats = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph),
            'is_connected': nx.is_connected(self.graph),
            'number_of_components': len(list(nx.connected_components(self.graph))),
            'average_degree': (
                sum(d for _, d in self.graph.degree()) / self.graph.number_of_nodes()
                if self.graph.number_of_nodes() > 0 else 0
            ),
            'max_degree': max([d for n, d in self.graph.degree()]) if self.graph.number_of_nodes() > 0 else 0
        }
        
        return stats
    
    def save_graph(self, filename: str):
        """Guardar el grafo en formato JSON."""
        graph_data = {
            'nodes': list(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True)),
            'statistics': self.get_graph_statistics(),
            'term_frequencies': dict(self.term_frequencies),
            'cooccurrence_matrix': dict(self.cooccurrence_matrix)
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
        
        # Restaurar datos adicionales
        self.term_frequencies = Counter(graph_data.get('term_frequencies', {}))
        self.cooccurrence_matrix = defaultdict(int, graph_data.get('cooccurrence_matrix', {}))
        
        print(f"📂 Grafo cargado desde {filename}")
        return len(self.graph.nodes())

def main():
    """Función principal para probar el grafo de coocurrencia."""
    print("🔬 Iniciando análisis de grafo de coocurrencia...")
    
    # Crear instancia del grafo
    cooccurrence_graph = CooccurrenceGraph(min_frequency=3, min_cooccurrence=2)
    
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
    for term, degree in top_terms:
        print(f"  {term}: {degree} conexiones")
    
    # Encontrar componentes conexas
    components = cooccurrence_graph.find_connected_components()
    
    # Analizar temas
    themes = cooccurrence_graph.get_component_themes(components)
    print(f"\n🎯 Temas identificados en {len(themes)} componentes:")
    for theme_id, theme_data in list(themes.items())[:5]:  # Mostrar solo los primeros 5
        print(f"  Tema {theme_id}: {theme_data['size']} términos")
        print(f"    Top términos: {[term for term, _ in theme_data['top_terms']]}")
    
    # Calcular centralidad
    centrality = cooccurrence_graph.calculate_centrality_measures()
    
    # Guardar grafo
    cooccurrence_graph.save_graph("Data/cooccurrence_graph.json")
    
    print("✅ Análisis de grafo de coocurrencia completado")

if __name__ == "__main__":
    main()
