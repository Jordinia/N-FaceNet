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
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO EntryLog (employee_id, checkin_time, checkout_time) 
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (entry['employee_id'], entry['checkin_time'], entry['checkout_time']))
    connection.commit()

    entry_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {"message": "Entry created successfully!", "entry_id": entry_id}

def get_entries():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM EntryLog")
    entries = cursor.fetchall()

    cursor.close()
    connection.close()

    return entries

def get_entry_by_id(entry_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM EntryLog WHERE entry_id = %s", (entry_id,))
    entry = cursor.fetchone()

    cursor.close()
    connection.close()

    return entry

def get_entry_by(**conditions):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
    query = f"SELECT * FROM EntryLog WHERE {where_clause}"

    cursor.execute(query, tuple(conditions.values()))

    entry = cursor.fetchone()

    cursor.close()
    connection.close()

    return entry

def update_entry_by_id(entry):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE EntryLog 
    SET employee_id = %s, checkin_time = %s, checkout_time = %s 
    WHERE entry_id = %s
    """
    cursor.execute(query, (entry['employee_id'], entry['checkin_time'], entry['checkout_time'], entry['entry_id']))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Entry updated successfully!"}

def delete_entry_by_id(entry_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM EntryLog WHERE entry_id = %s", (entry_id,))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Entry deleted successfully!"}
