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
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| token_id     | int         | NO   | PRI | NULL    | auto_increment |
| token        | varchar(16) | NO   |     | NULL    |                |
| employee_id  | int         | NO   |     | NULL    |                |
| created_date | datetime    | NO   |     | NULL    |                |
| expired_date | datetime    | NO   |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
"""

def create_token(token):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO Token (token, employee_id, created_date, expired_date) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (token['token'], token['employee_id'], token['created_date'], token['expired_date']))
        connection.commit()

        token_id = cursor.lastrowid

        return {"status": "success", "message": "Token created successfully!", "token_id": token_id}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_tokens():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Token")
        tokens = cursor.fetchall()

        return {"data": tokens, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_token_by_id(token_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Token WHERE token_id = %s", (token_id,))
        token = cursor.fetchone()

        return {"data": token, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_token_by(**conditions):
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
        query = f"SELECT * FROM Token WHERE {where_clause}"

        cursor.execute(query, tuple(values))
        token = cursor.fetchall()

        if len(token) == 1:
            token = token[0]

        if token == []:
            token = None

        return {"data": token, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        # Catch any other unforeseen errors, like DB connection issues, SQL errors
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_token_by_id(token):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        UPDATE Token 
        SET token = %s, employee_id = %s, created_date = %s, expired_date = %s 
        WHERE token_id = %s
        """
        cursor.execute(query, (token['token'], token['employee_id'], token['created_date'], token['expired_date'], token['token_id']))
        connection.commit()

        return {"status": "success", "message": "Token updated successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def delete_token_by_id(token_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Token WHERE token_id = %s", (token_id,))
        connection.commit()

        return {"status": "success", "message": "Token deleted successfully!"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()
