import sqlite3
from pathlib import Path

DB_PATH = Path("studytrack.db")


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with connect_db() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS study_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                study_date TEXT NOT NULL,
                study_time TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                mood TEXT,
                focus_level INTEGER
            )
        """)
        connection.commit()


def add_study_session(
    subject,
    study_date,
    study_time,
    duration_minutes,
    mood,
    focus_level
):
    with connect_db() as connection:
        connection.execute("""
            INSERT INTO study_sessions (
                subject,
                study_date,
                study_time,
                duration_minutes,
                mood,
                focus_level
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            subject,
            study_date,
            study_time,
            duration_minutes,
            mood,
            focus_level
        ))
        connection.commit()


def fetch_sessions():
    with connect_db() as connection:
        cursor = connection.execute("""
            SELECT *
            FROM study_sessions
            ORDER BY id ASC
        """)
        return cursor.fetchall()


def get_session_by_id(session_id):
    with connect_db() as connection:
        cursor = connection.execute("""
            SELECT *
            FROM study_sessions
            WHERE id = ?
        """, (session_id,))
        return cursor.fetchone()


def update_study_session(
    session_id,
    subject,
    study_date,
    study_time,
    duration_minutes,
    mood,
    focus_level
):
    with connect_db() as connection:
        connection.execute("""
            UPDATE study_sessions
            SET
                subject = ?,
                study_date = ?,
                study_time = ?,
                duration_minutes = ?,
                mood = ?,
                focus_level = ?
            WHERE id = ?
        """, (
            subject,
            study_date,
            study_time,
            duration_minutes,
            mood,
            focus_level,
            session_id
        ))
        connection.commit()


def delete_study_session(session_id):
    with connect_db() as connection:
        connection.execute("""
            DELETE FROM study_sessions
            WHERE id = ?
        """, (session_id,))
        connection.commit()