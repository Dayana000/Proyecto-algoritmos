# Fundamentación del Uso de IA en el Proyecto

Este documento resume dónde, cómo y con qué propósito se emplean técnicas o modelos de
Inteligencia Artificial dentro del proyecto, y qué aspectos deben considerarse al ejecutarlo o
ampliarlo.

---

## 1. Alcance del uso de IA

1. **Requerimiento 2 – Similitud textual:**
   - Se implementan cuatro algoritmos clásicos (**Levenshtein**, **Jaccard**, **Dice** y **Coseno TF‑IDF**).
   - Adicionalmente, se ofrecen **dos algoritmos basados en modelos de IA** mediante embeddings
     semánticos que aprovechan la librería `sentence-transformers`.
   - Cuando los modelos están disponibles, se calcula la similitud del coseno entre los embeddings de
     cada abstract para capturar relaciones semánticas más profundas (sinónimos, paráfrasis, etc.).
   - Si la librería no está instalada, el sistema continúa funcionando con los algoritmos clásicos y
     notifica que las métricas de IA no se ejecutaron.

2. **Resto de requerimientos (1, 3, 4 y 5):**
   - Se apoyan en técnicas estadístico-computacionales propias (TF‑IDF manual, clustering, gráficos
     de coocurrencia, etc.) sin emplear modelos de IA externos.

---

## 2. Fundamento técnico de los algoritmos IA en Req. 2

| Algoritmo | Modelo | Descripción | Consideraciones |
|-----------|--------|-------------|-----------------|
| `ia_embeddings` | `all-MiniLM-L6-v2` (Sentence-BERT) | Genera un embedding denso (384 dimensiones) para cada texto y calcula similitud del coseno. | Modelo ligero optimizado para capturar significado general de frases. |
| `ia_embeddings_alt` | `paraphrase-MiniLM-L6-v2` | Entrenado específicamente para detección de paráfrasis. | Útil para comparar resultados con un modelo orientado al reconocimiento semántico. |

### Beneficios
- Captura la semántica del texto más allá de coincidencias léxicas.
- Permite comparar abstracts con vocabularios distintos pero significado similar.

### Limitaciones
- Requiere descargar modelos pre-entrenados (decenas/centenas de MB).
- Necesita acceso a internet la primera vez que se ejecuta para descargar los pesos.
- Consumo de memoria y tiempo mayor al de los algoritmos clásicos.

---

## 3. Aspectos de uso responsable

1. **Reproducibilidad:** documentar la versión de los modelos (`sentence-transformers`, embeddings)
   y mantener un registro de cuándo se descargaron. Cambios en los pesos pueden alterar resultados.

2. **Privacidad:** los abstracts analizados permanecen localmente; no se envía información a servicios
   externos durante la inferencia (los modelos se descargan una vez y se ejecutan localmente).

3. **Dependencias opcionales:** el flujo detecta si `sentence-transformers` no está disponible y
   omite las métricas de IA, asegurando que el proyecto siga siendo utilizable sin esa librería.

4. **Interpretabilidad:** las métricas basadas en embeddings complementan, pero no sustituyen, la
   evaluación por algoritmos clásicos. Se recomienda analizar ambos tipos de resultados para tomar decisiones.

5. **Mantenimiento:** si se requiere compatibilidad con versiones futuras de Python, es posible que
   `sentence-transformers` tarde en ofrecer ruedas precompiladas; documentar este punto para futuros usuarios.

---

## 4. Recomendaciones para ejecutores y revisores

1. Instalar la librería `sentence-transformers` solo si se necesitan las métricas semánticas avanzadas.
2. Registrar en informes qué modelos se habilitaron, qué versión y de dónde provienen.
3. Comparar los resultados de IA con los algoritmos clásicos para detectar inconsistencias.
4. Mantener copias locales de los pesos (carpeta `.cache` de HuggingFace) si se requiere un entorno sin internet.
5. Informar a los usuarios que, si no se instala `sentence-transformers`, el script indicará que las métricas
   de IA fueron omitidas y el resultado sigue siendo válido con los algoritmos clásicos.

---

## 5. Resumen

- **Uso principal de IA:** complementar el análisis de similitud textual con embeddings semánticos (Req. 2).
- **Opcionalidad:** el sistema funciona sin la librería de IA; se recomienda instalarla cuando
  se necesite profundizar en la comparación semántica.
- **Documentación:** este archivo y `docs/AI_Declaration.md` constituyen la evidencia sobre cómo y
  por qué se utilizan herramientas de IA en el proyecto.

Para cualquier ampliación o auditoría, se sugiere mantener actualizada esta fundamentación junto con los
informes de versiones y pruebas correspondientes.***

