from google import genai
from genres import SKILL_LEVELS

client = genai.Client()
MODEL = "gemini-2.5-flash-preview-04-17"


def get_beat_review(file_path: str, prompt: str) -> str:
    print("Uploading audio to Gemini...")
    audio_file = client.files.upload(file=file_path)

    print("Generating review...")
    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, audio_file],
    )

    client.files.delete(name=audio_file.name)
    return response.text


def follow_up_loop(prompt: str, review: str, skill_level: str) -> None:
    chat = client.chats.create(
        model=MODEL,
        history=[
            {"role": "user", "parts": [{"text": prompt}]},
            {"role": "model", "parts": [{"text": review}]},
        ],
    )

    print("\n" + "─" * 50)
    if skill_level == "beginner":
        print("Got questions about your beat? Ask anything — I'll keep it simple.")
    elif skill_level == "intermediate":
        print("Got follow-up questions? Ask away.")
    else:
        print("Follow-up questions open.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            if skill_level == "beginner":
                print("\nGood luck with the beat — keep making music!")
            else:
                print("\nDone. Go fix that mix.")
            break
        if not question:
            continue

        response = chat.send_message(question)
        print(f"\nAssistant: {response.text}\n")
