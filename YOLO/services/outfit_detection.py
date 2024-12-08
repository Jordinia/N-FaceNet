import cv2
import os
from ultralytics import YOLO

def checkOutfit(crop_resized, person_id):
    """
    Detect outfit components (top, bottom, dress) in a cropped person image
    using a YOLO model and save the detected components.
    
    Args:
        crop_resized: numpy.ndarray of shape (640, 640, 3)
        person_id: string identifier for the person
    """
    # Create outfit directory if it doesn't exist
    outfit_dir = "outfit"
    os.makedirs(outfit_dir, exist_ok=True)
    
    # Load the outfit detection model
    outfit_model = YOLO("../yolo-Weights/topbottom.pt")
    
    # Perform outfit detection
    results = outfit_model.predict(crop_resized)
    
    # Process each detection
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Get class and confidence
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            
            # Get class name
            class_name = ["bottom", "dress", "top"][cls]
            
            # Crop the outfit component
            outfit_crop = crop_resized[y1:y2, x1:x2]
            
            # Generate filename with person ID and outfit class
            filename = f"{outfit_dir}/{person_id}_{class_name}.jpg"
            
            # Draw bounding box on the image
            cv2.rectangle(crop_resized, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(crop_resized, f"{class_name} {conf:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 0, 0), 2)
            
            # Save the cropped outfit component
            cv2.imwrite(filename, outfit_crop)
    
    # Save the annotated full person image with outfit detections
    cv2.imwrite(f"{outfit_dir}/{person_id}_full.jpg", crop_resized)
    
    return crop_resized