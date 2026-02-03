import os
import shutil


def clear():
    os.system("clear")


def render(match: dict):
    clear()

    width = shutil.get_terminal_size((80, 20)).columns
    line = "─" * width

    question = match["question"]
    confidence = int(match["_confidence"] * 100)
    anchors = match["anchors"]

    print(line)
    print(f"🎯 QUESTION ({confidence}%)".center(width))
    print(question.center(width))
    print("\n📌 ANCHORS".center(width))
    for a in anchors:
        print(f"• {a}".center(width))
    print(line)
