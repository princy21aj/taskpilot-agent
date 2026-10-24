from types import SimpleNamespace

from agent.loop import run_agent


class FakeCompletions:
    def __init__(self, responses):
        self.responses = iter(responses)

    def create(self, **kwargs):
        return next(self.responses)


def test_run_agent_returns_tool_steps_and_uses_session_notes():
    tool_call = SimpleNamespace(
        id="call-1",
        function=SimpleNamespace(name="save_note", arguments='{"text":"Buy milk"}'),
    )
    responses = [
        SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(tool_calls=[tool_call]))]
        ),
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(tool_calls=None, content="Note saved.")
                )
            ]
        ),
    ]
    client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions(responses))
    )
    history = []
    notes = []
    tool_steps = []

    answer, steps = run_agent(
        "Save a note to buy milk.",
        history,
        notes=notes,
        client=client,
        model="test-model",
        on_tool_step=tool_steps.append,
    )

    assert answer == "Note saved."
    assert steps == ["Using tool: save_note"]
    assert tool_steps == steps
    assert "Buy milk" in notes[0]
    assert [message["role"] for message in history] == ["user", "assistant"]
