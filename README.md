# AI-Based Attendance Management System Using Face Recognition
AI-Based Attendance Management System Using Face Recognition with OpenCV and LBPH Algorithm

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Project Overview

The AI-Based Attendance Management System is an intelligent attendance automation application developed using Python, Streamlit, OpenCV, and the Local Binary Pattern Histogram (LBPH) face recognition algorithm.

The system automatically identifies registered students through facial recognition and records attendance in a secure SQLite database. It provides a user-friendly interface for administrators and faculty to manage students, train facial recognition models, monitor attendance, and generate reports.

---

## Features

- Secure Administrator and Faculty Login
- Password Encryption using bcrypt
- Student Registration
- Faculty Registration
- Face Image Capture using Webcam
- Face Detection using Haar Cascade Classifier
- Face Recognition using LBPH Algorithm
- Automatic Attendance Recording
- Duplicate Attendance Prevention
- Attendance Dashboard
- Attendance Report Generation
- CSV Report Export
- SQLite Database Integration
- Streamlit Web Interface

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| Streamlit | User Interface |
| OpenCV | Face Detection & Recognition |
| LBPH | Face Recognition Algorithm |
| Haar Cascade | Face Detection |
| SQLite | Database |
| Pandas | Data Processing |
| NumPy | Numerical Computation |
| Plotly | Dashboard Visualization |
| bcrypt | Password Hashing |

---

## System Architecture

```
                    Streamlit Interface
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
 Authentication      Student Module      Dashboard
        │                  │                  │
        └──────────────┬───┴──────────────┐
                       │                  │
                Face Capture         Reports
                       │
                       ▼
                Model Training
                       │
                       ▼
              Face Recognition
                       │
                       ▼
             Attendance Database
```

---

## Project Structure

```
AI_Attendance_System/
│
├── app.py
├── auth.py
├── database.py
├── attendance.py
├── capture_faces.py
├── recognize_faces.py
├── train_model.py
├── dashboard.py
├── report.py
│
├── dataset/
├── trainer/
├── reports/
├── images/
├── attendance.db
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Attendance-System.git

cd AI-Attendance-System
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually

```bash
pip install streamlit
pip install opencv-contrib-python
pip install face_recognition
pip install numpy
pip install pandas
pip install pillow
pip install plotly
pip install bcrypt
```

---

## Running the Application

```bash
streamlit run app.py
```

The application will automatically open in your default web browser.

---

## Workflow

### Step 1

Login using Administrator account.

### Step 2

Register Faculty members.

### Step 3

Register Students.

### Step 4

Capture student face images.

### Step 5

Train the LBPH model.

### Step 6

Start Face Recognition.

### Step 7

Attendance is automatically recorded.

### Step 8

Generate attendance reports.

---

## Database

The system uses SQLite with three primary tables.

### Users

- UserID
- Username
- Password
- Role

### Students

- StudentID
- StudentName
- Class
- ImagePath

### Attendance

- AttendanceID
- StudentID
- Date
- Time
- Status

---

## Face Recognition Algorithm

This project uses:

- Haar Cascade Classifier for Face Detection
- Local Binary Pattern Histogram (LBPH) for Face Recognition

Advantages of LBPH:

- Fast
- Lightweight
- High Accuracy
- Works under varying illumination
- Suitable for real-time applications

---

## Screenshots

Add screenshots here.

```
Login Screen

Student Registration

Face Capture

Training Module

Attendance Dashboard

Reports
```

---

## Future Improvements

- Deep Learning Face Recognition
- Mobile Application
- Cloud Deployment
- Multi-Camera Support
- SMS/Email Notifications
- QR Code Backup Attendance
- REST API
- LMS Integration
- ERP Integration

---

## Testing

The application has been tested using:

- Unit Testing
- Integration Testing
- Functional Testing
- User Acceptance Testing (UAT)

---

## Requirements

- Python 3.10+
- Webcam
- Windows 10/11
- 4 GB RAM Minimum
- Internet (for installation only)

---

## Author

**Arup Dutta**

M.Sc. Data Science

Chandigarh University

Project Title:

**AI-Based Attendance Management System Using Face Recognition with OpenCV and LBPH Algorithm**

---

## Acknowledgements

- Chandigarh University
- OpenCV Community
- Streamlit Team
- Python Software Foundation
- SQLite Developers

---

## License

This project is licensed under the MIT License.

---

## Star the Repository

If you found this project useful, please consider giving it a ⭐ on GitHub.
