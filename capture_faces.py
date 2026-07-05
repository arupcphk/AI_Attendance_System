import cv2
import os
import streamlit as st

face_detector = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml'
)



def capture_faces(student_id, student_name):

    path = f"dataset/user_{student_id}"

    if not os.path.exists(path):
        os.makedirs(path)

    cam = cv2.VideoCapture(0)

    count = 0

    while True:
        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            count += 1
            file_name = f"dataset/User_{student_id}/User.{student_id}.{count}.jpg"
            cv2.imwrite(
                file_name,
                gray[y:y+h, x:x+w]
            )
            

            cv2.imshow('Capturing Faces', frame)

        k = cv2.waitKey(100) & 0xff

        if k == 27:
            break

        elif count >= 30:
            break

    cam.release()
    cv2.destroyAllWindows()

    return True