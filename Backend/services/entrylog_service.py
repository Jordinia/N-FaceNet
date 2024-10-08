from repositories import entrylog_repository
from services import employee_service
from datetime import datetime

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
        # Get the employee details
        employee = employee_service.get_employee(employee_id)
        if employee['data'] is None:
            return {"data": None, "status": "error", "message": employee['message']}

        # Check if there's an existing entry without a checkout time
        existing_entry = entrylog_repository.get_entry_by(employee_id=employee_id, checkout_time=("IS", None))
        if existing_entry['data']:
            return {"data": None, "status": "error", "message": "Duplicate check-in"}

        # Prepare entry data for check-in
        entry = {
            "employee_id": employee_id,
            "checkin_time": datetime.now(),
            "checkout_time": None
        }

        # Prepare detection data
        detection = {
            "current_room_id": 1,  # Example: hardcoded room, can be dynamic
            "top_color_id": data['top_color_id'],
            "bottom_color_id": data['bottom_color_id']
        }

        # Save the entry and update employee detection data
        result = entrylog_repository.create_entry(entry)
        employee = employee_service.update_employee_detection(employee_id, detection)

        # Add entry ID to the entry object
        entry['entry_id'] = result['entry_id']

        return {"data": {"entry": entry, "employee": employee['data']}, "status": "success", "message": result["message"]}
    
    except KeyError:
        return {"data": employee, "status": "error", "message": "Invalid data"}

def checkout(employee_id):
    try:
        existing_employee = employee_service.get_employee(employee_id)
        if existing_employee['data'] == None:
            return {"data": None, "status": "error", "message": existing_employee['message']}
        
        existing_entry = entrylog_repository.get_entry_by(employee_id=employee_id, checkout_time=("IS", None))
        if existing_entry['data'] == None:
            return {"data": None, "status": "error", "message": "Employee has not checked in yet"}
        if existing_entry['status'] == "error":
            return {"data": None, "status": "error", "message": existing_entry['message']}

        existing_entry_data = existing_entry['data']

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
        return {"data": existing_entry, "status": "error", "message": "Invalid data"}

# Retrieve all entries
def get_entries():
    try:
        entries = entrylog_repository.get_entries()

        return {"count":len(entries), "data": entries, "status": "success"}
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
        if entry['data'] == None:
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
def delete_entry(entry_id):
    try:
        entry = get_entry(entry_id)
        result = entrylog_repository.delete_entry_by_id(entry_id)

        return {"data": entry['data'], "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
