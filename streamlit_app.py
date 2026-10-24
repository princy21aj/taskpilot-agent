import streamlit as st

from agent.config import create_client
from agent.loop import MAX_HISTORY_MESSAGES, run_agent
from agent.toolkit import TOOLS

st.set_page_config(page_title="TaskPilot", page_icon="🧭")
st.title("TaskPilot 🧭")
st.caption("Ask a question, and TaskPilot will use its tools to find an answer.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "notes" not in st.session_state:
    st.session_state.notes = []

examples = [
    "What time is it?",
    "What is the weather in Chennai?",
    "Search Wikipedia for the Python programming language.",
    "Save a note to buy groceries.",
]

with st.sidebar:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.chat_history = []

    st.subheader("Available tools")
    for tool in TOOLS:
        st.write(f"- {tool['function']['name']}")

    st.subheader("Try an example")
    selected_prompt = None
    for index, example in enumerate(examples):
        if st.button(example, key=f"example_{index}", use_container_width=True):
            selected_prompt = example

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if len(st.session_state.chat_history) >= MAX_HISTORY_MESSAGES:
    st.info("You've reached the 20-message chat limit. Clear the chat to start a new conversation.")
    prompt = None
else:
    prompt = selected_prompt or st.chat_input("Ask TaskPilot...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    history_size = len(st.session_state.chat_history)
    tool_steps = []
    with st.status("TaskPilot is working...", expanded=True) as status:
        try:
            client, model = create_client(st.secrets)
            answer, tool_steps = run_agent(
                prompt,
                st.session_state.chat_history,
                notes=st.session_state.notes,
                client=client,
                model=model,
                on_tool_step=status.write,
            )
            status.update(label="TaskPilot is ready", state="complete", expanded=False)
        except Exception as error:
            status.update(label="TaskPilot couldn't complete that request", state="error")
            answer = f"Sorry, something went wrong: {error}"

    with st.chat_message("assistant"):
        if tool_steps:
            with st.expander("Tools used"):
                for tool_step in tool_steps:
                    st.write(tool_step)
        st.markdown(answer)

    if len(st.session_state.chat_history) == history_size:
        st.session_state.chat_history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ])
        del st.session_state.chat_history[:-MAX_HISTORY_MESSAGES]
