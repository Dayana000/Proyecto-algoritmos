# req2/req2Backend.py
"""
Módulo backend para el Requerimiento 2: Análisis de similitud textual.

Este módulo implementa:
1. Cuatro algoritmos clásicos de similitud textual:
   - Levenshtein (distancia de edición)
   - Jaccard (vectorización estadística)
   - Dice (vectorización estadística)
   - Coseno TF-IDF (vectorización estadística)
2. Dos algoritmos con modelos de IA:
   - IA Embeddings (SBERT - Sentence-BERT)
   - IA Embeddings con modelo alternativo (Universal Sentence Encoder o similar)
"""

import re
from math import sqrt
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util

# Modelos IA para embeddings (si no están instalados: pip install sentence-transformers)
# Modelo 1: SBERT (Sentence-BERT) - modelo ligero y rápido
modelo_embeddings_sbert = SentenceTransformer('all-MiniLM-L6-v2')

# Modelo 2: Modelo alternativo para comparación (usando otro modelo de SBERT)
# Si se quiere usar un modelo diferente, se puede cambiar aquí
modelo_embeddings_alternativo = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def limpiar(texto):
    """
    Función auxiliar para limpiar y normalizar texto antes del análisis.
    
    Esta función:
    1. Convierte el texto a minúsculas (normalización)
    2. Elimina caracteres especiales, manteniendo solo letras, números y espacios
    3. Normaliza espacios múltiples a un solo espacio
    
    Args:
        texto (str): Texto a limpiar
        
    Returns:
        str: Texto normalizado y limpio
    """
    # Convertir a minúsculas para normalización
    texto = texto.lower()
    # Eliminar caracteres especiales, mantener solo letras, números y espacios
    # r"[^a-z0-9áéíóúüñ\s]" significa: cualquier cosa que NO sea letra, número o espacio
    texto = re.sub(r"[^a-z0-9áéíóúüñ\s]", " ", texto)
    # Normalizar espacios múltiples a un solo espacio
    # r"\s+" significa: uno o más espacios en blanco
    texto = re.sub(r"\s+", " ", texto)
    # Eliminar espacios al inicio y final
    return texto.strip()

# -----------------------------------------------------------
# 1) LEVENSHTEIN (Distancia de Edición)
# -----------------------------------------------------------
def distancia_levenshtein(a, b):
    """
    Calcula la distancia de Levenshtein entre dos textos.
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    La distancia de Levenshtein es el número mínimo de operaciones (inserción,
    eliminación o sustitución) necesarias para transformar un texto en otro.
    
    Fórmula matemática (programación dinámica):
    - dp[i][j] = distancia entre los primeros i caracteres de a y los primeros j caracteres de b
    - Casos base:
      * dp[0][j] = j (insertar j caracteres)
      * dp[i][0] = i (eliminar i caracteres)
    - Caso general:
      * Si a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] (sin costo)
      * Si a[i-1] != b[j-1]: dp[i][j] = min(
          dp[i-1][j] + 1,      # Eliminación
          dp[i][j-1] + 1,      # Inserción
          dp[i-1][j-1] + 1     # Sustitución
        )
    
    Complejidad: O(m * n) donde m y n son las longitudes de los textos.
    Espacio: O(m * n) para la matriz de programación dinámica.
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        int: Distancia de Levenshtein (número mínimo de operaciones)
    """
    a, b = limpiar(a), limpiar(b)
    m, n = len(a), len(b)

    # Inicializar matriz de programación dinámica
    # dp[i][j] = distancia entre a[0:i] y b[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Casos base: distancia de cadena vacía a otra cadena
    for i in range(m + 1):
        dp[i][0] = i  # Eliminar i caracteres
    for j in range(n + 1):
        dp[0][j] = j  # Insertar j caracteres

    # Llenar la matriz usando programación dinámica
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Si los caracteres son iguales, no hay costo
            costo = 0 if a[i - 1] == b[j - 1] else 1
            # Calcular mínimo entre las tres operaciones posibles
            dp[i][j] = min(
                dp[i-1][j] + 1,      # Eliminación: eliminar a[i-1]
                dp[i][j-1] + 1,      # Inserción: insertar b[j-1]
                dp[i-1][j-1] + costo # Sustitución: reemplazar a[i-1] por b[j-1]
            )

    # La distancia final está en dp[m][n]
    return dp[m][n]

# -----------------------------------------------------------
# 2) JACCARD (Vectorización Estadística)
# -----------------------------------------------------------
def similitud_jaccard(a, b):
    """
    Calcula la similitud de Jaccard entre dos textos.
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    El coeficiente de Jaccard mide la similitud entre dos conjuntos.
    Se basa en la intersección y unión de los conjuntos de palabras.
    
    Fórmula matemática:
    J(A, B) = |A ∩ B| / |A ∪ B|
    
    Donde:
    - A = conjunto de palabras del texto 1
    - B = conjunto de palabras del texto 2
    - |A ∩ B| = número de palabras comunes (intersección)
    - |A ∪ B| = número de palabras únicas en ambos textos (unión)
    
    Algoritmo paso a paso:
    1. Limpiar y normalizar ambos textos
    2. Convertir cada texto en un conjunto de palabras (tokens)
    3. Calcular intersección: palabras que aparecen en ambos textos
    4. Calcular unión: todas las palabras únicas de ambos textos
    5. Dividir tamaño de intersección entre tamaño de unión
    
    Resultado: Valor entre 0 y 1
    - 0 = textos completamente diferentes (sin palabras comunes)
    - 1 = textos idénticos (mismas palabras)
    
    Complejidad: O(n + m) donde n y m son el número de palabras únicas.
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        float: Similitud de Jaccard entre 0 y 1
    """
    # Convertir textos en conjuntos de palabras
    set1 = set(limpiar(a).split())
    set2 = set(limpiar(b).split())
    
    # Si alguno de los conjuntos está vacío, similitud es 0
    if not set1 or not set2:
        return 0
    
    # Calcular intersección (palabras comunes)
    interseccion = len(set1 & set2)
    
    # Calcular unión (todas las palabras únicas)
    union = len(set1 | set2)
    
    # Retornar coeficiente de Jaccard
    return interseccion / union

# -----------------------------------------------------------
# 3) DICE (Vectorización Estadística)
# -----------------------------------------------------------
def bigramas(texto):
    """
    Extrae los bigramas (pares de caracteres consecutivos) de un texto.
    
    Args:
        texto (str): Texto del cual extraer bigramas
        
    Returns:
        set: Conjunto de bigramas únicos
    """
    texto = limpiar(texto)
    # Generar todos los pares de caracteres consecutivos
    return {texto[i:i+2] for i in range(len(texto)-1)}

def similitud_dice(a, b):
    """
    Calcula el coeficiente de Dice (Sørensen-Dice) entre dos textos.
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    El coeficiente de Dice mide la similitud entre dos conjuntos basándose
    en bigramas (pares de caracteres consecutivos).
    
    Fórmula matemática:
    Dice(A, B) = (2 * |A ∩ B|) / (|A| + |B|)
    
    Donde:
    - A = conjunto de bigramas del texto 1
    - B = conjunto de bigramas del texto 2
    - |A ∩ B| = número de bigramas comunes
    - |A| + |B| = suma del número de bigramas en cada texto
    
    Algoritmo paso a paso:
    1. Limpiar y normalizar ambos textos
    2. Extraer bigramas de cada texto (pares de caracteres consecutivos)
    3. Calcular intersección: bigramas comunes
    4. Calcular suma de tamaños: |A| + |B|
    5. Aplicar fórmula: (2 * intersección) / suma
    
    Diferencias con Jaccard:
    - Dice da más peso a la intersección (multiplica por 2)
    - Jaccard usa unión, Dice usa suma
    - Dice es más sensible a textos con muchas palabras comunes
    
    Resultado: Valor entre 0 y 1
    - 0 = textos completamente diferentes
    - 1 = textos idénticos
    
    Complejidad: O(n + m) donde n y m son las longitudes de los textos.
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        float: Coeficiente de Dice entre 0 y 1
    """
    # Extraer bigramas de cada texto
    b1 = bigramas(a)
    b2 = bigramas(b)
    
    # Si alguno está vacío, similitud es 0
    if not b1 or not b2:
        return 0
    
    # Calcular intersección (bigramas comunes)
    interseccion = len(b1 & b2)
    
    # Calcular suma de tamaños
    suma = len(b1) + len(b2)
    
    # Aplicar fórmula de Dice
    return (2 * interseccion) / suma

# -----------------------------------------------------------
# 4) COSENO TF-IDF (Vectorización Estadística)
# -----------------------------------------------------------
def similitud_coseno_tfidf(a, b):
    """
    Calcula la similitud del coseno usando vectores TF-IDF entre dos textos.
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    La similitud del coseno mide el ángulo entre dos vectores en un espacio
    de alta dimensionalidad. Usa TF-IDF para ponderar las palabras.
    
    TF-IDF (Term Frequency-Inverse Document Frequency):
    - TF(t, d) = frecuencia del término t en el documento d
    - IDF(t) = log(N / df(t)) donde N es el número de documentos y df(t) es
      el número de documentos que contienen el término t
    - TF-IDF(t, d) = TF(t, d) * IDF(t)
    
    Fórmula de similitud del coseno:
    cos(θ) = (A · B) / (||A|| * ||B||)
    
    Donde:
    - A · B = producto punto (suma de productos elemento por elemento)
    - ||A|| = norma euclidiana del vector A = sqrt(Σ(Ai²))
    - ||B|| = norma euclidiana del vector B = sqrt(Σ(Bi²))
    
    Algoritmo paso a paso:
    1. Crear vectorizador TF-IDF
    2. Transformar ambos textos en vectores TF-IDF
       - Cada palabra se convierte en una dimensión
       - El valor en cada dimensión es el TF-IDF de esa palabra
    3. Calcular producto punto: suma de v1[i] * v2[i] para todo i
    4. Calcular norma de cada vector: sqrt(Σ(vi²))
    5. Dividir producto punto entre producto de normas
    
    Ventajas:
    - Considera la importancia de las palabras (TF-IDF)
    - Normaliza por longitud de texto
    - Efectivo para textos de diferentes tamaños
    
    Resultado: Valor entre 0 y 1
    - 0 = textos ortogonales (sin palabras comunes relevantes)
    - 1 = textos idénticos en términos de palabras importantes
    
    Complejidad: O(n * m) donde n es el número de palabras únicas y m es
    el número de palabras en los textos.
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        float: Similitud del coseno TF-IDF entre 0 y 1
    """
    # Crear vectorizador TF-IDF
    vect = TfidfVectorizer()
    
    # Transformar textos en vectores TF-IDF
    # Cada texto se convierte en un vector donde cada dimensión es una palabra
    matriz = vect.fit_transform([a, b])
    v1, v2 = matriz.toarray()
    
    # Calcular producto punto: suma de productos elemento por elemento
    # v1 · v2 = Σ(v1[i] * v2[i])
    dot = sum(v1[i] * v2[i] for i in range(len(v1)))
    
    # Calcular norma euclidiana de cada vector
    # ||v|| = sqrt(Σ(vi²))
    norma1 = sqrt(sum(x*x for x in v1))
    norma2 = sqrt(sum(x*x for x in v2))
    
    # Calcular similitud del coseno
    # cos(θ) = (v1 · v2) / (||v1|| * ||v2||)
    # Se suma 1e-9 para evitar división por cero
    return dot / (norma1 * norma2 + 1e-9)

# -----------------------------------------------------------
# 5) IA EMBEDDINGS (SBERT - Sentence-BERT)
# -----------------------------------------------------------
def similitud_embeddings(a, b):
    """
    Calcula la similitud usando embeddings de IA (Sentence-BERT).
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    Sentence-BERT (SBERT) es un modelo de IA que genera representaciones
    vectoriales densas (embeddings) de oraciones completas.
    
    Proceso del modelo:
    1. El texto se pasa por una red neuronal transformer (BERT)
    2. La red genera un vector de alta dimensionalidad (embedding)
    3. Este vector captura el significado semántico del texto
    
    Fórmula de similitud:
    Se usa similitud del coseno entre los embeddings:
    sim(A, B) = cos(θ) = (emb_A · emb_B) / (||emb_A|| * ||emb_B||)
    
    Algoritmo paso a paso:
    1. Codificar texto A en un embedding usando el modelo SBERT
       - El modelo procesa el texto con atención transformer
       - Genera un vector de 384 dimensiones (para all-MiniLM-L6-v2)
    2. Codificar texto B de la misma manera
    3. Calcular similitud del coseno entre los dos embeddings
    
    Ventajas sobre métodos clásicos:
    - Captura significado semántico, no solo palabras
    - Entiende sinónimos y contexto
    - Funciona bien con textos de diferentes longitudes
    - Considera el orden y la estructura de las palabras
    
    Modelo usado: all-MiniLM-L6-v2
    - Basado en BERT
    - Optimizado para velocidad y eficiencia
    - Genera embeddings de 384 dimensiones
    
    Complejidad: O(n) donde n es la longitud del texto (procesamiento del modelo).
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        float: Similitud del coseno entre embeddings (0-1)
    """
    # Codificar textos en embeddings usando el modelo SBERT
    # convert_to_tensor=True para usar tensores de PyTorch (más eficiente)
    emb1 = modelo_embeddings_sbert.encode(a, convert_to_tensor=True)
    emb2 = modelo_embeddings_sbert.encode(b, convert_to_tensor=True)
    
    # Calcular similitud del coseno entre los embeddings
    return float(util.cos_sim(emb1, emb2))

# -----------------------------------------------------------
# 6) IA EMBEDDINGS ALTERNATIVO (Modelo Paraphrase)
# -----------------------------------------------------------
def similitud_embeddings_alternativo(a, b):
    """
    Calcula la similitud usando un segundo modelo de IA (Paraphrase-MiniLM).
    
    EXPLICACIÓN MATEMÁTICA Y ALGORÍTMICA:
    -------------------------------------
    Este es un segundo modelo de IA para comparar resultados con el primero.
    Usa un modelo diferente entrenado específicamente para detectar paráfrasis.
    
    Modelo usado: paraphrase-MiniLM-L6-v2
    - Entrenado específicamente para detectar similitud semántica
    - Optimizado para tareas de paráfrasis y similitud de significado
    - Genera embeddings de 384 dimensiones
    
    El proceso es similar a similitud_embeddings pero con un modelo diferente:
    1. Codificar texto A con el modelo paraphrase
    2. Codificar texto B con el mismo modelo
    3. Calcular similitud del coseno
    
    Ventajas del modelo paraphrase:
    - Mejor para detectar textos con el mismo significado pero diferentes palabras
    - Entrenado específicamente para similitud semántica
    - Puede dar resultados diferentes al modelo SBERT estándar
    
    Complejidad: O(n) donde n es la longitud del texto.
    
    Args:
        a (str): Primer texto
        b (str): Segundo texto
        
    Returns:
        float: Similitud del coseno entre embeddings (0-1)
    """
    # Codificar textos con el modelo alternativo
    emb1 = modelo_embeddings_alternativo.encode(a, convert_to_tensor=True)
    emb2 = modelo_embeddings_alternativo.encode(b, convert_to_tensor=True)
    
    # Calcular similitud del coseno
    return float(util.cos_sim(emb1, emb2))

# -----------------------------------------------------------
# FUNCIÓN PRINCIPAL USADA POR EL MENÚ
# -----------------------------------------------------------
def analizar_similitud(texto1, texto2):
    """
    Analiza la similitud entre dos textos usando todos los algoritmos implementados.
    
    Esta función ejecuta:
    - 4 algoritmos clásicos: Levenshtein, Jaccard, Dice, Coseno TF-IDF
    - 2 algoritmos de IA: SBERT y Paraphrase-MiniLM
    
    Args:
        texto1 (str): Primer texto (abstract del primer artículo)
        texto2 (str): Segundo texto (abstract del segundo artículo)
        
    Returns:
        dict: Diccionario con los resultados de todos los algoritmos:
            - "levenshtein": int (distancia, menor es más similar)
            - "jaccard": float (0-1, mayor es más similar)
            - "dice": float (0-1, mayor es más similar)
            - "coseno_tfidf": float (0-1, mayor es más similar)
            - "ia_embeddings": float (0-1, mayor es más similar)
            - "ia_embeddings_alt": float (0-1, mayor es más similar)
    """
    # Ejecutar todos los algoritmos y retornar resultados en un diccionario
    return {
        # Algoritmos clásicos (4 algoritmos)
        "levenshtein": distancia_levenshtein(texto1, texto2),  # Distancia de edición
        "jaccard": similitud_jaccard(texto1, texto2),          # Coeficiente de Jaccard
        "dice": similitud_dice(texto1, texto2),                 # Coeficiente de Dice
        "coseno_tfidf": similitud_coseno_tfidf(texto1, texto2),  # Similitud del coseno TF-IDF
        
        # Algoritmos de IA (2 algoritmos)
        "ia_embeddings": similitud_embeddings(texto1, texto2),                    # SBERT
        "ia_embeddings_alt": similitud_embeddings_alternativo(texto1, texto2)      # Paraphrase-MiniLM
    }


# ============================================================================
# EJEMPLO DE USO DESDE EL MAIN
# ============================================================================
"""
CÓMO SE LLAMA ESTE MÓDULO DESDE EL MAIN:
----------------------------------------

Este módulo NO se llama directamente desde main.py. En su lugar, se usa a través
del archivo req2.py que actúa como interfaz de usuario (menú).

FLUJO COMPLETO:
--------------

1. Desde main.py o cualquier script principal:
   ```python
   from req2.req2 import iniciar_menu
   
   # Llamar al menú interactivo
   iniciar_menu()
   ```

2. El archivo req2.py importa las funciones de este módulo:
   ```python
   # En req2.py
   from req2.req2Backend import analizar_similitud
   from req2.req2 import cargar_articulos_desde_bib
   ```

3. Flujo de ejecución en req2.py:
   ```python
   def iniciar_menu():
       # 1. Solicitar ruta del archivo .bib
       ruta = input("Ingrese la ruta del archivo .bib: ").strip()
       
       # 2. Cargar artículos desde el archivo .bib
       articulos = cargar_articulos_desde_bib(ruta)
       
       # 3. Mostrar lista de artículos disponibles
       mostrar_articulos(articulos)
       
       # 4. Permitir al usuario seleccionar dos artículos
       art1 = seleccionar_articulo("Seleccione el primer artículo: ", articulos)
       art2 = seleccionar_articulo("Seleccione el segundo artículo: ", articulos)
       
       # 5. Extraer los abstracts de los artículos seleccionados
       texto1 = art1["abstract"]
       texto2 = art2["abstract"]
       
       # 6. Llamar a la función principal de este módulo
       # Esta función ejecuta todos los algoritmos de similitud
       resultados = analizar_similitud(texto1, texto2)
       
       # 7. Mostrar los resultados
       print("--- ALGORITMOS CLÁSICOS ---")
       print("Levenshtein (distancia):", resultados["levenshtein"])
       print("Jaccard (0-1):", resultados["jaccard"])
       print("Dice (0-1):", resultados["dice"])
       print("Coseno TF-IDF (0-1):", resultados["coseno_tfidf"])
       
       print("\n--- ALGORITMOS DE IA ---")
       print("IA Embeddings SBERT (0-1):", resultados["ia_embeddings"])
       print("IA Embeddings Paraphrase (0-1):", resultados["ia_embeddings_alt"])
   ```

USO DIRECTO (sin menú):
----------------------
Si necesitas usar las funciones directamente sin el menú:

```python
# Importar las funciones necesarias
from req2.req2Backend import analizar_similitud
from req2.req2 import cargar_articulos_desde_bib

# 1. Cargar artículos desde archivo .bib
articulos = cargar_articulos_desde_bib("Data/unificados.bib")

# 2. Seleccionar dos artículos (por índice o directamente)
art1 = articulos[0]  # Primer artículo
art2 = articulos[1]  # Segundo artículo

# 3. Extraer los abstracts
texto1 = art1["abstract"]
texto2 = art2["abstract"]

# 4. Analizar similitud usando todos los algoritmos
resultados = analizar_similitud(texto1, texto2)

# 5. Acceder a los resultados individuales
print(f"Distancia de Levenshtein: {resultados['levenshtein']}")
print(f"Similitud Jaccard: {resultados['jaccard']:.3f}")
print(f"Similitud Dice: {resultados['dice']:.3f}")
print(f"Similitud Coseno TF-IDF: {resultados['coseno_tfidf']:.3f}")
print(f"Similitud IA SBERT: {resultados['ia_embeddings']:.3f}")
print(f"Similitud IA Paraphrase: {resultados['ia_embeddings_alt']:.3f}")
```

USO DE FUNCIONES INDIVIDUALES:
------------------------------
Si solo necesitas un algoritmo específico:

```python
from req2.req2Backend import (
    distancia_levenshtein,
    similitud_jaccard,
    similitud_dice,
    similitud_coseno_tfidf,
    similitud_embeddings,
    similitud_embeddings_alternativo
)

# Ejemplo: solo calcular similitud de Jaccard
texto1 = "Este es el abstract del primer artículo..."
texto2 = "Este es el abstract del segundo artículo..."

similitud = similitud_jaccard(texto1, texto2)
print(f"Similitud Jaccard: {similitud:.3f}")
```

ESTRUCTURA DE DATOS ESPERADA:
-----------------------------
Los artículos deben ser una lista de diccionarios con al menos la clave "abstract":

```python
articulos = [
    {
        "title": "Título del artículo 1",
        "abstract": "Texto completo del abstract...",
        "author": "Autor",
        # ... otros campos opcionales
    },
    {
        "title": "Título del artículo 2",
        "abstract": "Texto completo del abstract...",
        # ...
    }
]
```

NOTAS IMPORTANTES:
------------------
1. Los modelos de IA se cargan automáticamente al importar el módulo
2. La primera vez que se ejecuta, los modelos se descargan automáticamente
3. Los algoritmos clásicos son rápidos y no requieren dependencias externas
4. Los algoritmos de IA son más lentos pero capturan mejor el significado semántico
5. Todos los algoritmos de similitud (excepto Levenshtein) retornan valores entre 0 y 1
6. Levenshtein retorna una distancia (número entero), donde menor = más similar
"""
