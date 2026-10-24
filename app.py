from agent.loop import run_agent

print("TaskPilot ready. Type 'quit' to exit.")
history = []

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if user_input.lower() == "reset":
        history.clear()
        print("TaskPilot: Chat history cleared.")
        continue
    if not user_input:
        continue
    answer, _ = run_agent(
        user_input,
        history,
        on_tool_step=lambda step: print(f"  {step}"),
    )
    print("TaskPilot:", answer)