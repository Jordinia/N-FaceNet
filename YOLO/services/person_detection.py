import cv2
from ultralytics import YOLO
import time
import os
from datetime import datetime

# Load the YOLO model
model = YOLO("../yolo-Weights/yolo11m.engine")

# Open the RTSP stream
cap = cv2.VideoCapture()
cap.open("http://100.111.29.103:4747/video")
cap.set(3, 640)
cap.set(4, 480)

# Object classes
classNames = ["person"]

# Create output directory for cropped images
output_dir = "detected_persons"
os.makedirs(output_dir, exist_ok=True)

# Create a resizable window
cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

# Variables for saving images
last_save_time = time.time()
save_interval = 5  # Save every 1 second

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Run detection
    results = model.predict(img)
    
    # Counter for people in current frame
    person_count = 0
    
    # Process results
    for r in results:
        boxes = r.boxes
        
        # Count total persons in frame
        person_count = sum(1 for box in boxes if int(box.cls[0]) == 0)
        
        # Display total count on frame
        cv2.putText(img, f"Total Persons: {person_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Process each detection
        for idx, box in enumerate(boxes):
            # Extract coordinates and class
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            cls = int(box.cls[0])
            
            # Only process if class is 'person'
            if cls == 0:
                # Assign ID to person
                person_id = f"Person_{idx + 1}"
                
                # Draw bounding box and label with ID
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"{person_id} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Save cropped images every second
                current_time = time.time()
                if current_time - last_save_time >= save_interval:
                    # Crop the detected person
                    crop = img[y1:y2, x1:x2]
                    
                    # Resize to 640x640
                    crop_resized = cv2.resize(crop, (640, 640))
                    
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{output_dir}/{person_id}_{timestamp}.jpg"
                    
                    # Save the cropped image
                    cv2.imwrite(filename, crop_resized)
        
        # Update last save time
        if time.time() - last_save_time >= save_interval:
            last_save_time = time.time()

    # Display the frame
    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()