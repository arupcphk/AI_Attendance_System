import streamlit as st

import sqlite3
import pandas as pd
import time
import os
import re
from database import create_tables
from dashboard import dashboard
from report import report_dashboard

from capture_faces import capture_faces
from recognize_faces import recognize_faces
from streamlit_option_menu import option_menu
from capture_faces import capture_faces
from recognize_faces import recognize_faces
from train_model import train_faces

from auth import (
    login,
    register_faculty,
    register_student,
    change_password,
    create_default_admin
)

DB_PATH = 'database/attendance.db'

create_tables()
create_default_admin()
st.set_page_config(page_title="AI Attendance System", layout="wide")

st.title("AI-Powered Attendance System")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


menu = []
 
menu = [
    "Home",
    "Login",
]

if st.session_state.logged_in:
    # menu = [
        # "Logout",
        # "Change Password"
    # ]
    if st.session_state.role == "admin":
        menu.extend([
            "Logout",
            "Register Faculty",
            "Add Student",
            "Train Model",
            "Mark Attendance",
            "Dashboard",
            "Reports",
            "Change Password"
        ])
        st.success(f"Logged in as {st.session_state.role}")
    elif st.session_state.role == "faculty":
        menu.extend([
            "Logout",
            "Add Student",
            "Train Model",
            "Mark Attendance", 
            "Dashboard",
            "Reports",
            "Change Password"
        ])
        st.success(f"Logged in as {st.session_state.role}")



# SIDEBAR
with st.sidebar:
    choice = option_menu(
        menu_title="AI Attendance",
        options=menu,
        icons=[
            "🏠",   # Home
            "box-arrow-in-right",   # Login
            "box-arrow-in-left",    # LogOut
            "person-badge",         # Register Faculty
            "person-plus",          # Add Student
            "cpu",                  # Train Model
            "camera-video",         # Mark Attendance
            "speedometer2",         # Dashboard
            "bar-chart-line"        # Reports
        ],
        menu_icon="grid-fill",
        default_index=0,
    )
    



# --------------------------
# LOGIN FUNCTION
# --------------------------


if choice == "Login":

    st.subheader("Enter your Credentials")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        db_role=login(username, password)
        if not db_role=="":
            st.success("Login Successful")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = db_role
            st.success("Login Successful")
            username=""
            password=""
            st.rerun()
        else:
            st.error("Invalid Credentials")
# LOGOUT FUNCTION
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.role = None
    st.success("✅ Logged out successfully")
    st.rerun()
# REGISTER FACULTY    
elif choice == "Register Faculty":
    for key in ["user_name", "pwd"]:
        if key not in st.session_state:
            st.session_state[key] = ""
    st.subheader("Register Faculty")
  
    st.text_input("Username ", key="user_name")
    st.text_input("Password", type='password', key="pwd")
    
    try:
        if st.button("Register"):
            user_name = st.session_state.user_name
            pwd = st.session_state.pwd
            # Validation
            if " " in user_name:
                st.error("Username cannot contain spaces. Please remove spaces.")
            elif user_name.strip() == "":
                st.error("Username cannot be blank.")
            # Password validation
            elif not re.search(r"[A-Z]", pwd):
                st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
            elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
                st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
            elif len(pwd) < 6:
                st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
            else:
                if register_faculty(user_name, pwd):
                    st.success(f"Faculty '{user_name}' registered successfully!")
                    time.sleep(2)
                    for key in ["user_name", "pwd"]:
                        if key in st.session_state:
                            del st.session_state[key]                    
                    st.rerun()        
    except Exception as e:
         st.error(f"Error during registration: {e}")                        

# ADD STUDENT
elif choice == "Add Student":

    st.subheader("📸 Student Registration & Face Capture")

    # name = st.text_input("Student Name")
    # roll = st.text_input("Roll Number")
    # class_name = st.text_input("Class Name")
    # email = st.text_input("Email")
    # phone = st.text_input("Phone")
    # Initialize session state variables
    for key in ["name", "roll", "class_name", "email", "phone", "face_captured","image_path"]:
        if key not in st.session_state:
            st.session_state[key] = "" if key != "face_captured" else False
    
    # Input fields bound to session_state
    name = st.text_input("Student Name", key="name")
    roll = st.text_input("Roll Number (3 digits)", key="roll")
    class_name = st.text_input("Class Name", key="class_name")
    email = st.text_input("Email", key="email")
    phone = st.text_input("Phone", key="phone")
    
    # # Initialize session state for face capture
    # if "face_captured" not in st.session_state:
        # st.session_state.face_captured = False
    
    # Number of samples to capture
    # num_samples = st.slider("Number of face samples to capture", 10, 50, 30)

    # Button to trigger face capture
    if st.button("Capture Faces"):
        
 # New Code
        # Validation
        if roll.strip() == "":
            st.error("Student ID is required.")
        elif not roll.isdigit():
            st.error("Student ID must be numeric.")
        elif len(roll) != 3:
            st.error("Student ID must be exactly 3 digits.")
        elif name.strip() == "":
            st.error("Student Name is required.")
        elif class_name.strip() == "":
            st.error("Class/Section is required.")
        else:
            try:
                sid = int(roll)    
                # Capture face samples
                capture_faces(sid, name)
                #capture_faces(sid, student_name, num_samples=num_samples)

                # Check if face samples exist
                dataset_path = f"dataset/user_{sid}"
                #path = f"dataset/user_{sid}"
                files = [f for f in os.listdir(dataset_path) if f.startswith(f"User.{sid}.")]
                if len(files) == 0:
                    st.error("❌ No face samples captured. Student data will not be saved.")
                    st.session_state.face_captured = False
                else:
                    st.info("✅ Face samples captured. Preview below:")
                    st.session_state.face_captured = True
                    # Show thumbnails of captured faces
                    cols = st.columns(5)
                    for i, file in enumerate(files[:10]):  # show up to 10 samples
                        img_path = os.path.join(dataset_path, file)
                        with cols[i % 5]:
                            st.image(img_path, caption=f"Sample {i+1}", width=120)

                    # Confirmation button before saving                        
            except Exception as e:
                st.error(f"Error during registration: {e}")
        
    if st.button("Save Student"):
        if st.session_state.face_captured:
            try:                           
                st.session_state.image_path = f"dataset/user_{roll}"
                if register_student(st.session_state.name,st.session_state.roll,st.session_state.class_name,st.session_state.email,st.session_state.phone,st.session_state.image_path):
                    st.success(f"Student {name} (ID: {roll}) registered successfully with face samples.")                    
                    time.sleep(2)
                    for key in ["name", "roll", "class_name", "email", "phone", "face_captured","image_path"]:
                        if key in st.session_state:
                            del st.session_state[key]                    
                    st.rerun()        
                else:
                    st.error("Data not Saved....")
        
            except Exception as e:
                st.error(f"Error during registration: {e}") 
        else:
            st.error("Capture face before saving the data......")

# TRAIN FACES
elif choice == "Train Model":

    st.subheader("Train AI Model")

    if st.button("Start Training"):

        train_faces()

        st.success("Face Training Completed")


# MARK ATTENDANCE
elif choice == "Mark Attendance":

    st.subheader("AI Attendance")

    st.warning("Press ESC to close webcam")

    if st.button("Start Attendance"):

        recognize_faces()
        

# DASHBOARD
elif choice == "Dashboard":
    dashboard()

# REPORTS
elif choice == "Reports":

    report_dashboard()
elif choice == "Change Password":

    st.subheader("📸 Change Password")

    userid = st.text_input("Enter User Name")
    oldpwd = st.text_input("Enter Old Password", type='password')
    newpwd = st.text_input("Enter New Password", type='password')
    rnewpwd = st.text_input("Repeat New Password", type='password')
    
    # Button to Reset Password
    if st.button("Reset Password"):
        
 # New Code
        # Validation
        if userid.strip() == "":
            st.error("User ID is required.")
        elif len(userid) < 3 or len(userid)>8 :
            st.error("User ID must be atleaset 3 and maximum of 8 character")
        elif oldpwd.strip() == "":
            st.error("Old Password is required.")
        elif newpwd.strip() == "":
            st.error("New Password is required.")
        elif not re.search(r"[A-Z]", newpwd):
            st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", newpwd):
            st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
        elif len(newpwd) < 6:
            st.error("Password must be at least 6 characters long and contain at least one uppercase letter and one special character.")
        elif rnewpwd.strip() == "":
            st.error("Re-enter New Password.")
        elif newpwd!=rnewpwd :
            st.error("Mismatch in New Password Entries")
        else:
            if change_password(userid, oldpwd, newpwd):
                st.success("✅ Password Change Successful")
            else:
                st.error("❌ Password Change not Successful, one of the information provided is incorrect")
                
                
            