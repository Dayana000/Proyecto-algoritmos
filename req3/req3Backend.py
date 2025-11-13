# req3/req3Backend.py
"""
Módulo backend para el Requerimiento 3: Análisis de frecuencia de conceptos en abstracts.

Este módulo implementa:
1. Cálculo de frecuencia de palabras asociadas a la categoría "Concepts of Generative AI in Education"
2. Generación de nuevas palabras relevantes usando TF-IDF (máximo 15)
3. Medición de precisión de las nuevas palabras sugeridas

CÓMO SE LLAMA DESDE EL MAIN:
-----------------------------
Este módulo NO se llama directamente desde main.py. En su lugar, se usa a través de req3.py:

1. Desde main.py o cualquier script principal:
   ```python
   from req3.req3 import iniciar_menu
   iniciar_menu()
   ```

2. El archivo req3.py importa las funciones de este módulo:
   ```python
   from req3.req3Backend import frecuencia_palabras_asociadas, nuevas_palabras_relevantes, medir_precision
   ```

3. Flujo de uso típico en req3.py:
   ```python
   # 1. Cargar artículos desde archivo .bib
   from req2.req2 import cargar_articulos_desde_bib
   articulos = cargar_articulos_desde_bib(ruta_archivo)
   
   # 2. Calcular frecuencias de palabras asociadas
   frecuencias = frecuencia_palabras_asociadas(articulos)
   # Retorna: {"generative models": 5, "prompting": 12, ...}
   
   # 3. Generar nuevas palabras relevantes (máximo 15)
   nuevas = nuevas_palabras_relevantes(articulos)
   # Retorna: [("neural", 0.234), ("deep", 0.189), ...]
   
   # 4. Medir precisión de las nuevas palabras
   precision = medir_precision(nuevas)
   # Retorna: 0.73 (73% de precisión)
   ```

USO DIRECTO (si se necesita usar las funciones directamente):
-------------------------------------------------------------
```python
from req3.req3Backend import frecuencia_palabras_asociadas, nuevas_palabras_relevantes, medir_precision
from req2.req2 import cargar_articulos_desde_bib

# Cargar artículos
articulos = cargar_articulos_desde_bib("Data/unificados.bib")

# Calcular frecuencias
frecuencias = frecuencia_palabras_asociadas(articulos)
for palabra, freq in frecuencias.items():
    print(f"{palabra}: {freq}")

# Obtener nuevas palabras
nuevas = nuevas_palabras_relevantes(articulos, limite=15)
for palabra, score in nuevas:
    print(f"{palabra}: {score:.3f}")

# Medir precisión
precision = medir_precision(nuevas)
print(f"Precisión: {precision:.2f}")
```

NOTA: Las funciones esperan que los artículos sean una lista de diccionarios con al menos
la clave "abstract" que contenga el texto del abstract de cada artículo.
"""

import re
from collections import Counter
from math import log

# Palabras asociadas a la categoría "Concepts of Generative AI in Education"
# Estas son las palabras clave definidas en el requerimiento que se deben buscar en los abstracts
PALABRAS_ASOCIADAS = [
    "generative models", "prompting", "machine learning", "multimodality",
    "fine-tuning", "training data", "algorithmic bias", "explainability",
    "transparency", "ethics", "privacy", "personalization",
    "human-ai interaction", "ai literacy", "co-creation"
]

STOPWORDS_EN = {
    "a", "an", "and", "the", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "for", "on", "with", "as", "by", "at", "from", "up", "down",
    "out", "about", "into", "over", "after", "before", "between", "but", "if",
    "because", "while", "do", "does", "did", "doing", "this", "that", "these",
    "those", "he", "she", "it", "they", "them", "his", "her", "their", "our", "we",
    "you", "your", "i", "me", "my", "mine", "ours", "yours", "hers", "him",
    "himself", "herself", "yourself", "themselves", "itself", "what", "which",
    "who", "whom", "where", "when", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "can", "will", "just", "don",
    "should", "now"
}

def limpiar_texto(texto):
    """
    Normaliza y limpia el texto para facilitar el análisis.
    
    Args:
        texto (str): Texto a limpiar
        
    Returns:
        str: Texto normalizado (minúsculas, sin caracteres especiales, espacios normalizados)
    """
    # Convertir a minúsculas para búsqueda case-insensitive
    texto = texto.lower()
    # Eliminar caracteres especiales, mantener solo letras, números, espacios y guiones
    texto = re.sub(r"[^a-zA-Záéíóúüñ0-9\s-]", " ", texto)
    # Normalizar espacios múltiples a un solo espacio
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def _tokenizar(texto: str) -> list[str]:
    """Tokeniza un texto en palabras significativas, filtrando stopwords y términos cortos."""
    return [
        token for token in limpiar_texto(texto).split()
        if token and token not in STOPWORDS_EN and len(token) > 2
    ]


def _tfidf_promedio(token_lists: list[list[str]]) -> dict[str, float]:
    """
    Calcula un score promedio TF-IDF para cada término dado un corpus tokenizado.
    Se promedia por documento para favorecer términos que aparecen consistentemente en múltiples abstracts.
    """
    if not token_lists:
        return {}

    documentos = len(token_lists)
    df = Counter()
    for tokens in token_lists:
        df.update(set(tokens))

    idf = {
        palabra: log((documentos + 1) / (df[palabra] + 1)) + 1.0
        for palabra in df.keys()
    }

    importancia: dict[str, float] = Counter()
    for tokens in token_lists:
        conteo = Counter(tokens)
        longitud = len(tokens) or 1
        for palabra, frecuencia in conteo.items():
            tf = frecuencia / longitud
            importancia[palabra] += tf * idf.get(palabra, 1.0)

    for palabra in list(importancia.keys()):
        importancia[palabra] /= documentos

    return dict(importancia)

def frecuencia_palabras_asociadas(articulos):
    """
    Calcula la frecuencia de aparición de cada palabra asociada en los abstracts de los artículos.
    
    Esta función cumple con la primera parte del Requerimiento 3: calcular y presentar
    la frecuencia de aparición de las palabras asociadas a la categoría, teniendo como
    fuente el abstract de cada artículo.
    
    CÓMO SE LLAMA DESDE EL MAIN:
    ----------------------------
    Esta función se llama desde req3.py en la función iniciar_menu():
    
    ```python
    # En req3.py
    from req3.req3Backend import frecuencia_palabras_asociadas
    from req2.req2 import cargar_articulos_desde_bib
    
    articulos = cargar_articulos_desde_bib(ruta)
    frecuencias = frecuencia_palabras_asociadas(articulos)
    
    # Mostrar resultados
    for palabra, freq in frecuencias.items():
        print(f"{palabra}: {freq}")
    ```
    
    Args:
        articulos (list): Lista de diccionarios con información de artículos (debe tener clave "abstract")
                         Ejemplo: [{"abstract": "texto del abstract", ...}, ...]
        
    Returns:
        dict: Diccionario con cada palabra asociada como clave y su frecuencia total como valor
              Ejemplo: {"generative models": 5, "prompting": 12, "machine learning": 8, ...}
    """
    conteo = Counter()

    # Recorrer todos los artículos
    for articulo in articulos:
        # Obtener y limpiar el abstract del artículo
        abstract = limpiar_texto(articulo.get("abstract", ""))

        # Buscar cada palabra asociada en el abstract
        for palabra in PALABRAS_ASOCIADAS:
            # Escapar caracteres especiales para búsqueda literal
            patron = re.escape(palabra.lower())
            # Contar cuántas veces aparece la palabra en el abstract
            apariciones = len(re.findall(patron, abstract))
            # Acumular el conteo total
            conteo[palabra] += apariciones

    return dict(conteo)

def nuevas_palabras_relevantes(articulos, limite=15):
    """
    Genera un listado de nuevas palabras relevantes (máximo 15) analizando todos los abstracts.
    
    Esta función cumple con la segunda parte del Requerimiento 3: usar un algoritmo que
    analice todos los abstracts y genere un listado de palabras asociadas (máximo 15).
    
    Utiliza TF-IDF (Term Frequency-Inverse Document Frequency) para identificar palabras
    que son relevantes pero que no están en la lista de palabras asociadas originales.
    
    CÓMO SE LLAMA DESDE EL MAIN:
    ----------------------------
    Esta función se llama desde req3.py en la función iniciar_menu():
    
    ```python
    # En req3.py
    from req3.req3Backend import nuevas_palabras_relevantes
    from req2.req2 import cargar_articulos_desde_bib
    
    articulos = cargar_articulos_desde_bib(ruta)
    nuevas = nuevas_palabras_relevantes(articulos)  # Por defecto retorna máximo 15
    
    # Mostrar resultados
    for palabra, score in nuevas:
        print(f"{palabra}: {score:.3f}")
    ```
    
    Args:
        articulos (list): Lista de diccionarios con información de artículos (debe tener clave "abstract")
                         Ejemplo: [{"abstract": "texto del abstract", ...}, ...]
        limite (int): Número máximo de palabras a retornar (por defecto 15)
        
    Returns:
        list: Lista de tuplas (palabra, score_tfidf) ordenadas por relevancia descendente
              Ejemplo: [("neural", 0.234), ("deep", 0.189), ("network", 0.156), ...]
              Cada tupla contiene: (palabra, score_tfidf) donde score_tfidf es un float
    """
    token_lists = [_tokenizar(a.get("abstract", "")) for a in articulos]
    importancia_promedio = _tfidf_promedio(token_lists)

    if not importancia_promedio:
        return []

    asociadas = set(pal.lower() for pal in PALABRAS_ASOCIADAS)
    ranking = [
        (palabra, score)
        for palabra, score in importancia_promedio.items()
        if palabra not in asociadas
    ]

    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:limite]

def medir_precision(nuevas_palabras):
    """
    Determina qué tan precisas son las nuevas palabras sugeridas.
    
    Esta función cumple con la tercera parte del Requerimiento 3: determinar qué tan
    precisas son las nuevas palabras. Evalúa si las palabras sugeridas están relacionadas
    con los temas de IA y educación, que son relevantes para la categoría.
    
    La precisión se calcula como el porcentaje de palabras que contienen términos clave
    relacionados con IA y educación.
    
    CÓMO SE LLAMA DESDE EL MAIN:
    ----------------------------
    Esta función se llama desde req3.py en la función iniciar_menu(), después de obtener
    las nuevas palabras:
    
    ```python
    # En req3.py
    from req3.req3Backend import nuevas_palabras_relevantes, medir_precision
    from req2.req2 import cargar_articulos_desde_bib
    
    articulos = cargar_articulos_desde_bib(ruta)
    nuevas = nuevas_palabras_relevantes(articulos)
    precision = medir_precision(nuevas)  # Recibe el resultado de nuevas_palabras_relevantes
    
    # Mostrar resultado
    print(f"Precisión estimada de nuevas palabras: {precision:.2f}")
    ```
    
    Args:
        nuevas_palabras (list): Lista de tuplas (palabra, score) retornada por nuevas_palabras_relevantes()
                               Ejemplo: [("neural", 0.234), ("deep", 0.189), ...]
        
    Returns:
        float: Precisión estimada entre 0.0 y 1.0 (0.0 = 0%, 1.0 = 100%)
               Ejemplo: 0.73 significa 73% de precisión
               Retorna 0.0 si nuevas_palabras está vacía
    """
    # Palabras clave que indican relevancia con IA y educación
    palabras_clave = ["ai", "human", "model", "learning", "data", "education", "interaction"]

    # Si no hay palabras nuevas, precisión es 0
    if not nuevas_palabras:
        return 0.0

    # Contar cuántas palabras nuevas contienen al menos una palabra clave
    validas = 0
    for palabra, _ in nuevas_palabras:
        # Verificar si la palabra contiene alguna palabra clave
        if any(key in palabra for key in palabras_clave):
            validas += 1

    # Precisión = palabras válidas / total de palabras nuevas
    # Esta métrica es heurística: asume que nuevas palabras deberían incluir términos ligados a IA/educación.
    return validas / len(nuevas_palabras)
