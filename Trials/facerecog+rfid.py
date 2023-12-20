import tkinter as tk
import cv2
from PIL import Image, ImageTk

# Use OpenCV to capture the video feed from the default camera
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def update_frame():
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    photo = ImageTk.PhotoImage(image)
    video_label.config(image=photo)
    video_label.image = photo

    root.after(5, update_frame)

# Function to update the label text with RFID ID
def update_label(rfid_id):
    label.config(text=f"RFID Tag ID: {rfid_id}")

# Function to handle the button click event
def scan_button_clicked():
    # Simulating RFID input as keyboard input (replace this with your actual logic)
    # For demonstration purposes, using an input
    rfid_input = input("Enter RFID ID: ")
    update_label(rfid_input)  # Update the label with the RFID ID


# Create the main application window
root = tk.Tk()
root.title("N-FACENET")

# Create a label
label = tk.Label(root, text="RFID Tag ID: ", font=("Arial", 18))
label.pack(pady=20)

# Create a button
scan_button = tk.Button(root, text="Scan RFID", command=scan_button_clicked, width=15)
scan_button.pack(pady=10)

# Create a label for displaying video feed
video_label = tk.Label(root)
video_label.pack()

# Run the application
update_frame()
root.mainloop()
