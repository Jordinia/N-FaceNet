import cv2
import numpy as np
from ultralytics import YOLO
import time
import os
import requests
from threading import Thread
from outfit_detection_v2 import check_outfit

def process_camera_stream(cam_id, cam_url):
    """
    Processes the video stream from the given URL, detects persons and their outfits,
    and displays the annotated video with detections.

    Parameters:
        cam_id (int): The ID of the camera.
        cam_url (str): The URL of the video stream.
    """

    # Load the YOLO models
    person_model = YOLO("../yolo-Weights/yolo11m.engine")
    outfit_model = YOLO("../yolo-Weights/topbottomv2_fp32.engine")

    # Variables for the frame
    frame = None
    ret = False

    # Frame capture thread
    def capture_frames(cam_url):
        nonlocal frame, ret
        cap = cv2.VideoCapture(cam_url)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
        cap.release()

    # Start the frame capture thread
    frame_thread = Thread(target=capture_frames, args=(cam_url,))
    frame_thread.daemon = True
    frame_thread.start()

    # Toggle the LED on the camera (if applicable)
    def toggle_camera_led():
        base_url = cam_url.rstrip('/video')
        led_url = f"{base_url}/cam/1/led_toggle"
        response = requests.get(led_url)
        if response.status_code == 200:
            print("LED toggled successfully.")
        else:
            print(f"Failed to toggle LED. Status code: {response.status_code}")

    # Call the function to toggle the LED
    toggle_camera_led()

    # Create output directory for cropped images
    output_dir = "detected_persons"
    os.makedirs(output_dir, exist_ok=True)

    # Create a resizable window
    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

    # Variables for frame processing
    last_processed_time = time.time()
    process_interval = 0.2  # Time interval between processing frames in seconds

    while True:
        if frame is not None and ret:
            current_time = time.time()
            elapsed_time = current_time - last_processed_time

            # Check if it's time to process the next frame
            if elapsed_time >= process_interval:
                # Resize frame for faster processing
                img = cv2.resize(frame, (640, 480))

                # Run detection for persons
                person_results = person_model.predict(img, conf=0.5)

                # Counter for people in current frame
                person_count = 0

                for r in person_results:
                    boxes = r.boxes

                    # Count total persons in frame
                    person_count = sum(1 for box in boxes if int(box.cls[0]) == 0)

                    # Display total count on frame
                    cv2.putText(img, f"Total Persons: {person_count}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    # Process each detection
                    for idx, box in enumerate(boxes):
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = box.conf[0]
                        cls = int(box.cls[0])

                        if cls == 0:  # Only process if class is 'person'
                            person_id = f"Person_{idx + 1}"

                            # Draw bounding box
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

                            # Crop the detected person
                            crop = frame[y1:y2, x1:x2]

                            # Call the check_outfit function and pass the outfit model
                            annotated_image, outfit = check_outfit(crop, outfit_model)

                            # Print the detected outfit information
                            print(f"Detected outfit for {person_id}: {outfit}")

                            # Construct the API URL with query parameters
                            api_url = (
                                f"http://127.0.0.1:5000/employee"
                                f"?top_color_id={outfit['top']['color_id']}"
                                f"&bottom_color_id={outfit['bottom']['color_id']}"
                            )

                            # Make the API call
                            response = requests.get(api_url)

                            # Check the response status
                            if response.status_code == 200:
                                response_json = response.json()
                                if response_json['status'] == 'success' and response_json['data']:
                                    name = response_json['data'][0]['name']
                                    print(f"Detected user: {name}")
                                    cv2.putText(
                                        img, f"{person_id}-{name} {conf:.2f}",
                                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.9, (0, 255, 0), 2
                                    )
                                elif response_json['status'] == 'success' and not response_json['data']:
                                    print("No matching user found.")
                                    cv2.putText(
                                        img, f"{person_id} {conf:.2f}",
                                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.9, (0, 255, 0), 2
                                    )
                                else:
                                    print(f"API call failed with status: {response_json['status']}")
                                    cv2.putText(
                                        img, f"{person_id} {conf:.2f}",
                                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.9, (0, 255, 0), 2
                                    )
                            else:
                                print(f"API call failed with status code: {response.status_code}")
                                cv2.putText(
                                    img, f"{person_id} {conf:.2f}",
                                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9, (0, 255, 0), 2
                                )

                # Update the last processed time
                last_processed_time = current_time

                # Display the frame
                cv2.imshow('Webcam', img)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

# # TESTING
