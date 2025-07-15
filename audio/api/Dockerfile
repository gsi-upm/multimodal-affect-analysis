# Usa una imagen base de Python 3.12 con Debian (ya que Whisper necesita Linux)
FROM python:3.12-slim

# Actualiza el sistema e instala las dependencias de Ubuntu necesarias para Whisper
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /api

# Copia los archivos de requisitos de la aplicación al contenedor
COPY requirements.txt /api/

# Instala las dependencias de Python de tu proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Instala las dependencias de Python incluyendo Whisper desde GitHub
RUN pip install --no-cache-dir fastapi uvicorn python-multipart \
    && pip install git+https://github.com/openai/whisper.git

#Instalo python así para ver si se conecta el contenedor a internet. 
RUN apt-get update && apt-get install -y iputils-ping
# Copia el resto de los archivos de la aplicación al contenedor
COPY . /api/

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 8000

# Define el comando para iniciar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# Se utiliza 0.0.0.0 porque si utilizo 127.0.0.1 apunto a la dirección local del contenedor
#no a la máquina. Para que el servidor sea accesible desde fuera del contenedor,
# es necesario que escuche a 0.0.0.0:800 dentro del contenedor.
