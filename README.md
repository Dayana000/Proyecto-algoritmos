# Sistema de Descarga y Unificación de Bases de Datos

Este proyecto permite descargar artículos académicos de tres bases de datos principales (ACM Digital Library, IEEE Xplore, y Sage Journals) y unificar la información en un solo archivo, detectando duplicados en el proceso.

## 🚀 Características

- **Scraping automatizado** de tres bases de datos académicas
- **Unificación de datos** en formato BibTeX estándar
- **Detección de duplicados** basada en títulos de artículos
- **Similitud textual** sobre abstracts con 4 algoritmos clásicos y 2 basados en IA
- **Frecuencia de conceptos** y detección de nuevas palabras asociadas
- **Análisis de grafos de citaciones** con algoritmos de caminos mínimos
- **Análisis de grafos de coocurrencia** de términos
- **Visualización interactiva** de redes y componentes
- **Dashboards bibliométricos**: mapa geográfico, nube de palabras y línea temporal exportables a PDF
- **Clustering jerárquico** de abstracts con dendrogramas comparativos (HTML sin dependencias externas)
- **Interfaz de línea de comandos** fácil de usar
- **Reportes de estadísticas** detallados

## 📋 Requisitos

- Python 3.7+
- Navegador web (Chrome/Chromium)
- Credenciales de acceso a las bases de datos

## 🛠️ Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Dayana000/Proyecto-algoritmos.git
   cd Proyecto-algoritmos
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instalar Playwright:**
   ```bash
   playwright install
   ```

4. **Configurar credenciales:**
   ```bash
   cp env.template .env
   ```
   
   Edita el archivo `.env` con tus credenciales:
   ```
   EMAIL_USER=tu_email@ejemplo.com
   EMAIL_PASSWORD=tu_contraseña_de_aplicacion
   ```

## 🎯 Uso

### Ejecución completa
```bash
python main.py
```

### Ejecución individual de scrapers
```bash
# ACM Digital Library
python Scraping/ACM.py

# IEEE Xplore
python Scraping/IEE.py

# Sage Journals
python Scraping/Sage.py
```

### Unificación de datos
```bash
python Unificador_duplicador/Categorizacion.py
```

### Análisis y visualizaciones
```bash
# Análisis completo de grafos (citaciones y coocurrencia)
python graph_analysis_main.py

# Solo grafo de citaciones
python Graph_Analysis/citation_graph.py

# Solo grafo de coocurrencia
python Graph_Analysis/cooccurrence_graph.py

# Visualizaciones
python Graph_Analysis/visualization.py

# Similitud textual (Req. 2)
python req2/req2.py

# Frecuencia de conceptos (Req. 3)
python req3/req3.py

# Clustering jerárquico (Req. 4)
python req4/req4.py --entrada Data/unificados.bib --salida Data/visualizations/req4
# Genera dendrogramas en HTML (single, complete, average) y un resumen JSON

# Visualizaciones bibliométricas (Req. 5)
python req5/generate_visualizations.py --entrada Data/unificados.bib --salida Data/visualizations/req5
# Crea PNG y un PDF con mapa geográfico, nube de palabras y línea temporal

### Menú interactivo
```bash
python menu_requerimientos.py
```
- Permite ejecutar los requerimientos 2, 3, 4 o 5 y, opcionalmente, limitar la cantidad de artículos a procesar en los dos últimos.
```

## 📁 Estructura del Proyecto

```
Proyecto-algoritmos/
├── Scraping/                 # Scripts de scraping
│   ├── ACM.py               # Scraper para ACM Digital Library
│   ├── IEE.py               # Scraper para IEEE Xplore
│   └── Sage.py              # Scraper para Sage Journals
├── Unificador_duplicador/   # Scripts de procesamiento
│   └── Categorizacion.py    # Unificación y detección de duplicados
├── Graph_Analysis/          # Análisis de grafos
│   ├── citation_graph.py    # Grafo de citaciones
│   ├── cooccurrence_graph.py # Grafo de coocurrencia
│   └── visualization.py     # Visualizaciones
├── Data/                    # Archivos de datos
│   ├── resultados_ACM.bib   # Artículos de ACM
│   ├── resultados_ieee.bib  # Artículos de IEEE
│   ├── resultados_Sage.bib  # Artículos de Sage
│   ├── unificados.bib       # Artículos únicos unificados
│   ├── duplicados.bib       # Artículos duplicados detectados
│   ├── citation_graph.json  # Grafo de citaciones
│   ├── cooccurrence_graph.json # Grafo de coocurrencia
│   └── visualizations/      # Gráficos y visualizaciones
├── main.py                  # Script principal
├── graph_analysis_main.py   # Script principal de análisis de grafos
├── requirements.txt         # Dependencias de Python
├── env.template            # Plantilla de variables de entorno
└── README.md               # Este archivo
```

## 📊 Formato de Datos

Los artículos se almacenan en formato BibTeX estándar:

```bibtex
@article{ref1,
  title = {Título del artículo},
  author = {Autor1, Autor2},
  year = {2024},
  journal = {Nombre de la revista},
  tipo = {Tipo de publicación},
  publisher = {Editorial},
  abstract = {Resumen del artículo},
  url = {https://url-del-articulo}
}
```

## ⚙️ Configuración

### Variables de Entorno

El archivo `.env` debe contener:

- `EMAIL_USER`: Tu email institucional
- `EMAIL_PASSWORD`: Contraseña de aplicación de Google (para IEEE y Sage)

### Ubicaciones manuales de autores (Req. 5)

El script de visualizaciones (`req5/generate_visualizations.py`) intenta inferir el país del primer autor
mediante servicios públicos (`nationalize.io` y `restcountries.com`), cacheando los resultados en
`Data/cache/`. Si deseas fijar países manualmente para ciertos autores (o evitar llamadas externas),
crea el archivo `Data/author_locations_override.json`, por ejemplo:

```json
{
  "rencong huang": "China",
  "rami a. abdel-rahem": "Jordania"
}
```

Los nombres se comparan en minúsculas y con espacios/puntuación simples.

### Dependencias adicionales (Req. 2 y Req. 3)

Los algoritmos clásicos y el cálculo de frecuencias se implementan con utilidades propias, sin librerías externas.  
Para habilitar los dos algoritmos de IA (Req. 2) se recomienda instalar `sentence-transformers`
—el script los cargará de forma diferida y, si no están disponibles, mostrará un aviso y omitirá esas métricas.

### Términos de Búsqueda

Los scrapers buscan artículos relacionados con "generative artificial intelligence". Para cambiar el término de búsqueda, edita la variable correspondiente en cada script de scraping.

## 🔧 Solución de Problemas

### Error de credenciales
- Verifica que el archivo `.env` esté configurado correctamente
- Asegúrate de usar una contraseña de aplicación de Google, no tu contraseña normal

### Error de Playwright
```bash
playwright install
```

### Error de dependencias
```bash
pip install -r requirements.txt
```

## 📈 Estadísticas

El script principal genera un reporte con:
- Número de artículos por base de datos
- Total de artículos únicos
- Artículos duplicados detectados

## 🔬 Análisis de Grafos

### Grafo de Citaciones (Requerimiento 1)
- **Construcción automática** basada en similitud de títulos, autores y abstracts
- **Algoritmos de caminos mínimos**: Dijkstra y Floyd-Warshall
- **Componentes fuertemente conexas** para identificar grupos interrelacionados
- **Análisis de conectividad** y centralidad en la red

### Grafo de Coocurrencia (Requerimiento 2)
- **Construcción automática** basada en coocurrencia de términos en abstracts
- **Cálculo de grados** para identificar términos más relacionados
- **Componentes conexas** para reconocer temas asociados
- **Medidas de centralidad** (grado, intermediación, cercanía, vector propio)

### Visualizaciones
- **Grafos interactivos** con NetworkX y Matplotlib
- **Distribuciones de grados** y tamaños de componentes
- **Análisis de centralidad** con gráficos detallados
- **Reportes visuales** en formato PNG de alta calidad

## 🧾 Declaración de uso de IA

Este proyecto incluye un documento de transparencia sobre el uso de herramientas de Inteligencia Artificial durante su desarrollo. Puedes consultarlo en:

- `docs/AI_Declaration.md`


## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- Anderson Neil Peña
- Dayana Buitrago
- David Clavijo

## 🙏 Agradecimientos

- ChatGPT para la estructura de los scrapers
- Playwright para la automatización del navegador
- Las bases de datos académicas por proporcionar acceso a la información
