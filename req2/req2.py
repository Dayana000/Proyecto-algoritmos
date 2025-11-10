# req2/menu_req2.py
"""
Interfaz de línea de comandos para el Requerimiento 2.

Permite:
1. Cargar un archivo BibTeX con artículos.
2. Seleccionar dos o más artículos (por índice).
3. Ejecutar todos los algoritmos de similitud textual disponibles.
"""

from pathlib import Path
import sys

# Asegura que el directorio raíz del proyecto esté en sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from itertools import combinations

from req2.req2Backend import (
    analizar_similitud,
    cargar_articulos_desde_bib,
)


def mostrar_articulos(articulos):
    print("\n===== LISTA DE ARTÍCULOS =====")
    for i, art in enumerate(articulos):
        titulo = art.get("title", "Título desconocido")
        autores = art.get("author", "Autor desconocido")
        print(f"{i:>4}: {titulo[:70]}  —  {autores[:40]}")
    print("==============================\n")


def seleccionar_indices(articulos):
    while True:
        raw = input(
            "Ingresa los índices de dos o más artículos separados por coma (ej. 0,3,5): "
        ).strip()
        if not raw:
            print("Debes ingresar al menos dos índices.")
            continue
        try:
            indices = sorted({int(x) for x in raw.replace(" ", "").split(",")})
        except ValueError:
            print("Entrada inválida. Usa números separados por comas.")
            continue

        if len(indices) < 2:
            print("Selecciona al menos dos artículos.")
            continue

        if any(i < 0 or i >= len(articulos) for i in indices):
            print("Alguno de los índices está fuera de rango.")
            continue

        return indices


def imprimir_resultados(titulo1, titulo2, resultados):
    print("===== RESULTADOS =====")
    print(f"Título 1: {titulo1}")
    print(f"Título 2: {titulo2}\n")

    print("--- ALGORITMOS CLÁSICOS ---")
    print(f"Levenshtein (distancia): {resultados['levenshtein']}")
    print(f"Jaccard (0-1): {resultados['jaccard']:.4f}")
    print(f"Dice (0-1): {resultados['dice']:.4f}")
    print(f"Coseno TF-IDF (0-1): {resultados['coseno_tfidf']:.4f}")

    print("\n--- ALGORITMOS DE IA ---")
    if resultados["ia_modelos_disponibles"]:
        print(f"IA Embeddings SBERT (0-1): {resultados['ia_embeddings']:.4f}")
        print(f"IA Embeddings Paraphrase (0-1): {resultados['ia_embeddings_alt']:.4f}")
    else:
        print("⚠️  Modelos de IA no disponibles (instala sentence-transformers).")
    print("=========================\n")


def iniciar_menu():
    print("\n=== ANÁLISIS DE SIMILITUD TEXTUAL ===\n")

    ruta = input("Ingrese la ruta del archivo .bib (ej: Data/unificados.bib): ").strip()
    try:
        articulos = cargar_articulos_desde_bib(ruta)
    except FileNotFoundError as exc:
        print(exc)
        return

    if len(articulos) < 2:
        print("Se necesitan al menos 2 artículos en el archivo.")
        return

    mostrar_articulos(articulos)
    indices = seleccionar_indices(articulos)

    for i, j in combinations(indices, 2):
        art1 = articulos[i]
        art2 = articulos[j]

        texto1 = art1.get("abstract", "")
        texto2 = art2.get("abstract", "")

        if not texto1 or not texto2:
            print(f"⚠️  Alguno de los artículos {i} o {j} no tiene abstract. Se omite.")
            continue

        print(f"\nComparando artículos {i} y {j}...")
        resultados = analizar_similitud(texto1, texto2)
        imprimir_resultados(art1.get("title", ""), art2.get("title", ""), resultados)


if __name__ == "__main__":
    iniciar_menu()