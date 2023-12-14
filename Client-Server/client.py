import tkinter as tk
import requests
import json
import time
import cv2
from PIL import Image, ImageTk

# Function to update the label text with RFID ID
def update_label(event):
    char_pressed = event.char
    if char_pressed and char_pressed not in ('\r', '\n', '\t', '\b'):
        current_text = label['text']
        if current_text.endswith(": "):
            label.config(text=f"RFID Tag ID: {char_pressed}")
            root.after(1000, capture_image)
        else:
            label.config(text=current_text + char_pressed)
        
        # Schedule clearing the input after 1 second (1000 milliseconds)
        root.after(2000, clear_input)

# Function to capture image
def capture_image():
    # Simulating RFID input as keyboard input (replace this with your actual logic)
    # For demonstration purposes, using an input
    #rfid_input = input("Enter RFID ID: ")
    #update_label(rfid_input)  # Update the label with the RFID ID

    # Capture a frame from the video feed
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        return

    # Save the frame as an image
    image_id = str(int(time.time())) # Use the current timestamp as the image ID
    image_path = f"D:\\Documents\\Semester5\\RPL\\Captured\\{image_id}.jpg" #harus diganti
    cv2.imwrite(image_path, frame)

    headers = {'Content-Type': 'image/jpeg'} 
    with open(image_path, 'rb') as f:
        image_data = f.read()
    response = requests.post(test_url, data=image_data, headers=headers)

    # Send the image to the URL
    # with open(image_path, 'rb') as f:
    #     image_data = f.read()
    # response = requests.post(test_url, files={'image': (image_path, image_data, 'image/jpeg')})
    print(response.text)

# Function to clear the input
def clear_input():
    label.config(text="RFID Tag ID: ")

addr = 'http://192.168.146.81:5000'
test_url = addr + '/api/test'

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
    video_label.config(image=photo)
    video_label.image = photo

    root.after(5, update_frame)

# Create the main application window
root = tk.Tk()
root.title("N-FACENET")

# Create a label
label = tk.Label(root, text="RFID Tag ID: ", font=("Arial", 18))
label.pack(pady=20)

# Bind Key event to the root window to capture keypresses globally
root.bind("<Key>", update_label)

# Create a label for displaying video feed
video_label = tk.Label(root)
video_label.pack()

# Run the application
update_frame()
root.mainloop()
