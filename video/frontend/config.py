# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Intervalos (en segundos)
SEG_COMPLETA       = int(os.getenv("SEG_COMPLETA", "10"))
SEG_EMOCIONES      = int(os.getenv("SEG_EMOCIONES", "2"))
SEG_RECONOCIMIENTO = int(os.getenv("SEG_RECONOCIMIENTO", "5"))

# Codigo BGR para el color de ventana en Desconocido
B = int(os.getenv("B", "0"))
G = int(os.getenv("G", "255"))
R = int(os.getenv("R", "0"))

# Código BGR para el color de modo de deteccion de Emociones
B2 = int(os.getenv("B2", "0"))
G2 = int(os.getenv("G2", "0"))
R2 = int(os.getenv("R2", "255"))

# URLs y nombres de modelo
API_URL            = os.getenv("API_URL", "http://localhost:8000")
EMOTION_MODEL_NAME = os.getenv("EMOTION_MODEL_NAME", "oscarparro/emotion_detection_vit")

# Rutas a ficheros de modelo
PROTOTXT_PATH      = os.getenv("PROTOTXT_PATH", "model/deploy.prototxt")
CAFFE_MODEL_PATH   = os.getenv("CAFFE_MODEL_PATH", "model/res10_300x300_ssd_iter_140000.caffemodel")

# Fichero JSON de persistencia
REGISTERED_FACES_FILE = os.getenv("REGISTERED_FACES_FILE", "data/registered_faces.json")

# Cámara
CAMERA_INDEX   = int(os.getenv("CAMERA_INDEX", "0"))
CAMERA_BACKEND_NAME = os.getenv("CAMERA_BACKEND_NAME", "CAP_DSHOW")

