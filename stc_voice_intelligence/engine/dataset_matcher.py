import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets" / "interview_questions.json"


def load_dataset():
    with open(DATASET_PATH, "r") as f:
        data = json.load(f)
    return data["questions"]


def normalize(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str):
    stopwords = {"how", "do", "you", "to", "the", "is", "and", "a", "of"}
    return {
        w for w in normalize(text).replace("?", "").split()
        if w not in stopwords and len(w) > 3
    }


def score_question(transcript: str, q: dict) -> float:
    transcript_n = normalize(transcript)
    score = 0.0

    # 1️⃣ Exact question match
    if normalize(q["question"]) in transcript_n:
        score += 0.6

    # 2️⃣ Anchor hits
    anchor_hits = 0
    for a in q.get("anchors", []):
        if normalize(a) in transcript_n:
            anchor_hits += 1

    if anchor_hits:
        score += min(0.3, anchor_hits * 0.1)

    # 3️⃣ Keyword overlap (NEW)
    q_tokens = tokenize(q["question"])
    t_tokens = tokenize(transcript)

    if q_tokens and t_tokens:
        overlap = q_tokens.intersection(t_tokens)
        if overlap:
            score += min(0.25, len(overlap) * 0.08)

    return round(min(score, 1.0), 2)


def match_intent(transcript: str, threshold: float = 0.30):
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
