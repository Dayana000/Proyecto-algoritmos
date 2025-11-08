# req2/menu_req2.py
from req2.req2 import cargar_articulos_desde_bib, analizar_similitud

def mostrar_articulos(articulos):
    print("\n===== LISTA DE ARTÍCULOS =====")
    for i, art in enumerate(articulos):
        print(f"{i}. {art['title'][:80]}...")
    print("==============================\n")

def seleccionar_articulo(msg, articulos):
    while True:
        try:
            index = int(input(msg))
            if 0 <= index < len(articulos):
                return articulos[index]
            print("Índice inválido, inténtelo de nuevo.")
        except ValueError:
            print("Debe ingresar un número.")

def iniciar_menu():
    print("\n=== ANÁLISIS DE SIMILITUD TEXTUAL ===\n")

    ruta = input("Ingrese la ruta del archivo .bib (ej: Data/unificados.bib): ").strip()
    articulos = cargar_articulos_desde_bib(ruta)

    if len(articulos) < 2:
        print("Se necesitan al menos 2 artículos en el archivo.")
        return

    mostrar_articulos(articulos)

    art1 = seleccionar_articulo("Seleccione el primer artículo: ", articulos)
    art2 = seleccionar_articulo("Seleccione el segundo artículo: ", articulos)

    texto1 = art1["abstract"]
    texto2 = art2["abstract"]

    print("\nCalculando similitudes...\n")
    resultados = analizar_similitud(texto1, texto2)

    print("===== RESULTADOS =====")
    print(f"Título 1: {art1['title']}")
    print(f"Título 2: {art2['title']}\n")

    print("Levenshtein (distancia):", resultados["levenshtein"])
    print("Jaccard (0-1):", resultados["jaccard"])
    print("Coseno TF-IDF (0-1):", resultados["coseno_tfidf"])
    print("Dice (0-1):", resultados["dice"])
    print("IA Embeddings (0-1):", resultados["ia_embeddings"])
    print("======================\n")

if __name__ == "__main__":
    iniciar_menu()

#Asi llamar desde main
#from req2.menu_req2 import iniciar_menu

#def main():
 #   iniciar_menu()

#if __name__ == "__main__":
 #   main()