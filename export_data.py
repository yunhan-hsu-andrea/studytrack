import csv

from database import fetch_sessions


def export_sessions_to_csv(filename="studytrack.csv"):
    sessions = fetch_sessions()

    if not sessions:
        print("\nNo study sessions found to export.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "id",
            "subject",
            "study_date",
            "study_time",
            "duration_minutes",
            "mood",
            "focus_level"
        ])

        for session in sessions:
            writer.writerow([
                session["id"],
                session["subject"],
                session["study_date"],
                session["study_time"],
                session["duration_minutes"],
                session["mood"],
                session["focus_level"]
            ])

    print(f"\nSessions exported to {filename}")