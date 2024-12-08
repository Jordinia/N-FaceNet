import cv2
from ultralytics import YOLO

# Load the YOLO model from the TensorRT engine file
model = YOLO("./yolo-Weights/yolo11m.engine")

# Open the RTSP stream
cap = cv2.VideoCapture()
# cap = cv2.VideoCapture("rtsp://admin:qwerty123@172.16.0.109:554/cam/realmonitor?channel=1&subtype=0")
cap.open("http://100.111.29.103:4747/video")
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

    # Run detection using the TensorRT engine
    results = model.predict(img)

    # Process results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            # Extract confidence score
            conf = box.conf[0]
            # Extract class index
            cls = int(box.cls[0])

            # Only process if class is 'person' (class index 0)
            if cls == 0:
                # Draw bounding box and label
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img, f"{classNames[cls]} {conf:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()