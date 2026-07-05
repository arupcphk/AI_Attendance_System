import bcrypt
import sqlite3
import streamlit as st
import json
import os

USER_FILE = "users.json"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    print(password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login(username, password):
    conn = sqlite3.connect('database/attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM faculty WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        return verify_password(password, user[0])
    return False


DB_PATH = 'database/attendance.db'




def create_default_admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            role TEXT
        )
    """)

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    admin_exists = cursor.fetchone()

    if not admin_exists:

        default_password = "admin123"

        hashed = bcrypt.hashpw(
            default_password.encode('utf-8'),
            bcrypt.gensalt()
        )

        cursor.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed, "admin")
        )

        conn.commit()

        
    conn.close()


def register_faculty(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    )

    user_exists = cursor.fetchone()

    if not user_exists:
        try:
            hashed = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            )

            cursor.execute(
                "INSERT INTO users(username, password, role) VALUES (?, ?, ?)",
                (username, hashed, "faculty")
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error during registration: {e}")
            return False
    else:
        st.error(f"User {username} already Exists")
        return False
    
 
def register_student(name,roll_number,class_name,email="Unknown",phone="Unknown",image_path="Not provided"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE roll_number=?",
        (roll_number,)
    )

    student_exists = cursor.fetchone()

    if not student_exists:
        try:
            #print("INSERT INTO users(username, password, role) VALUES (?, ?, ?, ?, ?, ?)",name,roll,class_name,email,phone,image_path)
            cursor.execute(
                "INSERT INTO students(name,roll_number,class_name,email,phone,image_path) VALUES (?, ?, ?, ?, ?, ?)",
                (name,roll_number,class_name,email,phone,image_path)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            st.error(f"Error during registration: {e}")
            return False
    else:
        st.error(f"Roll Number Already Exists")
        return False 

def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT password,role FROM users WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user:
        if verify_password(password, user[0]):
            print(user[1])
            return user[1]
        else:
            return ""

    return ""


def change_password(username, old_password, new_password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    if not user:
        conn.close()
        return False

    stored_password = user[0]

    if bcrypt.checkpw(
        old_password.encode('utf-8'),
        stored_password
    ):

        new_hashed = hash_password(new_password) 
        

        cursor.execute(
            "UPDATE users SET password=? WHERE username=?",
            (new_hashed, username)
        )
        st.success("Password Updated")
        conn.commit()
        conn.close()     
        return True
        
    else:
        st.error("Old Password Incorrect")

    conn.close()
    return False    
    

