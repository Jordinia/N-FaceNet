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
+----------+--------------+------+-----+---------+----------------+
| Field    | Type         | Null | Key | Default | Extra          |
+----------+--------------+------+-----+---------+----------------+
| color_id | tinyint      | NO   | PRI | NULL    | auto_increment |
| color    | varchar(100) | YES  |     | NULL    |                |
+----------+--------------+------+-----+---------+----------------+
"""

def create_color(Color):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        color = Color['color']

        query = """
        INSERT INTO Color (color) 
        VALUES (%s)
        """
        cursor.execute(query, (color,))
        connection.commit()

        color_id = cursor.lastrowid

        return {"status": "success", "color_id": color_id, "message": "Color created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"data": color, "status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()



def get_colors():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Color")
        colors = cursor.fetchall()

        return {"data": colors, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_color_by_id(color_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Color WHERE color_id = %s", (color_id))
        Color = cursor.fetchone()

        return {"data": Color, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_color_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

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
        query = f"SELECT * FROM Color WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        Colors = cursor.fetchall()

        return {"data": Colors, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_color_by_id(color_id, Color):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        color = Color['color']

        query = """
        UPDATE Color 
        SET color = %s
        WHERE color_id = %s
        """
        cursor.execute(query, (color, color_id))
        connection.commit()

        return {"status": "success", "message": "Color updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_color_by_id(color_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Color WHERE color_id = %s", (color_id))
        connection.commit()

        return {"status": "success", "message": "Color deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
