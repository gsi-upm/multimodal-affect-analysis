# Face and Emotion Recognition System

Proyecto completo de reconocimiento facial y detección de emociones, compuesto por:

- **Backend**: API en FastAPI para registrar rostros, listar registros, eliminar registros y procesar imágenes para identificación y predicción de emociones.  
- **Frontend**: App en Streamlit con tres pestañas para:
  1. **Identificación en Tiempo Real**  
     - Selector de modo de funcionamiento:  
       - “Detección completa” (reconocimiento + emoción)  
       - “Detección emociones” (solo emoción)  
       - “Detección rostros” (solo reconocimiento)  
       - “No hacer nada”  
     - Botón “Aplicar Modo” para confirmar cambios  
     - Botones “Activar Cámara” / “Detener Cámara”  
     - Streaming de vídeo con detección local de rostros y llamadas periódicas al endpoint `/identify_face`
  2. **Registro de Rostro**  
     - Captura desde cámara  
     - Introducción de nombre  
     - Envío al endpoint `/register_face`  
     - Guarda en JSON (con ID, encoding facial, miniatura Base64, color aleatorio y timestamp)
 
  3. **Historial de Registros**  
     - Lista todos los rostros registrados (miniaturas, nombre, fecha y color)  
     - Botón “Eliminar” junto a cada registro → llama a `/delete_face` y actualiza la lista


## 🔧 Instalación

1. Clona este repositorio y sitúate en la carpeta:

   ```bash
   git clone https://github.com/oscarparro/streamlit-app.git
   cd streamlit-app-docker

2. Crea un entorno virtual

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate     # Linux / macOS
   .venv\Scripts\activate        # Windows
   ```

3. Instala las dependencias correspondientes

   ```bash
   pip install --upgrade pip
   cd frontend
   pip install -r requirements.txt
   ```

4. Directorio para el almacenamiento de rostros

   ```bash
   cd ..
   mkdir -p data
   ```


## 🐋 Desplegar el Backend con Docker

**Construye la imagen**

   ```bash
   docker compose up -d --build
   ```


## 🚀 Arrancar la aplicación
   
**Frontend**
  
   ```bash
    streamlit run streamlit-app.py
   ```


## ⚠️ IMPORTANTE

- Puedes usar la pestaña de Identificación en Tiempo Real sin necesidad de registro previo, pero recuerda pulsar siempre “Detener Cámara” antes de cambiar de pestaña o cerrar la aplicación, para liberar el dispositivo de captura.

- Los registros se guardan en un archivo JSON y sobreviven al cierre de la app. Sin embargo, después de reiniciar Streamlit debes navegar a la pestaña Historial de Registros y recargar (refrescar) dicha pestaña para que se muestren los rostros guardados de sesiones anteriores.

- Dentro del archivo /frontend/.env se encuentran las variables de entorno. En caso de utilizar un SO de Linux se debe cambiar el valor de `CAMERA_BACKEND=CAP_DSHOW` por `CAMERA_BACKEND=CAP_V4L2`.

- Si al instalar face_recognition, dlib u OpenCV obtienes errores de CMake o librerías gráficas faltantes, asegúrate de tener:

```bash
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    libgl1-mesa-glx \
    libglib2.0-0
```
