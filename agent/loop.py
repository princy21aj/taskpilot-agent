import json
from pathlib import Path

from agent.config import MODEL, PROVIDER, client
from agent.toolkit import TOOLS, TOOL_FUNCTIONS

MAX_STEPS = 5
MEMORY_SIZE = 10  # how many past messages to remember
MEMORY_FILE = Path("memory.json")

SYSTEM_PROMPT = (
    "You are TaskPilot, a helpful assistant. Use your tools when needed. "
    "In your final answer, always include the actual data you found "
    "(numbers, facts, saved text), not just a statement that you did the task. "
    "Keep answers short and clear."
)

# Remember only the user's questions and TaskPilot's final answers.
if MEMORY_FILE.exists():
    history = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
else:
    history = []

print(f"Using provider: {PROVIDER} (model: {MODEL})")


def save_memory():
    MEMORY_FILE.write_text(
        json.dumps(history[-MEMORY_SIZE:], indent=2) + "\n",
        encoding="utf-8",
    )


def clear_memory():
    history.clear()
    save_memory()


def run_agent(user_message):
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history[-MEMORY_SIZE:]
        + [{"role": "user", "content": user_message}]
    )

    for step in range(1, MAX_STEPS + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = response.choices[0].message

        if not msg.tool_calls:  # no tool needed -> final answer
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": msg.content})
            history[:] = history[-MEMORY_SIZE:]
            save_memory()
            return msg.content

        messages.append(msg)
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            print(f"  [step {step}] tool: {name} {args}")
            try:
                result = TOOL_FUNCTIONS[name](**args)
            except Exception as e:
                result = f"Error: {e}"
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
    return "Stopped: reached the maximum number of steps."