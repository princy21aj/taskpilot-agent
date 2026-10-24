from datetime import datetime
from pathlib import Path
import requests

NOTES_FILE = Path("notes.txt")
HEADERS = {"User-Agent": "TaskPilot/0.1 (student project)"}


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_note(text, notes=None):
    if notes is not None:
        notes.append(f"[{get_current_time()}] {text}")
        return "Note saved."

    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{get_current_time()}] {text}\n")
    return "Note saved."


def read_notes(notes=None):
    if notes is not None:
        return "\n".join(notes) if notes else "No notes yet."

    if not NOTES_FILE.exists():
        return "No notes yet."
    return NOTES_FILE.read_text(encoding="utf-8")


def get_weather(city):
    # Step 1: turn the city name into coordinates
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        headers=HEADERS, timeout=10,
    ).json()
    if not geo.get("results"):
        return f"Could not find a city named {city}."
    place = geo["results"][0]

    # Step 2: ask for the current weather at those coordinates
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        },
        headers=HEADERS, timeout=10,
    ).json()
    cur = weather["current"]
    return (
        f"{place['name']}, {place.get('country', '')}: "
        f"{cur['temperature_2m']} °C, humidity {cur['relative_humidity_2m']}%, "
        f"wind {cur['wind_speed_10m']} km/h"
    )


def search_wikipedia(query):
    data = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query", "format": "json",
            "generator": "search", "gsrsearch": query, "gsrlimit": 3,
            "prop": "extracts", "exintro": 1, "explaintext": 1,
        },
        headers=HEADERS, timeout=10,
    ).json()
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return "No results found."
    results = []
    for page in pages.values():
        results.append(f"{page['title']}: {page.get('extract', '')[:500]}")
    return "\n\n".join(results)


TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "save_note": save_note,
    "read_notes": read_notes,
    "get_weather": get_weather,
    "search_wikipedia": search_wikipedia,
}

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
    {"type": "function", "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "City name, e.g. Chennai"}},
            "required": ["city"],
        },
    }},
    {"type": "function", "function": {
        "name": "search_wikipedia",
        "description": "Look up facts about a person, place, concept, or event on Wikipedia.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string", "description": "What to look up"}},
            "required": ["query"],
        },
    }},
]