from repositories import employee_repository
from datetime import datetime

def create_employee(data):
    try:

        employee_data = {
            "current_room_id" : data['current_room_id'],
            "gender" : data['gender'],
            "age" : data['age'],
            "top_color_id" : data['top_color_id'],
            "bottom_color_id" : data['bottom_color_id']
        }
        
        result = employee_repository.create_employee(employee_data)

        employee_data['employee_id'] = result['employee_id']

        return {"data": employee_data, "status": "success", "message": "Employee created successfully!"}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def get_employees():

    employees = employee_repository.get_employees()
    return {"count": len(employees), "data": employees, "status": "success"}

# Retrieve a specific employee
def get_employee(employee_id):
    employee = employee_repository.get_employee_by_id(employee_id)

    return {"data": employee, "status": "success"}

# Update an employee
def update_employee(employee_id, data):

    try:
        employee_data = {
            "current_room_id" : data.get('current_room_id'),
            "gender" : data.get('gender'),
            "age" : data.get('age'),
            "top_color_id" : data.get('top_color_id'),
            "bottom_color_id" : data.get('bottom_color_id')
        }
    
        result = employee_repository.update_employee_by_id(employee_id, employee_data)

        return {"data": employee_data, "status": "success", "message": result["message"]}
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
