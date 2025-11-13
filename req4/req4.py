#!/usr/bin/env python3
"""
Módulo para el Requerimiento 4: clustering jerárquico y dendrogramas.

Esta implementación no depende de bibliotecas externas (solo usa la biblioteca
estándar de Python). Permite:
1. Cargar artículos desde un archivo BibTeX.
2. Preprocesar los abstracts y construir representaciones TF-IDF sencillas.
3. Calcular distancias coseno y ejecutar clustering jerárquico aglomerativo con
   tres variantes clásicas: single, complete y average.
4. Generar dendrogramas en formato HTML/SVG junto con un resumen en JSON que
   incluye el coeficiente cophenético aproximado de cada método.

Uso:
    python req4/req4.py --entrada Data/unificados.bib \
        --salida Data/visualizations/req4 --max-articulos 200
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


# ---------------------------------------------------------------------------
# Datos y utilidades básicas
# ---------------------------------------------------------------------------

STOPWORDS = {
    "the",
    "and",
    "for",
    "are",
    "with",
    "that",
    "this",
    "from",
    "have",
    "were",
    "was",
    "been",
    "they",
    "their",
    "there",
    "which",
    "into",
    "while",
    "where",
    "when",
    "will",
    "shall",
    "would",
    "could",
    "should",
    "about",
    "after",
    "before",
    "between",
    "because",
    "over",
    "under",
    "such",
    "than",
    "then",
    "them",
    "these",
    "those",
    "through",
    "using",
    "used",
    "use",
    "based",
    "also",
    "more",
    "most",
    "other",
    "only",
    "both",
    "each",
    "many",
    "some",
    "any",
    "can",
    "may",
    "might",
    "must",
    "however",
    "within",
    "across",
    "per",
    "via",
    "our",
    "your",
    "its",
    "very",
    "like",
    "just",
    "well",
}

METHOD_LABELS = {
    "single": "Enlace sencillo",
    "complete": "Enlace completo",
    "average": "Enlace promedio",
}


@dataclass
class Article:
    """Información relevante del artículo para el clustering."""

    id: str
    title: str
    abstract: str
    year: str


@dataclass
class ClusterNode:
    """Nodo dentro del dendrograma."""

    id: int
    members: Tuple[int, ...]
    left: int | None
    right: int | None
    distance: float


# ---------------------------------------------------------------------------
# Lectura de BibTeX
# ---------------------------------------------------------------------------

def load_articles_from_bibtex(path: str, max_items: int | None = None) -> List[Article]:
    """Carga artículos desde un archivo BibTeX."""

    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró el archivo BibTeX: {path}")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    articles: List[Article] = []
    current: Dict[str, str] = {}
    current_id = ""
    inside = False

    # Recorremos el texto completo, detectando el inicio y cierre de cada bloque @article.
    # Cada bloque se traduce en un diccionario con las claves del BibTeX tal como aparecen.
    # Solo convertimos a Article aquellos registros que poseen título y abstract, porque el resto
    # no aporta información útil al clustering.
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("@article"):
            # Nuevo artículo: reiniciamos el estado y capturamos el identificador.
            inside = True
            current = {}
            current_id = stripped.split("{", 1)[1].split(",", 1)[0].strip()
        elif inside and stripped == "}":
            if current:
                # Validamos que existan título y abstract antes de materializar el objeto Article.
                abstract = current.get("abstract", "").strip()
                title = current.get("title", "").strip()
                if abstract and title:
                    article = Article(
                        id=current_id or f"ref{len(articles)}",
                        title=title,
                        abstract=abstract,
                        year=current.get("year", "Unknown"),
                    )
                    articles.append(article)
                    # Si el usuario estableció un límite, salimos tan pronto como lo alcanzamos.
                    if max_items and len(articles) >= max_items:
                        break
            inside = False
        elif inside and "=" in stripped:
            # Dentro de un bloque copiamos pares clave=valor limpiando comas y llaves.
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().rstrip(",")
            value = value.strip("{}").strip()
            current[key] = value

    return articles


# ---------------------------------------------------------------------------
# Preprocesamiento y TF-IDF básico
# ---------------------------------------------------------------------------

def preprocess_text(text: str) -> List[str]:
    """Convierte el abstract en tokens filtrados."""

    # Extraemos solo secuencias alfabéticas de al menos 3 caracteres y las normalizamos.
    # Este paso unifica criterios: todo en minúscula y sin símbolos para que TF-IDF trate cada término de forma consistente.
    tokens = re.findall(r"[a-zA-Z]{3,}", text.lower())
    # Eliminamos palabras vacías para concentrarnos en términos relevantes del dominio.
    # Las stopwords (the, and, etc.) no aportan significado para medir similitud entre abstracts.
    filtered = [token for token in tokens if token not in STOPWORDS]
    return filtered


def compute_tfidf_vectors(articles: Sequence[Article]) -> List[Dict[str, float]]:
    """Calcula representaciones TF-IDF sencillas por documento."""

    # Preprocesamos cada abstract para obtener su lista de tokens limpia.
    # El resultado de este paso son listas de palabras con stopwords removidas y en minúscula.
    documents = [preprocess_text(article.abstract) for article in articles]
    doc_count = len(documents)
    if doc_count == 0:
        return []

    # Calculamos la frecuencia de documentos (DF) por término para el IDF.
    # La estructura df almacena cuántos abstracts contienen cada token en al menos una ocasión.
    df: Dict[str, int] = {}
    for tokens in documents:
        unique_terms = set(tokens)
        for term in unique_terms:
            df[term] = df.get(term, 0) + 1

    # Construimos un vector TF-IDF disperso para cada documento.
    # Cada vector es un diccionario {término: peso}; esto evita almacenar ceros explícitos.
    tfidf_vectors: List[Dict[str, float]] = []
    for tokens in documents:
        term_counts: Dict[str, int] = {}
        for term in tokens:
            term_counts[term] = term_counts.get(term, 0) + 1

        vector: Dict[str, float] = {}
        total_terms = len(tokens) or 1
        for term, count in term_counts.items():
            # tf captura qué tan frecuente es el término en este documento.
            tf = count / total_terms
            # idf atenúa términos ubicuos entre documentos y refuerza los raros.
            idf = math.log((doc_count + 1) / (df.get(term, 0) + 1)) + 1.0
            vector[term] = tf * idf
        tfidf_vectors.append(vector)

    return tfidf_vectors


# ---------------------------------------------------------------------------
# Distancias y clustering jerárquico
# ---------------------------------------------------------------------------

def cosine_distance(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
    """Distancia coseno entre dos vectores representados como diccionarios."""

    # Si alguno de los vectores es vacío, asumimos distancia máxima (no hay información compartida).
    if not vec_a or not vec_b:
        return 1.0

    # Producto punto considerando únicamente las dimensiones compartidas.
    dot = sum(value * vec_b.get(term, 0.0) for term, value in vec_a.items())
    norm_a = math.sqrt(sum(value * value for value in vec_a.values()))
    norm_b = math.sqrt(sum(value * value for value in vec_b.values()))
    # Ante normas nulas devolvemos distancia máxima para mantener el algoritmo estable.
    if norm_a == 0.0 or norm_b == 0.0:
        return 1.0

    # Clamp para evitar errores de redondeo flotante.
    similarity = max(min(dot / (norm_a * norm_b), 1.0), -1.0)
    return 1.0 - similarity


def pairwise_distances(vectors: Sequence[Dict[str, float]]) -> Dict[Tuple[int, int], float]:
    """Construye una matriz dispersa de distancias coseno entre todos los pares de documentos."""

    distances: Dict[Tuple[int, int], float] = {}
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            # Guardamos solo (i, j) con i < j para evitar duplicados y ahorrar memoria.
            distances[(i, j)] = cosine_distance(vectors[i], vectors[j])
    return distances


def cluster_distance(
    members_a: Iterable[int],
    members_b: Iterable[int],
    base_distances: Dict[Tuple[int, int], float],
    method: str,
) -> float:
    """Calcula la distancia entre dos clústeres acorde al esquema de enlace solicitado."""

    values: List[float] = []
    for i in members_a:
        for j in members_b:
            if i == j:
                continue
            key = (i, j) if i < j else (j, i)
            values.append(base_distances.get(key, 1.0))

    # Si no hay pares (p.ej. clústeres vacíos), devolvemos distancia máxima.
    # Este caso puede ocurrir si ambos clústeres apuntan al mismo índice (situación degenerada).
    if not values:
        return 1.0
    if method == "single":
        # Enlace sencillo: se queda con el par más cercano entre los clústeres.
        # Favorece unir clústeres que tengan al menos un documento muy parecido (sensibilidad alta).
        return min(values)
    if method == "complete":
        # Enlace completo: exige que incluso el par más distante sea aceptable.
        # Útil cuando se desea evitar que un clúster contenga elementos demasiado dispares.
        return max(values)

    # Enlace promedio: evalúa la distancia media entre todos los pares.
    # Balance intermedio: suaviza extremos y tiende a formar clústeres cohesionados sin ser estrictos.
    return sum(values) / len(values)


def hierarchical_clustering(
    base_distances: Dict[Tuple[int, int], float],
    n_obs: int,
    method: str,
) -> Tuple[List[ClusterNode], int]:
    """Ejecuta clustering jerárquico aglomerativo."""

    if n_obs < 2:
        raise ValueError("Se requieren al menos dos observaciones para el clustering.")

    # Inicializamos cada observación como clúster hoja independiente.
    clusters: Dict[int, ClusterNode] = {
        idx: ClusterNode(id=idx, members=(idx,), left=None, right=None, distance=0.0)
        for idx in range(n_obs)
    }
    # Convertimos la matriz de distancias en un diccionario de accesos rápidos.
    distances: Dict[frozenset[int], float] = {
        frozenset((i, j)): dist for (i, j), dist in base_distances.items()
    }

    next_id = n_obs
    history: List[ClusterNode] = []

    # Fusionamos clústeres hasta que quede una única raíz.
    while len(clusters) > 1:
        # Escogemos el par con la distancia más baja de las que tenemos almacenadas.
        pair, pair_distance = min(distances.items(), key=lambda item: item[1])
        ids = tuple(pair)
        if len(ids) != 2:
            raise ValueError("El cálculo de distancias produjo un par inválido.")
        a_id, b_id = ids

        cluster_a = clusters[a_id]
        cluster_b = clusters[b_id]

        # Creamos un nodo interno que representa la fusión de los dos clústeres más próximos.
        new_members = cluster_a.members + cluster_b.members
        new_cluster = ClusterNode(
            id=next_id,
            members=new_members,
            left=a_id,
            right=b_id,
            distance=pair_distance,
        )
        history.append(new_cluster)

        # Eliminamos los clústeres fusionados y preparamos el diccionario de distancias actualizado.
        del clusters[a_id]
        del clusters[b_id]
        new_distances: Dict[frozenset[int], float] = {}

        for key, value in distances.items():
            if a_id in key or b_id in key:
                continue
            new_distances[key] = value

        clusters[new_cluster.id] = new_cluster

        # Recalculamos las distancias entre el clúster recién creado y todos los restantes.
        for other_id, other_cluster in clusters.items():
            if other_id == new_cluster.id:
                continue
            distance = cluster_distance(
                new_cluster.members, other_cluster.members, base_distances, method
            )
            new_distances[frozenset({new_cluster.id, other_id})] = distance

        distances = new_distances
        next_id += 1

    final_root = history[-1].id if history else next_id - 1

    # Garantizamos que los nodos hoja también estén presentes en el historial.
    for idx in range(n_obs):
        if not any(node.id == idx for node in history):
            history.append(
                ClusterNode(id=idx, members=(idx,), left=None, right=None, distance=0.0)
            )

    history.sort(key=lambda node: node.id)
    return history, final_root


# ---------------------------------------------------------------------------
# Métricas y visualización
# ---------------------------------------------------------------------------

"""Calcula un coeficiente cophenético aproximado a partir del historial de merges (es la correlacion de pearson entre la distancia original y la distancia cophenética)."""
def compute_cophenetic_coefficient(
    history: Sequence[ClusterNode],
    base_distances: Dict[Tuple[int, int], float],
) -> float:
    """Calcula un coeficiente cophenético aproximado a partir del historial de merges."""

    # El coeficiente mide la correlación entre distancias originales y alturas del dendrograma.
    nodes = {node.id: node for node in history}
    n_obs = sum(1 for node in history if node.left is None and node.right is None)

    # Construimos la matriz cophenética: para cada par, registramos la altura del nodo donde se unen.
    # Esto refleja "en qué nivel" del dendrograma aparecen juntos dos artículos y permite compararlo con la distancia original.
    cophenetic: Dict[Tuple[int, int], float] = {}
    for node in history:
        if node.left is None or node.right is None:
            continue
        left_members = nodes[node.left].members
        right_members = nodes[node.right].members
        for i in left_members:
            for j in right_members:
                key = (i, j) if i < j else (j, i)
                if key not in cophenetic:
                    cophenetic[key] = node.distance

    # Creamos listas paralelas con las distancias originales y las cophenéticas para correlacionarlas.
    original: List[float] = []
    coph: List[float] = []
    for i in range(n_obs):
        for j in range(i + 1, n_obs):
            key = (i, j)
            original.append(base_distances.get(key, 1.0))
            coph.append(cophenetic.get(key, 1.0))

    if not original:
        return 0.0

    mean_orig = sum(original) / len(original)
    mean_coph = sum(coph) / len(coph)

    num = sum((o - mean_orig) * (c - mean_coph) for o, c in zip(original, coph))
    den1 = math.sqrt(sum((o - mean_orig) ** 2 for o in original))
    den2 = math.sqrt(sum((c - mean_coph) ** 2 for c in coph))
    if den1 == 0.0 or den2 == 0.0:
        return 0.0

    return max(min(num / (den1 * den2), 1.0), -1.0)


def layout_positions(
    history: Sequence[ClusterNode],
    root_id: int,
    labels: Sequence[str],
    height: int,
    width: int,
) -> Dict[int, Tuple[float, float]]:
    """Calcula posiciones (x, y) para cada nodo del dendrograma."""

    nodes = {node.id: node for node in history}
    leaves = [node for node in history if node.left is None and node.right is None]
    leaves.sort(key=lambda n: n.id)

    margin_x = 140
    margin_y = 130
    available_width = max(width - 2 * margin_x, 100)
    available_height = max(height - 2 * margin_y, 100)

    # Espaciamos las hojas equitativamente a lo largo del eje X.
    leaf_spacing = available_width / max(len(leaves), 1)
    positions: Dict[int, Tuple[float, float]] = {}

    for idx, leaf in enumerate(leaves):
        x = margin_x + idx * leaf_spacing + leaf_spacing / 2
        y = height - margin_y
        positions[leaf.id] = (x, y)

    # Usamos la distancia máxima para escalar la altura de los nodos internos.
    max_distance = max((node.distance for node in history), default=1.0) or 1.0

    def set_position(node_id: int) -> Tuple[float, float]:
        if node_id in positions:
            return positions[node_id]

        node = nodes[node_id]
        if node.left is None or node.right is None:
            return positions[node_id]

        left_pos = set_position(node.left)
        right_pos = set_position(node.right)

        # Los nodos internos se ubican en el punto medio horizontal de sus hijos y a una altura proporcional a la distancia.
        x = (left_pos[0] + right_pos[0]) / 2
        y = height - margin_y - (node.distance / max_distance) * available_height
        positions[node_id] = (x, y)
        return positions[node_id]

    set_position(root_id)
    return positions


def write_dendrogram_svg(
    history: Sequence[ClusterNode],
    root_id: int,
    labels: Sequence[str],
    output_path: str,
    is_best: bool,
    coherence: float,
    method_key: str,
    best_method_key: str,
    best_coherence: float,
) -> str:
    """Genera un archivo HTML con un SVG del dendrograma."""

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    width = max(1600, 240 * len(labels))
    plot_height = max(900, 220 * len(labels))
    extra_bottom = 240
    total_height = plot_height + extra_bottom

    positions = layout_positions(history, root_id, labels, plot_height, width)

    lines: List[str] = []
    texts: List[str] = []

    # Dibujamos las ramas verticales y horizontales de cada fusión.
    for node in history:
        if node.left is None or node.right is None:
            continue
        x_parent, y_parent = positions[node.id]
        x_left, y_left = positions[node.left]
        x_right, y_right = positions[node.right]

        lines.append(
            f'<line x1="{x_left:.2f}" y1="{y_left:.2f}" '
            f'x2="{x_left:.2f}" y2="{y_parent:.2f}" stroke="#444" stroke-width="2"/>'
        )
        lines.append(
            f'<line x1="{x_right:.2f}" y1="{y_right:.2f}" '
            f'x2="{x_right:.2f}" y2="{y_parent:.2f}" stroke="#444" stroke-width="2"/>'
        )
        lines.append(
            f'<line x1="{x_left:.2f}" y1="{y_parent:.2f}" '
            f'x2="{x_right:.2f}" y2="{y_parent:.2f}" stroke="#222" stroke-width="2"/>'
        )

    # Añadimos etiquetas rotadas para evitar solapamientos y mejorar la legibilidad.
    for idx, label in enumerate(labels):
        if idx not in positions:
            continue
        x, y = positions[idx]
        text_x = x + 16
        text_y = y + 84
        texts.append(
            f'<text x="{text_x:.2f}" y="{text_y:.2f}" font-size="12" '
            f'fill="#111" text-anchor="end" '
            f'transform="rotate(-35 {text_x:.2f} {text_y:.2f})">{html.escape(label)}</text>'
        )

    svg_content = "\n".join(lines + texts)
    metodo_actual = METHOD_LABELS.get(method_key, method_key.title())
    mejor_metodo = METHOD_LABELS.get(best_method_key, best_method_key.title())
    if is_best:
        best_line = (
            "Método con mayor coherencia entre los tres analizados."
        )
    else:
        best_line = (
            f"Método más coherente: {mejor_metodo} (coeficiente {best_coherence:.3f})."
        )

    note_lines = [
        f"Coeficiente cophenético: {coherence:.3f}",
        best_line,
        "Archivo generado automáticamente por req4.py",
    ]
    note_content = "<br/>".join(note_lines)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <title>Dendrograma </title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #fafafa; margin: 0; }}
    .container {{
      margin: 24px auto;
      padding: 16px;
      max-width: 95vw;
      background: #ffffff;
      border-radius: 12px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
    }}
    h2 {{ margin-top: 0; }}
    .canvas-wrapper {{
      overflow: auto;
      padding: 12px;
      border: 1px solid #ccc;
      border-radius: 8px;
      background: #fff;
    }}
    svg {{
      min-width: {width}px;
      min-height: {total_height}px;
      width: 100%;
      margin-bottom: 24px;
      padding-bottom: 24px;
    }}
    .note {{
      margin-top: 12px;
      padding: 12px;
      border-radius: 8px;
      background: #f5f8ff;
      border: 1px solid #dce5ff;
      color: #31456a;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h2>Dendrograma – {metodo_actual}</h2>
    <div class="canvas-wrapper">
      <svg xmlns="http://www.w3.org/2000/svg"
           viewBox="0 0 {width} {total_height}"
           preserveAspectRatio="xMidYMid meet">
        {svg_content}
      </svg>
    </div>
    <div class="note">
      <p>{note_content}</p>
    </div>
  </div>
</body>
</html>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path


# ---------------------------------------------------------------------------
# Flujo principal del requerimiento
# ---------------------------------------------------------------------------

def run_clustering_pipeline(
    bibtex_path: str,
    output_dir: str,
    max_articles: int | None = None,
    metric: str = "cosine",
) -> Dict[str, Dict[str, float | str]]:
    """Ejecuta el flujo de clustering jerárquico y genera resultados."""

    if metric != "cosine":
        raise ValueError("Esta implementación simplificada solo soporta la métrica 'cosine'.")

    # 1) Cargamos los artículos y validamos que haya suficientes abstracts.
    articles = load_articles_from_bibtex(bibtex_path, max_articles)
    if len(articles) < 2:
        raise ValueError(
            f"Se necesitan al menos dos artículos con abstract válido. Encontrados: {len(articles)}"
        )

    print(f"📚 Artículos cargados para clustering: {len(articles)}")

    # 2) Generamos los vectores TF-IDF y la matriz de distancias coseno.
    vectors = compute_tfidf_vectors(articles)
    base_dist = pairwise_distances(vectors)

    # 3) Creamos etiquetas amigables para las visualizaciones.
    labels = [
        f"Artículo {idx + 1} – {art.title[:55]}"
        for idx, art in enumerate(articles)
    ]
    methods = ("single", "complete", "average")
    results: Dict[str, Dict[str, float | str]] = {}

    # 4) Ejecutamos el clustering para cada método de enlace y guardamos datos intermedios.
    intermediate: Dict[str, Dict[str, object]] = {}
    for method in methods:
        print(f"🧪 Ejecutando clustering jerárquico ({method})…")
        history, root_id = hierarchical_clustering(base_dist, len(articles), method)
        coherence = compute_cophenetic_coefficient(history, base_dist)
        intermediate[method] = {
            "history": history,
            "root_id": root_id,
            "coherence": coherence,
        }

    # 5) Determinamos el método con mayor coherencia (mejor ajuste del dendrograma).
    best_method = max(
        intermediate.items(), key=lambda item: item[1]["coherence"]
    )[0]
    best_coherence = float(intermediate[best_method]["coherence"])

    # 6) Generamos visualizaciones HTML y consolidamos el reporte final para cada método.
    for method in methods:
        data = intermediate[method]
        coherence = float(data["coherence"])
        output_path = os.path.join(output_dir, f"dendrogram_{method}.html")
        write_dendrogram_svg(
            history=data["history"],
            root_id=data["root_id"],
            labels=labels,
            output_path=output_path,
            is_best=(method == best_method),
            coherence=coherence,
            method_key=method,
            best_method_key=best_method,
            best_coherence=best_coherence,
        )

        results[method] = {
            "cophenetic": coherence,
            "visualization": output_path,
            "method_label": METHOD_LABELS.get(method, method.title()),
        }
        print(f"   → Dendrograma generado en {output_path}")
        print(f"   → Coeficiente cophenético aproximado: {coherence:.3f}")

    print(f"✅ Método con mayor coherencia (aprox.): {best_method}")

    # 7) Persistimos un resumen JSON para facilitar el análisis posterior.
    os.makedirs(output_dir, exist_ok=True)
    summary_path = os.path.join(output_dir, "req4_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f_summary:
        json.dump(
            {
                "metric": metric,
                "results": results,
                "best_method": best_method,
                "best_method_label": METHOD_LABELS.get(best_method, best_method.title()),
                "best_coherence": best_coherence,
            },
            f_summary,
            indent=2,
        )
    print(f"💾 Resumen guardado en {summary_path}")

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clustering jerárquico para abstracts (Req. 4)"
    )
    parser.add_argument(
        "--entrada",
        default="Data/unificados.bib",
        help="Ruta al archivo BibTeX de entrada.",
    )
    parser.add_argument(
        "--salida",
        default="Data/visualizations/req4",
        help="Directorio donde se guardarán las visualizaciones y resúmenes.",
    )
    parser.add_argument(
        "--max-articulos",
        type=int,
        default=None,
        help="Número máximo de artículos a considerar (útil para pruebas rápidas).",
    )
    parser.add_argument(
        "--metrica",
        default="cosine",
        choices=["cosine"],
        help="Métrica de distancia para el clustering (solo 'cosine' en esta versión).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_clustering_pipeline(
        bibtex_path=args.entrada,
        output_dir=args.salida,
        max_articles=args.max_articulos,
        metric=args.metrica,
    )


if __name__ == "__main__":
    main()

