import pytest
from unittest.mock import patch, MagicMock
import main
import calendar_api

@pytest.fixture
def mock_calendar_api(monkeypatch):
    # Fixture to mock calendar_api functions
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
    # Test the exit functionality of the main menu
    inputs = iter(["4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "---Calendar App---" in captured.out
    assert "Goodbye!" in captured.out

def test_main_invalid_choice(monkeypatch, capsys):
    # Mock user selecting invalid option then exit
    inputs = iter(["9", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "Invalid Choice" in captured.out
    assert "Goodbye!" in captured.out

def test_add_event(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs for adding event then exit
    inputs = iter([
        "1",               #
        "Test Meeting",    
        "2025",           
        "4",            
        "25",            
        "10:00",          
        "11:00",           
        "4"                
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "=== Add Event ===" in captured.out
    assert "Event 'Test Meeting' created successfully" in captured.out
    mock_calendar_api["add_event"].assert_called_once_with(
        "Test Meeting", "2025-04-25T10:00:00", "2025-04-25T11:00:00"
    )

def test_view_events(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs for viewing events then exit
    inputs = iter(["3", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "=== View Events ===" in captured.out
    assert "1. Event 1" in captured.out
    assert "2. Event 2" in captured.out
    mock_calendar_api["fetch_upcoming_events"].assert_called_once()

def test_delete_event(monkeypatch, capsys, mock_calendar_api):
    # Mock user inputs for deleting event then exit
    inputs = iter(["2", "1", "4"])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "=== Delete Event ===" in captured.out
    assert "Event deleted successfully" in captured.out
    mock_calendar_api["delete_event"].assert_called_once_with("event1")

def test_no_events_to_view(monkeypatch, capsys):
    # Mock empty events list
    mock_fetch = MagicMock(return_value=[])
    monkeypatch.setattr(calendar_api, "fetch_upcoming_events", mock_fetch)
    
    # Mock user inputs for viewing events then exit
    inputs = iter(["3", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "No upcoming events found" in captured.out

def test_add_event_exception(monkeypatch, capsys):
    # Mock add_event to raise an exception
    def mock_raise_exception(*args):
        raise ValueError("Invalid date format")
    
    monkeypatch.setattr(calendar_api, "add_event", mock_raise_exception)
    
    inputs = iter([
        "1",              
        "Test Meeting",    
        "2025",           
        "4",              
        "25",              
        "10:00",           
        "11:00",           
        "4"               
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    main.main()
    captured = capsys.readouterr()
    
    assert "Error with date/time format" in captured.out