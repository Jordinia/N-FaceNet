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
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| camera_id    | serial       | NO   | PRI | NULL    | auto_increment |
| room_id      | integer      | NO   |     | NULL    |                |
| created_date | timestamp    | NO   |     | NULL    |                |
| stream_url   | varchar(255) | NO   |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
"""

def create_camera(room_data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        room_id = room_data['room_id']
        created_date = room_data['created_date']
        stream_url = room_data['stream_url']

        query = """
        INSERT INTO camera (room_id, created_date, stream_url) 
        VALUES (%s, %s, %s)
        RETURNING camera_id
        """
        cursor.execute(query, (room_id, created_date, stream_url))
        connection.commit()

        camera_id = cursor.fetchone()[0]
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
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM camera")
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
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM camera WHERE camera_id = %s", (camera_id,))
        camera = cursor.fetchone()

        return {"data": camera, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_camera_by(**conditions):
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
        query = f"SELECT * FROM Camera WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        entry = cursor.fetchall()

        return {"data": entry, "status": "success"}
    
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
        stream_url = room_data['stream_url']

        query = """
        UPDATE camera 
        SET room_id = %s, stream_url = %s
        WHERE camera_id = %s
        """
        cursor.execute(query, (room_id, stream_url, camera_id))
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

        cursor.execute("DELETE FROM camera WHERE camera_id = %s", (camera_id,))
        connection.commit()

        return {"status": "success", "message": "Camera room deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
