from repositories import camera_repository
from datetime import datetime

def create_camera(camera):
    try:
        new_camera = {
            "created_date": datetime.now(),
            "room_id": camera['room_id'],
            "stream_url": camera['stream_url'],
        }
        
        result = camera_repository.create_camera(new_camera)
        new_camera['camera_id'] = result['camera_id']

        created_camera = camera_repository.get_camera_by_id(new_camera['camera_id'])

        return {"data": created_camera['data'], "status": "success", "message": result['message']}
    except KeyError:
        return {"data": None, "status": "error", "message": "Create camera room failed"}

def get_cameras():
    try:
        cameras = camera_repository.get_cameras()
        return {"count": len(cameras['data']), "data": cameras['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Camera rooms not found"}

def get_camera(camera_id):
    try:
        camera = camera_repository.get_camera_by_id(camera_id)
        if camera['data'] is None:
            return {"data": None, "status": "error", "message": "Camera room not found"}

        return {"data": camera['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get camera room failed"}
    
def get_camera_by_name(room_id):
    try:
        existing_camera = camera_repository.get_camera_by(room_id=room_id)
        return {"count": len(existing_camera['data']), "data": existing_camera['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get camera room by name failed"}
    
def update_camera(camera_id, camera):
    try:     
        existing_camera = camera_repository.get_camera_by_id(camera_id)
        if existing_camera['data'] is None:
            return {"data": None, "status": "error", "message": "Camera room not found"}

        updated_camera = {
            "room_id": camera.get('room_id', existing_camera['data']['room_id'])
        }

        result = camera_repository.update_camera_by_id(camera_id, updated_camera)
        updated_data = camera_repository.get_camera_by_id(camera_id)

        return {"data": updated_data['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Update camera room failed"}
    
def delete_camera(camera_id):
    try:
        camera = camera_repository.get_camera_by_id(camera_id)
        if camera['data'] is None:
            return {"status": "error", "message": "Camera room not found"}

        result = camera_repository.delete_camera_by_id(camera_id)
        return {"data": camera['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Delete camera room failed"}
