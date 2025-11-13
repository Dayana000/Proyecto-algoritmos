FROM python:3.11-slim

# 1. Dependencias de sistema necesarias para Playwright/Chromium y NLTK.
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget unzip ca-certificates \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libpango-1.0-0 libasound2 fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# 2. Definir directorio de trabajo y copiar proyecto.
WORKDIR /app
COPY . /app

# 3. Preparar entorno Python.
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install chromium && \
    python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"

# 4. Comando por defecto (sobrescribible al ejecutar el contenedor).
CMD ["python", "menu_requerimientos.py"]


