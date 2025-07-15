from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import whisper
from transformers import AutoModelForAudioClassification,pipeline, AutoFeatureExtractor
import tempfile
from pysentimiento import create_analyzer
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import librosa
import numpy as np

router = APIRouter()

# ENV
model_name = os.getenv("WHISPER_MODEL", 'tiny') #CHANGE ME
model = whisper.load_model(model_name)  


@router.post("/whisper")
async def upload_file(file: UploadFile = File(...),  language: str = Form(...) ):
    # It is created a route for the destination file where uploaded audios will be saved.
    upload_dir = os.path.join(os.getcwd(), "uploads")  

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Complete route to save the file
    file_path = os.path.join(upload_dir, file.filename)

    # The file is saved
    with open(file_path, "wb") as myfile: 
        content = await file.read()
        myfile.write(content)

    
    # Audio is loaded and prepared
    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)
    
    # Audio is converted to Log_Mel Spectogram
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)
    

    # Create a Mel frequency list linearly spaced
    mel_np = mel.cpu().numpy()
    mel_norm = (mel_np - mel_np.min()) / (mel_np.max() - mel_np.min() + 1e-9)
    n_mels = mel.shape[0]
    mel_frequencies_hz = librosa.mel_frequencies(n_mels=n_mels, fmin=0, fmax=500)

    # Create a Spectogram images
    fig, ax = plt.subplots(figsize=(10, 4))
    img = ax.imshow(mel_norm, aspect='auto', origin='lower')
    ax.set_xlim(0, 500)
    # Ticks visibles and its labels
    tick_freqs = [0, 100, 200, 300, 400, 500]
    tick_pos = [np.argmin(np.abs(mel_frequencies_hz - f)) for f in tick_freqs]

    ax.set_yticks(tick_pos)
    ax.set_yticklabels([str(f) for f in tick_freqs])
    ax.set_ylabel("Frequency (Hz)")
    ax.set_xlabel("Time (frames)")
    ax.set_title("Log-Mel Spectrogram")
    plt.colorbar(img, ax=ax, label="Intensity")
    buf=BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    # Codify the image in base64 for sending as string
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    plt.close(fig)

    # Detect language
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    
    if language== "auto":
         result = model.transcribe(file_path)  # Whisper detects the language automatically
        
    elif detected_language != language:
            result = model.transcribe(file_path,language=language, task="translate")  # Whisper will traduce to English
        
    else:
        result = model.transcribe(file_path, language=language)  # Use the selected language

    print (result["text"])

  
# JSON return
    return JSONResponse(content={"message": "Success", "filename": file.filename, "text": result["text"], "language": detected_language, "spectrogram_image_base64": image_base64})




"""
model_path = "./model/english"
modelo_path= "./model/spanish"
"""
model_path = "gsi-upm/wav2vec_english_emotion-analysis"
modelo_path= "gsi-upm/wav2vec_spanish_emotion-analysis"

audio_model = AutoModelForAudioClassification.from_pretrained(model_path)
audio_modelo= AutoModelForAudioClassification.from_pretrained(modelo_path)

processor = AutoFeatureExtractor.from_pretrained(model_path)
processor_sp = AutoFeatureExtractor.from_pretrained(modelo_path)

classifier = pipeline("audio-classification", model=audio_model, feature_extractor=processor)
clasificador= pipeline("audio-classification", model=audio_modelo, feature_extractor=processor_sp)

print(processor.sampling_rate)


@router.post("/emotion")
async def predict(file: UploadFile = File(...), language: str = Form(...) ):
    
    # Save temporarly the audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # English inference
    if language =="en":
        prediction = classifier(tmp_path)

    
    # Spanish inference
    elif language=="es":
        prediction = clasificador(tmp_path)
    
    return {
        "emotions": [
        {"label": p["label"], "score": round(p["score"], 4)}
        for p in prediction
    ]
    }


@router.post("/multimodal")
async def sentiment (file: UploadFile = File(...), language: str = Form(...)):
    
    upload_dir = os.path.join(os.getcwd(), "uploads")  

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_path = os.path.join(upload_dir, file.filename)

    # The file is saved
    with open(file_path, "wb") as myfile: 
        content = await file.read()
        myfile.write(content)
        

    audio = whisper.load_audio(file_path)
    audio = whisper.pad_or_trim(audio)

    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

     # Language detection
    _, probs = model.detect_language(mel)
    detected_language = max(probs, key=probs.get)
    
    if language== "auto":
         result = model.transcribe(file_path)  
        
    elif detected_language != language:
            result = model.transcribe(file_path,language=language, task="translate")  
    else:
        result = model.transcribe(file_path, language=language) 

    print (result["text"])

    analyzer_sentiment = create_analyzer(task="sentiment", lang=detected_language)
    sentiment_prediction = analyzer_sentiment.predict(result["text"])
    sentiment_label= sentiment_prediction.output
    print(sentiment_label)

    if detected_language == "en":
            audio_emotion = classifier(file_path)
    elif detected_language == "es":
            audio_emotion = clasificador(file_path)
    

    return JSONResponse(
            content={
                "message": "Success",
                "filename": file.filename,
                "language": detected_language,
                "transcription": result["text"],
                "text_sentiment": sentiment_prediction.output,
                "audio_emotions": [
                    {"label": p["label"], "score": round(p["score"], 4)}
                    for p in audio_emotion
                ],
            }
        )
