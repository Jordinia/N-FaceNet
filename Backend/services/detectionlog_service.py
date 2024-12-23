from repositories import detectionlog_repository
from services import entrylog_service, employee_service, camera_service
from datetime import datetime

def create_detection(employee_id, Detection):
    try:
        existing_entry = entrylog_service.get_entry_by_employee(employee_id)
        if existing_entry['data'] == None:
            return {"data": None, "status": "error", "message": existing_entry['message']}
        
        camera_id = Detection['camera_id']
        
        Camera = camera_service.get_camera(camera_id)
        if Camera['data'] == None:
            return {"data": None, "status": "error", "message": Camera['message']}
        
        camera_data = Camera['data']

        detection = {
            "camera_id" : Detection['camera_id'],
            "employee_id" : employee_id,
            "room_id" : camera_data['room_id'],
            "timestamp" : datetime.now(),
        }

        detected_employee = {
            "current_room_id" : camera_data['room_id']
        }
        updated_employee = employee_service.update_employee(employee_id, detected_employee)
        if updated_employee['data'] == None:
            return {"data": None, "status": "error", "message": updated_employee['message']}
        
        result = detectionlog_repository.create_detection(detection)
        created_detection = detectionlog_repository.get_detection_by_id(result['detection_id'])

        return {"data": created_detection['data'], "status": "success", "message": result['message']}
    except KeyError:
        return {"data": result, "status": "error", "message": result['message']}

def get_detections():
    try:
        detections = detectionlog_repository.get_detections()

        return {"count":len(detections['data']), "data": detections['data'], "status": "success"}
    
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
     
def get_detection(detection_id):
    try:
        detection = detectionlog_repository.get_detection_by_id(detection_id)
        if detection['data'] == None:
            return {"data": None, "status": "error", "message": "Detection not found"}

        return {"data": detection['data'], "status": "success"}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def update_detection(detection_id, data):
    try:
        existing_employee = employee_service.get_employee(data['employee_id'])
        if existing_employee['data'] == None:
            return {"data": None, "status": "error", "message": existing_employee['message']}
        
        detection = {
            "camera_id" : data['camera_id'],
            "employee_id" : data['employee_id'],
            "room_id" : data['room_id'],
            "confidence" : data['confidence']
        }
    
        result = detectionlog_repository.update_detection_by_id(detection_id, detection)
        updated_detection = get_detection(detection_id)

        return {"data": updated_detection['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

def delete_detection(detection_id):
    try:
        detection = get_detection(detection_id)
        result = detectionlog_repository.delete_detection_by_id(detection_id)

        return {"data": detection['data'], "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
