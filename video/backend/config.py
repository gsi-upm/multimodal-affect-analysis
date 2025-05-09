# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Modelo de detección de emociones
EMOTION_MODEL_NAME = os.getenv("EMOTION_MODEL_NAME", "oscarparro/emotion_detection_vit")

# Rutas a ficheros de modelo
PROTOTXT_PATH      = os.getenv("PROTOTXT_PATH", "model/deploy.prototxt")
CAFFE_MODEL_PATH   = os.getenv("CAFFE_MODEL_PATH", "model/res10_300x300_ssd_iter_140000.caffemodel")

# Fichero JSON de persistencia
REGISTERED_FACES_FILE = os.getenv("REGISTERED_FACES_FILE", "data/registered_faces.json")