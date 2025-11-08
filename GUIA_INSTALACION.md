# 📋 Guía de Instalación y Configuración

## ✅ Requisitos Previos

- ✅ Python 3.7+ (Ya tienes Python 3.13.3 instalado)
- ⚠️ Navegador Chrome/Chromium (se instalará automáticamente con Playwright)
- ⚠️ Credenciales de acceso a las bases de datos (email institucional)

---

## 🚀 Pasos de Instalación

### Paso 1: Instalar Dependencias de Python

Abre PowerShell o CMD en la carpeta del proyecto y ejecuta:

```bash
py -m pip install -r requirements.txt
```

O si tienes `pip` configurado directamente:

```bash
pip install -r requirements.txt
```

**Nota:** Si tienes problemas, prueba con:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

### Paso 2: Instalar Playwright y Navegadores

Playwright necesita descargar los navegadores. Ejecuta:

```bash
py -m playwright install
```

O:

```bash
playwright install
```

Esto descargará Chromium automáticamente (puede tardar unos minutos).

---

### Paso 3: Descargar Recursos de NLTK

Para el análisis de grafos de coocurrencia, necesitas descargar recursos de NLTK:

```bash
py -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

O ejecuta Python interactivamente:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

---

### Paso 4: Configurar Credenciales

1. **Copia el archivo de plantilla:**
   - En Windows PowerShell:
     ```bash
     Copy-Item env.template .env
     ```
   - O manualmente: copia `env.template` y renómbralo a `.env`

2. **Edita el archivo `.env`** con un editor de texto (Notepad, VS Code, etc.) y completa:

   ```
   EMAIL_USER=tu_email@institucional.edu.co
   EMAIL_PASSWORD=tu_contraseña_de_aplicacion_google
   ```

   **⚠️ IMPORTANTE:**
   - `EMAIL_USER`: Tu email institucional de la Universidad del Quindío
   - `EMAIL_PASSWORD`: **NO** uses tu contraseña normal de Google
   - Debes crear una **"Contraseña de aplicación"** de Google:
     1. Ve a tu cuenta de Google → Seguridad
     2. Activa la verificación en 2 pasos (si no está activada)
     3. Ve a "Contraseñas de aplicaciones"
     4. Genera una nueva contraseña para "Correo"
     5. Usa esa contraseña de 16 caracteres en el archivo `.env`

---

## 🎯 Ejecución del Proyecto

### Opción A: Ejecución Completa (Recomendado)

Ejecuta todo el proceso: scraping + unificación + reporte:

```bash
py main.py
```

O:

```bash
python main.py
```

**¿Qué hace?**
1. ✅ Verifica la configuración
2. 🔄 Ejecuta los 3 scrapers (ACM, IEEE, Sage)
3. 🔗 Unifica los datos y detecta duplicados
4. 📊 Genera reporte de estadísticas

**⏱️ Tiempo estimado:** 30-60 minutos (depende de la velocidad de internet y las bases de datos)

---

### Opción B: Ejecución por Módulos

#### Solo Scraping de ACM:
```bash
py Scraping/ACM.py
```

#### Solo Scraping de IEEE:
```bash
py Scraping/IEE.py
```

#### Solo Scraping de Sage:
```bash
py Scraping/Sage.py
```

#### Solo Unificación de Datos:
```bash
py Unificador_duplicador/Categorizacion.py
```

#### Análisis de Grafos (requiere datos unificados):
```bash
py graph_analysis_main.py
```

#### Análisis Rápido (muestra limitada):
```bash
py quick_graph_analysis.py
```

---

## 📁 Estructura de Archivos Generados

Después de ejecutar, encontrarás en la carpeta `Data/`:

- `resultados_ACM.bib` - Artículos de ACM
- `resultados_ieee.bib` - Artículos de IEEE  
- `resultados_Sage.bib` - Artículos de Sage
- `unificados.bib` - Artículos únicos unificados
- `duplicados.bib` - Artículos duplicados detectados
- `citation_graph.json` - Grafo de citaciones
- `cooccurrence_graph.json` - Grafo de coocurrencia
- `graph_analysis_report.json` - Reporte completo

---

## 🔧 Solución de Problemas Comunes

### Error: "No se encontró el archivo .env"
- ✅ Asegúrate de haber creado el archivo `.env` desde `env.template`
- ✅ Verifica que esté en la raíz del proyecto (misma carpeta que `main.py`)

### Error: "ModuleNotFoundError: No module named 'playwright'"
- ✅ Ejecuta: `py -m pip install playwright`
- ✅ Luego: `py -m playwright install`

### Error: "ModuleNotFoundError: No module named 'nltk'"
- ✅ Ejecuta: `py -m pip install nltk`
- ✅ Descarga recursos: `py -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"`

### Error de credenciales al hacer login
- ✅ Verifica que `EMAIL_USER` y `EMAIL_PASSWORD` estén correctos en `.env`
- ✅ Asegúrate de usar una **contraseña de aplicación** de Google, no tu contraseña normal
- ✅ Verifica que tengas acceso a las bases de datos a través del portal de la universidad

### Error: "No se encontró el archivo Data/unificados.bib"
- ✅ Primero ejecuta el scraping y la unificación: `py main.py`
- ✅ O ejecuta manualmente: `py Unificador_duplicador/Categorizacion.py`

### El navegador no se abre o hay errores de Playwright
- ✅ Ejecuta: `py -m playwright install chromium`
- ✅ Verifica que Chrome/Chromium esté instalado en tu sistema

### Error de permisos o acceso denegado
- ✅ Ejecuta PowerShell o CMD como Administrador
- ✅ Verifica que tengas permisos de escritura en la carpeta del proyecto

---

## 📝 Notas Importantes

1. **Tiempo de ejecución:** El scraping puede tardar mucho tiempo (30-60 minutos) porque:
   - Navega por múltiples páginas
   - Extrae información de cada artículo
   - Espera tiempos de carga de las páginas

2. **Acceso a bases de datos:** Necesitas acceso institucional a:
   - ACM Digital Library
   - IEEE Xplore
   - Sage Journals
   - A través del portal: https://library.uniquindio.edu.co/databases

3. **Término de búsqueda:** Por defecto busca "generative artificial intelligence"
   - Para cambiar, edita los archivos en `Scraping/` y busca la línea con el término

4. **Modo headless:** Los scrapers abren el navegador visible (`headless=False`)
   - Puedes ver el proceso en tiempo real
   - Para ejecutar en segundo plano, cambia a `headless=True` en los archivos de scraping

---

## ✅ Verificación de Instalación

Para verificar que todo está correcto, ejecuta:

```bash
py -c "import playwright; import networkx; import nltk; import matplotlib; print('✅ Todas las dependencias están instaladas')"
```

Si no hay errores, ¡estás listo para ejecutar el proyecto!

---

## 🎉 ¡Listo!

Una vez completados estos pasos, puedes ejecutar:

```bash
py main.py
```

Y el proyecto comenzará a funcionar automáticamente.

