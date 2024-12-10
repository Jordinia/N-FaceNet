import os
import json
import pysftp
import requests
import random
import shutil
from functools import wraps

class TokenError(Exception):
    """Custom exception to indicate token-related errors."""
    pass

class ApprovalError(Exception):
    """Custom exception to indicate approval-related errors."""
    pass

def requires_approval(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.is_approved:
            raise ApprovalError("Operation not allowed. Face registration is not approved.")
        return method(self, *args, **kwargs)
    return wrapper

class Face:
    def __init__(self, token):
        self.token = token
        self.employee_id = None
        self.folder_path = None
        self.json_data = None
        self.is_approved = False

        response = self.findToken()

        if response.get("status") == "success" and response.get("data") is not None:
            token_data = response["data"]
            self.employee_id = token_data["employee_id"]
            self.folder_path = f"Employees/{self.employee_id}"
            self.is_approved = token_data["is_approved"]

            os.makedirs(self.folder_path, exist_ok=True)
        else:
            raise TokenError("Invalid or expired token.")

    @requires_approval
    def jsonize(self):
        filenames = os.listdir(self.folder_path)
        images = {f"filename_{i+1}": filename for i, filename in enumerate(filenames)}

        data = {
            "employee_id": self.employee_id,
            "folder_path": self.folder_path,
            "count": len(filenames),
            "images": images
        }

        self.json_data = data
        return data

    @requires_approval
    def upToServer(self):
        sftp_host = "112.78.144.146"
        sftp_username = "jordinia"
        sftp_password = "3701"
        sftp_port = 22098  # Specify the SSH port
        remote_folder = f"Employees/{self.employee_id}"

        # Set up the connection options to ignore host key checking
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Disable host key checking

        # Connect using the specified host, port, username, and password with the connection options
        with pysftp.Connection(host=sftp_host, username=sftp_username, password=sftp_password, port=sftp_port, cnopts=cnopts) as sftp:
            # Check if the remote folder exists, if not create it
            if not sftp.exists(remote_folder):
                sftp.makedirs(remote_folder)

            # Upload all files from the specified local folder
            for filename in os.listdir(self.folder_path):
                local_path = os.path.join(self.folder_path, filename)
                remote_path = f"{remote_folder}/{filename}"
                sftp.put(local_path, remote_path)  # Upload file
                print(f"Uploaded {filename} to {remote_path}")

        return {"status": "success", "message": "All files uploaded successfully."}

    @requires_approval
    def register(self):
        endpoint_url = f"http://127.0.0.1:5000/employee/face/{self.token}"

        response = requests.put(endpoint_url, json=self.json_data)
        return response.json()

    def findToken(self):
        endpoint_url = f"http://127.0.0.1:5000/token/{self.token}"
        try:
            response = requests.get(endpoint_url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Token '{self.token}' is invalid."}
        except requests.RequestException as e:
            raise TokenError(f"Request failed: {str(e)}")

    @requires_approval
    def capture(self):
        source_folder = r"C:\Users\rianr\OneDrive\Gambar\Screenshots"
        destination_folder = self.folder_path

        if not os.path.exists(source_folder):
            raise FileNotFoundError("Source folder not found.")

        images = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        
        if len(images) < 6:
            raise ValueError("Not enough images in the source folder to copy.")

        selected_images = random.sample(images, 6)

        for image in selected_images:
            src = os.path.join(source_folder, image)
            dst = os.path.join(destination_folder, image)
            try:
                shutil.copy2(src, dst)
            except Exception as e:
                raise RuntimeError(f"Failed to copy some images: {e}")

        return {"status": "success", "message": "Images captured successfully."}

if __name__ == "__main__":
    while True:
        try:
            token_input = input("Enter your token: ")
            face = Face(token_input)

            # No need to check approval here since it's handled in the methods directly
            capture_result = face.capture()
            print(capture_result)

            jsonize_result = face.jsonize()
            print(jsonize_result)

            upload_result = face.upToServer()
            print(upload_result)

            register_result = face.register()
            print(register_result)

            print("Face registration completed successfully.")
            break  # Exit the loop if everything is successful

        except TokenError as e:
            print(f"Token error: {e}")
        
        except ApprovalError as e:
            print(f"Approval error: {e}")
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Exit on unexpected errors
