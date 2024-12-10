import time
import requests

def post_employee_detection(camera):
    url = "http://localhost:5000/detection/employee/2"
    payload = {
        "camera_id": 2,
        "confidence": 0.993754
    }

    try:
        while True:
            response = requests.post(url, json=payload)
            print(f"Camera {camera['camera_id']} Posted to {url}, status code: {response.status_code}")
            time.sleep(10)  # Wait for 5 seconds before the next POST
    except KeyboardInterrupt:
        print("Loop stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
