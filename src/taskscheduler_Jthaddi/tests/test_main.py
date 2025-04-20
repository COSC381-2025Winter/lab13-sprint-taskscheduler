import pytest
from unittest.mock import MagicMock
import main
from scheduler import calendar_api
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def mock_calendar_api(monkeypatch):
    mock_add_event = MagicMock(return_value={"id": "test_id", "summary": "Test Event"})
    mock_fetch_events = MagicMock(return_value=[
        {"id": "event1", "summary": "Event 1", "start": {"dateTime": "2025-04-25T10:00:00"}},
        {"id": "event2", "summary": "Event 2", "start": {"dateTime": "2025-04-26T11:00:00"}}
    ])
    mock_delete_event = MagicMock()

    monkeypatch.setattr(calendar_api, "add_event", mock_add_event)
    monkeypatch.setattr(calendar_api, "fetch_upcoming_events", mock_fetch_events)
    monkeypatch.setattr(calendar_api, "delete_event", mock_delete_event)

    return {
        "add_event": mock_add_event,
        "fetch_upcoming_events": mock_fetch_events,
        "delete_event": mock_delete_event
    }

def test_main_exit(monkeypatch, capsys):
    inputs = iter(["4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "📅 Task Scheduler Menu" in captured.out
    assert "👋 Exiting..." in captured.out

def test_main_invalid_choice(monkeypatch, capsys):
    inputs = iter(["9", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "❌ Invalid option. Try again." in captured.out
    assert "👋 Exiting..." in captured.out

def test_add_event(monkeypatch, capsys, mock_calendar_api):
    inputs = iter(["1", "Test Meeting", "2025", "4", "25", "10:00", "11:00", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "✅ Event created" in captured.out
    mock_calendar_api["add_event"].assert_called_once_with(
        "Test Meeting", "2025-04-25T10:00:00", "2025-04-25T11:00:00"
    )

def test_view_events(monkeypatch, capsys, mock_calendar_api):
    inputs = iter(["3", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "Event 1" in captured.out
    assert "Event 2" in captured.out
    mock_calendar_api["fetch_upcoming_events"].assert_called_once()

def test_delete_event(monkeypatch, capsys, mock_calendar_api):
    inputs = iter(["2", "event1", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "🗑️ Event deleted." in captured.out
    mock_calendar_api["delete_event"].assert_called_once_with("event1")

def test_no_events_to_view(monkeypatch, capsys, mock_calendar_api):
    mock_calendar_api["fetch_upcoming_events"].return_value = []

    inputs = iter(["3", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "No upcoming events found." in captured.out

def test_add_event_exception(monkeypatch, capsys, mock_calendar_api):
    def mock_raise_exception(*args):
        raise ValueError("Invalid date format")

    monkeypatch.setattr(calendar_api, "add_event", mock_raise_exception)

    inputs = iter(["1", "Test Meeting", "2025", "4", "25", "10:00", "11:00", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    main.main()
    captured = capsys.readouterr()

    assert "❌ Failed to add event" in captured.out
