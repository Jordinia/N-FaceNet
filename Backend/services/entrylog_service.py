from repositories import entrylog_repository
from services import employee_service, color_service
from machine_learning import determine_color, determine_employee_id
from datetime import datetime
import pysftp
import os

# Create a new entry
def create_entry(data):
    try:
        entry = {
            "employee_id" : data['employee_id'],
            "checkin_time" : data['checkin_time'],
            "checkout_time" : data['checkout_time']
        }
        
        # Pass data to the repository for saving
        result = entrylog_repository.create_entry(entry)

        return {"status": "success", "message": result}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}
    
def checkin(employee_id, data):
    try:
        face_data = {
            "employee_id": employee_id,
            "faceImagePath": data['faceImagePath'],
        }

        download_face(face_data)

        # Get the employee details
        employee = employee_service.get_employee(employee_id)
        if employee['data'] is None:
            return {"data": None, "status": "error", "message": employee['message']}
        

        # Check if there's an existing entry without a checkout time
        existing_entry = entrylog_repository.get_entry_by(employee_id=employee_id, checkout_time=("IS", None))
        if len(existing_entry['data']) > 0:
            return {"data": None, "status": "error", "message": "Duplicate check-in"}

        # Prepare entry data for check-in
        entry = {
            "employee_id": employee_id,
            "checkin_time": datetime.now(),
            "checkout_time": None
        }

        # Prepare detection data
        detection = {
            "current_room_id": 1,
            "top_color_id": data.get('top_color_id', 1),
            "bottom_color_id": data.get('bottom_color_id', 2),
            "dress_color_id": data.get('dress_color_id', None)
        }

        print('dor')
        # Save the entry and update employee detection data
        result = entrylog_repository.create_entry(entry)
        employee = employee_service.update_employee_detection(employee_id, detection)

        # Add entry ID to the entry object
        entry['entry_id'] = result['entry_id']

        return {"data": {"entry": entry, "employee": employee['data']}, "status": "success", "message": result["message"]}
    
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def checkout(employee_id):
    try:
        existing_employee = employee_service.get_employee(employee_id)
        if existing_employee['data'] == None:
            return {"data": None, "status": "error", "message": existing_employee['message']}
        
        existing_entry = get_entry_by_employee(employee_id)
        if existing_entry['data'] is None:
            return {"data": None, "status": "error", "message": "Employee has not checked in yet"}
        if existing_entry['status'] == "error":
            return {"data": None, "status": "error", "message": existing_entry['message']}

        existing_entry_data = existing_entry['data'][0]

        entry = {
            "entry_id" : existing_entry_data['entry_id'],
            "employee_id" : employee_id,
            "checkin_time" : existing_entry_data['checkin_time'],
            "checkout_time" : datetime.now()
        }

        result = entrylog_repository.update_entry_by_id(entry)
        updated_entry = entrylog_repository.get_entry_by_id(existing_entry_data["entry_id"])
        
        return {"data": updated_entry['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

# Retrieve all entries
def get_entries():
    try:
        entries = entrylog_repository.get_entries()

        return {"count":len(entries['data']), "data": entries['data'], "status": "success"}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

# Retrieve a specific entry
def get_entry(entry_id):
    try:
        entry = entrylog_repository.get_entry_by_id(entry_id)
        if entry['data'] == None:
            return {"data": None, "status": "error", "message": "Entry not found"} 

        return {"data": entry['data'], "status": "success"}
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
    
def get_entry_by_employee(employee_id):
    try:
        employee = employee_service.get_employee(employee_id)
        if employee['data'] == None:
            return {"data": None, "status": "error", "message": employee['message']} 
        
        entry = entrylog_repository.get_entry_by(employee_id=employee_id, checkout_time=("IS", None))
        if len(entry['data']) == 0:
            return {"data": None, "status": "error", "message": "Employee haven't checked in"} 

        return {"data": entry['data'], "status": "success"}
    except KeyError:
        return {"data": None, "status": "error", "message": "Get entry failed"} 

# Update an entry
def update_entry(entry_id, data):
    try:
        entry = {
            "employee_id" : data.get('employee_id'),
            "checkin_time" : data.get('checkin_time'),
            "checkout_time" : data.get('checkout_time')
        }

        result = entrylog_repository.update_entry_by_id(entry_id, entry)
        return {"data": entry, "status": "success", "message": result["message"]} 
    
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 

# Delete an entry
def download_face(face_data):
    # SFTP server credentials
    sftp_host = "112.78.144.146"
    sftp_username = "jordinia"
    sftp_password = "3701"
    sftp_port = 22098  # Specify the SSH port
    
    try:
        # Set up the connection options to ignore host key checking
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Disable host key checking

        # Set up SFTP connection with the specified port
        with pysftp.Connection(host=sftp_host, username=sftp_username, password=sftp_password, port=sftp_port, cnopts=cnopts) as sftp:
            # Extract the remote path from face_data
            remote_file_path = face_data['faceImagePath']  # Example: 'Checkin/2/1733871835419.png'
            
            # Extract the local folder and filename
            local_folder_path = os.path.dirname(remote_file_path)
            local_file_path = os.path.join(local_folder_path, os.path.basename(remote_file_path))

            # Ensure local folder exists
            os.makedirs(local_folder_path, exist_ok=True)

            # Download the file
            print(f"Downloading file from remote path: {remote_file_path}")
            sftp.get(remote_file_path, local_file_path)
            print(f"Downloaded {remote_file_path} to {local_file_path}")

        print("File download completed.")

    except Exception as e:
        print(f"Error: {e}")