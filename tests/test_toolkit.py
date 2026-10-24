from datetime import datetime

from agent import toolkit


def test_save_note_uses_temporary_file(monkeypatch, tmp_path):
    notes_file = tmp_path / "notes.txt"
    monkeypatch.setattr(toolkit, "NOTES_FILE", notes_file)

    assert toolkit.save_note("Buy milk") == "Note saved."
    assert "Buy milk" in notes_file.read_text(encoding="utf-8")


def test_read_notes_uses_temporary_file(monkeypatch, tmp_path):
    notes_file = tmp_path / "notes.txt"
    notes_file.write_text("Test note\n", encoding="utf-8")
    monkeypatch.setattr(toolkit, "NOTES_FILE", notes_file)

    assert toolkit.read_notes() == "Test note\n"


def test_notes_can_be_kept_in_a_session():
    notes = []

    assert toolkit.save_note("Buy milk", notes=notes) == "Note saved."
    assert "Buy milk" in toolkit.read_notes(notes=notes)
    assert toolkit.read_notes(notes=[]) == "No notes yet."


def test_get_current_time_format():
    datetime.strptime(toolkit.get_current_time(), "%Y-%m-%d %H:%M:%S")
