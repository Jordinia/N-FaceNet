from repositories import color_repository

def create_color(Color):
    try:
        existing_color = color_repository.get_color_by(color=Color['color'])
        if len(existing_color['data']) > 0:
            return {"data": None, "status": "error", "message": "Duplicate color"}

        new_Color = {
            "color" : Color['color']
        }
        
        result = color_repository.create_color(new_Color)
        new_Color['color_id'] = result['color_id']

        created_Color = color_repository.get_color_by_id(new_Color['color_id'])

        return {"data": created_Color['data'], "status": "success", "message": result['message']}
    except KeyError:
        return {"data": result, "status": "error", "message": "Create color failed"}

def get_colors():

    try:
        Colors = color_repository.get_colors()
        return {"count": len(Colors['data']), "data": Colors['data'], "status": "success"}
    
    except:
        return {"data": None, "status": "error", "message": "Color not Found"}

def get_color(color_id):
    try:
        Color = color_repository.get_color_by_id(color_id)
        if Color['data'] is None:
            return {"data": None, "status": "error", "message": "Color not Found"}

        return {"data": Color['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get Color failed"}
    
def get_color_by_color(color):
    try:
        existing_Color = color_repository.get_color_by(color=color)
        return {"count": len(existing_Color['data']), "data": existing_Color['data'], "status": "success"}
    except:
        return {"data": None, "status": "error", "message": "Get Color by color failed"}
    
def update_color(color_id, Color):
    try:     
        existing_Color = color_repository.get_color_by_id(color_id)
        if existing_Color['color'] is None:
            return {"data": None, "status": "error", "message": existing_Color['message']}

        new_Color = {
            "color": Color['color'] if Color.get('color') else existing_Color['color'],
            "capacity": Color['capacity'] if Color.get('capacity') else existing_Color['capacity']
        }

        result = color_repository.update_color_by_id(color_id, new_Color)
        updated_color = color_repository.get_color_by_id(color_id)

        return {"color": updated_color['color'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"Color": None, "status": "error", "message": "Update Color failed"}
    
def delete_color(color_id):
    try:
        Color = color_repository.get_color_by_id(color_id)
        result = color_repository.delete_color_by_id(color_id)

        return {"data": Color['data'], "status": "success", "message": result["message"]}
    except KeyError:
        return {"status": "error", "message": "Delete Color failed"} 
