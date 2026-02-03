# STC Voice Intelligence — Dataset Scaling Contract (E6)

STATUS: LOCKED / GOVERNED / AUTHORITATIVE  
SCOPE: interview_questions.json  
OWNER: STC AI / Voice Intelligence  
EFFECTIVE PHASE: E6+

---

## 🎯 Purpose

This contract governs how the interview dataset scales safely to 200–300 questions
without degrading:

- Intent accuracy
- Alias precision
- Confidence scoring
- HUD stability
- STC AI reasoning quality

This file is the **single source of truth** for dataset design decisions.

---

## 1️⃣ Canonical Question Schema (LOCKED)

Every question **MUST** conform to this structure.

```json
{
  "id": "Q###",
  "level": "L1 | L2 | L3 | L4",
  "domain": "string",
  "cloud": "agnostic | aws | azure | gcp",
  "question": "string",
  "intent_aliases": ["optional", "array", "of", "strings"],
  "opening": "string",
  "anchors": ["array", "of", "short", "tokens"],
  "closing": "string"
}
🔒 Schema Rules
id must be unique and zero-padded (Q001, Q045, Q128)

question text must be globally unique

anchors must be nouns or noun phrases, never sentences

intent_aliases are OPTIONAL and added only after a miss

No two questions may share the same alias

2️⃣ Metadata Taxonomy (DO NOT DRIFT)
Levels
Level	Meaning
L1	Fundamentals / definitions
L2	Practitioner / hands-on
L3	Architect / system design
L4	Staff / Principal / leadership
Domains (Controlled Vocabulary)
Only the following domains are allowed:

identity

networking

storage

compute

governance

logging

detection

incident-response

zero-trust

leadership

behavioral

⚠️ New domains require an explicit design decision and contract update.

3️⃣ Alias Strategy (CRITICAL)
When to add aliases
Add intent_aliases only if:

A real user paraphrase failed

Keyword overlap + anchors were insufficient

What aliases SHOULD be
Full phrases users actually say

Lowercase

No punctuation

Natural language (not keywords)

What aliases MUST NOT be
Single words

Generic phrases (e.g. “how do you handle security”)

Overlapping with another question’s meaning

📌 Rule:
If two questions want the same alias → merge or refactor questions.

4️⃣ Batch Growth Rules (MANDATORY)
Questions are never added casually.

Approved batch sizes
✅ 5 questions — ideal

⚠️ 10 questions — maximum

❌ More than 10 — not allowed

After every batch, you MUST run:
jq . stc_voice_intelligence/datasets/interview_questions.json >/dev/null
python -m stc_voice_intelligence.api.local_api
Manual validation required
1 exact question

1 paraphrase

1 vague input

5️⃣ Collision Detection (Design Responsibility)
Before adding a new question, ask:

“Could this be confused with an existing question?”

If yes:

tighten anchors

refine wording

or add it as an alias instead

❌ Do NOT rely on the matcher to resolve ambiguity.
This is a dataset design responsibility.

6️⃣ Scaling Phases (FREEZE BETWEEN PHASES)
Phase A — Core (≈50)
Cloud-agnostic

Identity-first

Behavioral + leadership

No aliases initially

Phase B — Cloud Depth (≈100)
AWS / Azure parity

IAM, networking, governance

Minimal aliases

Phase C — Senior Edge (200–300)
Tradeoffs

Failure scenarios

Executive decision-making

More aliases allowed

Each phase is frozen before the next begins.

7️⃣ Explicit “Do Not Break” List
❌ Do not change existing question text casually
❌ Do not reuse aliases
❌ Do not inflate anchors
❌ Do not lower confidence thresholds to compensate for bad data
❌ Do not add ML to fix dataset design

✅ What This Contract Guarantees
Governed dataset growth

Predictable intent behavior

Stable confidence scoring

Clean STC AI ingestion

Confidence to scale without fear

This is the difference between a tool and a platform.
