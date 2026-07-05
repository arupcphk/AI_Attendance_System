import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = 'database/attendance.db'


def connect_db():
    return sqlite3.connect(DB_PATH)


def fetch_attendance():

    conn = connect_db()

    query = """
    SELECT
        students.name,
        students.roll_number,
        students.class_name,
        attendance.date,
        attendance.time,
        attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id = students.roll_number
    ORDER BY attendance.date DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def report_dashboard():

    st.title("Attendance Reports")

    df = fetch_attendance()

    st.dataframe(df)

    csv = df.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='attendance_report.csv',
        mime='text/csv'
    )