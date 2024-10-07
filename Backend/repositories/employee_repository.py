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
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| employee_id     | int          | NO   | PRI | NULL    | auto_increment |
| current_room_id | int          | YES  |     | NULL    |                |
| gender          | tinyint(1)   | YES  |     | NULL    |                |
| age             | int          | YES  |     | NULL    |                |
| top_color_id    | tinyint      | YES  |     | NULL    |                |
| bottom_color_id | tinyint      | YES  |     | NULL    |                |
| name            | varchar(255) | YES  |     | NULL    |                |
| role_id         | tinyint      | YES  |     | NULL    |                |
| nik             | varchar(10)  | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
"""

def create_employee(employee_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    nik = employee_data['nik']
    name = employee_data['name']
    role_id = employee_data['role_id']
    current_room_id = employee_data['current_room_id']
    gender = employee_data['gender']
    age = employee_data['age']
    top_color_id = employee_data['top_color_id']
    bottom_color_id = employee_data['bottom_color_id']

    query = """
    INSERT INTO Employee (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id))
    connection.commit()

    employee_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {"employee_id": employee_id}

def get_employees():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()

    cursor.close()
    connection.close()

    return employees

def get_employee_by_id(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Employee WHERE employee_id = %s", (employee_id,))
    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return employee

def get_employee_by(**conditions):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
    query = f"SELECT * FROM Employee WHERE {where_clause}"

    cursor.execute(query, tuple(conditions.values()))

    employee = cursor.fetchone()

    cursor.close()
    connection.close()

    return employee

def update_employee_by_id(employee_id, employee):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    nik = employee['nik']
    name = employee['name']
    role_id = employee['role_id']
    current_room_id = employee['current_room_id']
    gender = employee['gender']
    age = employee['age']
    top_color_id = employee['top_color_id']
    bottom_color_id = employee['bottom_color_id']
    face_path = employee['face_path']

    query = """
    UPDATE Employee 
    SET nik = %s, name = %s, role_id = %s, current_room_id = %s, gender = %s, age = %s, top_color_id = %s, bottom_color_id = %s, face_path = %s
    WHERE employee_id = %s
    """
    cursor.execute(query, (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id, face_path, employee_id))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Employee updated successfully!"}

def delete_employee_by_id(employee_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Employee WHERE employee_id = %s", (employee_id,))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Employee deleted successfully!"}
