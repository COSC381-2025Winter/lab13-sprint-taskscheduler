import logging
from datetime import datetime
from scheduler import calendar_api 

def main():
    userInput = ""
    while userInput != "4":
        print("\n---Calendar App---")
        print("1. Add Event")
        print("2. Delete Event")
        print("3. View Events")
        print("4. Exit")
        userInput = input("Choose From The Following Options: ")
        
        match userInput:
            case "1":
                print("=== Add Event ===")
                summary = input("Enter event title: ")
                
                # Ask for date components separately
                year = input("Enter year (e.g., 2025): ")
                month = input("Enter month (1-12): ")
                day = input("Enter day (1-31): ")
                
                # Format month and day to ensure two digits
                month = month.zfill(2)  # Adds leading zero if needed
                day = day.zfill(2)      # Adds leading zero if needed
                
                # Ask for start and end times directly
                start_time = input("Enter start time (HH:MM, e.g., 10:00): ")
                end_time = input("Enter end time (HH:MM, e.g., 11:00): ")
                
                # Ensure proper time format
                if ":" not in start_time:
                    start_time = f"{start_time}:00"
                if ":" not in end_time:
                    end_time = f"{end_time}:00"
                
                # Construct ISO format datetime strings
                date = f"{year}-{month}-{day}"
                start_datetime = f"{date}T{start_time}:00"
                end_datetime = f"{date}T{end_time}:00"
                
                try:
                    event = calendar_api.add_event(summary, start_datetime, end_datetime)
                    print(f"Event '{summary}' created successfully for {date} from {start_time} to {end_time}")
                except ValueError as e:
                    print(f"Error with date/time format: {e}")
                    print("Please ensure you're using valid date and time values.")
                except Exception as e:
                    print(f"Failed to create event: {e}")
                
            case "2":
                print("=== Delete Event ===")
                events = calendar_api.fetch_upcoming_events()
                
                if not events:
                    print("No upcoming events found.")
                else:
                    print("Upcoming events:")
                    for i, event in enumerate(events, 1):
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(f"{i}. {event['summary']} ({start})")
                    
                    event_index = int(input("Enter the number of the event to delete (0 to cancel): ")) - 1
                    if 0 <= event_index < len(events):
                        try:
                            calendar_api.delete_event(events[event_index]['id'])
                            print("Event deleted successfully.")
                        except Exception as e:
                            print(f"Failed to delete event: {e}")
                    elif event_index == -1:
                        print("Operation cancelled.")
                    else:
                        print("Invalid event number.")
                
            case "3":
                print("=== View Events ===")
                events = calendar_api.fetch_upcoming_events()
                
                if not events:
                    print("No upcoming events found.")
                else:
                    print("Upcoming events:")
                    for i, event in enumerate(events, 1):
                        start = event['start'].get('dateTime', event['start'].get('date'))
                        print(f"{i}. {event['summary']} ({start})")
                        
            case "4":
                print("Goodbye!")
                
            case _:
                print("Invalid Choice")

if __name__ == "__main__":
    main()