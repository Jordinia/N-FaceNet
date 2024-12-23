import psycopg2
from psycopg2.extras import RealDictCursor
import config

def get_db_connection():
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        database=config.POSTGRES_DB
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
+--------------+------------+------+-----+---------+----------------+
"""

def create_detection(detection_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        camera_id = detection_data['camera_id']
        employee_id = detection_data['employee_id']
        room_id = detection_data['room_id']
        timestamp = detection_data['timestamp']

        query = """
        INSERT INTO DetectionLog (camera_id, employee_id, room_id, timestamp) 
        VALUES (%s, %s, %s, %s) 
        RETURNING detection_id
        """
        cursor.execute(query, (camera_id, employee_id, room_id, timestamp))
        connection.commit()

        # Get the last inserted detection_id
        detection_id = cursor.fetchone()[0]

        return {"status": "success", "message": "Detection created successfully!", "detection_id": detection_id}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_detections():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM DetectionLog")
        detections = cursor.fetchall()

        return {"data": detections, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_detection_by_id(detection_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM DetectionLog WHERE detection_id = %s", (detection_id,))
        detection = cursor.fetchone()

        return {"data": detection, "status": "success"}

    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_detection_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        where_clauses = []
        values = []

        for column, condition in conditions.items():
            if isinstance(condition, tuple):
                operator, value = condition
                if operator in ["IS", "IS NOT"] and value is None:
                    # For IS NULL or IS NOT NULL, no placeholder is needed
                    where_clauses.append(f"{column} {operator} NULL")
                else:
                    where_clauses.append(f"{column} {operator} %s")
                    values.append(value)
            else:
                # Default to equality
                where_clauses.append(f"{column} = %s")
                values.append(condition)

        where_clause = " AND ".join(where_clauses)
        query = f"SELECT * FROM DetectionLog WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        detection = cursor.fetchall()

        if len(detection) == 1:
            detection = detection[0]

        if detection == []:
            detection = None

        return {"data": detection, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_detection_by_id(detection_id, detection_data):
    try:
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

        return {"status": "success", "message": "Detection updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_detection_by_id(detection_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM DetectionLog WHERE detection_id = %s", (detection_id,))
        connection.commit()

        return {"status": "success", "message": "Detection deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
