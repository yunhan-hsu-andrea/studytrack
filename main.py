from datetime import datetime

from analyze import (
    total_study_time,
    average_focus,
    most_studied_subject,
    study_time_by_subject,
    session_count_by_subject,
    average_session_duration
)

from database import (
    init_db,
    add_study_session,
    fetch_sessions,
    get_session_by_id,
    update_study_session,
    delete_study_session
)

from export_data import export_sessions_to_csv

# Subject options for study sessions
SUBJECT_OPTIONS = [
   "Math",
    "English",
    "Biology",
    "Chemistry",
    "Physics",
    "History",
    "Geography",
    "Computer Science",
    "Foreign Language",
    "Art",
    "Music",
    "Physical Education",
    "Health",
    "Other"
]


# Mood options for study sessions
MOOD_OPTIONS = [
    "Focused",
    "Motivated",
    "Calm",
    "Productive",
    "Tired",
    "Distracted",
    "Stressed",
    "Bored",
    "Confident",
    "Frustrated"
]


# Focus scale for study sessions
FOCUS_LEVELS = {
    1: "Very Distracted",
    2: "Distracted",
    3: "Low Focus",
    4: "Slightly Focused",
    5: "Average Focus",
    6: "Focused",
    7: "Highly Focused",
    8: "Deep Focus",
    9: "Intense Focus",
    10: "Flow State"
}


def show_menu():
    print("\n=== Welcome to StudyTrack ===")
    print("Track your study sessions and monitor your progress.\n")

    print("1. Add study session")
    print("2. View all sessions")
    print("3. Find session by ID")
    print("4. View analytics")
    print("5. Edit a session")
    print("6. Delete a session")
    print("7. Export to CSV")
    print("8. Exit")


# Helper functions
def get_nonempty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty. Please try again.")


def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt).strip())

            if min_value is not None and value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}.")
                continue

            if max_value is not None and value > max_value:
                print(f"Please enter a number less than or equal to {max_value}.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def pick_session():
    sessions = fetch_sessions()

    if not sessions:
        print("\nNo study sessions found.")
        return None, None

    show_sessions()

    session_id = ask_session_id()
    session = get_session_by_id(session_id)

    if not session:
        print("No session found with that ID.")
        return None, None

    return session_id, session


# Get date
def ask_date():
    while True:
        value = input("Study date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value

        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


# Get time
def ask_time():
    while True:
        value = input("Start time in 24-hour format HH:MM: ").strip()

        try:
            datetime.strptime(value, "%H:%M")
            return value

        except ValueError:
            print("Please enter a valid time in 24-hour format.")


# Get duration
def ask_duration():
    return get_int_input(
        "Duration in minutes: ",
        min_value=1
    )


# Get session ID to search for the specific entry later
def ask_session_id():
    return get_int_input(
        "Enter the session ID: ",
        min_value=1
    )


def ask_subject():
    print("\nSubject Options:")

    for index, subject in enumerate(SUBJECT_OPTIONS, start=1):
        print(f"{index}. {subject}")

    choice = get_int_input(
        "Choose a subject: ",
        min_value=1,
        max_value=len(SUBJECT_OPTIONS)
    )

    selected = SUBJECT_OPTIONS[choice - 1]

    if selected == "Other":
        return get_nonempty_input("Enter custom subject: ")

    return selected


def ask_mood():
    print("\nMood Options:")

    for index, mood in enumerate(MOOD_OPTIONS, start=1):
        print(f"{index}. {mood}")

    choice = get_int_input(
        "Choose a mood: ",
        min_value=1,
        max_value=len(MOOD_OPTIONS)
    )

    return MOOD_OPTIONS[choice - 1]


def ask_focus_level():
    print("\nFocus Levels:")

    for level, description in FOCUS_LEVELS.items():
        print(f"{level}. {description}")

    return get_int_input(
        "Choose a focus level (1-10): ",
        min_value=1,
        max_value=10
    )


# Update/ Edit subject
def edit_subject(current_value):
    print("\nSubject Options:")
    print("0. Keep current subject")

    for index, subject in enumerate(SUBJECT_OPTIONS, start=1):
        print(f"{index}. {subject}")

    choice = get_int_input(
        f"Choose a subject [current: {current_value}]: ",
        min_value=0,
        max_value=len(SUBJECT_OPTIONS)
    )

    if choice == 0:
        return current_value

    selected = SUBJECT_OPTIONS[choice - 1]

    if selected == "Other":
        return get_nonempty_input("Enter custom subject: ")

    return selected


# Update/ Edit date
def edit_date(current_value):
    while True:
        value = input(
            f"Study date (YYYY-MM-DD) [{current_value}]: "
        ).strip()

        if not value:
            return current_value

        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value

        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")


# Update/ Edit time
def edit_time(current_value):
    while True:
        value = input(
            f"Study time (HH:MM) [{current_value}]: "
        ).strip()

        if not value:
            return current_value

        try:
            datetime.strptime(value, "%H:%M")
            return value

        except ValueError:
            print("Please enter a valid time in HH:MM format.")


# Update/ Edit duration
def edit_duration(current_value):
    while True:
        value = input(
            f"Duration in minutes [{current_value}]: "
        ).strip()

        if not value:
            return current_value

        try:
            number = int(value)

            if number <= 0:
                print("Duration must be greater than 0.")
                continue

            return number

        except ValueError:
            print("Please enter a valid number.")


# Update/ Edit mood
def edit_mood(current_value):
    print("\nMood Options:")
    print("0. Keep current mood")

    for index, mood in enumerate(MOOD_OPTIONS, start=1):
        print(f"{index}. {mood}")

    choice = get_int_input(
        f"Choose a mood [current: {current_value}]: ",
        min_value=0,
        max_value=len(MOOD_OPTIONS)
    )

    if choice == 0:
        return current_value

    return MOOD_OPTIONS[choice - 1]


# Update/ Edit focus level
def edit_focus_level(current_value):
    current_description = FOCUS_LEVELS.get(
        current_value,
        "Unknown"
    )

    print("\nFocus Levels:")
    print("0. Keep current focus level")

    for level, description in FOCUS_LEVELS.items():
        print(f"{level}. {description}")

    choice = get_int_input(
        f"Choose a focus level [current: {current_value} - {current_description}]: ",
        min_value=0,
        max_value=10
    )

    if choice == 0:
        return current_value

    return choice


def print_session(session):
    print(
        f"ID: {session['id']}\n"
        f"Subject: {session['subject']}\n"
        f"Study Date: {session['study_date']}\n"
        f"Study Time: {session['study_time']}\n"
        f"Duration: {session['duration_minutes']} minutes\n"
        f"Mood: {session['mood']}\n"
        f"Focus Level: {session['focus_level']} - "
        f"{FOCUS_LEVELS.get(session['focus_level'], 'Unknown')}\n"
    )


def add_new_session():
    print("\nEnter a new study session:\n")

    subject = ask_subject()
    study_date = ask_date()
    study_time = ask_time()
    duration = ask_duration()
    mood = ask_mood()
    focus_level = ask_focus_level()

    # Save the study session to the SQLite database
    add_study_session(
        subject,
        study_date,
        study_time,
        duration,
        mood,
        focus_level
    )

    print("\nYour study session was saved successfully.")


# Display all saved sessions
def show_sessions():
    sessions = fetch_sessions()

    if not sessions:
        print("\nYou haven't added any study sessions yet.")
        return

    print("\n=== All Study Sessions ===")

    for session in sessions:
        print_session(session)
        print("-" * 30)


def search_session():
    session_id = ask_session_id()

    session = get_session_by_id(session_id)

    if not session:
        print("No session found with that ID.")
        return

    print("\n=== Study Session ===")
    print_session(session)


# Study statistics from all saved sessions
def view_analytics():
    sessions = fetch_sessions()

    if not sessions:
        print("\nNo study sessions found yet.")
        return

    total_minutes = total_study_time(sessions)
    mean_focus = average_focus(sessions)
    top_subject = most_studied_subject(sessions)
    subject_time = study_time_by_subject(sessions)
    subject_counts = session_count_by_subject(sessions)
    average_duration = average_session_duration(sessions)

    print("\n=== Study Analytics ===")
    print(f"You've studied for {total_minutes} minutes in total.")
    print(f"You've completed {len(sessions)} study sessions.")
    print(f"Average session duration: {average_duration} minutes.")
    print(f"Your average focus level is {mean_focus}.")
    print(f"Your most studied subject is: {top_subject or 'None yet'}")

    print("\nStudy time by subject:")
    for subject, minutes in sorted(subject_time.items(), key=lambda item: item[1], reverse=True):
        print(f"- {subject}: {minutes} minutes")

    print("\nSession count by subject:")
    for subject, count in sorted(subject_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"- {subject}: {count} sessions")


def edit_session():
    session_id, session = pick_session()

    if not session:
        return

    subject = session["subject"]
    study_date = session["study_date"]
    study_time = session["study_time"]
    duration = session["duration_minutes"]
    mood = session["mood"]
    focus_level = session["focus_level"]

    while True:
        print("\n=== Edit Session ===")
        print("1. Edit subject")
        print("2. Edit study date")
        print("3. Edit study time")
        print("4. Edit duration")
        print("5. Edit mood")
        print("6. Edit focus level")
        print("7. Save and exit")

        choice = get_int_input(
            "Choose an option: ",
            min_value=1,
            max_value=7
        )

        if choice == 1:
            subject = edit_subject(subject)
            print(f"Subject updated to: {subject}")

        elif choice == 2:
            study_date = edit_date(study_date)
            print(f"Study date updated to: {study_date}")

        elif choice == 3:
            study_time = edit_time(study_time)
            print(f"Study time updated to: {study_time}")

        elif choice == 4:
            duration = edit_duration(duration)
            print(f"Duration updated to: {duration} minutes")

        elif choice == 5:
            mood = edit_mood(mood)
            print(f"Mood updated to: {mood}")

        elif choice == 6:
            focus_level = edit_focus_level(focus_level)
            print(f"Focus level updated to: {focus_level}")

        elif choice == 7:
            update_study_session(
                session_id,
                subject,
                study_date,
                study_time,
                duration,
                mood,
                focus_level
            )
            print("\nStudy session updated successfully.")
            break


def delete_session():
    session_id, session = pick_session()

    if not session:
        return

    print("\nYou are about to delete this session:\n")
    print_session(session)

    confirm = input(
        "\nDelete this session? (y/n): "
    ).strip().lower()

    if confirm == "y":
        delete_study_session(session_id)
        print("Study session deleted.")
    else:
        print("Session was not deleted.")


def main():
    init_db()

    while True:
        show_menu()

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice not in [
            "1", "2", "3", "4",
            "5", "6", "7", "8"
        ]:
            print("Please choose a valid option.")
            continue

        if choice == "1":
            add_new_session()

        elif choice == "2":
            show_sessions()

        elif choice == "3":
            search_session()

        elif choice == "4":
            view_analytics()

        elif choice == "5":
            edit_session()

        elif choice == "6":
            delete_session()

        elif choice == "7":
            export_sessions_to_csv()

        elif choice == "8":
            print(
                "\nThanks for using StudyTrack. "
                "Keep studying hard!"
            )
            break


if __name__ == "__main__":
    main()