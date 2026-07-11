import streamlit as st
import pandas as pd
import librosa
import librosa.display
import matplotlib.pyplot as plt

from save_results import save_result
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

    # Save uploaded audio
    audio_path = f"uploads/{uploaded_file.name}"

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Audio uploaded successfully.")

    # Audio Playback
    st.subheader("Audio Playback")
    st.audio(audio_path)

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

    # Save result
    save_result(score, result_grade)

    # Display Answers
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reference Answer")
        st.write(expected_answer)

    with col2:
        st.subheader("Student Answer")
        st.write(student_answer)

    # Metrics
    st.subheader("Evaluation Metrics")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Semantic Similarity",
            f"{semantic_score:.2f}%"
        )

    with m2:
        st.metric(
            "Final Score",
            f"{score:.2f}"
        )

    with m3:
        st.metric(
            "Grade",
            result_grade
        )

    st.write(
        f"Filler Ratio: {filler_ratio_value:.2f}"
    )

    st.write(
        f"Pause Ratio: {pause_ratio:.2f}"
    )

    # Progress Bar
    st.subheader("Understanding Score")

    progress_value = min(
        max(int(score), 0),
        100
    )

    st.progress(progress_value)

    # Result
    st.subheader("Result")
    st.success(result_grade)

    # Generate PDF
    report_path = generate_report(
        "Voice Comprehension",
        expected_answer,
        student_answer,
        score,
        result_grade
    )

    # Download PDF
    st.subheader("Report")

    with open(report_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name="comprehension_report.pdf",
        mime="application/pdf"
    )

# ==================================
# Evaluation History
# ==================================

st.subheader("Evaluation History")

try:
    history = pd.read_csv(
        "reports/results.csv"
    )

    st.dataframe(
        history,
        use_container_width=True
    )

      # Download CSV History

with open("reports/results.csv", "rb") as file:
    csv_bytes = file.read()

st.download_button(
    label="📥 Download Evaluation History",
    data=csv_bytes,
    file_name="evaluation_history.csv",
    mime="text/csv"
)

    # ==================================
    # Score Trend
    # ==================================

    st.subheader("Score Trend")

    scores = pd.to_numeric(
        history["Score"],
        errors="coerce"
    )

    scores = scores.dropna()

    if len(scores) > 0:

        fig, ax = plt.subplots()

        ax.plot(
            range(1, len(scores) + 1),
            scores.tolist(),
            marker="o"
        )

        ax.set_xlabel(
            "Evaluation Number"
        )

        ax.set_ylabel(
            "Score"
        )

        ax.set_title(
            "Performance Trend"
        )

        st.pyplot(fig)

    else:
        st.warning(
            "No valid scores available."
        )

except FileNotFoundError:

    st.info(
        "No evaluation history available."
    )

except Exception as e:

    st.error(
        f"History Error: {e}"
    )