# outfit_detection.py

import cv2
import numpy as np
from ultralytics import YOLO
import time
from color_detection_v4 import get_dominant_color  # Import the function

def check_outfit(image, model):
    """
    Detects outfit components in the input image, identifies the dominant color of each component,
    and returns the annotated image along with the outfit dictionary.

    Parameters:
        image_input (str or numpy.ndarray): Image file path or image array.
        person_id (int or str): Identifier for the person.
        model (YOLO): Loaded YOLO model for outfit detection.

    Returns:
        annotated_image (numpy.ndarray): The image with bounding boxes and labels drawn.
        outfit (dict): Dictionary containing detected outfit components and their color information.
    """
    # Check if input is a file path or image array
    # if isinstance(image_input, str):
    #     # Load the image from file path
    #     image = cv2.imread(image_input)
    #     if image is None:
    #         raise FileNotFoundError(f"Image file not found: {image_input}")
    # elif isinstance(image_input, np.ndarray):
    #     # Use the provided image array
    #     image = image_input.copy()
    # else:
    #     raise ValueError("Input must be a file path or an image array.")
    if isinstance(image, str):
        # Load and resize the image from file path
        image = cv2.imread(image)
    elif not isinstance(image, np.ndarray):
        raise ValueError("Input must be a file path or an image array.")
    # Object classes
    classNames = ["bottom", "dress", "top"]

    # Initialize the outfit dictionary with default values
    outfit = {
        'top': {'color_id': 11, 'rgb': (-1, -1, -1)},
        'bottom': {'color_id': 11, 'rgb': (-1, -1, -1)},
        'dress': {'color_id': 11, 'rgb': (-1, -1, -1)}
    }

    # Run detection
    results = model.predict(image)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Extract bounding box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Extract confidence score
            conf = box.conf[0]
            # Extract class index
            cls = int(box.cls[0])
            class_name = classNames[cls]

            # Crop the detected outfit component
            outfit_crop = image[y1:y2, x1:x2]

            # Get the dominant color
            color_name, color_id, rgb = get_dominant_color(outfit_crop)

            # Update the outfit dictionary
            outfit[class_name] = {'color_id': color_id, 'rgb': tuple(map(int, rgb))}

            # Construct the label with class name and color info
            label = f"{class_name}-{color_name}-{color_id} {conf:.2f}"

            # Draw bounding box and label on the image
            cv2.rectangle(
                image, (x1, y1), (x2, y2), (0, 255, 0), 2
            )
            cv2.putText(
                image, label, (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2
            )

    return image, outfit

# # TESTING
# outfit_model = YOLO("../yolo-Weights/topbottomv2_fp32.engine")
# image_path = "./outfit/contoh/contoh1.png"
# # image_path = "./outfit/contoh/955082.jpg"
# start_time = time.time()
# image, outfit = check_outfit(image_path, outfit_model)
# end_time = time.time()

# print(f"Time taken to call check_outfit: {end_time - start_time:.2f} seconds")
# print(outfit)
# # cv2.imshow("Detected Outfit", image)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()