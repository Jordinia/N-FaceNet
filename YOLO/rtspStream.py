import cv2
import math
import torch
# import win32gui
from ultralytics import YOLO

# Set device
detectDevice = torch.cuda.is_available()
print(detectDevice)
device = torch.device('cuda') if detectDevice else torch.device('cpu')
print(device)

# Load YOLO model
model = YOLO("YOLO/yolo-Weights/yolov10s.pt")
model.to(device)

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture()
# cap = cv2.VideoCapture("rtsp://admin:qwerty123@172.16.0.106:554/cam/realmonitor?channel=1&subtype=0") # RTSP Stream
cap.open("http://172.18.160.1:65000/") # change the IP address of the stream
cap.set(3, 640)
cap.set(4, 480)

# Object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# # Function to minimize window
# def minimize_window(window_name):
#     hwnd = win32gui.FindWindow(None, window_name)
#     if hwnd:
#         win32gui.ShowWindow(hwnd, 6)  # 6 = SW_MINIMIZE

# Create a resizable window
cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    results = model(img, stream=True)

    # Coordinates and display results
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to int values

            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # Class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # Object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)

    k = cv2.waitKey(1)
    if k == ord('q'):  # Quit
        break

cap.release()
cv2.destroyAllWindows()