# req3/menu_req3.py
from req2.req2 import cargar_articulos_desde_bib
from req3.req3 import frecuencia_palabras_asociadas, nuevas_palabras_relevantes, medir_precision

def iniciar_menu():
    print("\n=== FRECUENCIA DE CONCEPTOS EN ABSTRACTS ===\n")

    ruta = input("Ingrese la ruta del archivo .bib: ").strip()
    articulos = cargar_articulos_desde_bib(ruta)

    print("\nCalculando frecuencias...\n")
    frecuencias = frecuencia_palabras_asociadas(articulos)

    print("=== FRECUENCIAS DE PALABRAS ASOCIADAS ===")
    for palabra, freq in frecuencias.items():
        print(f"{palabra}: {freq}")

    print("\nBuscando nuevas palabras relevantes...\n")
    nuevas = nuevas_palabras_relevantes(articulos)

    print("=== NUEVAS PALABRAS SUGERIDAS ===")
    for palabra, score in nuevas:
        print(f"{palabra}: {score:.3f}")

    precision = medir_precision(nuevas)
    print(f"\nPrecisión estimada de nuevas palabras: {precision:.2f}")
    print("==========================================\n")

if __name__ == "__main__":
    iniciar_menu()



# así se llama desde el  main.py
#from req3.menu_req3 import iniciar_menu

#if __name__ == "__main__":
 #   iniciar_menu()