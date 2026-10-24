from agent.loop import clear_memory, run_agent

print("TaskPilot ready. Type 'quit' to exit.")
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if user_input.lower() == "reset":
        clear_memory()
        print("TaskPilot: Memory cleared.")
        continue
    if not user_input:
        continue
    print("TaskPilot:", run_agent(user_input))