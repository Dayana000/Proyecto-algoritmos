# 📊 EXPLICACIÓN DEL PROYECTO: ANÁLISIS DE ALGORITMOS DE ORDENAMIENTO

## 🎯 **OBJETIVO DEL PROYECTO**

Este proyecto implementa y compara **12 algoritmos de ordenamiento diferentes** para analizar su rendimiento en términos de tiempo de ejecución, utilizando datos reales de productos académicos (artículos, papers, etc.) extraídos de archivos BibTeX.

---

## 📋 **FUNCIONALIDADES PRINCIPALES**

### 1. **Análisis de Rendimiento de Algoritmos**
- Compara 12 algoritmos de ordenamiento diferentes
- Mide tiempos de ejecución en datos reales
- Genera estadísticas detalladas de rendimiento

### 2. **Visualización de Resultados**
- Gráficos de barras con tiempos ordenados ascendentemente
- Tablas comparativas de rendimiento
- Representación ASCII cuando matplotlib no está disponible

### 3. **Análisis de Autores Académicos**
- Identifica los 15 autores más frecuentes
- Ordena resultados de manera ascendente
- Genera gráficos de frecuencia de autores

### 4. **Reportes Estadísticos**
- Conteo de archivos procesados por método
- Estadísticas de tiempo (mínimo, máximo, promedio)
- Rankings de algoritmos más rápidos y lentos

---

## 🔧 **ALGORITMOS IMPLEMENTADOS**

### **Métodos Especializados para Datos Numéricos:**
1. **Pigeonhole Sort** - Eficiente para rangos pequeños de valores
2. **Radix Sort** - Ordena por dígitos (base 10)
3. **Bucket Sort** - Distribuye elementos en cubetas
4. **Bitonic Sort** - Para secuencias bitónicas

### **Métodos Generales de Ordenamiento:**
5. **TimSort** - Algoritmo híbrido de Python (built-in)
6. **Comb Sort** - Burbuja mejorado con gap decreciente
7. **Selection Sort** - Selecciona el menor elemento
8. **Tree Sort** - Utiliza árbol binario de búsqueda
9. **QuickSort** - Divide y conquista con pivote
10. **HeapSort** - Utiliza estructura de datos heap
11. **Gnome Sort** - Intercambio simple
12. **Binary Insertion Sort** - Inserción con búsqueda binaria

---

## 📊 **ESTRUCTURA DEL CÓDIGO**

### **Sección 1: Configuración e Imports**
```python
# Importaciones necesarias
import time, os, re, matplotlib.pyplot, numpy

# Configuración del archivo de datos
file_name = "Data/unificados.bib"
```

### **Sección 2: Implementación de Algoritmos**
- 12 funciones de ordenamiento completamente documentadas
- Cada algoritmo con su complejidad temporal explicada
- Manejo de diferentes tipos de datos

### **Sección 3: Análisis de Datos**
- `read_bibtex()`: Lee y parsea archivos BibTeX
- `analyze_sorting_total_time()`: Ejecuta análisis completo
- `extract_authors()`: Extrae y normaliza autores

### **Sección 4: Visualización**
- `create_sorting_time_chart()`: Gráficos de tiempos
- `plot_top_authors()`: Gráficos de autores
- `display_results()`: Tablas de resultados

### **Sección 5: Función Principal**
- Flujo completo de ejecución
- Configuración de algoritmos
- Generación de reportes

---

## 🚀 **CÓMO FUNCIONA EL PROGRAMA**

### **Paso 1: Carga de Datos**
```
📚 Carga archivo BibTeX → Extrae artículos → Procesa campos
```

### **Paso 2: Configuración de Algoritmos**
```
🔧 Define métodos numéricos → Define métodos generales → Prepara ejecución
```

### **Paso 3: Análisis de Rendimiento**
```
⏱️ Ejecuta cada algoritmo → Mide tiempos → Cuenta archivos procesados
```

### **Paso 4: Visualización de Resultados**
```
📊 Genera tablas → Crea gráficos → Muestra estadísticas
```

### **Paso 5: Análisis de Autores**
```
👥 Extrae autores → Cuenta frecuencia → Genera top 15
```

---

## 📈 **SALIDAS GENERADAS**

### **1. Tabla de Tiempos de Ordenamiento**
```
Método                    Campo           Tiempo (s)    
------------------------------------------------------------
TimSort (Python built-in) title          0.001234      
QuickSort                  year           0.001456      
...
```

### **2. Gráfico de Barras (Tiempos Ascendentes)**
```
📊 ALGORITMOS ORDENADOS POR TIEMPO MÁXIMO (ASCENDENTE):
================================================================================
Posición  Algoritmo                                    Tiempo Máx (s)  Barra Visual
--------------------------------------------------------------------------------
1         Pigeonhole Sort                              0.000456        █░░░░░░░░░░░░░░░
2         RadixSort                                    0.000789        ██░░░░░░░░░░░░░░
...
```

### **3. Análisis de Autores**
```
TOP 15 AUTORES CON MÁS APARICIONES (ORDEN ASCENDENTE)
======================================================================
Pos.     Autor                                        Apariciones
----------------------------------------------------------------------
1        smith, john                                   15
2        garcia, maria                                 12
...
```

### **4. Archivos Generados**
- `tiempos_ordenamiento.png` - Gráfico de tiempos
- `top15_autores.png` - Gráfico de autores
- Salida en consola con estadísticas completas

---

## 🎓 **APRENDIZAJES DEL PROYECTO**

### **Conceptos de Algoritmos:**
- **Complejidad Temporal**: O(n²), O(n log n), O(n)
- **Algoritmos Estables vs Inestables**
- **Casos Mejor, Promedio y Peor**
- **Algoritmos Adaptativos**

### **Análisis de Datos:**
- **Procesamiento de archivos BibTeX**
- **Normalización de datos**
- **Medición de rendimiento**
- **Visualización de resultados**

### **Programación:**
- **Manejo de errores**
- **Funciones modulares**
- **Documentación de código**
- **Visualización con matplotlib**

---

## 🔍 **RESULTADOS ESPERADOS**

### **Rendimiento de Algoritmos:**
- **Más Rápidos**: TimSort, QuickSort, HeapSort
- **Más Lentos**: Gnome Sort, Binary Insertion Sort
- **Especializados**: Pigeonhole Sort (rangos pequeños)

### **Análisis de Autores:**
- Identificación de investigadores más productivos
- Patrones de colaboración académica
- Distribución de publicaciones por autor

---

## 💡 **VALOR ACADÉMICO**

### **Para Análisis de Algoritmos:**
- Comparación práctica de 12 algoritmos
- Medición real de rendimiento
- Visualización de diferencias de tiempo

### **Para Análisis de Datos:**
- Procesamiento de datos académicos reales
- Extracción de información relevante
- Generación de reportes estadísticos

### **Para Programación:**
- Implementación de algoritmos complejos
- Manejo de archivos y datos
- Visualización y reportes

---

## 🚀 **CÓMO USAR EL PROYECTO**

### **Ejecución Básica:**
```bash
python seguimientos/seguimiento.py
```

### **Instalación de Dependencias:**
```bash
pip install matplotlib numpy
```

### **Archivos Necesarios:**
- `Data/unificados.bib` - Archivo con datos académicos
- `seguimientos/seguimiento.py` - Código principal

---

## 📊 **MÉTRICAS DE RENDIMIENTO**

### **Tiempos Típicos (ejemplo):**
- **TimSort**: 0.000123 segundos
- **QuickSort**: 0.000456 segundos
- **HeapSort**: 0.000789 segundos
- **Gnome Sort**: 0.005678 segundos

### **Estadísticas Generadas:**
- Tiempo más rápido
- Tiempo más lento
- Tiempo promedio
- Diferencia entre extremos
- Top 3 más rápidos
- Top 3 más lentos

---

## 🎯 **CONCLUSIONES**

Este proyecto demuestra:

1. **Diferencias significativas** en rendimiento entre algoritmos
2. **Importancia de elegir** el algoritmo correcto para cada caso
3. **Utilidad de la visualización** para entender resultados
4. **Aplicación práctica** de conceptos teóricos de algoritmos
5. **Análisis de datos reales** en contexto académico

**El proyecto combina teoría de algoritmos con análisis de datos reales, proporcionando una experiencia de aprendizaje completa y práctica.**
