import sys
import os
from unittest.mock import patch

import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler import calendar_api

@pytest.fixture(autouse=True)
def disable_webbrowser_open(monkeypatch):
    monkeypatch.setattr("webbrowser.open", lambda *args, **kwargs: True)

@patch("scheduler.calendar_api.fetch_upcoming_events")
def test_fetch_upcoming_events(mock_fetch):
    mock_fetch.return_value = [
        {
            "id": "test-event-1",
            "summary": "Test Event",
            "start": {"dateTime": "2025-04-25T15:00:00"},
            "end": {"dateTime": "2025-04-25T16:00:00"}
        }
    ]
    
    events = calendar_api.fetch_upcoming_events()
    assert isinstance(events, list)
    assert events[0]["summary"] == "Test Event"
