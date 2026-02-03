from stc_voice_intelligence.engine.stt import transcribe
from stc_voice_intelligence.engine.dataset_matcher import match_intent


def run():
    print("🧠 STC Voice Intelligence — Live Mode")
    print("Type interviewer question and press Enter.\n")

    while True:
        transcript = transcribe()

        if transcript.lower() in ["exit", "quit"]:
            print("👋 Exiting.")
            break

        match = match_intent(transcript)

        if not match:
            print("❌ No intent matched.\n")
            continue

        print(f"\n🎯 Intent matched ({match['_confidence'] * 100:.0f}% confidence):")
        print("→", match["question"])
        print("📌 Anchors:")
        for a in match["anchors"]:
            print(" -", a)

        if match.get("_alternatives"):
            print("\n🔁 Alternatives:")
            for alt in match["_alternatives"]:
                print(f"   • {alt['question']} ({alt['confidence'] * 100:.0f}%)")

        print()


# 🔑 THIS IS THE MISSING PIECE
if __name__ == "__main__":
    run()
