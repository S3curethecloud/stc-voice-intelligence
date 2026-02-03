import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets" / "interview_questions.json"


def load_dataset():
    with open(DATASET_PATH, "r") as f:
        data = json.load(f)
    return data["questions"]


def normalize(text: str) -> str:
    return text.lower().strip()


def score_question(transcript: str, q: dict) -> float:
    transcript_n = normalize(transcript)
    score = 0.0

    # 1️⃣ Question text match (strong signal)
    if normalize(q["question"]) in transcript_n:
        score += 0.6

    # 2️⃣ Anchor hits (semantic hints)
    anchor_hits = 0
    for a in q.get("anchors", []):
        if normalize(a) in transcript_n:
            anchor_hits += 1

    if anchor_hits:
        score += min(0.3, anchor_hits * 0.1)

    # 3️⃣ Domain / cloud hints (tie-breaker)
    for hint in [q.get("domain", ""), q.get("cloud", "")]:
        if hint and hint in transcript_n:
            score += 0.05

    return round(min(score, 1.0), 2)


def match_intent(transcript: str, threshold: float = 0.35):
    questions = load_dataset()
    scored = []

    for q in questions:
        s = score_question(transcript, q)
        if s > 0:
            scored.append((s, q))

    if not scored:
        return None

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    best_score, best_match = scored[0]

    if best_score < threshold:
        return None

    # Attach score for display
    best_match["_confidence"] = best_score
    best_match["_alternatives"] = [
        {"question": q["question"], "confidence": s}
        for s, q in scored[1:3]
    ]

    return best_match
