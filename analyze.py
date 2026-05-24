def total_study_time(sessions):
    return sum(row["duration_minutes"] for row in sessions)


def average_focus(sessions):
    valid_focus_values = [
        row["focus_level"]
        for row in sessions
        if row["focus_level"] is not None
    ]

    if not valid_focus_values:
        return 0

    return round(sum(valid_focus_values) / len(valid_focus_values), 2)


def most_studied_subject(sessions):
    if not sessions:
        return None

    subject_totals = {}

    for row in sessions:
        subject = row["subject"]
        duration = row["duration_minutes"]

        subject_totals[subject] = (
            subject_totals.get(subject, 0)
            + duration
        )

    return max(subject_totals, key=subject_totals.get)


def study_time_by_subject(sessions):
    subject_totals = {}

    for row in sessions:
        subject = row["subject"]
        duration = row["duration_minutes"]

        subject_totals[subject] = subject_totals.get(subject, 0) + duration

    return subject_totals


def session_count_by_subject(sessions):
    subject_counts = {}

    for row in sessions:
        subject = row["subject"]
        subject_counts[subject] = subject_counts.get(subject, 0) + 1

    return subject_counts


def average_session_duration(sessions):
    if not sessions:
        return 0

    total_minutes = sum(
        row["duration_minutes"]
        for row in sessions
    )

    return round(total_minutes / len(sessions), 2)