# =============================================================================
# IMPORTS Y CONFIGURACIÓN INICIAL
# =============================================================================

# Importaciones estándar de Python
import time    # Para medir tiempos de ejecución
import os      # Para operaciones del sistema de archivos
import re      # Para expresiones regulares (limpieza de datos)

# Importaciones para visualización y análisis de datos
import matplotlib.pyplot as plt  # Para crear gráficos
import numpy as np               # Para operaciones numéricas y arrays

"""
PROYECTO: ANÁLISIS DE ALGORITMOS DE ORDENAMIENTO
================================================

Este proyecto implementa y compara 12 algoritmos de ordenamiento diferentes:
- Métodos numéricos especializados: Pigeonhole Sort, Radix Sort, Bucket Sort, Bitonic Sort
- Métodos generales: TimSort, Comb Sort, Selection Sort, Tree Sort, QuickSort, HeapSort, Gnome Sort, Binary Insertion Sort

FUNCIONALIDADES PRINCIPALES:
1. Análisis de rendimiento de algoritmos de ordenamiento
2. Visualización de tiempos de ejecución
3. Análisis de autores más frecuentes en productos académicos
4. Generación de gráficos y reportes

DATOS DE ENTRADA:
- Archivo BibTeX con productos académicos (artículos, papers, etc.)
- Campos analizados: título, autor, año, revista

AUTOR: Proyecto para seguimiento 1 - Análisis de Algoritmos
"""

# =============================================================================
# CONFIGURACIÓN DE ARCHIVOS
# =============================================================================

# Ruta del archivo BibTeX principal que contiene los datos a analizar
file_name = r"C:\Users\USUARIO\Desktop\algoritmos\al3\Proyecto-algoritmos\Data\unificados.bib"
# =============================================================================
# ALGORITMOS DE ORDENAMIENTO
# =============================================================================

"""
IMPLEMENTACIÓN DE 12 ALGORITMOS DE ORDENAMIENTO
===============================================

Esta sección contiene la implementación de diferentes algoritmos de ordenamiento
para comparar su rendimiento en términos de tiempo de ejecución.

ALGORITMOS IMPLEMENTADOS:
1. Comb Sort - Algoritmo de burbuja mejorado con gap decreciente
2. Selection Sort - Selecciona el menor elemento en cada iteración
3. Tree Sort - Utiliza un árbol binario de búsqueda
4. Bitonic Sort - Algoritmo especializado para secuencias bitónicas
5. Pigeonhole Sort - Eficiente para rangos pequeños de valores
6. Bucket Sort - Distribuye elementos en cubetas
7. Quick Sort - Algoritmo divide y conquista con pivote
8. Heap Sort - Utiliza la estructura de datos heap
9. Gnome Sort - Algoritmo simple de intercambio
10. Binary Insertion Sort - Inserción con búsqueda binaria
11. Radix Sort - Ordena por dígitos (implementado)
12. TimSort - Algoritmo híbrido de Python (built-in)

NOTA: Algunas implementaciones fueron desarrolladas con asistencia de ChatGPT
para asegurar corrección y eficiencia.
"""

# =============================================================================
# ALGORITMOS DE ORDENAMIENTO - IMPLEMENTACIONES
# =============================================================================

def comb_sort(data):
    """
    COMB SORT - Algoritmo de ordenamiento con gap decreciente
    
    DESCRIPCIÓN:
    - Mejora del algoritmo de burbuja
    - Utiliza un "gap" que se reduce en cada iteración
    - Factor de reducción típico: 1.3
    - Complejidad: O(n²) en el peor caso, O(n log n) en promedio
    
    PARÁMETROS:
    - data: Lista a ordenar (se modifica in-place)
    
    ALGORITMO:
    1. Inicializar gap = tamaño del array
    2. Reducir gap por factor de contracción
    3. Comparar elementos separados por el gap
    4. Repetir hasta que gap = 1 y no haya intercambios
    """
    n = len(data) #tamaño del arreglo
    gap = n # Inicializa el valor de gap (separación) al tamaño del arreglo.
    shrink = 1.3  # Factor de reducción del gap
    sorted = False # Inicializa el estado de "ordenado" como falso.
    while not sorted:
        gap = int(gap / shrink)  # Reducir el gap en cada iteración
        if gap <= 1:
            gap = 1 # Establece el gap a 1 (mínimo posible).
            sorted = True
        i = 0 # Inicializa el índice para iterar sobre el arreglo.
        while i + gap < n:  # Comparar elementos separados por el gap
            if data[i] > data[i + gap]: # Si el elemento actual es mayor que el elemento separado por el gap:
                # Intercambio de elementos si están fuera de orden
                data[i], data[i + gap] = data[i + gap], data[i]
                sorted = False
            i += 1

def selection_sort(data):
    """
    SELECTION SORT - Algoritmo de ordenamiento por selección
    
    DESCRIPCIÓN:
    - Encuentra el elemento más pequeño en cada iteración
    - Lo coloca en la posición correcta
    - Complejidad: O(n²) en todos los casos
    - Estable: No cambia el orden relativo de elementos iguales
    
    PARÁMETROS:
    - data: Lista a ordenar (se modifica in-place)
    
    ALGORITMO:
    1. Para cada posición i desde 0 hasta n-1
    2. Encuentra el elemento más pequeño desde i hasta n-1
    3. Intercambia el elemento más pequeño con el de la posición i
    """
    for i in range(len(data)):
        min_idx = i  # Índice del elemento más pequeño
        for j in range(i + 1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j  # Actualizar el índice del mínimo
        # Intercambiar el elemento más pequeño con el actual
        data[i], data[min_idx] = data[min_idx], data[i]

# TreeSort: Usa un árbol binario de búsqueda para ordenar elementos.
def tree_sort(data):
    # Define una clase interna para los nodos del árbol binario de búsqueda.
    class Node:
        def __init__(self, key):
            # Inicializa un nodo con una clave, un hijo izquierdo y un hijo derecho.
            self.key = key
            self.left = None
            self.right = None

    # Función para insertar un valor en el árbol binario de búsqueda de manera iterativa.
    def insert_iterative(root, key):
        if root is None:
            # Si el árbol está vacío, crea un nuevo nodo como raíz.
            return Node(key)
        current = root
        # Itera para encontrar la posición adecuada para el nuevo nodo.
        while True:
            if key < current.key:
                # Si la clave es menor que la clave actual, ir al subárbol izquierdo.
                if current.left is None:
                    # Si no hay nodo a la izquierda, insertar aquí.
                    current.left = Node(key)
                    break
                current = current.left
            else:
                # Si la clave es mayor o igual, ir al subárbol derecho.
                if current.right is None:
                    # Si no hay nodo a la derecha, insertar aquí.
                    current.right = Node(key)
                    break
                current = current.right
        return root  # Devuelve la raíz del árbol (puede haber cambiado).

    # Función para realizar un recorrido inorden del árbol y obtener elementos ordenados.
    def inorder_traversal(root, res):
        stack = []  # Pila para almacenar nodos mientras se navega por el árbol.
        current = root
        while stack or current:
            # Mientras haya nodos en la pila o un nodo actual:
            while current:
                # Descender al nodo más a la izquierda.
                stack.append(current)
                current = current.left
            # Procesar el nodo más a la izquierda.
            current = stack.pop()
            res.append(current.key)  # Agregar la clave del nodo a la lista de resultados.
            current = current.right  # Continuar con el subárbol derecho.

    root = None  # Inicializa el árbol como vacío.
    for val in data:
        # Inserta cada elemento de la lista en el árbol binario de búsqueda.
        root = insert_iterative(root, val)
    res = []  # Lista para almacenar los resultados ordenados.
    inorder_traversal(root, res)  # Realiza el recorrido inorden del árbol.
    return res  # Devuelve la lista de elementos ordenados.


# BitonicSort: Método especializado que utiliza una secuencia bitónica.
def bitonic_sort(arr):
    # Función para realizar la fusión bitónica en una secuencia.
    def bitonic_merge(start, length, direction):
        if length > 1:
            mid = length // 2
            for i in range(start, start + mid):
                # Comparación y ordenamiento en función de la dirección:
                # Si la dirección es ascendente (True) y el elemento actual es mayor que su par, se intercambian.
                # Si la dirección es descendente (False) y el elemento actual es menor que su par, se intercambian.
                if (direction and arr[i] > arr[i + mid]) or (not direction and arr[i] < arr[i + mid]):
                    arr[i], arr[i + mid] = arr[i + mid], arr[i]
            # Llamada recursiva para fusionar las mitades de forma bitónica.
            bitonic_merge(start, mid, direction)
            bitonic_merge(start + mid, mid, direction)

    # Función recursiva para dividir y ordenar las subsecuencias en forma bitónica.
    def bitonic_sort_recursive(start, length, direction):
        if length > 1:
            mid = length // 2
            # Crear una subsecuencia ascendente.
            bitonic_sort_recursive(start, mid, True)
            # Crear una subsecuencia descendente.
            bitonic_sort_recursive(start + mid, mid, False)
            # Fusionar las subsecuencias en una secuencia bitónica.
            bitonic_merge(start, length, direction)

    n = len(arr)  # Longitud del arreglo original.
    # Ajustar el tamaño del arreglo a la potencia de 2 más cercana superior.
    next_power_of_two = 1 << (n - 1).bit_length()
    if n < next_power_of_two:
        # Rellenar con infinitos para igualar la longitud a una potencia de 2.
        arr.extend([float('inf')] * (next_power_of_two - n))
    
    # Ordenar el arreglo utilizando el algoritmo de Bitonic Sort.
    bitonic_sort_recursive(0, len(arr), True)

    # Eliminar los elementos extras añadidos previamente (valores infinitos).
    while len(arr) > n:
        arr.pop()



# Pigeonhole Sort: Ordena elementos utilizando una estrategia de "agujeros" basados en el rango de valores.
def pigeonhole_sort(data):
    # Validación: verifica que los datos no sean nulos y que todos los elementos sean números (int o float).
    if not data or not all(isinstance(x, (int, float)) for x in data):
        raise ValueError("Pigeonhole Sort solo admite datos numéricos.")
    
    # Encuentra el valor mínimo en el conjunto de datos.
    min_val = min(data)
    # Encuentra el valor máximo en el conjunto de datos.
    max_val = max(data)
    
    # Calcula el tamaño del rango de valores necesarios para los "agujeros".
    size = int(max_val - min_val + 1)
    # Inicializa los "agujeros" como un arreglo de ceros. Cada índice representará un valor en el rango.
    holes = [0] * size

    # Distribuye cada elemento del conjunto de datos en el agujero correspondiente.
    for x in data:
        # Calcula el índice del agujero correspondiente restando el valor mínimo.
        holes[int(x - min_val)] += 1

    # Reconstruye el arreglo ordenado desde los agujeros.
    i = 0  # Índice para sobrescribir el arreglo original.
    for count in range(size):
        # Mientras haya elementos en el agujero actual, se añaden de vuelta al arreglo.
        while holes[count] > 0:
            # Asigna el valor correspondiente al índice actual.
            data[i] = count + min_val
            i += 1  # Avanza al siguiente índice en el arreglo.
            holes[count] -= 1  # Disminuye el contador del agujero actual.


# Bucket Sort: Ordena los elementos distribuyéndolos en cubetas según su valor.
def bucket_sort(data):
    # Verifica si el conjunto de datos está vacío
    if len(data) == 0:
        return

    # Encuentra el valor máximo y calcula el tamaño de los intervalos
    max_val = max(data)
    size = max_val / len(data)

    # Crea una lista de cubetas vacías, una para cada elemento del conjunto de datos
    buckets = [[] for _ in range(len(data))]

    # Distribuye los elementos en las cubetas correspondientes
    for x in data:
        index = int(x / size)  # Determina la cubeta en la que debe ir el elemento
        if index != len(data):  # Si el índice está dentro del rango
            buckets[index].append(x)
        else:  # Si no, agrega el elemento a la última cubeta
            buckets[len(data) - 1].append(x)

    # Ordena cada cubeta individualmente
    for bucket in buckets:
        bucket.sort()

    # Combina los elementos ordenados de todas las cubetas en un solo arreglo
    result = []
    for bucket in buckets:
        result.extend(bucket)

    # Copia los resultados ordenados de nuevo en el arreglo original
    data[:] = result


# Quick Sort: Divide y conquista utilizando un pivote para ordenar.
def quick_sort(data):
    # Condición base: si el tamaño es 1 o menor, el arreglo ya está ordenado
    if len(data) <= 1:
        return data

    # Selecciona un pivote (el elemento central) y divide los datos en tres partes
    pivot = data[len(data) // 2]
    left = [x for x in data if x < pivot]  # Elementos menores que el pivote
    middle = [x for x in data if x == pivot]  # Elementos iguales al pivote
    right = [x for x in data if x > pivot]  # Elementos mayores que el pivote

    # Llama recursivamente a Quick Sort en las partes izquierda y derecha
    return quick_sort(left) + middle + quick_sort(right)


# Heap Sort: Ordena utilizando un montículo (heap).
def heap_sort(data):
    import heapq  # Biblioteca para manejar montículos (heaps)

    # Convierte el arreglo en un montículo (estructura de datos que permite extraer el mínimo rápidamente)
    heapq.heapify(data)

    # Extrae los elementos del montículo en orden ascendente
    data[:] = [heapq.heappop(data) for _ in range(len(data))]


# Gnome Sort: Ordena verificando y corrigiendo el orden de los elementos de manera iterativa.
def gnome_sort(data):
    index = 0  # Inicializa el índice en 0
    while index < len(data):
        # Si el índice es 0 o los elementos están en el orden correcto, avanza al siguiente índice
        if index == 0 or data[index] >= data[index - 1]:
            index += 1
        else:
            # Si no, intercambia los elementos actuales y retrocede un índice
            data[index], data[index - 1] = data[index - 1], data[index]
            index -= 1


# Binary Insertion Sort: Inserta elementos en su posición correcta usando búsqueda binaria.
def binary_insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]  # Elemento a insertar
        low, high = 0, i - 1  # Define el rango para la búsqueda binaria

        # Encuentra la posición de inserción usando búsqueda binaria
        while low <= high:
            mid = (low + high) // 2  # Encuentra el índice medio
            if data[mid] > key:  # Si el valor medio es mayor que el elemento clave
                high = mid - 1  # Ajusta el límite superior
            else:  # Si no, ajusta el límite inferior
                low = mid + 1

        # Inserta el elemento en la posición encontrada
        data[:] = data[:low] + [key] + data[low:i] + data[i + 1:]


# Radix Sort: Ordena los números procesando dígitos de menor a mayor significancia.
def radix_sort(data):
    RADIX = 10  # Base decimal (10 dígitos posibles: 0-9)
    max_digit = max(data)  # Encuentra el número más grande para determinar el número de dígitos
    exp = 1  # Inicializa el exponente como 1 (dígito menos significativo)

    # Repite el proceso mientras haya dígitos en el número más grande
    while max_digit // exp > 0:
        # Crea 10 cubetas (listas vacías) para agrupar números según el dígito actual
        buckets = [[] for _ in range(RADIX)]

        # Distribuye los números en las cubetas según el dígito actual
        for i in data:
            buckets[(i // exp) % RADIX].append(i)

        # Reconstruye el arreglo a partir de las cubetas
        data[:] = [item for bucket in buckets for item in bucket]

        # Incrementa el exponente para procesar el siguiente dígito más significativo
        exp *= RADIX
    

# =============================================================================
# LECTURA Y PROCESAMIENTO DE DATOS BIBTEX
# =============================================================================

def read_bibtex(file_name):
    """
    LECTURA DE ARCHIVO BIBTEX
    =========================
    
    DESCRIPCIÓN:
    - Lee y parsea un archivo BibTeX
    - Extrae información de artículos académicos
    - Maneja diferentes formatos de campos
    
    PARÁMETROS:
    - file_name: Ruta del archivo BibTeX
    
    RETORNA:
    - Lista de diccionarios, cada uno representa un artículo con sus campos
    
    CAMPOS EXTRAÍDOS:
    - title: Título del artículo
    - author: Autor(es) del artículo
    - year: Año de publicación
    - journal: Revista o conferencia
    - Otros campos según disponibilidad
    
    FORMATO ESPERADO:
    @article{key,
        title = {Título del artículo},
        author = {Autor1 and Autor2},
        year = {2023},
        journal = {Nombre de la revista}
    }
    """
    data = []
    with open(file_name, "r", encoding="utf-8") as file:
        article = {}
        for line in file:
            line = line.strip()
            if line.startswith("@article"):
                article = {}  # Iniciar un nuevo artículo
            elif line.startswith("}"):
                if article:  # Guardar el artículo actual si no está vacío
                    data.append(article)
            else:
                # Separar clave y valor del campo del artículo
                key_value = line.split("=", 1)
                if len(key_value) == 2:
                    key = key_value[0].strip()
                    value = key_value[1].strip().strip("{}").strip(",")
                    article[key] = value
    return data

# =============================================================================
# ANÁLISIS DE RENDIMIENTO Y MEDICIÓN DE TIEMPOS
# =============================================================================

def analyze_sorting_total_time(articles, numeric_methods, general_methods):
    """
    ANÁLISIS COMPLETO DE RENDIMIENTO DE ALGORITMOS DE ORDENAMIENTO
    =============================================================
    
    DESCRIPCIÓN:
    - Ejecuta múltiples algoritmos de ordenamiento sobre diferentes campos de datos
    - Mide tiempos de ejecución para cada combinación algoritmo-campo
    - Maneja métodos especializados para datos numéricos y métodos generales
    - Cuenta archivos procesados por cada método
    
    PARÁMETROS:
    - articles: Lista de artículos extraídos del archivo BibTeX
    - numeric_methods: Diccionario de métodos especializados para datos numéricos
    - general_methods: Diccionario de métodos generales de ordenamiento
    
    RETORNA:
    - results: Diccionario con tiempos de ejecución por método y campo
    - file_counts: Diccionario con conteo de archivos procesados por método
    
    PROCESO:
    1. Extrae datos numéricos del campo 'year' para métodos especializados
    2. Procesa campos generales (title, author, year, journal) para métodos generales
    3. Ejecuta cada algoritmo y mide tiempo de ejecución
    4. Maneja errores y continúa con el siguiente algoritmo si uno falla
    5. Cuenta archivos procesados para estadísticas
    """
    results = {}
    file_counts = {}  # Contador de archivos revisados por método

    print("Procesando métodos para datos numéricos...")
    numeric_field_data = []
    for article in articles:
        if "year" in article:
            raw_year = str(article["year"]).strip()
            cleaned_year = re.sub(r"[^\d]", "", raw_year)  # Limpiar valores no numéricos
            if re.match(r"^\d{4}$", cleaned_year):  # Validar formato de año
                numeric_field_data.append(int(cleaned_year))

    # Procesar métodos de ordenamiento en campo "year"
    if not numeric_field_data:
        print("No se encontraron datos numéricos válidos en el campo 'year'.")
    else:
        for name, method in numeric_methods.items():
            try:
                print(f"Ejecutando {name} para el campo 'year'...")
                start_time = time.time()
                method(numeric_field_data.copy())  # Ordenar copia de los datos
                end_time = time.time()
                if name not in results:
                    results[name] = {}
                    file_counts[name] = 0
                results[name]["year"] = end_time - start_time
                file_counts[name] += len(numeric_field_data)
                print(f"  → {name} revisó {len(numeric_field_data)} archivos en el campo 'year'")
            except Exception as e:
                print(f"Error al ordenar con '{name}': {e}")

    # Procesar métodos para todos los campos generales
    print("Procesando métodos para todos los campos...")
    for name, method in general_methods.items():
        if name not in results:
            results[name] = {}
            file_counts[name] = 0
        
        for field in ["title", "author", "year", "journal"]:
            field_data = [article[field] for article in articles if field in article and article[field]]
            
            if not field_data:
                print(f"Campo '{field}' omitido por falta de datos válidos.")
                continue
            
            try:
                # Convertir todos los valores a minúsculas para uniformidad
                if all(isinstance(val, str) for val in field_data):
                    field_data = [val.lower() for val in field_data]
                elif all(isinstance(val, (int, float)) for val in field_data):
                    field_data = list(map(float, field_data))
                else:
                    raise ValueError(f"Datos en '{field}' no son comparables.")
            except Exception as e:
                print(f"Error procesando el campo '{field}': {e}")
                continue
            
            try:
                print(f"Ejecutando {name} para el campo '{field}'...")
                start_time = time.time()
                method(field_data.copy())  # Ordenar copia de los datos
                end_time = time.time()
                results[name][field] = end_time - start_time
                file_counts[name] += len(field_data)
                print(f"  → {name} revisó {len(field_data)} archivos en el campo '{field}'")
            except Exception as e:
                print(f"Error al ordenar con '{name}' en el campo '{field}': {e}")
                continue

    return results, file_counts

# =============================================================================
# VISUALIZACIÓN Y REPORTES
# =============================================================================

def display_results(results):
    """
    MOSTRAR RESULTADOS EN FORMATO TABULAR
    ====================================
    
    DESCRIPCIÓN:
    - Muestra los tiempos de ejecución en formato de tabla
    - Organiza resultados por método y campo
    - Formato legible para análisis de rendimiento
    
    PARÁMETROS:
    - results: Diccionario con tiempos de ejecución por método y campo
    
    FORMATO DE SALIDA:
    Método                    Campo           Tiempo (s)    
    ------------------------------------------------------------
    TimSort (Python built-in) title          0.001234      
    TimSort (Python built-in) author         0.001456      
    ...
    """
    print(f"{'Método':<25} {'Campo':<15} {'Tiempo (s)':<15}")
    print("-" * 60)
    for method, fields in results.items():
        for field, time_taken in fields.items():
            print(f"{method:<25} {field:<15} {time_taken:<15.6f}")

# Mostrar resumen de archivos revisados por método
def display_file_counts(file_counts):
    print("\n" + "="*70)
    print("RESUMEN DE ARCHIVOS REVISADOS POR MÉTODO DE ORDENAMIENTO")
    print("="*70)
    print(f"{'Método de Ordenamiento':<35} {'Archivos Revisados':<20}")
    print("-" * 70)
    
    # Ordenar métodos por cantidad de archivos revisados (descendente)
    sorted_methods = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
    
    for method, count in sorted_methods:
        print(f"{method:<35} {count:<20}")
    
    total_files = sum(file_counts.values())
    print("-" * 70)
    print(f"{'TOTAL':<35} {total_files:<20}")
    print("="*70)

# Crear diagrama de barras con tiempos de ordenamiento
def create_sorting_time_chart(results):
    """
    Crea un diagrama de barras mostrando los tiempos de ejecución de los algoritmos
    de ordenamiento ordenados de manera ascendente.
    """
    # Recopilar todos los tiempos de todos los métodos y campos
    all_times = []
    method_names = []
    
    for method, fields in results.items():
        for field, time_taken in fields.items():
            all_times.append(time_taken)
            method_names.append(f"{method} ({field})")
    
    # Crear arrays de numpy para ordenamiento
    times_array = np.array(all_times)
    names_array = np.array(method_names)
    
    # Obtener índices para ordenar de manera ascendente
    sorted_indices = np.argsort(times_array)
    
    # Ordenar los datos
    sorted_times = times_array[sorted_indices]
    sorted_names = names_array[sorted_indices]
    
    # Mostrar resultados en formato de tabla
    print(f"\n📊 ALGORITMOS ORDENADOS POR TIEMPO MÁXIMO (ASCENDENTE):")
    print("="*80)
    print(f"{'Posición':<8} {'Algoritmo':<45} {'Tiempo Máx (s)':<15} {'Barra Visual':<20}")
    print("-"*80)
    
    # Crear representación visual con caracteres ASCII
    max_time = max(sorted_times)
    for i, (name, time_val) in enumerate(zip(sorted_names, sorted_times), 1):
        # Crear barra visual proporcional
        bar_length = int((time_val / max_time) * 15) if max_time > 0 else 0
        bar_visual = "█" * bar_length + "░" * (15 - bar_length)
        
        print(f"{i:<8} {name:<45} {time_val:<15.6f} {bar_visual}")
    
    # Mostrar estadísticas adicionales
    print(f"\n📈 ESTADÍSTICAS DE RENDIMIENTO (TIEMPO MÁXIMO POR MÉTODO):")
    print(f"   • Tiempo más rápido: {min(sorted_times):.6f} segundos")
    print(f"   • Tiempo más lento: {max(sorted_times):.6f} segundos")
    print(f"   • Tiempo promedio: {np.mean(sorted_times):.6f} segundos")
    print(f"   • Diferencia entre el más rápido y el más lento: {max(sorted_times) - min(sorted_times):.6f} segundos")
    
    # Mostrar los 3 más rápidos
    print(f"\n🏆 TOP 3 ALGORITMOS MÁS RÁPIDOS:")
    for i in range(min(3, len(sorted_times))):
        print(f"   {i+1}. {sorted_names[i]}: {sorted_times[i]:.6f} segundos")
    
    # Mostrar los 3 más lentos
    print(f"\n🐌 TOP 3 ALGORITMOS MÁS LENTOS:")
    for i in range(max(0, len(sorted_times)-3), len(sorted_times)):
        print(f"   {len(sorted_times)-i}. {sorted_names[i]}: {sorted_times[i]:.6f} segundos")
    
    # Intentar crear gráfico con matplotlib si está disponible
    try:
        import matplotlib.pyplot as plt
        
        # Configurar el gráfico
        plt.figure(figsize=(15, 10))
        bars = plt.bar(range(len(sorted_times)), sorted_times, 
                       color=plt.cm.viridis(np.linspace(0, 1, len(sorted_times))))
        
        # Personalizar el gráfico
        plt.title('Tiempos Máximos de Ejecución de Algoritmos de Ordenamiento\n(Ordenados de Menor a Mayor Tiempo)', 
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Algoritmos de Ordenamiento', fontsize=12, fontweight='bold')
        plt.ylabel('Tiempo de Ejecución (segundos)', fontsize=12, fontweight='bold')
        
        # Configurar las etiquetas del eje x
        plt.xticks(range(len(sorted_names)), sorted_names, rotation=45, ha='right')
        
        # Agregar valores en las barras
        for i, (bar, time_val) in enumerate(zip(bars, sorted_times)):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(sorted_times)*0.01,
                    f'{time_val:.6f}s', ha='center', va='bottom', fontsize=8, rotation=90)
        
        # Ajustar el layout para evitar que se corten las etiquetas
        plt.tight_layout()
        
        # Agregar grid para mejor legibilidad
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Mostrar el gráfico
        plt.show()
        
        # También guardar el gráfico como imagen
        plt.savefig('tiempos_ordenamiento.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráfico guardado como 'tiempos_ordenamiento.png'")
        
    except ImportError:
        print(f"\n⚠️  Matplotlib no está disponible. Se muestra solo la representación en texto.")
        print(f"💡 Para instalar matplotlib: pip install matplotlib")


# ----------------------------------------------CHATGPT------------------------------------------#

# =============================================================================
# ANÁLISIS DE AUTORES Y FRECUENCIA
# =============================================================================

def extract_authors(articles):
    """
    EXTRACCIÓN Y NORMALIZACIÓN DE AUTORES
    ====================================
    
    DESCRIPCIÓN:
    - Extrae todos los autores de los artículos académicos
    - Normaliza nombres (minúsculas, sin espacios extra)
    - Maneja diferentes formatos de separación de autores
    - Soporta formatos BibTeX estándar
    
    PARÁMETROS:
    - articles: Lista de artículos con información de autores
    
    RETORNA:
    - Lista de nombres de autores normalizados
    
    FORMATOS SOPORTADOS:
    - "Autor1 and Autor2 and Autor3" (formato BibTeX estándar)
    - "Autor1; Autor2; Autor3" (formato con punto y coma)
    - "Autor1, Autor2, Autor3" (formato con comas)
    
    NORMALIZACIÓN:
    - Convierte a minúsculas
    - Elimina espacios extra
    - Maneja caracteres especiales
    """
    """
    Extrae y normaliza autores desde la lista de artículos.
    Soporta formatos con separadores 'and' o comas.
    Devuelve una lista con todos los autores (normalizados en minúsculas y sin espacios extra).
    """
    authors = []
    for article in articles:
        raw = article.get("author", "")
        if not raw:
            continue
        text = str(raw).strip()
        # Separar por ' and ' típico de BibTeX o por comas si aplica
        if " and " in text.lower():
            parts = re.split(r"\s+and\s+", text, flags=re.IGNORECASE)
        else:
            # fallback: dividir por comas si no hay 'and'
            parts = [p.strip() for p in text.split(";")] if ";" in text else [p.strip() for p in text.split(",")]
        for p in parts:
            name = re.sub(r"\s+", " ", p).strip()
            if not name:
                continue
            authors.append(name.lower())
    return authors


def count_top_authors(authors, top_n=15):
    """
    Cuenta apariciones de autores, obtiene los top_n por mayor frecuencia,
    y luego ordena esos top_n de forma ascendente por número de apariciones.
    Devuelve lista de tuplas (autor, conteo).
    """
    from collections import Counter
    counts = Counter(authors)
    if not counts:
        return []
    # Seleccionar top N por mayor frecuencia
    top_desc = counts.most_common()
    top_desc = top_desc[:top_n]
    # Ordenar ascendentemente por conteo y por nombre para estabilidad
    top_asc = sorted(top_desc, key=lambda x: (x[1], x[0]))
    return top_asc


def display_top_authors(top_authors):
    """
    Muestra una tabla con autores y cantidad de apariciones, orden ascendente.
    """
    print("\n" + "="*70)
    print("TOP 15 AUTORES CON MÁS APARICIONES (ORDEN ASCENDENTE)")
    print("="*70)
    print(f"{'Pos.':<6} {'Autor':<45} {'Apariciones':<12}")
    print("-" * 70)
    for i, (author, count) in enumerate(top_authors, start=1):
        print(f"{i:<6} {author:<45} {count:<12}")
    print("-" * 70)
    total = sum(c for _, c in top_authors)
    print(f"{'TOTAL LISTADO':<51} {total:<12}")
    print("="*70)


def plot_top_authors(top_authors):
    """
    Grafica el TOP 15 de autores en orden ascendente de apariciones.
    Si matplotlib no está disponible, muestra una gráfica ASCII en consola.
    """
    # Preparar datos en orden ascendente
    authors = [a for a, _ in top_authors]
    counts = [c for _, c in top_authors]

    # Fallback ASCII si no hay matplotlib
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        # Crear figura horizontal para mejor lectura de nombres
        plt.figure(figsize=(12, 8))
        y_pos = np.arange(len(authors))
        plt.barh(y_pos, counts, color=plt.cm.Blues(np.linspace(0.3, 0.9, len(counts))))
        plt.yticks(y_pos, authors)
        plt.xlabel('Apariciones', fontsize=12, fontweight='bold')
        plt.title('TOP 15 AUTORES CON MÁS APARICIONES (ORDEN ASCENDENTE)', fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        plt.tight_layout()
        plt.show()
        plt.savefig('top15_autores.png', dpi=300, bbox_inches='tight')
        print("\n📊 Gráfico de autores guardado como 'top15_autores.png'")
    except Exception:
        print("\n⚠️  Matplotlib no está disponible. Gráfica ASCII:")
        max_count = max(counts) if counts else 0
        for author, count in zip(authors, counts):
            bar_len = int((count / max_count) * 30) if max_count > 0 else 0
            bar = '█' * bar_len
            print(f"{author:<45} | {bar} {count}")

# =============================================================================
# FUNCIÓN PRINCIPAL Y FLUJO DE EJECUCIÓN
# =============================================================================

if __name__ == "__main__":
    """
    PUNTO DE ENTRADA PRINCIPAL DEL PROGRAMA
    =======================================
    
    FLUJO DE EJECUCIÓN:
    1. Carga y procesa archivo BibTeX
    2. Define algoritmos de ordenamiento (numéricos y generales)
    3. Ejecuta análisis de rendimiento
    4. Muestra resultados tabulares
    5. Genera visualizaciones de tiempos
    6. Analiza autores más frecuentes
    7. Crea gráficos de autores
    
    SALIDAS GENERADAS:
    - Tablas de rendimiento de algoritmos
    - Gráficos de tiempos de ordenamiento
    - Análisis de autores más frecuentes
    - Archivos PNG con visualizaciones
    - Estadísticas detalladas de rendimiento
    """
    # =========================================================================
    # INICIALIZACIÓN Y CONFIGURACIÓN
    # =========================================================================
    
    # Cargar datos desde archivo BibTeX
    articles = read_bibtex(file_name)  # Leer archivo BibTeX
    n = len(articles)
    print(f"📚 Artículos cargados: {n}")

    # =========================================================================
    # CONFIGURACIÓN DE ALGORITMOS DE ORDENAMIENTO
    # =========================================================================
    
    # Métodos especializados para datos numéricos (años de publicación)
    # Estos algoritmos son eficientes para rangos pequeños de valores enteros
    numeric_methods = {
        "Pigeonhole Sort": pigeonhole_sort,    # Eficiente para rangos pequeños
        "RadixSort": radix_sort,               # Ordena por dígitos
        "Bucket Sort": bucket_sort,            # Distribuye en cubetas
        "Bitonic Sort": bitonic_sort,          # Para secuencias bitónicas
    }

    # Métodos generales de ordenamiento (para cualquier tipo de datos)
    # Incluye algoritmos clásicos y el built-in de Python
    general_methods = {
        "TimSort (Python built-in)": sorted,              # Algoritmo híbrido de Python
        "Comb Sort": comb_sort,                            # Burbuja mejorado
        "Selection Sort": selection_sort,                  # Selección directa
        "Tree Sort": lambda data: tree_sort(data),         # Árbol binario
        "QuickSort": lambda data: quick_sort(data),        # Divide y conquista
        "HeapSort": heap_sort,                             # Estructura heap
        "Gnome Sort": gnome_sort,                          # Intercambio simple
        "Binary Insertion Sort": binary_insertion_sort,    # Inserción con búsqueda binaria
    }

    # =========================================================================
    # ANÁLISIS DE RENDIMIENTO DE ALGORITMOS DE ORDENAMIENTO
    # =========================================================================
    
    print(f"Tamaño de los datos: {n}")
    print("Resultados de ordenamiento:")
    print("-----------------------------------")
    
    # Ejecutar análisis completo de rendimiento
    # Mide tiempos de ejecución para cada algoritmo en diferentes campos
    total_times, file_counts = analyze_sorting_total_time(articles, numeric_methods, general_methods)
    
    # Mostrar resultados en formato tabular
    display_results(total_times)
    
    # Mostrar estadísticas de archivos procesados
    display_file_counts(file_counts)
    
    # =========================================================================
    # VISUALIZACIÓN DE TIEMPOS DE ORDENAMIENTO
    # =========================================================================
    
    # Crear y mostrar el diagrama de barras con tiempos ordenados ascendentemente
    print("\n" + "="*70)
    print("GENERANDO DIAGRAMA DE BARRAS DE TIEMPOS DE ORDENAMIENTO")
    print("="*70)
    create_sorting_time_chart(total_times)

    # =========================================================================
    # ANÁLISIS DE AUTORES MÁS FRECUENTES
    # =========================================================================
    
    print("\n" + "="*70)
    print("PROCESANDO TOP 15 AUTORES POR APARICIONES")
    print("="*70)
    
    # Extraer y normalizar todos los autores de los artículos
    all_authors = extract_authors(articles)
    
    # Obtener los 15 autores con más apariciones, ordenados ascendentemente
    top15_authors = count_top_authors(all_authors, top_n=15)
    
    if not top15_authors:
        print("No se encontraron autores válidos en los productos académicos.")
    else:
        # Mostrar tabla de autores más frecuentes
        display_top_authors(top15_authors)
        
        # =====================================================================
        # VISUALIZACIÓN DE AUTORES MÁS FRECUENTES
        # =====================================================================
        
        # Crear gráfico de barras para los autores más frecuentes
        print("\n" + "="*70)
        print("GENERANDO GRÁFICA: TOP 15 AUTORES (ORDEN ASCENDENTE)")
        print("="*70)
        plot_top_authors(top15_authors)
