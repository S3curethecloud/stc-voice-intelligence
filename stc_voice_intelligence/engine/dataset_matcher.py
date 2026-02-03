import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets" / "interview_questions.json"


def load_dataset():
    with open(DATASET_PATH, "r") as f:
        data = json.load(f)
    return data["questions"]


def normalize(text: str) -> str:
    return text.lower().strip()


def match_intent(transcript: str):
    transcript_n = normalize(transcript)
    questions = load_dataset()

    for q in questions:
        # match against question text
        if normalize(q["question"]) in transcript_n:
            return q

        # optional: anchor-based fuzzy hint
        for anchor in q.get("anchors", []):
            if normalize(anchor) in transcript_n:
                return q

    return None
