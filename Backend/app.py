from flask import Flask, request, jsonify, Blueprint
from flask.views import MethodView
from services import entrylog_service, detectionlog_service, employee_service, token_service
from datetime import datetime

app = Flask(__name__)

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

    if result.get('count'):
        response["count"] = result['count']

    if result.get('authentication'):
        response["authentication"] = result['authentication']

    return response

entry_bp = Blueprint('entry', __name__)
detection_bp = Blueprint('detection', __name__)
employee_bp = Blueprint('employee', __name__)
token_bp = Blueprint('registrationToken', __name__)

class EntryAPI(MethodView):
    def post(self):
        data = request.json
        result = entrylog_service.checkin(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self):
        data = request.json
        result = entrylog_service.checkout(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, entry_id=None):
        if entry_id is None:
            result = entrylog_service.get_entries()
            return jsonify(result), 200
        else:
            result = entrylog_service.get_entry(entry_id)
            return jsonify(result), 200 if result else 404
        
    def delete(self, entry_id):
        result = entrylog_service.delete_entry(entry_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400

class DetectionAPI(MethodView):
    def post(self):
        data = request.json
        result = detectionlog_service.create_detection(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, detection_id):
        data = request.json
        result = detectionlog_service.update_detection(detection_id, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, detection_id=None):
        if detection_id is None:
            result = detectionlog_service.get_detections()
            return jsonify(result), 200
        else:
            result = detectionlog_service.get_detection(detection_id)
            return jsonify(result), 200 if result else 404
        
    def delete(self, detection_id):
        result = detectionlog_service.delete_detection(detection_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400

class EmployeeAPI(MethodView):
    def post(self):
        data = request.json
        result = employee_service.create_employee(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, token):
        data = request.json
        result = employee_service.register_employee_face(token, data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, employee_id=None):
        if employee_id is None:
            result = employee_service.get_employees()
            return jsonify(create_response(result)), 200
        else:
            result = employee_service.get_employee(employee_id)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, employee_id):
        result = employee_service.delete_employee(employee_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400

class TokenAPI(MethodView):
    def post(self):
        data = request.json
        result = token_service.create_token(data)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def put(self, token_id):
        result = token_service.approve_token(token_id)
        return jsonify(create_response(result)), 201 if result['status'] == 'success' else 400

    def get(self, token_id=None):
        if token_id is None:
            result = token_service.get_tokens()
            return jsonify(create_response(result)), 200
        else:
            result = token_service.get_token(token_id)
            return jsonify(create_response(result)), 200 if result else 404
        
    def delete(self, token_id):
        result = token_service.delete_token(token_id)
        return jsonify(result), 201 if result['status'] == 'success' else 400

# Register the EntryAPI view
entry_view = EntryAPI.as_view('entry_api')
entry_bp.add_url_rule('/checkin', view_func=entry_view, methods=['POST'])
entry_bp.add_url_rule('/checkout', view_func=entry_view, methods=['PUT'])
entry_bp.add_url_rule('', view_func=entry_view, methods=['POST', 'GET'])
entry_bp.add_url_rule('/<int:entry_id>', view_func=entry_view, methods=['GET', 'PUT', 'DELETE'])

# Register the DetectionAPI view
detection_view = DetectionAPI.as_view('detection_api')
detection_bp.add_url_rule('', view_func=detection_view, methods=['POST', 'GET'])
detection_bp.add_url_rule('/<int:detection_id>', view_func=detection_view, methods=['GET', 'PUT', 'DELETE'])
detection_bp.add_url_rule('/employee/<int:employee_id>', view_func=detection_view, methods=['GET'])

# Register the EmployeeAPI view
employee_view = EmployeeAPI.as_view('employee_api')
employee_bp.add_url_rule('', view_func=employee_view, methods=['POST', 'GET'])
employee_bp.add_url_rule('/<int:employee_id>', view_func=employee_view, methods=['GET', 'DELETE'])
employee_bp.add_url_rule('/<string:token>', view_func=employee_view, methods=['PUT'])
employee_bp.add_url_rule('/employee/<int:employee_id>', view_func=employee_view, methods=['GET'])

# Register the TokenAPI view
token_view = TokenAPI.as_view('token_api')
token_bp.add_url_rule('', view_func=token_view, methods=['POST', 'GET'])
token_bp.add_url_rule('/<int:token_id>', view_func=token_view, methods=['GET', 'PUT', 'DELETE'])
token_bp.add_url_rule('/token/<int:token_id>', view_func=token_view, methods=['GET'])

# Register the blueprint in your main app
app.register_blueprint(entry_bp, url_prefix='/entry')
app.register_blueprint(detection_bp, url_prefix='/detection')
app.register_blueprint(employee_bp, url_prefix='/employee')
app.register_blueprint(token_bp, url_prefix='/token')

if __name__ == '__main__':
    app.run(debug=True)
