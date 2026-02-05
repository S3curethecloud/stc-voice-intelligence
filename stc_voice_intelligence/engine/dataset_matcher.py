import json
from pathlib import Path

DATASET_PATH = Path(__file__).parent.parent / "datasets" / "interview_questions.json"


def load_dataset():
    with open(DATASET_PATH) as f:
        data = json.load(f)

    # Dataset is a pure list (E6 normalized)
    if isinstance(data, list):
        return data

    # Backward compatibility (legacy wrapped format)
    if isinstance(data, dict) and "questions" in data:
        return data["questions"]

    raise ValueError("Unsupported dataset format")


def normalize(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str):
    stopwords = {"how", "do", "you", "to", "the", "is", "and", "a", "of"}
    tokens = set()

    for w in normalize(text).replace("?", "").split():
        if w in stopwords or len(w) <= 3:
            continue
        tokens.add(w)

    return tokens


def score_question(transcript: str, q: dict) -> float:
    transcript_n = normalize(transcript)
    score = 0.0

    # 1️⃣ Exact question match
    if normalize(q["question"]) in transcript_n:
        score += 0.6

    # 1️⃣b Intent alias match (STRONG)
    for alias in q.get("intent_aliases", []):
        alias_n = normalize(alias)
        if alias_n in transcript_n:
            score += 0.7  # deliberately strong

    # 2️⃣ Anchor hits
    anchor_hits = 0
    for a in q.get("anchors", []):
        if normalize(a) in transcript_n:
            anchor_hits += 1

    if anchor_hits:
        score += min(0.3, anchor_hits * 0.1)

    # 3️⃣ Keyword overlap
    q_tokens = tokenize(q["question"])
    t_tokens = tokenize(transcript)

    overlap = q_tokens.intersection(t_tokens)
    if overlap:
        score += min(0.25, len(overlap) * 0.08)

    return round(min(score, 1.0), 2)


def match_intent(transcript, threshold=0.7):
    questions = load_dataset()
    scored = []

    for q in questions:
        score = score_question(transcript, q)
        scored.append((score, q))

    if not scored:
        return None

    scored.sort(key=lambda x: x[0], reverse=True)

    best_score, best_match = scored[0]

    # 🔒 Fallback: closest intent (read-only, no execution)
    if best_score < threshold:
        return {
            "_mode": "closest_intent",
            "_confidence": best_score,
            "question": best_match["question"],
            "anchors": best_match.get("anchors", []),
            "_note": "No exact intent matched; showing closest governed intent"
        }

    # ✅ Exact match
    best_match["_confidence"] = best_score
    best_match["_alternatives"] = [
        {"question": q["question"], "confidence": s}
        for s, q in scored[1:3]
    ]

    return best_match
