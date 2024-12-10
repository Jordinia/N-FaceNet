from repositories import employee_repository
from services import token_service
from datetime import datetime
import pysftp
import os

def create_employee(data):
    try:
        conditions = {"nik": data['nik']}
        existing_employee = employee_repository.get_employee_by(**conditions)
        if len(existing_employee['data']) > 0:
            return {"data": None, "status": "error", "message": "Duplicate NIK"}

        employee_data = {
            "nik" : data['nik'],
            "name" : data['name'],
            "gender" : data['gender'],
            "age" : data['age'],
            "role_id" : 1,
            "current_room_id" : None,
            "top_color_id" : None,
            "bottom_color_id" : None,
            "face_path" : None,
        }
        
        result = employee_repository.create_employee(employee_data)

        employee_data['employee_id'] = result['employee_id']

        token = token_service.create_token(result['employee_id'])

        return {"data": employee_data, "authentication": token['data'], "status": "success", "message": result['message']}
    except KeyError:
        return {"data": None, "status": "error", "message": result['message']}

def get_employees():

    try:
        employees = employee_repository.get_employees()
        
        return {"count": len(employees['data']), "data": employees['data'], "status": "success"}
    
    except:
        return {"data": None, "status": "error", "message": employees['message']}

# Retrieve a specific employee
def get_employee(employee_id):
    try:
        employee = employee_repository.get_employee_by_id(employee_id)
        if employee['data'] == None:
            return {"data": None, "status": "error", "message": "Employee not Found"}

        return {"data": employee['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get employee failed"}
    
def get_employee_by_params(gender=None, age=None, top_color_id=None, bottom_color_id=None, current_room_id=None, name=None, nik=None):
    try:

        print(current_room_id)
        params = {}
        if gender is not None: 
            params['gender'] = gender
        if age is not None:
            params['age'] = age
        if top_color_id is not None:
            params['top_color_id'] = top_color_id
        if bottom_color_id is not None:
            params['bottom_color_id'] = bottom_color_id
        if current_room_id is not None:
            params['current_room_id'] = current_room_id
        if name is not None:
            params['name'] = name
        if nik is not None:
            params['nik'] = nik

        existing_employee = employee_repository.get_employee_by(**params)
        
        if existing_employee['data'] == []:
            return {"count": 0, "data": existing_employee['data'], "status": existing_employee['status'], "message": "No employee found with the provided parameters"}
        else:
            return {"count":len(existing_employee['data']), "data": existing_employee['data'], "status": existing_employee['status']}
    except Exception as e:
        return {"data": None, "status": "error", "message": str(e)}

# Update an employee
def update_employee(employee_id, data):
    
    try:     
        existing_employee = employee_repository.get_employee_by_id(employee_id)
        if existing_employee['data'] == None:
            return {"data": None, "status": "error", "message": existing_employee['message']}
        
        existing_employee_data = existing_employee['data']

        employee_data = {
            "current_room_id": data['current_room_id'] if data.get('current_room_id') else existing_employee_data['current_room_id'],
            "top_color_id": data['top_color_id'] if data.get('top_color_id') else existing_employee_data['top_color_id'],
            "bottom_color_id": data['bottom_color_id'] if data.get('bottom_color_id') else existing_employee_data['bottom_color_id'],
            "gender": data['gender'] if data.get('gender') else existing_employee_data['gender'],
            "name": data['name'] if data.get('name') else existing_employee_data['name'],
            "nik": data['nik'] if data.get('nik') else existing_employee_data['nik'],
            "role_id": data['role_id'] if data.get('role_id') else existing_employee_data['role_id'],
            "face_path": data['face_path'] if data.get('face_path') else existing_employee_data['face_path'],
            "age": data['age'] if data.get('age') else existing_employee_data['age']
        }

        result = employee_repository.update_employee_by_id(employee_id, employee_data)
        updated_employee = employee_repository.get_employee_by_id(employee_id)

        return {"data": updated_employee['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
    
def update_employee_detection(employee_id, data):
    try:        
        existing_employee = employee_repository.get_employee_by_id(employee_id)
        if existing_employee['data'] == None:
            return {"status": "error", "message": "Employee not found"}

        existing_employee_data = existing_employee['data']

        employee = {
            "current_room_id" : data['current_room_id'],
            "top_color_id" : data['top_color_id'],
            "bottom_color_id" : data['bottom_color_id'],
            "gender" : existing_employee_data['gender'],
            "name" : existing_employee_data['name'],
            "nik" : existing_employee_data['nik'],
            "role_id" : existing_employee_data['role_id'],
            "age" : existing_employee_data['age'],
            "face_path" : existing_employee_data['face_path']
        }
    
        result = employee_repository.update_employee_by_id(employee_id, employee)
        updated_employee = employee_repository.get_employee_by_id(employee_id)

        return {"data": updated_employee['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
    
def register_employee_face(token, data):
    try:
        registration_token = token_service.use_token(token)
        if registration_token['status'] == "error":
            return {"data": None, "status": "error", "message": registration_token['message']}
        
        registration_token_data = registration_token['data']

        employee_existing = employee_repository.get_employee_by_id(registration_token_data['employee_id'])
        if employee_existing['data'] == None:
            return {"status": "error", "message": "Employee not found"}

        employee_existing_data = employee_existing['data']
        download_face(data)

        employee = {
            "face_path" : data['folder_path'],
            "current_room_id" : employee_existing_data['current_room_id'],
            "top_color_id" : employee_existing_data['top_color_id'],
            "bottom_color_id" : employee_existing_data['bottom_color_id'],
            "gender" : employee_existing_data['gender'],
            "name" : employee_existing_data['name'],
            "nik" : employee_existing_data['nik'],
            "role_id" : employee_existing_data['role_id'],
            "age" : employee_existing_data['age']
        }
    
        result = employee_repository.update_employee_by_id(registration_token_data['employee_id'], employee)
        updated_employee = employee_repository.get_employee_by_id(employee_existing_data['employee_id'])

        return {"data": updated_employee['data'], "status": "success", "message": "Face registered succesfully"}
    except KeyError:
        return {"data": registration_token, "status": "error", "message": "Register Employee Face Failed"}

def download_face(face_data):
    # SFTP server credentials
    sftp_host = "112.78.144.146"
    sftp_username = "jordinia"
    sftp_password = "3701"
    sftp_port = 22098  # Specify the SSH port
    
    # Local and remote paths
    remote_folder_path = face_data['folder_path']
    local_folder_path = f"Employees/{face_data['employee_id']}"
    
    # List of filenames to download
    filenames = [filename for filename in face_data['images'].values()]

    try:
        # Set up the connection options to ignore host key checking
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  # Disable host key checking

        # Set up SFTP connection with the specified port
        with pysftp.Connection(host=sftp_host, username=sftp_username, password=sftp_password, port=sftp_port, cnopts=cnopts) as sftp:
            # Ensure local folder exists
            os.makedirs(local_folder_path, exist_ok=True)
            
            # Download each file from the remote server
            for filename in filenames:
                remote_file_path = f"{remote_folder_path}/{filename}"
                local_file_path = f"{local_folder_path}/{filename}"

                print(remote_file_path)
                
                # Download the file
                sftp.get(remote_file_path, local_file_path)
                print(f"Downloaded {filename} to {local_file_path}")

        print("All files downloaded successfully.")

    except Exception as e:
        print(f"Error downloading files: {e}")

# Delete an employee
def delete_employee(employee_id):
    try:
        employee = get_employee(employee_id)
        result = employee_repository.delete_employee_by_id(employee_id)

        return {"data": employee['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
