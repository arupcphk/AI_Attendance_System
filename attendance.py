import sqlite3
from datetime import datetime

DB_PATH = 'database/attendance.db'


def mark_attendance(student_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Prevent duplicate attendance
    cursor.execute("""
    SELECT * FROM attendance
    WHERE student_id=? AND date=?
    """, (student_id, date))

    already_marked = cursor.fetchone()

    if not already_marked:

        cursor.execute("""
        INSERT INTO attendance(student_id, date, time, status)
        VALUES (?, ?, ?, ?)
        """, (student_id, date, time, "Present"))

        conn.commit()

    conn.close()