import cv2
from ultralytics import YOLO
import time
import os
import requests
from outfit_detection_v2 import check_outfit  # Import the check_outfit function

def process_camera_stream(cam_id: int, cam_url: str):
    """
    Processes the video stream from a camera, detects persons and their outfits,
    and displays the annotated video with detections.

    Parameters:
        cam_id (int): The ID of the camera.
        cam_url (str): The URL of the video stream.
    """

    # Load the YOLO models
    person_model = YOLO("../yolo-Weights/yolo11m.engine")
    outfit_model = YOLO("../yolo-Weights/topbottomv2_fp32.engine")

    # Open the video stream
    cap = cv2.VideoCapture(cam_url)
    if not cap.isOpened():
        print(f"Error: Could not open video stream from URL: {cam_url}")
        return

    # Create output directory for cropped images
    output_dir = "detected_persons"
    os.makedirs(output_dir, exist_ok=True)

    # Create a resizable window
    window_name = f'Webcam_{cam_id}'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Variables for frame processing
    last_processed_time = time.time()
    process_interval = 0.3  # Time interval between processing frames in seconds

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Could not read frame.")
            break
        
        img = cv2.resize(img, (640, 480))
        current_time = time.time()
        elapsed_time = current_time - last_processed_time

        # Check if it's time to process the next frame
        if elapsed_time >= process_interval:
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
                        crop = img[y1:y2, x1:x2]

                        # Call the check_outfit function and pass the outfit model
                        annotated_image, outfit = check_outfit(crop, outfit_model)

                        # Print the detected outfit information
                        print(f"Detected outfit for {person_id}: {outfit}")

                        # Construct the API URL with query parameters
                        if outfit['dress']['color_id'] == 11:
                            api_url = (
                                f"http://127.0.0.1:5000/employee"
                                f"?top_color_id={outfit['top']['color_id']}"
                                f"&bottom_color_id={outfit['bottom']['color_id']}"
                            )
                        elif outfit['top']['color_id'] == 11 and outfit['bottom']['color_id'] == 11:
                            api_url = (
                                f"http://127.0.0.1:5000/employee"
                                f"?dress_color_id={outfit['dress']['color_id']}"
                            )
                        else:
                            api_url = (
                                f"http://127.0.0.1:5000/employee"
                                f"?top_color_id={outfit['top']['color_id']}"
                                f"&bottom_color_id={outfit['bottom']['color_id']}"
                            )

                        # Make the GET API call
                        response = requests.get(api_url)

                        # Check the response status
                        if response.status_code == 200:
                            response_json = response.json()
                            if response_json['status'] == 'success' and response_json['data']:
                                # Extract employee information
                                employee_data = response_json['data'][0]
                                name = employee_data['name']
                                employee_id = employee_data['employee_id']

                                # Construct the POST API URL
                                api_url = f"http://100.71.234.28:5000/detection/employee/{employee_id}"

                                # Prepare the JSON data for POST request
                                post_data = {
                                    "camera_id": cam_id
                                }

                                # Make the POST API call
                                post_response = requests.post(api_url, json=post_data)

                                # Check the POST response status
                                if post_response.status_code == 200:
                                    post_response_json = post_response.json()
                                    if post_response_json['status'] == 'success':
                                        # Successful detection and recording
                                        print(f"Detected user: {name}")
                                        cv2.putText(
                                            img, f"{person_id}-{name} {conf:.2f}",
                                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.9, (0, 255, 0), 2
                                        )
                                    else:
                                        # User hasn't checked in or other error
                                        print("No matching user found.")
                                        cv2.putText(
                                            img, f"{person_id} {conf:.2f}",
                                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.9, (0, 0, 255), 2  # Use red color to indicate an issue
                                        )
                                else:
                                    print(f"POST API call failed with status code: {post_response.status_code}")
                                    cv2.putText(
                                        img, f"{person_id} {conf:.2f}",
                                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.9, (0, 0, 255), 2
                                    )
                            else:
                                # No matching user found in GET request
                                print("No matching user found.")
                                cv2.putText(
                                    img, f"{person_id} {conf:.2f}",
                                    (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9, (0, 0, 255), 2
                                )
                        else:
                            print(f"GET API call failed with status code: {response.status_code}")
                            cv2.putText(
                                img, f"{person_id} {conf:.2f}",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.9, (0, 0, 255), 2
                            )

                # Update the last processed time
                last_processed_time = current_time

        # Display the frame
        cv2.imshow(window_name, img)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    cam_id = 1
    # cam_url = "http://100.111.29.103:4747/video"
    cam_url = "rtsp://100.79.3.2:1945/"
    process_camera_stream(cam_id, cam_url)