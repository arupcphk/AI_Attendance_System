import cv2
import sqlite3
import datetime
import streamlit as st
def get_student_name(student_id):
    """Fetch student name from database using StudentID."""
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM students WHERE student_id=?", (student_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Unknown"

def mark_attendance(student_id, status="Present"):
    """Insert attendance record into Attendance."""
    conn = sqlite3.connect("database/attendance.db")
    cursor = conn.cursor()

    # Ensure Attendance table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(student_id)
        )
    """)

    # Current date and time
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Prevent duplicate marking for same student on same day
    cursor.execute("""
        SELECT * FROM attendance WHERE student_id=? AND date=? AND status='Present'
    """, (student_id, date_str))
    record = cursor.fetchone()

    if not record:
        cursor.execute("""
            INSERT INTO attendance (student_id, date, time, status)
            VALUES (?, ?, ?, ?)
        """, (student_id, date_str, time_str, status))
        conn.commit()
        st.success(f"✅ Attendance marked: Student {student_id} - {status} at {time_str}")
        conn.close()
        return True   # signal to stop capture
        # print(f"[INFO] Attendance marked: Student {student_id} - {status} at {time_str}")
    else:
        st.warning(f"⚠️ Attendance already marked for Student {student_id} today.")
        conn.close()
        return False
        # print(f"[INFO] Attendance already marked for Student {student_id} today.")

    

def recognize_faces(model_path="trainer.yml"):
    """Recognize faces in real-time and mark attendance."""
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(model_path)
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not access webcam.")
        return

    # print("[INFO] Starting real-time face recognition... Press 'q' to quit.")
    st.info("📷 Camera opened. Recognition in progress... Press 'q' to quit.")
    
    stop_capture = False
    
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            st.error("Error: Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            student_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 70:  # Good match
                student_name = get_student_name(student_id)
                label = f"{student_name} (ID: {student_id})"

                # Mark attendance
                # if mark_attendance(student_id, "Present"):
                mark_attendance(student_id, "Present")    
                stop_capture = True
            else:
                label = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Face Recognition & Attendance", frame)
        
        if stop_capture:
            st.info("✅ Attendance marked. Stopping camera...")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    st.info("[INFO] Face recognition stopped.")
