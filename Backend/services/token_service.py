from repositories import employee_repository, token_repository
from datetime import datetime, timedelta
import random
import string

def generate_token(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_token(data):
    try:
        token_data = {
            'token': generate_token(),
            'employee_id': employee_repository.create_employee(data).get('employee_id'),
            'created_date': datetime.now(),
            'expired_date': datetime.now() + timedelta(minutes=15)
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

def update_token(token_id, data):
    try:
        token = {
            "token" : data.get('token'),
            "employee_id" : data.get('employee_id'),
            "created_date" : data.get('created_date'),
            "expired_date" : data.get('expired_date')
        }

        result = token_repository.update_token_by_id(token_id, token)
        return {"data": token, "status": "success", "message": result["message"]} 
    
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
