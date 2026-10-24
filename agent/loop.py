import json

from agent.config import create_client
from agent.toolkit import TOOLS, TOOL_FUNCTIONS, read_notes, save_note

MAX_STEPS = 5
MAX_HISTORY_MESSAGES = 20

SYSTEM_PROMPT = (
    "You are TaskPilot, a helpful assistant. Use your tools when needed. "
    "In your final answer, always include the actual data you found "
    "(numbers, facts, saved text), not just a statement that you did the task. "
    "Keep answers short and clear."
)


def run_agent(
    user_message,
    history,
    notes=None,
    client=None,
    model=None,
    on_tool_step=None,
):
    if client is None:
        client, configured_model = create_client()
        model = model or configured_model

    tool_functions = TOOL_FUNCTIONS.copy()
    if notes is not None:
        tool_functions["save_note"] = lambda text: save_note(text, notes=notes)
        tool_functions["read_notes"] = lambda: read_notes(notes=notes)

    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history[-MAX_HISTORY_MESSAGES:]
        + [{"role": "user", "content": user_message}]
    )
    tool_steps = []

    for step in range(1, MAX_STEPS + 1):
        response = client.chat.completions.create(
            model=model, messages=messages, tools=TOOLS
        )
        msg = response.choices[0].message

        if not msg.tool_calls:  # no tool needed -> final answer
            answer = msg.content or ""
            history.extend([
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": answer},
            ])
            del history[:-MAX_HISTORY_MESSAGES]
            return answer, tool_steps

        messages.append(msg)
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            tool_step = f"Using tool: {name}"
            tool_steps.append(tool_step)
            if on_tool_step:
                on_tool_step(tool_step)
            try:
                result = tool_functions[name](**args)
            except Exception as e:
                result = f"Error: {e}"
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
    return "Stopped: reached the maximum number of steps.", tool_steps