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
| camera_id    | tinyint    | NO   | PRI | NULL    | auto_increment |
| room_id      | tinyint    | NO   |     | NULL    |                |
| created_date | datetime   | NO   |     | NULL    |                |
+--------------+------------+------+-----+---------+----------------+
"""

def create_camera(room_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        room_id = room_data['room_id']
        created_date = room_data['created_date']

        query = """
        INSERT INTO Camera (room_id, created_date) 
        VALUES (%s, %s)
        """
        cursor.execute(query, (room_id, created_date))
        connection.commit()

        camera_id = cursor.lastrowid
        return {"status": "success", "camera_id": camera_id, "message": "Camera room created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"data": room_data, "status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_cameras():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Camera")
        rooms = cursor.fetchall()

        return {"data": rooms, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_camera_by_id(camera_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Camera WHERE camera_id = %s", (camera_id,))
        camera = cursor.fetchone()

        return {"data": camera, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_camera_by_id(camera_id, room_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        room_id = room_data['room_id']

        query = """
        UPDATE Camera 
        SET room_id = %s
        WHERE camera_id = %s
        """
        cursor.execute(query, (room_id, camera_id))
        connection.commit()

        return {"status": "success", "message": "Camera room updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_camera_by_id(camera_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Camera WHERE camera_id = %s", (camera_id,))
        connection.commit()

        return {"status": "success", "message": "Camera room deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
