
import tkinter as tk
import cv2
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Face Detection")

label = tk.Label(root)
label.pack()

# Use OpenCV to capture the video feed from the default camera
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def update_frame():
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

    root.after(10, update_frame)

update_frame()

root.mainloop()
