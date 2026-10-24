import os
from collections.abc import Mapping

from dotenv import load_dotenv
from openai import OpenAI


def create_client(settings: Mapping[str, str] | None = None):
    if settings is None:
        load_dotenv()
        get_setting = os.getenv
    else:
        get_setting = settings.get

    provider = get_setting("PROVIDER", "groq").strip().lower()

    if provider == "groq":
        model = get_setting("GROQ_MODEL", "openai/gpt-oss-120b")
        api_key = get_setting("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
    elif provider == "openai":
        model = get_setting("OPENAI_MODEL", "gpt-4o-mini")
        api_key = get_setting("OPENAI_API_KEY")
        base_url = None
    else:
        raise ValueError("PROVIDER must be 'groq' or 'openai'.")

    if not api_key:
        raise ValueError(f"{provider.upper()} API key is not configured.")

    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)
    return client, model
