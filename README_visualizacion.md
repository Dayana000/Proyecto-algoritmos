#  Visualización de Algoritmos de Ordenamiento

## Descripción
Este proyecto incluye funcionalidad para visualizar los tiempos de ejecución de 12 algoritmos de ordenamiento diferentes, mostrándolos en orden ascendente (de menor a mayor tiempo).

## Características Implementadas

### ✅ Funcionalidades Agregadas:
1. **Contadores de archivos revisados**: Muestra la cantidad de archivos procesados por cada método
2. **Visualización en consola**: Representación de barras usando caracteres ASCII
3. **Estadísticas detalladas**: Tiempos mínimos, máximos, promedio y diferencias
4. **Ranking de algoritmos**: Top 3 más rápidos y más lentos
5. **Gráfico visual opcional**: Si matplotlib está disponible

###  Algoritmos Incluidos:
- **Métodos numéricos**: Pigeonhole Sort, Radix Sort, Bucket Sort, Bitonic Sort
- **Métodos generales**: TimSort, Comb Sort, Selection Sort, Tree Sort, QuickSort, HeapSort, Gnome Sort, Binary Insertion Sort

## Instalación de Dependencias

Para obtener la visualización completa con gráficos, instala las dependencias:

```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install matplotlib numpy
```

## Uso

Ejecuta el script principal:
```bash
python seguimientos/seguimiento.py
```

## Salida Esperada

El programa mostrará:

1. **Procesamiento de datos**: Información sobre archivos procesados
2. **Tabla de tiempos**: Resultados detallados por método y campo
3. **Resumen de archivos**: Cantidad de archivos revisados por método
4. **Visualización ASCII**: Barras de tiempo ordenadas ascendentemente
5. **Estadísticas**: Tiempos extremos, promedio y diferencias
6. **Rankings**: Top 3 más rápidos y lentos
7. **Gráfico PNG** (si matplotlib está disponible): `tiempos_ordenamiento.png`

## Ejemplo de Salida

```
 ALGORITMOS ORDENADOS POR TIEMPO (ASCENDENTE):
================================================================================
Posición  Algoritmo                                    Tiempo (s)      Barra Visual
--------------------------------------------------------------------------------
1         TimSort (Python built-in) (year)             0.000123        █░░░░░░░░░░░░░░░
2         QuickSort (year)                             0.000456        ██░░░░░░░░░░░░░░
3         HeapSort (year)                              0.000789        ███░░░░░░░░░░░░░
...

  ESTADÍSTICAS DE RENDIMIENTO:
   • Tiempo más rápido: 0.000123 segundos
   • Tiempo más lento: 0.005678 segundos
   • Tiempo promedio: 0.002345 segundos
   • Diferencia entre el más rápido y el más lento: 0.005555 segundos

  TOP 3 ALGORITMOS MÁS RÁPIDOS:
   1. TimSort (Python built-in) (year): 0.000123 segundos
   2. QuickSort (year): 0.000456 segundos
   3. HeapSort (year): 0.000789 segundos

  TOP 3 ALGORITMOS MÁS LENTOS:
   1. Gnome Sort (title): 0.005678 segundos
   2. Binary Insertion Sort (author): 0.004567 segundos
   3. Tree Sort (journal): 0.003456 segundos
```

## Archivos Generados

- `tiempos_ordenamiento.png`: Gráfico de barras (si matplotlib está disponible)
- `requirements.txt`: Dependencias del proyecto

## Notas Técnicas

- El código funciona sin matplotlib, mostrando solo la representación ASCII
- Los tiempos se ordenan de manera ascendente (menor a mayor)
- Se incluyen estadísticas completas de rendimiento
- Compatible con datos BibTeX del proyecto
