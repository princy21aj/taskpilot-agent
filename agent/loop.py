import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from agent.toolkit import TOOLS, TOOL_FUNCTIONS

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = "openai/gpt-oss-120b"  # use the one that worked for you
MAX_STEPS = 5
MEMORY_SIZE = 10  # how many past messages to remember

SYSTEM_PROMPT = (
    "You are TaskPilot, a helpful assistant. Use your tools when needed. "
    "In your final answer, always include the actual data you found "
    "(numbers, facts, saved text), not just a statement that you did the task. "
    "Keep answers short and clear."
)

# Short-term memory: only the user's questions and TaskPilot's final answers
history = []


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