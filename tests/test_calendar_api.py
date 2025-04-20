import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from scheduler.calendar_api import fetch_upcoming_events

@pytest.fixture(autouse=True)
def disable_webbrowser_open(monkeypatch):
    monkeypatch.setattr("webbrowser.open", lambda *args, **kwargs: True)

def test_fetch_upcoming_events():
    events = fetch_upcoming_events()
    assert isinstance(events, list)
