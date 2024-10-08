from repositories import employee_repository, token_repository
from datetime import datetime, timedelta
import random
import string

def generate_token(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_token(employee_id):
    try:
        token_data = {
            'token': generate_token(),
            'employee_id': employee_id,
            'created_date': datetime.now(),
            'expired_date': datetime.now() + timedelta(minutes=15),
            'is_approved': 0
        }
        
        result = token_repository.create_token(token_data)
        token_data['token_id'] = result['token_id']

        return {"data": token_data, "status": "success", "message": result.get('message')}
    
    except KeyError as e:
        return {"data": token_data, "status": "error", "message": f"Invalid data: {str(e)}"}
    
    except Exception as e:
        return {"data": token_data, "status": "error", "message": f"An error occurred: {str(e)}"}

def get_tokens():
    try:
        tokens = token_repository.get_tokens()

        return {"count":len(tokens), "data": tokens, "status": "success"}
    except KeyError:
        return {"status": "error", "message": "Invalid data"}

def get_token(token_id):
    try:
        token = token_repository.get_token_by_id(token_id)

        return {"data": token, "status": "success"}
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
    
def use_token(token):
    try:
        token = token_repository.get_token_by(token=token)
        if token['status'] == "error":
            return {"status": "error", "message": token['message']}
        if token['data'] == None:
            return {"status": "error", "message": "Token not found"}
        
        token_data = token['data']
        
        if token_data['is_approved'] == 0:
            return {"status": "error", "message": "Token haven't been approved"}
        if token_data['expired_date'] < datetime.now():
            return {"status": "error", "message": "Token already expired"}

        token_data['expired_date'] = datetime.now()
        result = token_repository.update_token_by_id(token_data['token_id'], token_data)

        return {"data": token_data, "status": "success", "message": result["message"]} 
    except:
        return {"data": None, "status": "error", "message": "Use token failed"}

def update_token(token_id, data):
    try:
        token = {
            "token" : data.get('token'),
            "employee_id" : data.get('employee_id')
        }

        result = token_repository.update_token_by_id(token_id, token)

        token['token_id'] = token_id

        return {"data": token, "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
    
def approve_token(token_id):
    try:
        token = token_repository.get_token_by_id(token_id)
        if token['data'] == None:
            return {"data": None, "status": "error", "message": "Token not found"}
        
        token_data = token['data']

        token_data['is_approved'] = 1
        result = token_repository.update_token_by_id(token_id, token_data)

        return {"data": token_data, "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
    
# Delete an token
def delete_token(token_id):
    try:
        token = get_token(token_id)
        result = token_repository.delete_token_by_id(token_id)

        return {"data": token['data'], "status": "success", "message": result["message"]} 
    except KeyError:
        return {"status": "error", "message": "Invalid data"} 
