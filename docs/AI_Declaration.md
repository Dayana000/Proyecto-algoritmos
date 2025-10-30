# Documento de respaldo del uso de Inteligencia Artificial

Proyecto: Sistema de scraping, unificación y análisis de grafos (citaciones y coocurrencia)

Repositorio: https://github.com/Dayana000/Proyecto-algoritmos.git

## 1. Propósito del documento
- Declarar de forma transparente el alcance, herramientas y metodología de uso de IA en el proyecto.
- Garantizar trazabilidad, reproducibilidad y apego a buenas prácticas académicas durante la evaluación.

## 2. Herramientas de IA empleadas
- Modelos/servicios:
  - ChatGPT (GPT-4/GPT-5): apoyo en diseño y revisión de componentes.
- Tareas asistidas:
  - Diseño de scrapers (Playwright) para ACM/IEEE/SAGE, selecciones de DOM, flujos de autenticación.
  - Parsing y limpieza básica de BibTeX; estructura de funciones de unificación y duplicados.
  - Diseño de grafos de citaciones (dirigido) y coocurrencia (no dirigido); definición de umbrales/medidas iniciales.
  - Implementación de versiones “completa” (NetworkX/visualización) y “simplificada” (solo estándar Python).
  - Redacción de documentación (README), prompts de soporte, scripts de prueba rápida.
  - Refactor incremental, manejo de errores comunes (llaves dobles en BibTeX, división por cero, JSON serializable).

## 3. Alcance y límites del uso de IA
- Generado/sugerido por IA:
  - Estructuras de módulos y APIs de funciones; pseudocódigo y plantillas de implementación.
  - Snippets para scraping, parsing, unificación, grafos, y visualización.
  - Borradores de documentación y prompts.
- Implementado/verificado por humanos:
  - Ejecución real de scrapers y validación de credenciales/login.
  - Limpieza de datos, verificación de formato BibTeX y correcciones manuales.
  - Pruebas locales (scripts rápidos y completos), ajuste de umbrales, selección de filtros de términos.
  - Revisión de resultados y decisión de aceptación de cambios.
- No hizo la IA:
  - Ejecución de experimentos finales sin supervisión.
  - Validación empírica de calidad de datos más allá de pruebas funcionales.
  - Aprobación académica ni decisiones evaluativas.

## 4. Metodología de interacción (trazabilidad)
- Estilo de prompts: iterativos, específicos por módulo (scraping, unificación, grafos, visualización), con criterios de éxito concretos.
- Criterios de aceptación:
  - Código compila/ejecuta sin errores; salidas esperadas generadas (p. ej., Data/unificados.bib, Data/*graph*.json).
  - Pruebas de muestra (quick) y, cuando aplica, pruebas completas.
  - Revisión manual de archivos de datos (BibTeX/JSON) y verificación de métricas reportadas.
- Manejo de sesgos/alucinaciones:
  - Verificación ejecutable de cada propuesta.
  - Sustitución de dependencias no esenciales por versiones “simplificadas” cuando era necesario (p. ej., sin NetworkX).
  - Validación de serialización (evitar tuplas como claves JSON).

## 5. Intervención humana y control de calidad
- Revisión por pares/equipo: confirmación de rutas, scripts, y salidas.
- Pruebas locales: uso de quick_graph_analysis.py para sanity-check; ejecución puntual de main.py y Categorizacion.py.
- Decisiones de diseño:
  - Umbrales de similitud (citaciones) y tamaños de muestra para viabilizar pruebas rápidas.
  - Filtros de términos en coocurrencia para reducir ruido (posible ampliación en futuras iteraciones).
  - Separación entre versiones completa (NetworkX) y simplificada (sin dependencias externas).

## 6. Conformidad ética y de integridad académica
- No plagio: el código fue generado/adaptado con atribución explícita a asistencia de IA y verificación humana.
- Licencias y términos: respeto a Términos de Uso de herramientas de IA y dependencias (Playwright, NetworkX, NLTK, etc.).
- Protección de datos: uso de .env para credenciales; no se exponen secretos en el repositorio.
- Reconocimiento: se declara la participación de IA como soporte a la productividad y estructuración.

## 7. Reproducibilidad
- Requisitos:
  - Python 3.10+; pip.
  - Playwright (navegadores instalados).
  - Para análisis completo: NetworkX, NLTK, Matplotlib, Seaborn (o usar la versión simplificada).
- Comandos clave:
  - `pip install -r requirements.txt`
  - `python -m playwright install`
  - Scraping+unificación: `python main.py`
  - Solo unificación: `python Unificador_duplicador/Categorizacion.py`
  - Análisis rápido (sin dependencias extra): `python quick_graph_analysis.py`
  - Análisis simple completo (sin NetworkX): `python simple_graph_analysis.py`
  - Análisis completo con visualizaciones: `python graph_analysis_main.py` y `python Graph_Analysis/visualization.py`
- Entradas/salidas esperadas:
  - Entradas: `Data/resultados_*.bib`
  - Salidas: `Data/unificados.bib`, `Data/duplicados.bib`, `Data/*cooccurrence_graph*.json`, `Data/*citation_graph*.json`, `Data/quick_graph_analysis_report.json`.

## 8. Riesgos y mitigaciones
- Formato BibTeX inconsistente (llaves dobles): limpieza y re-generación; escritura uniforme en unificación.
- Ruido en coocurrencia (doi, org, https): filtros de stop-words ampliables; normalización básica de tokens.
- Rendimiento/escasez de aristas en citaciones: ajuste de umbral de similitud y aumento de muestra; opción de análisis completo.
- Serialización JSON: evitar tuplas como claves; uso de listas/dict estructurados para edges y matrices.

## 9. Registro breve de prompts (Anexo)
- Diseño de scrapers Playwright con selectores robustos: objetivo, autenticación, paginación, exportación BibTeX.
- Limpieza y parsing de BibTeX: manejo de llaves, claves/valores, normalización de campos.
- Unificación y detección de duplicados: clave por título, tracking de archivos fuente, salida duplicados.
- Grafo de citaciones (dirigido): definición de similitud (título/autores/abstract), regla de dirección por año, Dijkstra y SCC.
- Grafo de coocurrencia (no dirigido): pipeline de tokens, filtros, coocurrencias por documento, pesos y grados.
- Visualizaciones: layouts, tamaños por grado, figuras de distribución, exportación PNG.
- Scripts de prueba rápida: reducción de muestra, umbrales, reporte compacto en JSON.
- Documentación: README con guía de instalación/uso, y esta declaración de IA.

## 10. Declaración final
- La Inteligencia Artificial se utilizó como herramienta de apoyo para ideación, estructuración y aceleración de desarrollo, con verificación, ejecución y control de calidad a cargo del equipo. Las decisiones de diseño, aceptación de cambios y la responsabilidad académica del contenido final corresponden a los autores del proyecto.

### Cómo citar esta declaración
“Documento de respaldo del uso de Inteligencia Artificial para el proyecto ‘Sistema de scraping, unificación y análisis de grafos (citaciones y coocurrencia)’, repositorio https://github.com/Dayana000/Proyecto-algoritmos.git, 2025.”
