import speech_recognition as sr
from ics import Calendar, Event
from datetime import datetime, timedelta

# 🎤 Convert voice to text
def voice_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Speak your idea...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("\n📝 You said:", text)
        return text
    except:
        print("❌ Could not understand audio")
        return ""


# 🧠 Extract tasks from text
def extract_tasks(text):
    tasks = []
    keywords = ["do", "finish", "complete", "start", "schedule", "call", "buy", "meet"]

    sentences = text.split(".")

    for sentence in sentences:
        for word in keywords:
            if word in sentence.lower():
                tasks.append(sentence.strip())
                break

    return tasks


# 📅 Create calendar file
def create_calendar(tasks):
    c = Calendar()

    for i, task in enumerate(tasks):
        e = Event()
        e.name = task
        e.begin = datetime.now() + timedelta(hours=i+1)
        e.duration = timedelta(hours=1)
        c.events.add(e)

    with open("tasks.ics", "w") as f:
        f.writelines(c)

    print("\n📅 Calendar file created: tasks.ics")
    print("👉 Import this file into Google Calendar")


# 🔄 Main function
def main():
    print("🚀 Voice Note → Action App\n")

    text = voice_to_text()

    if not text:
        return

    tasks = extract_tasks(text)

    if not tasks:
        print("\n🤔 No actionable tasks found")
        return

    print("\n✅ Extracted Tasks:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")

    create_calendar(tasks)


if __name__ == "__main__":
    main()
