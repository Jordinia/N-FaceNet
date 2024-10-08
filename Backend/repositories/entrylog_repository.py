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
+---------------+----------+------+-----+---------+----------------+
| Field         | Type     | Null | Key | Default | Extra          |
+---------------+----------+------+-----+---------+----------------+
| entry_id      | int      | NO   | PRI | NULL    | auto_increment |
| employee_id   | int      | NO   |     | NULL    |                |
| checkin_time  | datetime | YES  |     | NULL    |                |
| checkout_time | datetime | YES  |     | NULL    |                |
+---------------+----------+------+-----+---------+----------------+
"""

def create_entry(entry):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO EntryLog (employee_id, checkin_time, checkout_time) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (entry['employee_id'], entry['checkin_time'], entry['checkout_time']))
        connection.commit()

        entry_id = cursor.lastrowid

        return {"status": "success","entry_id": entry_id, "message": "Entry created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_entries():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM EntryLog")
        entries = cursor.fetchall()

        return {"data": entries, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_entry_by_id(entry_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM EntryLog WHERE entry_id = %s", (entry_id,))
        entry = cursor.fetchone()

        return {"data": entry, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_entry_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

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
        query = f"SELECT * FROM EntryLog WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        entry = cursor.fetchall()

        if len(entry) == 1:
            entry = entry[0]

        if entry == []:
            entry = None

        return {"data": entry, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_entry_by_id(entry):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        UPDATE EntryLog 
        SET employee_id = %s, checkin_time = %s, checkout_time = %s 
        WHERE entry_id = %s
        """
        cursor.execute(query, (entry['employee_id'], entry['checkin_time'], entry['checkout_time'], entry['entry_id']))
        connection.commit()

        return {"status": "success", "message": "Entry updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_entry_by_id(entry_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM EntryLog WHERE entry_id = %s", (entry_id,))
        connection.commit()

        return {"status": "success", "message": "Entry deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
