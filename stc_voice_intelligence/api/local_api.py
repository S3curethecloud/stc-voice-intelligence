from stc_voice_intelligence.engine.stt import transcribe
from stc_voice_intelligence.engine.dataset_matcher import match_intent
from stc_voice_intelligence.ui.hud import render


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

        # 🔗 HUD is now the single rendering authority
        render(match)


# 🔑 THIS IS THE MISSING PIECE
if __name__ == "__main__":
    run()
