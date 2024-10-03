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
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO Token (token, employee_id, created_date, expired_date) 
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (token['token'], token['employee_id'], token['created_date'], token['expired_date']))
    connection.commit()

    token_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return {"message": "Token created successfully!", "token_id": token_id}

def get_tokens():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Token")
    tokens = cursor.fetchall()

    cursor.close()
    connection.close()

    return tokens

def get_token_by_id(token_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Token WHERE token_id = %s", (token_id,))
    token = cursor.fetchone()

    cursor.close()
    connection.close()

    return token

def get_token_by(**conditions):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    where_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
    query = f"SELECT * FROM Token WHERE {where_clause}"

    cursor.execute(query, tuple(conditions.values()))

    token = cursor.fetchone()

    cursor.close()
    connection.close()

    return token

def update_token_by_id(token):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE Token 
    SET token = %s, employee_id = %s, created_date = %s, expired_date = %s 
    WHERE token_id = %s
    """
    cursor.execute(query, (token['token'], token['employee_id'], token['created_date'], token['expired_date'], token['token_id']))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Token updated successfully!"}

def delete_token_by_id(token_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM Token WHERE token_id = %s", (token_id,))
    connection.commit()

    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return {"status": "error", "message": "Nothing changed"}
    return {"status": "success", "message": "Token deleted successfully!"}
