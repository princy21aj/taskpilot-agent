# TaskPilot 🧭

An AI agent that decides which tools to use, runs them, and answers using the results. Built with Python and the function calling (tool use) feature of LLMs.

## What it can do
- Get the current weather for any city (Open-Meteo API)
- Look up facts on Wikipedia
- Save and read personal notes
- Chain several tools in one request, e.g. "Check the weather in Dindigul and save a note with the result"

## How it works
1. The user sends a request.
2. The LLM sees the request and the list of tools, and chooses one (or none).
3. My code runs the chosen tool and sends the result back to the LLM.
4. This repeats (maximum 5 steps) until the LLM gives a final answer.

## Tech
Python · OpenAI-compatible API (Groq, works with OpenAI) · Open-Meteo · Wikipedia API · python-dotenv

## Run it
git clone https://github.com/princy21aj/taskpilot-agent
cd taskpilot-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   (then add your API key to .env)
python app.py

## Configuration
The default provider is Groq. In `.env`, set `PROVIDER=groq` and add your
`GROQ_API_KEY`. You can optionally change `GROQ_MODEL`; it defaults to
`openai/gpt-oss-120b`.

To use OpenAI, set `PROVIDER=openai` and add your `OPENAI_API_KEY`. You can
optionally change `OPENAI_MODEL`; it defaults to `gpt-4o-mini`.

Only the API key for the selected provider is used.
To list the selected provider's available models, run `python -m scripts.list_models`.

## Memory
TaskPilot saves the last 10 chat messages in `memory.json` and loads them the
next time it starts. Type `reset` in the app to clear the saved memory.

## Example
You: Check the weather in Dindigul and save a note with the result.
[step 1] tool: get_weather
[step 2] tool: get_current_time
[step 3] tool: save_note
TaskPilot: Dindigul: 29.1 °C, humidity 72%. Note saved.

## Run tests
pytest

## What I learned
Function calling, agent loops, API integration, error handling, short-term memory.

## Next steps
Add more tools (web search, email), long-term memory, and a web interface.