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
+---------------+----------+------+-----+---------+----------------+
| Field         | Type     | Null | Key | Default | Extra          |
+---------------+----------+------+-----+---------+----------------+
| entry_id      | int      | NO   | PRI | NULL    | auto_increment |
| employee_id   | int      | NO   |     | NULL    |                |
| checkin_time  | timestamp| YES  |     | NULL    |                |
| checkout_time | timestamp| YES  |     | NULL    |                |
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

        entry_id = cursor.fetchone()[0]  # Get the last inserted entry ID

        return {"status": "success","entry_id": entry_id, "message": "Entry created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_entries():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM EntryLog")
        entries = cursor.fetchall()

        return {"data": entries, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_entry_by_id(entry_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

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
        query = f"SELECT * FROM EntryLog WHERE {where_clause}"

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
