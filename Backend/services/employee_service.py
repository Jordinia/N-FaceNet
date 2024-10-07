from repositories import employee_repository
from services import token_service
from datetime import datetime

def create_employee(data):
    try:
        conditions = {"nik": data['nik']}
        existing_employee = employee_repository.get_employee_by(**conditions)
        if existing_employee:
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

        return {"data": employee_data, "authentication": token['data'], "status": "success", "message": "Employee created successfully!"}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def get_employees():

    employees = employee_repository.get_employees()
    return {"count": len(employees), "data": employees, "status": "success"}

# Retrieve a specific employee
def get_employee(employee_id):

    try:
        employee = employee_repository.get_employee_by_id(employee_id)
    except:
        return {"data": None, "status": "error", "message": "Employee not Found"}

    return {"data": employee, "status": "success"}

# Update an employee
def update_employee(employee_id, data):
    
    try:        
        employee_data = {
            "current_room_id" : data['current_room_id'],
            "top_color_id" : data['top_color_id'],
            "bottom_color_id" : data['bottom_color_id'],
            "gender" : data['gender'],
            "name" : data['name'],
            "nik" : data['nik'],
            "role_id" : data['role_id'],
            "face_path" : data['face_path'],
            "age" : data['age']
        }
    
        result = employee_repository.update_employee_by_id(employee_id, employee_data)

        return {"data": employee_data, "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
    
def update_employee_detection(employee_id, data):
    try:        
        employee_existing = employee_repository.get_employee_by_id(employee_id)
        if employee_existing == None:
            return {"status": "error", "message": "Employee not found"}

        employee = {
            "current_room_id" : data['current_room_id'],
            "top_color_id" : data['top_color_id'],
            "bottom_color_id" : data['bottom_color_id'],
            "gender" : employee_existing['gender'],
            "name" : employee_existing['name'],
            "nik" : employee_existing['nik'],
            "role_id" : employee_existing['role_id'],
            "age" : employee_existing['age'],
            "face_path" : employee_existing['face_path']
        }
    
        result = employee_repository.update_employee_by_id(employee_id, employee)

        return {"data": employee, "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
    
def register_employee_face(token, data):
    
    try:
        registration_token = token_service.use_token(token)
        if registration_token['status'] == "error":
            return {"data": None, "status": "error", "message": registration_token['message']}
        
        registration_token_data = registration_token['data']

        employee_existing = employee_repository.get_employee_by_id(registration_token_data['employee_id'])
        if employee_existing == None:
            return {"status": "error", "message": "Employee not found"}

        employee = {
            "face_path" : data['face_path'],
            "current_room_id" : employee_existing['current_room_id'],
            "top_color_id" : employee_existing['top_color_id'],
            "bottom_color_id" : employee_existing['bottom_color_id'],
            "gender" : employee_existing['gender'],
            "name" : employee_existing['name'],
            "nik" : employee_existing['nik'],
            "role_id" : employee_existing['role_id'],
            "age" : employee_existing['age']
        }
    
        result = employee_repository.update_employee_by_id(registration_token_data['employee_id'], employee)

        return {"data": employee, "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

# Delete an employee
def delete_employee(employee_id):
    try:
        employee = get_employee(employee_id)
        result = employee_repository.delete_employee_by_id(employee_id)

        return {"data": employee['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
