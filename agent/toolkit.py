from datetime import datetime
from pathlib import Path

NOTES_FILE = Path("notes.txt")


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_note(text):
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{get_current_time()}] {text}\n")
    return "Note saved."


def read_notes():
    if not NOTES_FILE.exists():
        return "No notes yet."
    return NOTES_FILE.read_text(encoding="utf-8")


# Name -> function, so the loop can find the right one
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "save_note": save_note,
    "read_notes": read_notes,
}

# The "menu cards" the LLM reads
TOOLS = [
    {"type": "function", "function": {
        "name": "get_current_time",
        "description": "Get the current date and time.",
        "parameters": {"type": "object", "properties": {}},
    }},
    {"type": "function", "function": {
        "name": "save_note",
        "description": "Save a short note for the user to a file.",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "The note text"}},
            "required": ["text"],
        },
    }},
    {"type": "function", "function": {
        "name": "read_notes",
        "description": "Read all notes the user has saved before.",
        "parameters": {"type": "object", "properties": {}},
    }},
]