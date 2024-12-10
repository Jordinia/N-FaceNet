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
# model = YOLO("runs/detect/train13/weights/best.pt")
model = YOLO("./yolo-Weights/yolo11m.pt")
model.to(device)

#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture()
# cap = cv2.VideoCapture("rtsp://admin:qwerty123@172.16.0.106:554/cam/realmonitor?channel=1&subtype=0") # RTSP Stream
cap = cv2.VideoCapture("rtsp://admin:qwerty123@172.16.0.109:554/cam/realmonitor?channel=1&subtype=0") # RTSP Stream
# cap.open("http://192.168.0.100:65000/video") # change the IP address of the stream
cap.set(3, 640)
cap.set(4, 480)

# Object classes
classNames = ["person"]

# Create a resizable window
cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Run detection only for "person"
    results = model(img, classes=[0])

    # Process results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            # Extract confidence score
            conf = box.conf[0]
            # Draw bounding box and label
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, f"person {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()