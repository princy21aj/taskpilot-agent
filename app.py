from agent.loop import run_agent

print("TaskPilot ready. Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if not user_input:
        continue
    print("TaskPilot:", run_agent(user_input))