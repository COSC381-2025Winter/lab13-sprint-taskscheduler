import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler.calendar_api import fetch_upcoming_events

def test_fetch_upcoming_events():
    events = fetch_upcoming_events()
    assert isinstance(events, list)
