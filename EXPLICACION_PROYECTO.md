# 📊 EXPLICACIÓN DEL PROYECTO: DESCARGA, UNIFICACIÓN Y ANÁLISIS DE GRAFOS

## 🎯 Objetivo del proyecto

Construir un sistema completo que:
- Descargue artículos académicos desde ACM, IEEE y Sage.
- Unifique los resultados en un único archivo BibTeX, detectando duplicados.
- Analice relaciones entre artículos y términos mediante grafos de citaciones y coocurrencia.
- Genere visualizaciones y reportes estadísticos.

---

## 📋 Funcionalidades principales

- **Scraping automatizado**: Obtención de artículos desde tres bases de datos.
- **Unificación y deduplicación**: Fusión de resultados y separación de duplicados.
- **Grafo de citaciones (Req. 1)**: Relaciones entre artículos por similitud (título, autores, abstract) y caminos mínimos (Dijkstra/Floyd).
- **Grafo de coocurrencia (Req. 2)**: Red de términos en abstracts, componentes, centralidad y temas.
- **Visualizaciones**: Grafos y distribuciones con NetworkX/Matplotlib.
- **Reportes**: JSON con estadísticas y resúmenes del análisis.

---

## 🧭 Flujo general de trabajo

1. Ejecutar scrapers y descargar resultados (`ACM.py`, `IEE.py`, `Sage.py`).
2. Unificar resultados y detectar duplicados (`Unificador_duplicador/Categorizacion.py`).
3. Analizar grafos de citaciones y coocurrencia (`graph_analysis_main.py`).
4. Opcional: análisis rápido o simplificado (`quick_graph_analysis.py`, `simple_graph_analysis.py`).
5. Generar y revisar reportes y visualizaciones en `Data/`.

---

## 🗂️ Estructura relevante del código

- `main.py`: Orquesta scraping → unificación → reporte básico de conteos.
- `Unificador_duplicador/Categorizacion.py`: Unificación de BibTeX y detección de duplicados.
- `Graph_Analysis/citation_graph.py`: Construcción y análisis del grafo de citaciones.
- `Graph_Analysis/cooccurrence_graph.py`: Construcción y análisis del grafo de coocurrencia de términos.
- `Graph_Analysis/visualization.py`: Utilidades de visualización.
- `graph_analysis_main.py`: Pipeline completo de análisis de grafos.
- `simple_graph_analysis.py` y `quick_graph_analysis.py`: Versiones simplificadas/rápidas.

---

## 🔧 Requisitos e instalación

1) Python 3.7+
2) Dependencias:
```bash
pip install -r requirements.txt
```
3) Playwright para scraping (si aplica):
```bash
playwright install
```
4) Variables de entorno:
```bash
cp env.template .env
# Editar EMAIL_USER y EMAIL_PASSWORD (contraseña de aplicación)
```

---

## 🚀 Cómo usar

- Ejecución completa (scraping → unificación → reporte básico):
```bash
python main.py
```

- Unificación de resultados (si ya tienes los `.bib`):
```bash
python Unificador_duplicador/Categorizacion.py
```

- Análisis de grafos (completo):
```bash
python graph_analysis_main.py
```

- Análisis rápido/simplificado:
```bash
python quick_graph_analysis.py
python simple_graph_analysis.py
```

- Scrapers individuales:
```bash
python Scraping/ACM.py
python Scraping/IEE.py
python Scraping/Sage.py
```

---

## 📈 Salidas generadas en `Data/`

- `resultados_ACM.bib`, `resultados_ieee.bib`, `resultados_Sage.bib`: Resultados por fuente.
- `unificados.bib`: Artículos únicos unificados.
- `duplicados.bib`: Registros detectados como duplicados.
- Grafo de citaciones: `citation_graph.json`, `simple_citation_graph.json`, `quick_citation_graph.json`.
- Grafo de coocurrencia: `cooccurrence_graph.json`, `simple_cooccurrence_graph.json`, `quick_cooccurrence_graph.json`.
- Reportes: `graph_analysis_report.json`, `simple_graph_analysis_report.json`, `quick_graph_analysis_report.json`.

---

## 🧪 Análisis de grafos (resumen)

- **Citaciones**:
  - Construcción por similitud (umbral configurable).
  - Caminos mínimos (Dijkstra) y componentes fuertemente conexas.
  - Métricas: nodos, aristas, densidad, tamaños de componentes.

- **Coocurrencia de términos**:
  - Matriz de coocurrencia desde abstracts con filtros `min_frequency` y `min_cooccurrence`.
  - Componentes, centralidad (grado, closeness, betweenness, eigenvector) y temas por componente.
  - Top términos por grado/conectividad.

---

## 📊 Reportes y visualizaciones

- Resúmenes en JSON con estadísticas de grafos y términos clave.
- Visualizaciones de redes y distribuciones (PNG) generadas por `Graph_Analysis/visualization.py`.

---

## 💡 Valor académico

- Pipeline reproducible de adquisición, limpieza y análisis de literatura académica.
- Exploración de relaciones entre artículos y conceptos mediante teoría de grafos.
- Base para estudios de mapeo de conocimiento y detección de temas.

---

## ✅ Checklist rápido antes de ejecutar

- `Data/` existe y contiene `.bib` o ejecutar `main.py` para generarlos.
- `.env` configurado (scrapers que lo requieren).
- Dependencias instaladas (`requirements.txt`).

---

## 👥 Autores y créditos

- Anderson Neil Peña, Dayana Buitrago, David Clavijo.
- Declaración de uso de IA: `docs/AI_Declaration.md`.
