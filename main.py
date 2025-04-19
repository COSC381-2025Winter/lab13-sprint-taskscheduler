# main.py

from scheduler import calendar_api  # ✅ using module-level import for mocking

def main():
    while True:
        print("\n📅 Task Scheduler Menu")
        print("1. Add Event")
        print("2. Delete Event")
        print("3. View Events")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == "1":
            try:
                summary = input("Enter event title: ")
                year = input("Enter year (e.g. 2025): ")
                month = input("Enter month (e.g. 4): ")
                day = input("Enter day (e.g. 25): ")
                start = input("Enter start time (HH:MM): ")
                end = input("Enter end time (HH:MM): ")

                start_time = f"{year}-{month.zfill(2)}-{day.zfill(2)}T{start}:00"
                end_time = f"{year}-{month.zfill(2)}-{day.zfill(2)}T{end}:00"

                event = calendar_api.add_event(summary, start_time, end_time)
                print(f"✅ Event created: {event.get('id')}")
            except Exception as e:
                print(f"❌ Failed to add event: {e}")

        elif choice == "2":
            try:
                event_id = input("Enter event ID to delete: ")
                calendar_api.delete_event(event_id)
                print("🗑️ Event deleted.")
            except Exception as e:
                print(f"❌ Failed to delete event: {e}")

        elif choice == "3":
            events = calendar_api.fetch_upcoming_events()
            if not events:
                print("No upcoming events found.")
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(f"{event['id']} | {start} | {event.get('summary', 'No Title')}")

        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
