from repositories import detectionlog_repository
from datetime import datetime

def create_detection(data):
    try:
        detection = {
            "camera_id" : data['camera_id'],
            "employee_id" : data['employee_id'],
            "room_id" : data['room_id'],
            "timestamp" : datetime.now(),
            "confidence" : data['confidence']
        }
        
        result = detectionlog_repository.create_detection(detection)
        detection['detection_id'] = result['detection_id']

        return {"data": detection, "status": "success", "message": result['message']}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def get_detections():
    try:
        detections = detectionlog_repository.get_detections()

        return {"count":len(detections), "data": detections, "status": "success"}
    
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}
     
def get_detection(detection_id):
    try:
        detection = detectionlog_repository.get_detection_by_id(detection_id)

        return {"data": detection, "status": "success"}
    except KeyError:
        return {"data": None, "status": "error", "message": "Invalid data"}

def update_detection(detection_id, data):
    try:
        detection = {
            "camera_id" : data.get('camera_id'),
            "employee_id" : data.get('employee_id'),
            "room_id" : data.get('room_id'),
            "confidence" : data.get('confidence')
        }
    
        result = detectionlog_repository.update_detection_by_id(detection_id, detection)

        return {"data": detection, "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

def delete_detection(detection_id):
    try:
        detection = get_detection(detection_id)
        result = detectionlog_repository.delete_detection_by_id(detection_id)

        return {"data": detection['data'], "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
