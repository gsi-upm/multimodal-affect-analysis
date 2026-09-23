# Multimodal Cloud-Edge Emotion Detection

## Utilidad y funcionalidades

**Multimodal Cloud-Edge Emotion Detection** reúne servicios para analizar información afectiva (es decir, de emociones) en **texto, voz e imagen**. Cada modalidad dispone de su propia aplicación y puede ejecutarse de forma independiente. El módulo de audio devuelve conjuntamente el sentimiento del texto transcrito y las emociones de la voz; el código no implementa una fusión única de las tres modalidades ni un reparto automático del procesamiento entre nube y dispositivo.

El **módulo de texto** expone una API con LitServe y utiliza `roblesadrian/llama-3b-emotion-classifier`, un modelo orientado al inglés. Para cada entrada devuelve cinco puntuaciones: `anger`, `fear`, `joy`, `sadness` y `surprise`. Aplica una función sigmoide a cada salida, por lo que las puntuaciones son independientes y no tienen que sumar uno. El servidor no establece un umbral ni selecciona una única emoción.

El **módulo de audio** incorpora una API FastAPI y una interfaz web. Whisper transcribe el audio, identifica el idioma y genera un espectrograma; dos modelos Wav2Vec clasifican emociones de voz en español e inglés. La operación multimodal añade el sentimiento de la transcripción mediante pysentimiento y devuelve ambos resultados por separado. Los modelos utilizados son `gsi-upm/wav2vec_spanish_emotion-analysis` y `gsi-upm/wav2vec_english_emotion-analysis`.

El **módulo de vídeo** combina una API FastAPI con una aplicación Streamlit. Permite registrar rostros, consultar y eliminar registros, reconocer identidades registradas y estimar expresiones emocionales mediante `oscarparro/emotion_detection_vit`. La interfaz captura fotogramas, localiza rostros con OpenCV y consulta la API a intervalos configurables. El registro se conserva en un JSON con identificadores, vectores faciales y miniaturas. Las etiquetas obtenidas son predicciones del modelo, no una medida directa del estado emocional de una persona.

## Instalación y uso

La guía utiliza una terminal Bash en Linux y ejecuta **un módulo cada vez**, porque los tres despliegues publican su API en el puerto `8000`. El Compose de la raíz solo inicia texto; audio y vídeo tienen sus propios ficheros. Las versiones de las herramientas locales indicadas a continuación son referencias de la guía, no mínimos declarados por el repositorio.

- **Git (2.49.0)** y acceso al repositorio para descargar el código.

- **Docker Engine (28.0.4, referencia)** y **Docker Compose (2.34.0)** para construir y arrancar los contenedores.

- **Bash (5.2)** y **curl (8.5.0)** para ejecutar los comandos y las peticiones de ejemplo.

- Conexión a los repositorios de paquetes y modelos durante la primera ejecución; memoria y disco suficientes para sus pesos. El proyecto no especifica mínimos de RAM ni fija revisiones de los modelos.

**Paso 1. Descargar el código**

Se descarga el repositorio y se selecciona la revisión analizada. Los comandos siguientes parten de su carpeta raíz.

```bash
git clone https://github.com/gsi-upm/multimodal-affect-analysis.git
cd multimodal-affect-analysis
```

**Demo sencilla: análisis de texto**

- **Python (3.12, imagen `python:3.12-slim`)**, **LitServe (0.2.13)**, **Transformers (4.53.2)** y **PyTorch (2.7.1)** se instalan dentro de la imagen; no hace falta instalarlos en el equipo anfitrión. La imagen no fija la revisión de Python y `pytest` no tiene versión fijada.

**Paso 2. Construir y arrancar la API de texto**

```bash
docker compose up -d --build text-api
```

El primer arranque descarga el modelo. Se espera hasta que el registro indique que el servidor está listo; `Ctrl+C` cierra el seguimiento de los logs sin detener el contenedor. El Compose no configura acceso a GPU y el código no traslada explícitamente el modelo ni las entradas al dispositivo recibido por LitServe: este procedimiento no debe presentarse como un despliegue CUDA validado.

**Paso 3. Enviar una frase e interpretar la respuesta**

```bash
curl --fail-with-body --silent --show-error \
  http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  --data '{"text":"I feel happy and excited about this opportunity."}'
```

La API devuelve un objeto JSON con las cinco emociones. El siguiente ejemplo ilustra su estructura; sus cifras no proceden de una ejecución de esta guía.

```json
{
  "anger": 0.08,
  "fear": 0.03,
  "joy": 0.86,
  "sadness": 0.04,
  "surprise": 0.25
}
```

Una puntuación más alta indica una mayor activación de esa etiqueta. No representa una intensidad emocional calibrada ni excluye las demás categorías. Al terminar la prueba se libera el puerto antes de iniciar otra modalidad.

```bash
docker compose down
```

**Despliegue y prueba de audio**

- **Python (3.12, imagen `python:3.12-slim`)**, **FastAPI (0.115.4)** y **PyTorch (2.5.1)** se instalan en el contenedor. FFmpeg y libsndfile1 también se incorporan durante la construcción, sin versión fijada.

- El manifiesto declara `whisper==1.1.10`, pero el Dockerfile instala además OpenAI Whisper desde GitHub sin fijar revisión. Uvicorn, Transformers, pysentimiento, Matplotlib, NumPy, librosa y python-multipart tampoco están bloqueados. La web usa `nginx:alpine`, una etiqueta móvil.

- Para la prueba se necesita un **WAV con voz en español o inglés**. Se usará `ejemplo.wav`, situado en la raíz del repositorio; no es un archivo incluido en el proyecto.

**Paso 1. Arrancar audio**

```bash
docker compose -f audio/docker-compose.yml up -d --build
docker compose -f audio/docker-compose.yml logs -f api
```

La web se abre en `http://localhost:8080` y la documentación de la API en `http://localhost:8000/docs`. Whisper usa `tiny`, configurado mediante `WHISPER_MODEL` en el Compose. La API carga también los dos modelos Wav2Vec al arrancar. Las páginas HTML llaman a `127.0.0.1:8000`; para utilizarlas desde otro equipo hay que adaptar esas direcciones.

**Paso 2. Analizar la voz y la transcripción**

Selecciona un fichero de audio y sitúalo dentro de la carpeta /audio (utilizando como referencia la raiz del repositorio). Suponiendo que el fichero sea un .wav que se llame "ejemplo.wav", deberíamos ejecutar el comando abajo mostrado. Si el fichero tiene un nombre diferente, se debe sustituir "ejemplo.wav" por el nombre de nuestro fichero de audio en el comando:

**NOTA**: el formato *mp3* está permitido (en este caso, escribiríamos "ejemplo.mp3")

```bash
curl --fail-with-body --silent --show-error \
  http://localhost:8000/multimodal \
  -F 'file=@audio/ejemplo.wav' -F 'language=auto'
```

La respuesta incluye `message`, `filename`, `language`, `transcription`, `text_sentiment` y `audio_emotions`; esta última propiedad contiene pares `label` y `score`. Para obtener únicamente las emociones de voz se utiliza `POST /emotion` con `language=es` o `language=en`. Para transcribir y obtener el espectrograma se utiliza `POST /whisper`, que devuelve `text`, `language` y `spectrogram_image_base64`, además de los datos del archivo.

Estas son las rutas definidas en el código; `/api/transcribe`, mencionada en el README de audio, no está implementada. Conviene usar `language=auto` en la prueba multimodal: si se fuerza un idioma distinto del detectado, la implementación solicita a Whisper una traducción al inglés. El análisis emocional de voz solo contempla español e inglés.

**Paso 3. Detener audio**

```bash
docker compose -f audio/docker-compose.yml down
```

**Despliegue y prueba de imagen y vídeo**

- El backend usa **Python (3.11, imagen `python:3.11-slim`)**. FastAPI, Uvicorn, Transformers, PyTorch, Torchvision, Pillow, NumPy, OpenCV, face_recognition, python-multipart y python-dotenv no tienen versiones fijadas. El Dockerfile instala las herramientas de compilación necesarias, incluido CMake.

- La prueba de la API utiliza una imagen **JPEG o PNG en color** con un rostro, denominada `rostro.jpg` y situada en la raíz del repositorio. No necesita cámara ni un registro previo.

- La interfaz de cámara es opcional y requiere **Python (3.11, referencia para el entorno local)** y los paquetes de `video/frontend/requirements.txt`, todos sin versión fijada. También necesita acceso local a la cámara y las dependencias de compilación de dlib cuando no haya una distribución binaria compatible.

**Paso 1. Arrancar la API de vídeo**

```bash
mkdir -p video/data
docker compose -f video/docker-compose.yml up -d --build
docker compose -f video/docker-compose.yml logs -f backend
```

La API y su documentación quedan disponibles en `http://localhost:8000/docs` cuando termina la carga del modelo. El directorio `video/data` se monta en el contenedor para conservar `registered_faces.json` entre arranques. Los modelos Caffe de detección facial ya están incluidos en el repositorio.

**Paso 2. Probar una imagen sin registrar identidades**

```bash
curl --fail-with-body --silent --show-error \
  http://localhost:8000/identify_face \
  -F 'file=@rostro.jpg' -F 'mode=Deteccion emociones'
```

La respuesta contiene `name`, con el valor `N/A`, y `emotion`, con la etiqueta predicha. En este modo la API analiza directamente la imagen recibida: debe enviarse un recorte del rostro. Los otros valores de `mode` son `Deteccion completa`, `Deteccion rostros` y `No hacer nada`, escritos sin tilde. El reconocimiento de identidades requiere registrarlas previamente mediante `POST /register_face`, con los campos `name` y `file`; los registros se consultan con `GET /list_faces` y se eliminan mediante `POST /delete_face`, con el campo `id`.

**Paso 3. Abrir la interfaz de cámara, si se necesita**

En otra terminal, desde la raíz del repositorio, se prepara el frontend. El siguiente arranque corresponde a Linux; `CAMERA_BACKEND_NAME` es el nombre que lee el código, aunque el README de vídeo mencione otra variable.

```bash
cd video/frontend
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
API_URL=http://localhost:8000 \
CAMERA_BACKEND_NAME=CAP_V4L2 \
python -m streamlit run streamlit-app.py
```

Se abre `http://localhost:8501`, se elige un modo, se pulsa «Aplicar Modo» y después «Activar Cámara». La captura continua se realiza en el equipo que ejecuta Streamlit. Antes de cambiar de pestaña se pulsa «Detener Cámara». Las otras pestañas permiten registrar rostros y revisar su historial. Los intervalos por defecto son 10 segundos para detección completa, 2 para emociones y 5 para reconocimiento.

**Paso 4. Cerrar el demostrador**

Se cierra Streamlit con `Ctrl+C`. Desde la raíz del repositorio se detiene el backend; el directorio `video/data` conserva los registros.

```bash
docker compose -f video/docker-compose.yml down
```
