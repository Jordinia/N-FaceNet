from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
from services import entrylog_service, detectionlog_service, employee_service, token_service, room_service, camera_service
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Standardized response wrapper
def create_response(result):
    response = {
        "status": result['status'],
        "data": result['data'],
        "meta": {
            "request_time": datetime.utcnow().isoformat() + 'Z',
            "version": "1.0.0"
        }
    }

    if result.get('message'):
        response["message"] = result['message']

    if result.get('count') != None:
        response["count"] = result['count']

    if result.get('authentication'):
        response["authentication"] = result['authentication']

    return response

entry_bp = Blueprint('entry', __name__)
detection_bp = Blueprint('detection', __name__)
employee_bp = Blueprint('employee', __name__)
token_bp = Blueprint('token', __name__)
room_bp = Blueprint('room', __name__)
camera_bp = Blueprint('camera', __name__)

class EntryAPI(MethodView):
    def post(self, employee_id):
        data = request.json
        result = entrylog_service.checkin(employee_id, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, employee_id):
        result = entrylog_service.checkout(employee_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, entry_id=None):
        if entry_id is None:
            result = entrylog_service.get_entries()
            return jsonify(create_response(result)), 200 if result['status'] == 'success' else 400
        else:
            result = entrylog_service.get_entry(entry_id)
            return jsonify(create_response(result)), 200 if result['status'] == 'success' else 400
        
    def delete(self, entry_id):
        result = entrylog_service.delete_entry(entry_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

class DetectionAPI(MethodView):
    def post(self, employee_id):
        data = request.json
        result = detectionlog_service.create_detection(employee_id, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, detection_id):
        data = request.json
        result = detectionlog_service.update_detection(detection_id, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, detection_id=None):
        if detection_id is None:
            result = detectionlog_service.get_detections()
            return jsonify(create_response(result)), 200
        else:
            result = detectionlog_service.get_detection(detection_id)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, detection_id):
        result = detectionlog_service.delete_detection(detection_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

class EmployeeAPI(MethodView):
    def post(self):
        data = request.json
        result = employee_service.create_employee(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, token=None, employee_id=None):
        data = request.json
        if employee_id is None:
            result = employee_service.register_employee_face(token, data)
            return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400
        else:
            result = employee_service.update_employee(employee_id, data)
            return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, employee_id=None):
        if employee_id is None:
            gender = request.args.get('gender')
            age = request.args.get('age')
            top_color_id = request.args.get('top_color_id')
            bottom_color_id = request.args.get('bottom_color_id')
            name = request.args.get('name')
            current_room_id = request.args.get('current_room_id')
            nik = request.args.get('nik')

            if gender is None and age is None and top_color_id is None and bottom_color_id is None and name is None and current_room_id is None and nik is None:
                result = employee_service.get_employees()
            else:
                result = employee_service.get_employee_by_params(gender, age, top_color_id, bottom_color_id, current_room_id, name, nik)
            print(result)
            return jsonify(create_response(result)), 200
        else:
            result = employee_service.get_employee(employee_id)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, employee_id):
        result = employee_service.delete_employee(employee_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400

class TokenAPI(MethodView):
    def post(self, employee_id):
        result = token_service.create_token(employee_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, token_id):
        result = token_service.approve_token(token_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, token_id=None, token=None):
        if token_id is None and token is None:
            result = token_service.get_approval_token()
            return jsonify(create_response(result)), 200
        elif token_id is not None:
            result = token_service.get_token(token_id)
            return jsonify(create_response(result)), 200 if result else 404
        elif token is not None:
            result = token_service.get_available_token_by_token(token)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, token_id):
        result = token_service.delete_token(token_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400
    
class RoomAPI(MethodView):
    def post(self):
        data = request.json
        result = room_service.create_room(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, room_id):
        data = request.json
        result = room_service.update_room(room_id, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, room_id=None):
        if room_id is None:
            result = room_service.get_rooms()
            return jsonify(create_response(result)), 200
        else:
            result = room_service.get_room(room_id)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, room_id):
        result = room_service.delete_room(room_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400
    
class CameraAPI(MethodView):
    def post(self):
        data = request.json
        result = camera_service.create_camera(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, camera_id):
        data = request.json
        result = camera_service.update_camera(camera_id, data)
        return jsonify(create_response(result)), 200 if result['status'] == 'success' else 400

    def get(self, camera_id=None, room_id=None):
        if camera_id is None and room_id is None:
            result = camera_service.get_cameras()
            return jsonify(create_response(result)), 200
        elif room_id is None:
            result = camera_service.get_camera(camera_id)
            return jsonify(create_response(result)), 200 if result['status'] == 'success' else 404
        elif camera_id is None:
            result = camera_service.get_camera_by_room(room_id)
            return jsonify(create_response(result)), 200 if result['status'] == 'success' else 404
        
    def delete(self, camera_id):
        result = camera_service.delete_camera(camera_id)
        return jsonify(create_response(result)), 200 if result['status'] == 'success' else 400

# Register the EntryAPI view
entry_view = EntryAPI.as_view('entry_api')
entry_bp.add_url_rule('/checkin/<int:employee_id>', view_func=entry_view, methods=['POST'])
entry_bp.add_url_rule('/checkout/<int:employee_id>', view_func=entry_view, methods=['PUT'])
entry_bp.add_url_rule('', view_func=entry_view, methods=['POST', 'GET'])
entry_bp.add_url_rule('/<int:entry_id>', view_func=entry_view, methods=['GET', 'PUT', 'DELETE'])

# Register the DetectionAPI view
detection_view = DetectionAPI.as_view('detection_api')
detection_bp.add_url_rule('', view_func=detection_view, methods=['GET'])
detection_bp.add_url_rule('/<int:detection_id>', view_func=detection_view, methods=['GET', 'PUT', 'DELETE'])
detection_bp.add_url_rule('/employee/<int:employee_id>', view_func=detection_view, methods=['GET', 'POST'])

# Register the EmployeeAPI view
employee_view = EmployeeAPI.as_view('employee_api')
employee_bp.add_url_rule('', view_func=employee_view, methods=['POST', 'GET'])
employee_bp.add_url_rule('/<int:employee_id>', view_func=employee_view, methods=['GET', 'DELETE', 'PUT'])
employee_bp.add_url_rule('/face/<string:token>', view_func=employee_view, methods=['PUT'])

# Register the RoomAPI view
room_view = RoomAPI.as_view('room_api')
room_bp.add_url_rule('', view_func=room_view, methods=['POST', 'GET'])
room_bp.add_url_rule('/<int:room_id>', view_func=room_view, methods=['GET', 'DELETE', 'PUT'])

# Register the CameraPI view
camera_view = CameraAPI.as_view('camera_api')
camera_bp.add_url_rule('', view_func=camera_view, methods=['POST', 'GET'])
camera_bp.add_url_rule('room/<int:room_id>', view_func=camera_view, methods=['GET'])
camera_bp.add_url_rule('/<int:camera_id>', view_func=camera_view, methods=['GET', 'DELETE', 'PUT'])

# Register the TokenAPI view
token_view = TokenAPI.as_view('token_api')
token_bp.add_url_rule('', view_func=token_view, methods=['GET'])
token_bp.add_url_rule('<string:token>', view_func=token_view, methods=['GET'])
token_bp.add_url_rule('/<int:employee_id>', view_func=token_view, methods=['POST'])
token_bp.add_url_rule('/<int:token_id>', view_func=token_view, methods=['GET', 'PUT', 'DELETE'])
token_bp.add_url_rule('/token/<int:token_id>', view_func=token_view, methods=['GET'])

# Register the blueprint in your main app
app.register_blueprint(entry_bp, url_prefix='/entry')
app.register_blueprint(detection_bp, url_prefix='/detection')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(token_bp, url_prefix='/token')
app.register_blueprint(room_bp, url_prefix='/room')
app.register_blueprint(camera_bp, url_prefix='/camera')

if __name__ == '__main__':
    app.run(debug=True)