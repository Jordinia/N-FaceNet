import cv2
from ultralytics import YOLO
import time
import os
from datetime import datetime
import requests
from outfit_detection_v2 import check_outfit  # Import the check_outfit function

# Load the YOLO model for person detection
person_model = YOLO("../yolo-Weights/yolo11m.engine")

# Load the YOLO model for outfit detection
outfit_model = YOLO("../yolo-Weights/topbottomv2.engine")

# Open the RTSP stream
cap = cv2.VideoCapture()
cap.open("http://100.111.29.103:4747/video")
# cap.open("http://100.116.184.72:12000")

# Object classes
classNames = ["person"]

# Create output directory for cropped images
output_dir = "detected_persons"
os.makedirs(output_dir, exist_ok=True)

# Create a resizable window
cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

# Variables for saving images
last_save_time = time.time()
save_interval = 1  # Save every 8 seconds

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read frame.")
        break

    # Run detection for persons
    person_results = person_model.predict(img, conf=0.5)

    # Counter for people in current frame
    person_count = 0

    # Process person detection results
    for r in person_results:
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

                # Crop the detected person
                crop = img[y1:y2, x1:x2]

                # Save cropped images every 'save_interval' seconds
                current_time = time.time()
                if current_time - last_save_time >= save_interval:
                    # Generate filename with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    # Call the check_outfit function and pass the outfit model
                    annotated_image, outfit = check_outfit(crop, outfit_model)
         
                    # Print the detected outfit information
                    print(f"Detected outfit for {person_id}: {outfit}")

                    # Construct the API URL with query parameters
                    api_url = f"http://127.0.0.1:5000/employee?top_color_id={outfit['top']['color_id']}&bottom_color_id={outfit['bottom']['color_id']}"

                    # Make the API call
                    response = requests.get(api_url)

                    # Check the response status
                    if response.status_code == 200:
                        response_json = response.json()
                        if response_json['status'] == 'success' and response_json['data']:
                            print(f"Detected user: {response_json['data'][0]['name']}")
                            cv2.putText(img, f"{person_id}-{response_json['data'][0]['name']} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        elif response_json['status'] == 'success' and not response_json['data']:
                            print("No matching user found.")
                            cv2.putText(img, f"{person_id} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        else:
                            print(f"API call failed with status: {response_json['status']}")
                            cv2.putText(img, f"{person_id} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    else:
                        print(f"API call failed with status code: {response.status_code}")
                        cv2.putText(img, f"{person_id} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    # Update last save time
                    last_save_time = current_time
                else:
                    cv2.putText(img, f"{person_id} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                # Display the frame
                cv2.imshow('Webcam', img)   
                
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()