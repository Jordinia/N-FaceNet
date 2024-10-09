from repositories import room_repository

def create_room(Room):
    try:
        existing_Room = room_repository.get_room_by(room=Room['room'])
        if len(existing_Room['data']) > 0:
            return {"data": None, "status": "error", "message": "Duplicate room"}

        new_Room = {
            "room" : Room['room'],
            "capacity" : Room['capacity']
        }
        
        result = room_repository.create_room(new_Room)
        new_Room['room_id'] = result['room_id']

        created_Room = room_repository.get_room_by_id(new_Room['room_id'])

        return {"data": created_Room['data'], "status": "success"}
    except Exception as e:
        return {"data": None, "status": "error", "message": f"{str(e)}"}

def get_rooms():
    try:
        Rooms = room_repository.get_rooms()
        return {"count": len(Rooms['data']), "data": Rooms['data'], "status": "success"}
    
    except:
        return {"data": None, "status": "error", "message": "Room not Found"}

def get_room(room_id):
    try:
        Room = room_repository.get_room_by_id(room_id)
        if Room['data'] == None:
            return {"data": None, "status": "error", "message": "Room not Found"}

        return {"data": Room['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get Room failed"}
    
def update_room(room_id, Room):
    try:     
        existing_Room = room_repository.get_room_by_id(room_id)
        if existing_Room['data'] == None:
            return {"data": None, "status": "error", "message": existing_Room['message']}

        new_Room = {
            "room": Room['room'] if Room.get('room') else existing_Room['room'],
            "capacity": Room['capacity'] if Room.get('capacity') else existing_Room['capacity']
        }

        result = room_repository.update_room_by_id(room_id, new_Room)
        updated_Room = room_repository.get_room_by_id(room_id)

        return {"data": updated_Room['data'], "status": "success", "message": result["message"]}
    except Exception as e:
        return {"data": None, "status": "error", "message": f"{str(e)}"}
    
def delete_room(room_id):
    try:
        Room = room_repository.get_room_by_id(room_id)
        result = room_repository.delete_room_by_id(room_id)

        return {"data": Room['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"data": None, "status": "error", "message": "Delete Room failed"} 
