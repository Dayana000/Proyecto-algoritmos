# req3/menu_req3.py
"""
Menú para el Requerimiento 3: análisis de frecuencias y palabras asociadas.
"""

from pathlib import Path
import sys

# Asegura que el directorio raíz del proyecto esté en sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from req2.req2Backend import cargar_articulos_desde_bib
from req3 import req3Backend as backend


def iniciar_menu():
    """Flujo interactivo: carga el BibTeX, procesa frecuencias y muestra resultados."""
    print("\n=== FRECUENCIA DE CONCEPTOS EN ABSTRACTS ===\n")

    ruta = input("Ingrese la ruta del archivo .bib (ej: Data/unificados.bib): ").strip()
    try:
        articulos = cargar_articulos_desde_bib(ruta)
    except FileNotFoundError as exc:
        print(exc)
        return

    if not articulos:
        print("El archivo no contiene artículos con abstracts.")
        return

    print("\nCalculando frecuencias...\n")
    frecuencias = backend.frecuencia_palabras_asociadas(articulos)

    print("=== FRECUENCIAS DE PALABRAS ASOCIADAS ===")
    for palabra, freq in frecuencias.items():
        print(f"{palabra}: {freq}")

    print("\nBuscando nuevas palabras relevantes...\n")
    nuevas = backend.nuevas_palabras_relevantes(articulos)

    if nuevas:
        print("=== NUEVAS PALABRAS SUGERIDAS ===")
        for palabra, score in nuevas:
            print(f"{palabra}: {score:.3f}")
    else:
        print("No se encontraron palabras adicionales con relevancia significativa.")

    precision = backend.medir_precision(nuevas)
    print(f"\nPrecisión estimada de nuevas palabras: {precision:.2f}")
    print("==========================================\n")


if __name__ == "__main__":
    iniciar_menu()
