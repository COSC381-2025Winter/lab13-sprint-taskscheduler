import pytest
from unittest.mock import MagicMock
import sys
import os

import main  # 
from scheduler import calendar_api 

@pytest.fixture
def mock_calendar_api(monkeypatch):
    # Create mock functions
    mock_add = MagicMock(return_value={"id": "test123", "summary": "Test Event"})
    mock_fetch = MagicMock(return_value=[
        {"id": "event1", "summary": "Event 1", "start": {"dateTime": "2025-04-25T10:00:00"}},
        {"id": "event2", "summary": "Event 2", "start": {"dateTime": "2025-04-26T11:00:00"}}
    ])
    mock_delete = MagicMock()
    
    # Apply mocks to the calendar_api module
    monkeypatch.setattr("scheduler.calendar_api.add_event", mock_add)
    monkeypatch.setattr("scheduler.calendar_api.fetch_upcoming_events", mock_fetch)
    monkeypatch.setattr("scheduler.calendar_api.delete_event", mock_delete)
    
    return {
        "add_event": mock_add,
        "fetch_upcoming_events": mock_fetch,
        "delete_event": mock_delete
    }

def test_main_exit(monkeypatch, capsys):
    # Mock user input to select exit (option 4)
    inputs = iter(["4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "---Calendar App---" in captured.out
    assert "Goodbye!" in captured.out

def test_main_invalid_choice(monkeypatch, capsys):
    # Mock user inputs - first invalid option, then exit
    inputs = iter(["9", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "Invalid Choice" in captured.out
    assert "Goodbye!" in captured.out

def test_add_event(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs for adding an event
    inputs = iter([
        "1",              # Select Add Event
        "Test Meeting",   # Event title
        "2025",           # Year
        "4",              # Month
        "25",             # Day
        "10:00",          # Start time
        "11:00",          # End time
        "4"               # Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "=== Add Event ===" in captured.out
    assert "Event 'Test Meeting' created successfully" in captured.out
    
    # Verify add_event was called with correct parameters
    mock_calendar_api["add_event"].assert_called_once_with(
        "Test Meeting", "2025-04-25T10:00:00", "2025-04-25T11:00:00"
    )

def test_view_events(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs - view events then exit
    inputs = iter(["3", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "=== View Events ===" in captured.out
    assert "Upcoming events:" in captured.out
    
    # Verify fetch_upcoming_events was called
    mock_calendar_api["fetch_upcoming_events"].assert_called_once()

def test_delete_event(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs - delete events, select first event, then exit
    inputs = iter(["2", "1", "4"])  # Changed "event1" to "1" to match the expected numeric input
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "=== Delete Event ===" in captured.out
    assert "Event deleted successfully" in captured.out
    
    # Verify delete_event was called with correct event ID
    mock_calendar_api["delete_event"].assert_called_once_with("event1")

def test_add_event_exception(monkeypatch, capsys, mock_calendar_api):
    # Mock add_event to raise an exception
    mock_add = MagicMock(side_effect=ValueError("Invalid date format"))
    monkeypatch.setattr("scheduler.calendar_api.add_event", mock_add)
    
    # Mock user inputs
    inputs = iter([
        "1",              # Select Add Event
        "Test Meeting",   # Event title
        "2025",           # Year
        "4",              # Month
        "25",             # Day
        "10:00",          # Start time
        "11:00",          # End time
        "4"               # Exit
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    
    captured = capsys.readouterr()
    assert "Error with date/time format" in captured.out
    assert "Invalid date format" in captured.out
