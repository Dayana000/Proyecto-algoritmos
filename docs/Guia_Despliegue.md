# Guía de Despliegue y Entrega Académica

Este documento resume los pasos recomendados para preparar el proyecto **Proyecto-algoritmos** para su presentación o despliegue en un entorno académico (laboratorios, revisión docente o sustentación).

---

## 1. Preparar el entorno

### Windows

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\scripts\setup_windows.ps1
```

El script:

- Detecta automáticamente una instalación de Python 3.10/3.11.
- Crea/actualiza el entorno virtual `.venv`.
- Instala dependencias (`requirements.txt`), navegadores de Playwright y recursos de NLTK.

### Linux / macOS

```bash
chmod +x scripts/setup_unix.sh
scripts/setup_unix.sh
```

Opcionalmente puedes indicar otro nombre para el entorno:

```bash
scripts/setup_unix.sh venv_uq
```

---

## 2. Variables de entorno

1. Copia `env.template` → `.env`.
2. Completa las credenciales institucionales requeridas por los scrapers.

```env
EMAIL_USER=correo@uqvirtual.edu.co
EMAIL_PASSWORD=contraseña_de_aplicacion
```

---

## 3. Ejecución rápida

### Menú de requerimientos (Req. 2–5)

- **Windows** (PowerShell o CMD):
  ```powershell
  scripts\run_menu_windows.bat
  ```

- **Linux / macOS**:
  ```bash
  chmod +x scripts/run_menu_unix.sh
  scripts/run_menu_unix.sh
  ```

### Pipeline completo (Req. 1 + procesamiento)

- **Windows**:
  ```powershell
  scripts\run_main_windows.bat
  ```

- **Linux / macOS**:
  ```bash
  chmod +x scripts/run_main_unix.sh
  scripts/run_main_unix.sh
  ```

---

## 4. Verificación final

```powershell
.\.venv\Scripts\python.exe verificar_instalacion.py
```

Este script comprueba que:

- Las dependencias clave estén instaladas.
- Playwright y NLTK tengan sus recursos mínimos.
- Existan los archivos de datos requeridos (`Data/unificados.bib`, etc.).

---

## 5. Preparación para entrega

1. ✅ Ejecuta el pipeline (`scripts/run_main_*`) para generar los archivos en `Data/`.
2. ✅ Verifica que `Data/visualizations/` contenga los resultados de los requerimientos 4 y 5.
3. ✅ Revisa y exporta la documentación relevante:
   - `README.md`
   - `GUIA_INSTALACION.md`
   - `docs/IA_Fundamentacion.md`
   - `docs/AI_Declaration.md`
   - `docs/Guia_Despliegue.md` (este archivo)
4. ✅ (Opcional) Empaqueta todo en un archivo `.zip` para entregarlo o replicarlo en otra máquina.
5. ✅ Incluye capturas o las salidas PDF/HTML generadas si son requeridas como evidencias.

---

## 6. Despliegue en contenedor (Railway u otro proveedor)

### Construcción local

```bash
docker build -t proyecto-algoritmos:demo .
docker run --rm -it -v $(pwd)/Data:/app/Data proyecto-algoritmos:demo
```

El volumen mantiene las carpetas `Data/` y `Data/visualizations/` fuera del contenedor.

### Publicar la imagen

```bash
docker tag proyecto-algoritmos:demo tuusuario/proyecto-algoritmos:demo
docker push tuusuario/proyecto-algoritmos:demo
```

### Ejecución en Railway

1. Crea un nuevo servicio **Deploy from container image**.
2. Indica `tuusuario/proyecto-algoritmos:demo` como imagen.
3. Define un comando opcional (por ejemplo `python main.py` o `python menu_requerimientos.py --max-articulos 15`).
4. Añade variables de entorno necesarias (`EMAIL_USER`, `EMAIL_PASSWORD`) desde el panel.
5. Conecta un **Persistent Volume** (1 GB es suficiente) y monta `/app/Data`.
6. Lanza el deploy; revisa los logs en tiempo real.
7. Descarga los artefactos desde el volumen o via `railway run bash`.

> La imagen también es compatible con Azure Container Instances, Google Cloud Run Jobs o AWS Fargate.

---

## 7. Troubleshooting rápido

| Problema | Solución |
|----------|----------|
| `❌ No se encontró el entorno virtual` | Ejecuta nuevamente `scripts/setup_windows.ps1` o `scripts/setup_unix.sh`. |
| Error al instalar `playwright` | Ejecuta el script con privilegios de administrador o instala manualmente con `python -m playwright install`. |
| Falta `stopwords/punkt` | Corre `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"` dentro del entorno virtual. |
| Scrapers fallan al autenticarse | Revisa las credenciales en `.env` y que uses una contraseña de aplicación. |
| `sentence-transformers` tarda mucho | Es una dependencia opcional para métricas de IA (Req. 2). Desinstálala si no la necesitas. |

---

## 8. Lista de verificación (checklist)

- [ ] Entorno virtual creado y activable.
- [ ] Dependencias instaladas sin errores.
- [ ] Credenciales configuradas en `.env`.
- [ ] Archivos unificados generados (`Data/unificados.bib`, `Data/duplicados.bib`).
- [ ] Visualizaciones del Req. 4 (`Data/visualizations/req4/`) revisadas.
- [ ] PDF del Req. 5 (`Data/visualizations/req5/req5_visualizations.pdf`) revisado.
- [ ] Documentación actualizada en `/docs/`.
- [ ] Scripts de instalación y ejecución probados en un equipo limpio (si es posible).

¡Con estos pasos el proyecto queda listo para demostraciones, evaluaciones o entregas institucionales!

