FROM python:3.11-slim

# 1. Crear directorio de trabajo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      libgtk2.0-dev \
      libgl1 \
      libglib2.0-0 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Copiar y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el código
COPY api.py config.py /app/
COPY model/ ./model/

# 4. Crear carpeta data para el JSON
RUN mkdir -p /app/data

# 5. Exponer puerto y arrancar Uvicorn
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]