import logging
from datetime import datetime
from scheduler import calendar_api  # ✅ using module-level import for mocking

# Set up basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    while True:
        print("\n📅 Task Scheduler Menu")
        print("1. Add Event")
        print("2. Delete Event")
        print("3. View Events")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            try:
                # Get event details from the user
                summary = input("Enter event title: ").strip()
                year = input("Enter year (e.g. 2025): ").strip()
                month = input("Enter month (e.g. 04): ").strip()
                day = input("Enter day (e.g. 25): ").strip()

                # Validate date
                try:
                    datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                except ValueError:
                    print("❌ Invalid date format. Please use YYYY-MM-DD.")
                    continue

                start = input("Enter start time (HH:MM 24-hour format): ").strip()
                end = input("Enter end time (HH:MM 24-hour format): ").strip()

                # Validate time format
                try:
                    datetime.strptime(start, "%H:%M")
                    datetime.strptime(end, "%H:%M")
                except ValueError:
                    print("❌ Invalid time format. Please use HH:MM.")
                    continue

                # Format start and end times
                start_time = f"{year}-{month.zfill(2)}-{day.zfill(2)}T{start}:00"
                end_time = f"{year}-{month.zfill(2)}-{day.zfill(2)}T{end}:00"

                # Add event to calendar
                event = calendar_api.add_event(summary, start_time, end_time)
                logging.info(f"Event created: {event.get('id')}")
                print(f"✅ Event created: {event.get('id')}")
            except Exception as e:
                logging.error(f"Failed to add event: {e}")
                print(f"❌ Failed to add event: {e}")

        elif choice == "2":
            try:
                event_id = input("Enter event ID to delete: ")
                if not event_id:
                    print("❌ Invalid event ID. Please enter a valid ID.")
                    continue

                calendar_api.delete_event(event_id)
                logging.info(f"Event {event_id} deleted.")
                print("🗑️ Event deleted.")
            except Exception as e:
                logging.error(f"Failed to delete event: {e}")
                print(f"❌ Failed to delete event: {e}")

        elif choice == "3":
            try:
                events = calendar_api.fetch_upcoming_events()
                if not events:
                    print("No upcoming events found.")
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    start = datetime.fromisoformat(start).strftime("%Y-%m-%d %H:%M")
                    summary = event.get("summary", "No Title")
                    print(f"{event['id']} | {start} | {summary}")
            except Exception as e:
                logging.error(f"Failed to fetch events: {e}")
                print(f"❌ Failed to fetch events: {e}")

        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
