import psycopg2

def _get_last_id(cursor):
    cursor.execute("SELECT MAX(id) FROM usernames")
    id = cursor.fetchall()[0][0]
    return id

def add_user(username):
    connection = psycopg2.connect(
    dbname="postgres_db",
    user="postgres_user",
    password="postgres_password",
    host="localhost",
    port="5430"
    )
    cursor = connection.cursor()
    cursor.execute("INSERT INTO usernames VALUES (%s, %s);", (_get_last_id(cursor) + 1, username))
    connection.commit()
    cursor.close()
    connection.close()
    
def delete_user(username):
    connection = psycopg2.connect(
    dbname="postgres_db",
    user="postgres_user",
    password="postgres_password",
    host="localhost",
    port="5430"
    )
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usernames WHERE username = %s;", (username,))
    connection.commit()
    cursor.close()
    connection.close()

def change_name(old_username, new_username):
    connection = psycopg2.connect(
    dbname="postgres_db",
    user="postgres_user",
    password="postgres_password",
    host="localhost",
    port="5430"
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE usernames SET username = %s WHERE username = %s;", (new_username, old_username))
    connection.commit()
    cursor.close()
    connection.close()

def get_user(id):
    connection = psycopg2.connect(
    dbname="postgres_db",
    user="postgres_user",
    password="postgres_password",
    host="localhost",
    port="5430"
    )
    cursor = connection.cursor()
    max_id = _get_last_id(cursor)
    if id <= max_id:
        cursor.execute("SELECT username FROM usernames WHERE id = %s", (id,))
        username = cursor.fetchall()[0][0]
    else:
        username = 'Error'
    cursor.close()
    connection.close()
    return username
