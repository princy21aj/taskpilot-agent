import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
MODEL = "openai/gpt-oss-120b"  # use the one that worked for you


# 1. The tool: a normal Python function
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 2. The tool's "menu card" that the LLM reads
TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current date and time on the user's computer.",
        "parameters": {"type": "object", "properties": {}},
    },
}]

messages = [
    {"role": "system", "content": "You are TaskPilot. Use tools when needed."},
    {"role": "user", "content": "What time is it right now?"},
]

# 3. First call: the LLM decides whether it needs a tool
response = client.chat.completions.create(
    model=MODEL, messages=messages, tools=TOOLS
)
msg = response.choices[0].message

if msg.tool_calls:
    messages.append(msg)  # keep the LLM's request in the conversation
    for call in msg.tool_calls:
        print("Tool requested:", call.function.name)
        result = get_current_time()  # YOUR code runs the tool
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": result,
        })
    # 4. Second call: LLM reads the result and answers
    final = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    print(final.choices[0].message.content)
else:
    print(msg.content)