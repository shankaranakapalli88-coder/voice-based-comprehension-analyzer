import csv
import os
from datetime import datetime

def save_result(score, grade):
    file_path = "reports/results.csv"

    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Date", "Score", "Grade"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            score,
            grade
        ])