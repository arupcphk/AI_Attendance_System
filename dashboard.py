import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

DB_PATH = 'database/attendance.db'


def dashboard():

    st.title("Attendance Dashboard")

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
    SELECT students.name, attendance.date
    FROM attendance
    JOIN students
    ON attendance.student_id = students.roll_number
    """, conn)

    conn.close()

    st.dataframe(df)

    fig = px.histogram(
        df,
        x='name',
        title='Student Attendance Count'
    )

    st.plotly_chart(fig)