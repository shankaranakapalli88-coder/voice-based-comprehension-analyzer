import streamlit as st
import librosa
import librosa.display
import matplotlib.pyplot as plt

from speech_to_text import transcribe_audio
from semantic_eval import similarity_score
from scoring_engine import (
    filler_ratio,
    final_score,
    classify
)
from report_generator import generate_report

st.set_page_config(
    page_title="Voice Based Comprehension Analyzer",
    layout="wide"
)

st.title("🎤 Voice Based Comprehension Analyzer")

# Reference Answer
expected_answer = st.text_area(
    "Reference Answer",
    height=120
)

# Audio Upload
uploaded_file = st.file_uploader(
    "Upload WAV File",
    type=["wav"]
)

if uploaded_file is not None and expected_answer:

    # Save audio
    audio_path = f"uploads/{uploaded_file.name}"

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Audio uploaded successfully.")

    # Waveform
    st.subheader("Waveform")

    audio, sr = librosa.load(audio_path)

    fig, ax = plt.subplots(figsize=(10, 3))

    librosa.display.waveshow(
        audio,
        sr=sr,
        ax=ax
    )

    st.pyplot(fig)

    # Transcription
    student_answer = transcribe_audio(audio_path)

    # Semantic Similarity
    semantic_score = similarity_score(
        expected_answer,
        student_answer
    )

    # Filler Ratio
    filler_ratio_value = filler_ratio(
        student_answer
    )

    # Temporary Pause Ratio
    pause_ratio = 0.10

    # Final Score
    score = final_score(
        semantic_score,
        filler_ratio_value,
        pause_ratio
    )

    # Grade
    result_grade = classify(score)

    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reference Answer")
        st.write(expected_answer)

    with col2:
        st.subheader("Student Answer")
        st.write(student_answer)

    # Metrics
    st.subheader("Evaluation Metrics")

    st.write(
        f"Semantic Similarity: {semantic_score:.2f}%"
    )

    st.write(
        f"Filler Ratio: {filler_ratio_value:.2f}"
    )

    st.write(
        f"Pause Ratio: {pause_ratio:.2f}"
    )

    st.write(
        f"Final Score: {score:.2f}"
    )

    # Grade
    st.subheader("Grade")
    st.success(result_grade)

    # Generate PDF Report
    report_path = generate_report(
        "Voice Comprehension",
        expected_answer,
        student_answer,
        score,
        result_grade
    )

    st.subheader("Report")

    st.success("PDF report generated successfully.")

    with open(report_path, "rb") as pdf_file:
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name="comprehension_report.pdf",
            mime="application/pdf"
        )