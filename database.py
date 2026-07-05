import sqlite3

DB_PATH = 'database/attendance.db'


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Students Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_number TEXT UNIQUE,
        class_name TEXT,
        email TEXT,
        phone TEXT,
        image_path TEXT
    )
    """)

    # Faculty Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        faculty_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT
    )
    """)

    # Attendance Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        time TEXT,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()