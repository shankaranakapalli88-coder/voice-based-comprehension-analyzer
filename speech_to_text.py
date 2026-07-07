import whisper

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Model loaded successfully.")

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]