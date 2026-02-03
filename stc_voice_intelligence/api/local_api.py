from stc_voice_intelligence.engine.stt import transcribe
from stc_voice_intelligence.engine.dataset_matcher import match_intent



def run():
    print("🧠 STC Voice Intelligence — Live Mode")
    print("Type interviewer question and press Enter.\n")

    while True:
        transcript = transcribe()

        if transcript.lower() in ["exit", "quit"]:
            break

        match = match_intent(transcript)

        if not match:
            print("❌ No intent matched.\n")
            continue

        print("\n🎯 Intent matched:", match["question"])
        print("📌 Anchors:")
        for a in match["anchors"]:
            print(" -", a)
        print()
