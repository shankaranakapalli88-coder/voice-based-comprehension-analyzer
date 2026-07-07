from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(
    question,
    expected_answer,
    student_answer,
    score,
    grade
):
    report_path = "reports/comprehension_report.pdf"

    doc = SimpleDocTemplate(report_path)

    styles = getSampleStyleSheet()

    content = [

        Paragraph(
            "VOICE BASED COMPREHENSION REPORT",
            styles["Title"]
        ),

        Spacer(1, 12),

        Paragraph(
            f"<b>Question:</b> {question}",
            styles["BodyText"]
        ),

        Paragraph(
            f"<b>Expected Answer:</b> {expected_answer}",
            styles["BodyText"]
        ),

        Paragraph(
            f"<b>Student Answer:</b> {student_answer}",
            styles["BodyText"]
        ),

        Paragraph(
            f"<b>Score:</b> {score:.2f}%",
            styles["BodyText"]
        ),

        Paragraph(
            f"<b>Grade:</b> {grade}",
            styles["BodyText"]
        ),
    ]

    doc.build(content)

    return report_path