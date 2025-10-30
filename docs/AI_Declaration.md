# Documento de respaldo del uso de Inteligencia Artificial

Proyecto: Sistema de scraping, unificación y análisis de grafos (citaciones y coocurrencia)
Repositorio: https://github.com/Dayana000/Proyecto-algoritmos.git

## Propósito del documento
- Explicar con claridad cuándo y cómo se usó IA durante el desarrollo.
- Delimitar responsabilidades y asegurar trazabilidad y reproducibilidad.
- Dejar constancia para evaluación académica y auditorías técnicas.

## Herramientas de IA empleadas
- Modelos/servicios consultados:
  - ChatGPT (GPT‑4 y GPT‑5): apoyo puntual en ideación, revisión de enfoques, redacción técnica y sugerencias de código.
- Alcance típico de las consultas:
  - Prototipos de selectores Playwright y patrones de navegación (ACM/IEEE/SAGE) sin credenciales reales.
  - Sugerencias de parsing y normalización básica de BibTeX.
  - Esbozos de estructuras de datos y funciones para unificación y detección de duplicados.
  - Ideas para el modelado de grafos de citaciones (dirigido) y coocurrencia (no dirigido) y métricas iniciales.
  - Borradores de documentación (README, pautas de uso) y guiones de pruebas rápidas.

## Alcance y límites del uso de IA
- Contenidos sugeridos por IA (siempre revisados y adaptados):
  - Estructuras de módulos y APIs internas; pseudocódigo; snippets de referencia.
  - Alternativas de implementación “completa” (con NetworkX/visualización) y “simplificada” (std. Python).
  - Mensajes de error frecuentes y estrategias de manejo (p. ej., llaves duplicadas en BibTeX, serialización JSON).
- Implementación y verificación realizadas por el equipo:
  - Desarrollo final de scrapers, autenticación y manejo de sesiones.
  - Ejecución de scraping, consolidación y limpieza efectiva de datos.
  - Elección y ajuste de umbrales, filtros y parámetros; ejecución de pruebas locales y revisión de resultados.
  - Refactor, integración y aseguramiento de calidad previo a cada commit.
- Fuera de alcance de la IA:
  - Acceso a plataformas con credenciales reales o ejecución automática de experimentos sin supervisión.
  - Validación empírica de la calidad de datos más allá de pruebas funcionales.
  - Decisiones académicas o evaluativas.

## Metodología de interacción y trazabilidad
- Estilo de prompts: iterativos por módulo (scraping, unificación, grafos, visualización), con criterios de éxito verificables.
- Evidencias en repo:
  - Commits con mensajes descriptivos y scripts reproducibles.
  - Artefactos esperados en Data/ tras cada ejecución.
- Criterios de aceptación por módulo:
  - Código ejecuta sin errores en entorno limpio; outputs generados coinciden con especificación.
  - Revisión manual de archivos intermedios (BibTeX/JSON) y métricas reportadas.
- Control de sesgos/alucinaciones de IA:
  - Probar cada sugerencia en entorno local.
  - Preferir soluciones simples y auditablemente correctas ante alternativas “creativas”.
  - Sustituir dependencias no críticas por variantes simples si dificulta reproducir.

## Intervención humana y control de calidad
- Revisión por pares de rutas, parámetros y salidas.
- Pruebas locales:
  - quick_graph_analysis.py para sanity-check.
  - main.py y Unificador_duplicador/Categorizacion.py para flujos principales.
- Decisiones de diseño tomadas por el equipo:
  - Umbrales de similitud y tamaños de muestra para pruebas vs. corridas completas.
  - Filtros de términos en coocurrencia para reducir ruido.
  - Separación entre pipeline completo (NetworkX) y versión simplificada.

## Conformidad ética e integridad académica
- Transparencia: se declara el uso de IA como apoyo, no como sustituto del trabajo académico.
- Licencias: respeto de licencias y Términos de Uso de herramientas y dependencias (Playwright, NetworkX, NLTK, etc.).
- Datos y privacidad: uso de .env y variables de entorno; no se versionan secretos ni credenciales.
- Originalidad: el código final fue adaptado, probado y validado por el equipo; las decisiones de diseño son propias.

## Reproducibilidad
- Requisitos:
  - Python 3.10+ y pip.
  - Playwright con navegadores instalados.
  - Para análisis completo: NetworkX, NLTK, Matplotlib, Seaborn. Para la ruta simplificada no son obligatorios.
- Instalación y preparación:
  - pip install -r requirements.txt
  - python -m playwright install
- Comandos de ejecución:
  - Flujo completo de scraping + unificación: python main.py
  - Solo unificación/categorización: python Unificador_duplicador/Categorizacion.py
  - Análisis rápido (sin dependencias extra): python quick_graph_analysis.py
  - Análisis simple sin NetworkX: python simple_graph_analysis.py
  - Pipeline completo de análisis/visualización: python graph_analysis_main.py y python Graph_Analysis/visualization.py
- Entradas/salidas esperadas:
  - Entradas: Data/resultados_*.bib
  - Salidas: Data/unificados.bib, Data/duplicados.bib, Data/cooccurrence_graph.json, Data/citation_graph.json, Data/quick_graph_analysis_report.json
- Notas de entorno:
  - Corridas que requieren login deben proveer .env local y cumplir TOS de cada portal.
  - Algunas páginas cambian selectores; los scrapers incluyen tolerancia básica, pero podrían requerir ajustes.

## Riesgos conocidos y mitigaciones
- Inconsistencias BibTeX (llaves duplicadas, campos faltantes):
  - Normalización y escritura consistente; validadores simples antes de unificar.
- Ruido en coocurrencia (doi, org, urls):
  - Lista ampliable de stop-words; normalización de tokens.
- Pocas aristas o sesgos en citaciones:
  - Ajuste de umbrales, aumento de muestra y opción de ejecución completa cuando sea viable.
- Serialización JSON:
  - Evitar tuplas como claves; uso de estructuras listas/dict para nodos y edges.
- Fragilidad en scraping por cambios de DOM:
  - Selectores más robustos, esperas explícitas y guías para ajuste rápido.

## Registro breve de interacción con IA (anexo)
- Preguntas típicas:
  - Selectores Playwright, manejo de paginación y exportación BibTeX (sin credenciales).
  - Estrategias de parsing/limpieza de BibTeX y resolución de duplicados.
  - Diseño de grafos: definición de pesos, dirección por año y cálculo de métricas (grado, SCC, caminos).
  - Visualización: layouts, tamaños por grado y exportación de figuras.
  - Guiones de “smoke tests” y estructura del README.
- Evidencias:
  - Fragmentos aceptados aparecen adaptados en módulos específicos con comentarios y pruebas asociadas.

## Declaración final
La IA se empleó como soporte de productividad, ideación y revisión. El equipo implementó, ejecutó y validó el software; las decisiones de diseño y la responsabilidad académica del contenido final son de los autores.

## Cómo citar esta declaración
“Documento de respaldo del uso de Inteligencia Artificial para el proyecto ‘Sistema de scraping, unificación y análisis de grafos (citaciones y coocurrencia)’, repositorio https://github.com/Dayana000/Proyecto-algoritmos.git, 2025.”