#!/usr/bin/env python3
"""
Script de prueba para verificar que los métodos no se repiten
y se toma el tiempo máximo de cada uno.
"""

import numpy as np

def test_corrected_visualization():
    """Prueba la lógica corregida de ordenamiento sin métodos repetidos."""
    
    # Simular resultados de ordenamiento con métodos repetidos por campo
    results = {
        "TimSort (Python built-in)": {"title": 0.001234, "author": 0.001456, "year": 0.000987, "journal": 0.001123},
        "Comb Sort": {"title": 0.002345, "author": 0.002678, "year": 0.002123, "journal": 0.002456},
        "Selection Sort": {"title": 0.003456, "author": 0.003789, "year": 0.003234, "journal": 0.003567},
        "Tree Sort": {"title": 0.004567, "author": 0.004890, "year": 0.004345, "journal": 0.004678},
        "QuickSort": {"title": 0.001567, "author": 0.001890, "year": 0.001345, "journal": 0.001678},
        "HeapSort": {"title": 0.002678, "author": 0.003001, "year": 0.002456, "journal": 0.002789},
        "Gnome Sort": {"title": 0.005678, "author": 0.006001, "year": 0.005456, "journal": 0.005789},
        "Binary Insertion Sort": {"title": 0.003789, "author": 0.004112, "year": 0.003567, "journal": 0.003900},
        "Pigeonhole Sort": {"year": 0.000456},
        "RadixSort": {"year": 0.000789},
        "Bucket Sort": {"year": 0.001123},
        "Bitonic Sort": {"year": 0.001456}
    }
    
    print("🧪 PRUEBA DE VISUALIZACIÓN CORREGIDA (SIN MÉTODOS REPETIDOS)")
    print("="*80)
    
    # Recopilar el tiempo máximo de cada método (sin repetir métodos)
    method_max_times = {}
    method_names = []
    
    for method, fields in results.items():
        # Encontrar el tiempo máximo para este método
        max_time = max(fields.values()) if fields else 0
        method_max_times[method] = max_time
        method_names.append(method)
    
    # Crear arrays de numpy para ordenamiento
    times_array = np.array(list(method_max_times.values()))
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
    
    print(f"\n✅ CORRECCIÓN APLICADA EXITOSAMENTE!")
    print(f"📝 Se procesaron {len(sorted_times)} métodos únicos (sin repeticiones)")
    print(f"🔍 Cada método muestra su tiempo máximo entre todos los campos")

if __name__ == "__main__":
    test_corrected_visualization()
