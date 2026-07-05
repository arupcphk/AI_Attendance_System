import cv2
import os
import numpy as np
import streamlit as st
import time
from PIL import Image

# Create LBPH recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Haarcascade path
cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(cascadePath)

# Dataset path
path = 'dataset'

def getImagesAndLabels(path):

    faceSamples = []
    ids = []

    imagePaths = []

    # Read only image files
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                imagePaths.append(os.path.join(root, file))
    #info_placeholder = st.empty()
    progress_bar = st.progress(0)
    status = st.empty()
    i=0
    progress=0
    for imagePath in imagePaths:
             
        print("Processing:", imagePath)
        #info_placeholder.info(f"ℹ️ Processing:  {imagePath}")
        status.info(f"Processing: {imagePath}")
        time.sleep(1)  # simulate work
        progress=int((i+1)/len(imagePaths)*100)
        if progress>100:
                progress=100
        progress_bar.progress(progress)
        i=i+1
        try:
            PIL_img = Image.open(imagePath).convert('L')
        except Exception as e:
            print("Skipping:", imagePath, e)
            continue

        img_numpy = np.array(PIL_img, 'uint8')

        # Filename format:
        # User.1.5.jpg
        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except:
            print("Invalid filename:", imagePath)
            continue

        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    progress_bar.progress(100)        
    status.success("✅ All images processed!")
    return faceSamples, ids
    
def train_faces():
    
    st.info("Training faces...")

    faces, ids = getImagesAndLabels(path)

    recognizer.train(faces, np.array(ids))

    recognizer.write('trainer.yml')

    st.info("Model trained successfully!")
    time.sleep(2)
    #st.rerun() 