import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "groq":
    MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    API_KEY = os.getenv("GROQ_API_KEY")
    BASE_URL = "https://api.groq.com/openai/v1"
elif PROVIDER == "openai":
    MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = None
else:
    raise ValueError("PROVIDER must be 'groq' or 'openai'.")

if BASE_URL:
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
else:
    client = OpenAI(api_key=API_KEY)
