FILLERS = [
    "um",
    "uh",
    "like",
    "you know",
    "actually",
    "basically"
]

def filler_ratio(text):
    words = text.lower().split()

    filler_count = sum(
        words.count(f)
        for f in FILLERS
    )

    return filler_count / max(len(words), 1)


def final_score(
        semantic_score,
        filler_ratio_value,
        pause_ratio):

    score = (
        semantic_score * 0.7
        + (1 - filler_ratio_value) * 15
        + (1 - pause_ratio) * 15
    )

    return round(score, 2)


def classify(score):

    if score >= 80:
        return "Strong"

    elif score >= 60:
        return "Moderate"

    return "Poor"