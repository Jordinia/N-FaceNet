import psycopg2
import psycopg2.extras
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
+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| token_id     | int         | NO   | PRI | NULL    | auto_increment |
| token        | varchar(16) | NO   |     | NULL    |                |
| employee_id  | int         | NO   |     | NULL    |                |
| created_date | timestamp   | NO   |     | NULL    |                |
| expired_date | timestamp   | NO   |     | NULL    |                |
| is_approved  | boolean     | YES  |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+
"""

def create_token(token):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO Token (token, employee_id, created_date, expired_date, is_approved) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING token_id
        """
        cursor.execute(query, (token['token'], token['employee_id'], token['created_date'], token['expired_date'], token['is_approved']))
        token_id = cursor.fetchone()[0]
        connection.commit()

        return {"status": "success", "token_id": token_id, "message": "Token created successfully!"}

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
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM Token")
        tokens = cursor.fetchall()

        return {"data": tokens, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_token_by_id(token_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute("SELECT * FROM Token WHERE token_id = %s", (token_id,))
        token = cursor.fetchone()

        return {"data": token, "status": "success"}
    
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def get_token_by(**conditions):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

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
        return {"status": "error", "message": f"Database error: {str(e)}"}
    
    finally:
        cursor.close()
        connection.close()

def update_token_by_id(token_id, token):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        UPDATE Token 
        SET token = %s, employee_id = %s, is_approved = %s, expired_date = %s
        WHERE token_id = %s
        """
        cursor.execute(query, (token['token'], token['employee_id'], token['is_approved'], token['expired_date'], token_id))
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
