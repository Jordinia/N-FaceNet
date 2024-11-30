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
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| room_id  | serial       | NO   | PRI | NULL    | auto_increment |
| room     | varchar(100) | YES  |     | NULL    |                |
| capacity | integer      | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
"""

def create_room(Room):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        room = Room['room']
        capacity = Room['capacity']

        query = """
        INSERT INTO Room (room, capacity) 
        VALUES (%s, %s)
        RETURNING room_id
        """
        cursor.execute(query, (room, capacity))
        room_id = cursor.fetchone()[0]
        connection.commit()

        return {"status": "success", "room_id": room_id, "message": "Room created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_rooms():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM Room")
        rooms = cursor.fetchall()

        return {"data": rooms, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_room_by_id(room_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM Room WHERE room_id = %s", (room_id,))
        Room = cursor.fetchone()

        return {"data": Room, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_room_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        where_clauses = []
        values = []

        for column, condition in conditions.items():
            if isinstance(condition, tuple):
                operator, value = condition
                if operator in ["IS", "IS NOT"] and value is None:
                    where_clauses.append(f"{column} {operator} NULL")
                else:
                    where_clauses.append(f"{column} {operator} %s")
                    values.append(value)
            else:
                where_clauses.append(f"{column} = %s")
                values.append(condition)

        where_clause = " AND ".join(where_clauses)
        query = f"SELECT * FROM Room WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        Rooms = cursor.fetchall()

        return {"data": Rooms, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_room_by_id(room_id, Room):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        room = Room['room']
        capacity = Room['capacity']

        query = """
        UPDATE Room 
        SET room = %s, capacity = %s
        WHERE room_id = %s
        """
        cursor.execute(query, (room, capacity, room_id))
        connection.commit()

        return {"status": "success", "message": "Room updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_room_by_id(room_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Room WHERE room_id = %s", (room_id,))
        connection.commit()

        return {"status": "success", "message": "Room deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
