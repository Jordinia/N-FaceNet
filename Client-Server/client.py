import tkinter as tk
import requests
import json
import time
import cv2
from PIL import Image, ImageTk
import random
import base64



rfid_id =""
addr = 'http://127.0.0.1:5000'
test_url = addr + '/api/test'

def capture_image():
    # Simulating RFID input as keyboard input (replace this with your actual logic)
    # For demonstration purposes, using an input
    #rfid_input = input("Enter RFID ID: ")
    #update_label(rfid_input)  # Update the label with the RFID ID

    # Capture a frame from the video feed
    current_text = label['text']
    if current_text.startswith("RFID Tag ID: "):  # Pastikan input dimulai dengan "RFID Tag ID: "
        entered_id = current_text.split(": ")[1].strip()  # Ambil nilai ID yang dimasukkan
        rfid_id = entered_id
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        return


    # Save the frame as an image
    image_path = f"Client-Server\\ClientPhoto\\{rfid_id}.jpg" #harus diganti
    cv2.imwrite(image_path, frame)
    
    room_name ="K301"

    # with open(image_path, 'rb') as f:
    #     image_data = f.read()
    with open(image_path, 'rb') as f:
        image_data = f.read()
    #response = requests.post(test_url, files={'image': (image_path, image_data, 'image/jpeg')})
    headers = {'Content-Type': 'application/json'}
    #files = {'image': ('image.jpg', image_data, 'image/jpeg')}
    #data['rfid_id'] = rfid_id
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    #data['image'] = image_base64
    data={
        "rfid_id": rfid_id,
        "roomName": room_name,
        "image": image_base64
    }

    response = requests.post(test_url, json=data, headers=headers)
    print(response.text)

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

# Function to check access after RFID input
def check_access():
    # Mendefinisikan ID yang telah diketahui dan nama yang sesuai
    known_ids = {
        "3882029743": "Aldrian",
        "2492866845": "Rizki",
        # Tambahkan ID dan nama sesuai kebutuhan
    }

    current_text = label['text']
    if current_text.startswith("RFID Tag ID: "):  # Pastikan input dimulai dengan "RFID Tag ID: "
        entered_id = current_text.split(": ")[1].strip()  # Ambil nilai ID yang dimasukkan
        rfid_id = entered_id
        print(rfid_id)
        if entered_id in known_ids:
            name_label = tk.Label(root, text=f"Nama: {known_ids[entered_id]}", font=("Arial", 18))
            name_label.pack()  # Menampilkan label nama
        else:
            name_label = tk.Label(root, text=f"Try Again", font=("Arial", 18), fg="red")
            name_label.pack()  # Menampilkan label nama
    else:
        print("Input RFID tidak valid")  # Jika input tidak dimulai dengan "RFID Tag ID: "

    root.after(2000, lambda: name_label.destroy())  # Hapus label setelah 2 detik

# Function to clear the input
def clear_input():
    label.config(text="RFID Tag ID: ")

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def update_frame():
    ret, frame = cap.read()

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)  # 1 for horizontal flip, 0 for vertical, -1 for both

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    photo = ImageTk.PhotoImage(image)
    video_label.config(image=photo)
    video_label.image = photo

    root.after(50, update_frame)

# Create the main application window
root = tk.Tk()
root.geometry("720x600")
root.title("N-FACENET")

# Create a label for instructions
instruction_label = tk.Label(root, text="Please tap your ID Card on the scanner and \nmake sure your face is inside the frame", font=("Arial", 11))
instruction_label.pack(pady=20, padx=20)

# Create a label
label = tk.Label(root, text="RFID Tag ID: ", font=("Arial", 18))
label.pack(pady=20)

# Bind Key event to the root window to capture keypresses globally
root.bind("<Key>", update_label)

# Create a label for displaying video feed
video_label = tk.Label(root)
video_label.pack()

# Membuat label kedua untuk menampilkan gambar yang baru diambil
captured_label = tk.Label(root)
captured_label.pack()

# Run the application
update_frame()
root.mainloop()
