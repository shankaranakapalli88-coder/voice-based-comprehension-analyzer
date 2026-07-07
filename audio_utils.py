import librosa
import soundfile as sf
import numpy as np


def normalize_audio(input_path, output_path):
    audio, sr = librosa.load(input_path, sr=16000)

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak

    sf.write(output_path, audio, sr)

    return output_path


def extract_rms(audio_path):
    y, sr = librosa.load(audio_path)

    rms = librosa.feature.rms(y=y)

    return float(np.mean(rms))


def pause_ratio(audio_path):
    y, sr = librosa.load(audio_path)

    silence_frames = np.sum(np.abs(y) < 0.01)

    return float(silence_frames / len(y))

from audio_utils import extract_rms, pause_ratio

print("RMS:", extract_rms("uploads/sample.wav"))
print("Pause Ratio:", pause_ratio("uploads/sample.wav"))