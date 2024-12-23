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
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| employee_id     | int          | NO   | PRI | NULL    | auto_increment |
| current_room_id | int          | YES  |     | NULL    |                |
| gender          | tinyint(1)   | YES  |     | NULL    |                |
| age             | int          | YES  |     | NULL    |                |
| top_color_id    | tinyint      | YES  |     | NULL    |                |
| bottom_color_id | tinyint      | YES  |     | NULL    |                |
| dress_color_id  | tinyint      | YES  |     | NULL    |                |
| name            | varchar(255) | YES  |     | NULL    |                |
| role_id         | tinyint      | YES  |     | NULL    |                |
| nik             | varchar(10)  | YES  |     | NULL    |                |
| face_path       | varchar(255) | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
"""

def create_employee(employee_data):
    try:
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
        dress_color_id = employee_data['dress_color_id']
        face_path = employee_data['face_path']

        query = """
        INSERT INTO Employee (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id, dress_color_id, face_path) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING employee_id
        """
        cursor.execute(query, (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id, dress_color_id, face_path))
        connection.commit()

        employee_id = cursor.fetchone()[0]  # Fetch the returned employee_id

        return {"status": "success", "employee_id": employee_id, "message": "Employee created successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_employees():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM employee_room_view")
        employees = cursor.fetchall()

        return {"data": employees, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()


def get_employee_by_id(employee_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM employee_room_view WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()

        employee = dict(employee)

        return {"data": employee, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()


def get_employee_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        where_clauses = []
        values = []

        for column, condition in conditions.items():
            # Check if the column is "name" to apply the LIKE operator
            if column == "name":
                where_clauses.append(f"{column} LIKE %s")
                values.append(f"%{condition}%")  # Wrap the value in % for partial match

            elif isinstance(condition, tuple):
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
        query = f"SELECT * FROM employee_room_view WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        employee = cursor.fetchall()

        return {"data": employee, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()


def update_employee_by_id(employee_id, employee):
    try:
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
        dress_color_id = employee.get('dress_color_id', None)

        query = """
        UPDATE Employee 
        SET nik = %s, name = %s, role_id = %s, current_room_id = %s, gender = %s, age = %s, top_color_id = %s, bottom_color_id = %s, face_path = %s, dress_color_id = %s
        WHERE employee_id = %s
        """
        cursor.execute(query, (nik, name, role_id, current_room_id, gender, age, top_color_id, bottom_color_id, face_path, dress_color_id, employee_id))
        connection.commit()

        return {"status": "success", "message": "Employee updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()


def delete_employee_by_id(employee_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Employee WHERE employee_id = %s", (employee_id,))
        connection.commit()

        return {"status": "success", "message": "Employee deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
