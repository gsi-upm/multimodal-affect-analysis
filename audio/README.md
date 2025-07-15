# Natural Language Understanding System For Emotional Intelligence In Voice
## Description

This platform provides **three APIs** for voice emotion analysis, enabling audio transcription, spectrogram extraction, emotion detection from voice, and combined text-voice emotion analysis, as a multimodal insight.

## Architecture

- **API 1: Whisper Endpoint** Transcribes audio to text using Whisper and generates a spectrogram.
Whisper has several model sizes: `tiny`, `base`, `small`, `large-v2` and `large-v3`.   The default model is `tiny` (configurable via environment variable).

- **API 2: Emotion Recognition Endpoint** Detects emotions in voice using a wav2vec-based model.
- **API 3: Multimodal Endpoint** Performs combined analysis using Whisper-transcribed text (with pysentimiento) and voice-based emotion detection, with fine-tuned Wav2Vec-based model.


## Installation
The platform can be deployed by Docker-compose or Podman-compose. APIs and webs are deployed in different individual containers, and then orchested by Docker-compose.
```bash
docker-compose up --build
```
```bash
podman-compose up --build
```
## Accessing the Service

By default, the service runs locally on:

**http://localhost:8080**

Make sure port `8080` is not in use, or change the port in the `docker-compose.yml` file if needed. The UI is visible by a simple JavaScript browser.

## API Usage
### 1. Whisper Endpoint
**POST** `/api/transcribe`

Transcribes audio to text and generates a spectrogram image.

**Request:**
- Form-data with an audio file (e.g., `.wav`, `.mp3`)
- Language (e.g, 'auto', 'en','es')
**Response:**
- Text (transcription/translate).
- Detected language.
  
### 2. Emotion Recognition Endpoint
Analyzes voice to detect emotions using a Wav2Vec-based model.
**Request:**
- Form data with an audio file ( .wav) and audio language.
**Response:**
- Emotion detection with each scores.

### 3. Multimodal Endpoint
Performs joint emotion analysis using both voice and transcribed text via Whisper + Pysentimiento.
**Request:**
- Form data with an audio file ( .wav) and audio language.
**Response:**
- Emotion detection with each scores.
- Detected language by Whisper
- 
## UI Preview

The web interface allows users to upload audio and view emotional analysis in real time. The following images shows index and emotion recognition endpoint.

![Captura desde 2025-07-05 18-05-38](https://github.com/user-attachments/assets/ebf49f78-3229-4e5e-aa79-4e0e4518de04)
![image](https://github.com/user-attachments/assets/85c3f66c-1e2c-49c8-97be-d4ae3d2d9c69)


