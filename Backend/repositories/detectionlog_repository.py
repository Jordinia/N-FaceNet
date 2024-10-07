import mysql.connector
import config

def get_db_connection():
    return mysql.connector.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DB
    )

"""
+--------------+------------+------+-----+---------+----------------+
| Field        | Type       | Null | Key | Default | Extra          |
+--------------+------------+------+-----+---------+----------------+
| detection_id | int        | NO   | PRI | NULL    | auto_increment |
| camera_id    | tinyint    | NO   |     | NULL    |                |
| employee_id  | int        | NO   |     | NULL    |                |
| room_id      | tinyint    | NO   |     | NULL    |                |
| timestamp    | datetime   | NO   |     | NULL    |                |
| confidence   | float(9,6) | NO   |     | NULL    |                |
+--------------+------------+------+-----+---------+----------------+
"""

# Create a new detection in the DetectionLog table
def create_detection(detection_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    camera_id = detection_data['camera_id']
    employee_id = detection_data['employee_id']
    room_id = detection_data['room_id']
    timestamp = detection_data['timestamp']
    confidence = detection_data['confidence']

    query = """
    INSERT INTO DetectionLog (camera_id, employee_id, room_id, timestamp, confidence) 
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (camera_id, employee_id, room_id, timestamp, confidence))
    connection.commit()

    detection_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {"message": "Detection created successfully!", "detection_id": detection_id}

def get_detections():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM DetectionLog")
    detections = cursor.fetchall()

    cursor.close()
    connection.close()

    return detections

def get_detection_by_id(detection_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM DetectionLog WHERE detection_id = %s", (detection_id,))
    detection = cursor.fetchone()

    cursor.close()
    connection.close()

    return detection

def get_detection_by(**conditions):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
    query = f"SELECT * FROM DetectionLog WHERE {where_clause}"

    cursor.execute(query, tuple(conditions.values()))

    detection = cursor.fetchone()

    cursor.close()
    connection.close()

    return detection

def update_detection_by_id(detection_id, detection_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    camera_id = detection_data['camera_id']
    employee_id = detection_data['employee_id']
    room_id = detection_data['room_id']
    confidence = detection_data['confidence']

    query = """
    UPDATE DetectionLog 
    SET camera_id = %s, employee_id = %s, room_id = %s, confidence = %s
    WHERE detection_id = %s
    """
    cursor.execute(query, (camera_id, employee_id, room_id, confidence, detection_id))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Detection updated successfully!"}

def delete_detection_by_id(detection_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM DetectionLog WHERE detection_id = %s", (detection_id,))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Detection deleted successfully!"}
