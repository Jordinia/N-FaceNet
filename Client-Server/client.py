import tkinter as tk
import requests
import json
import time
import cv2
from PIL import Image, ImageTk


addr = 'http://192.168.1.46:5000'
test_url = addr + '/api/test'

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
    #rfid_input = input("Enter RFID ID: ")
    #update_label(rfid_input)  # Update the label with the RFID ID

   # Capture a frame from the video feed
    ret, frame = cap.read()
    if not ret:
       print("Failed to capture frame.")
       return

   # Save the frame as an image
    image_id = str(int(time.time())) # Use the current timestamp as the image ID
    image_path = f"C:\\Users\\AHMAD RIFQI.DESKTOP-ECPJ680\\Downloads\\{image_id}.jpg" #harus diganti
    cv2.imwrite(image_path, frame)

   # Send the image to the URL
    with open(image_path, 'rb') as f:
        image_data = f.read()
    response = requests.post(test_url, files={'image': (image_path, image_data, 'image/jpeg')})
    print(response.text)


    # content_type = 'image/jpeg'
    # headers = {'content-type': content_type}

    # img = cv2.imread('C:\\46032bdf79ce0c6b681d9d241484e2a6.jpeg')  # image path
    #     # encode image as jpeg
    # _, img_encoded = cv2.imencode('.jpg', img)
    #     # send http request with image and receive response
    # response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    #     # decode response
    # print(json.loads(response.text))
    


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