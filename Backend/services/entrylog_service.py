from repositories import entrylog_repository
from services import employee_service, color_service
from machine_learning import determine_color, determine_employee_id
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
        
        captured_employee = determine_employee_id()
        face_employee_id = captured_employee['data']['employee_id']

        if employee_id != face_employee_id:
            return {"data": None, "status": "error", "message": "data doesn't match the record"}

        # Get the employee details
        employee = employee_service.get_employee(employee_id)
        if employee['data'] is None:
            return {"data": None, "status": "error", "message": employee['message']}

        # Check if there's an existing entry without a checkout time
        existing_entry = entrylog_repository.get_entry_by(employee_id=employee_id, checkout_time=("IS", None))
        if len(existing_entry['data']) > 0:
            return {"data": None, "status": "error", "message": "Duplicate check-in"}
        
        captured_colors = determine_color()
        data['top_color'] = captured_colors['top_color']
        data['bottom_color'] = captured_colors['bottom_color']

        existing_top_Color = color_service.get_color_by_color(data['top_color'])
        if existing_top_Color['count'] == 0:
            new_Color = {
                "color": data['top_color']
            }
            top_Color = color_service.create_color(new_Color)['data']
        else: 
            top_Color = existing_top_Color['data'][0]

        top_color_id = top_Color['color_id']

        existing_bottom_Color = color_service.get_color_by_color(data['bottom_color'])
        if existing_bottom_Color['count'] == 0:
            new_Color = {
                "color": data['bottom_color']
            }
            bottom_Color = color_service.create_color(new_Color)['data']
        else: 
            bottom_Color = existing_bottom_Color['data'][0]

        bottom_color_id = bottom_Color['color_id']

        # Prepare entry data for check-in
        entry = {
            "employee_id": employee_id,
            "checkin_time": datetime.now(),
            "checkout_time": None
        }

        # Prepare detection data
        detection = {
            "current_room_id": 1,
            "top_color_id": top_color_id,
            "bottom_color_id": bottom_color_id
        }

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
def delete_entry(entry_id):
    try:
        entry = get_entry(entry_id)
        result = entrylog_repository.delete_entry_by_id(entry_id)

        return {"data": entry['data'], "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
