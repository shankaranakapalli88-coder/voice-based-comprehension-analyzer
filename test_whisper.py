from speech_to_text import transcribe_audio

text = transcribe_audio("uploads/sample.wav")

print("\nTRANSCRIPTION:")
print(text)