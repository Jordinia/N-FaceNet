from repositories import entrylog_repository
from datetime import datetime

# Create a new entry
def create_entry(data):
    try:
        employee_id = data['employee_id']
        checkin_time = data.get('checkin_time')
        checkout_time = data.get('checkout_time')
        
        # Pass data to the repository for saving
        result = entrylog_repository.create_entry(employee_id, checkin_time, checkout_time)
        return {"status": "success", "message": result}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}
    
def checkin(data):
    try:

        entry = {
            "employee_id" : data['employee_id'],
            "checkin_time" : datetime.now(),
            "checkout_time" : None
        }

        # Pass data to the repository for saving
        result = entrylog_repository.create_entry(entry)

        entry['entry_id'] = result['entry_id']
        
        return {"data": entry, "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}
    
def checkout(data):
    try:
        employee_id = data['employee_id']

        conditions = {"employee_id": employee_id}

        result = entrylog_repository.get_entry_by(**conditions)

        entry = {
            "entry_id" : result["entry_id"],
            "employee_id" : employee_id,
            "checkin_time" : result['checkin_time'],
            "checkout_time" : datetime.now()
        }

        result = entrylog_repository.update_entry_by_id(entry)
        
        return {"data": entry, "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

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

        return {"data": entry, "status": "success"}
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 

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
