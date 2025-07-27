import psycopg2
import config

def get_last_id(cursor):
    cursor.execute("SELECT MAX(id) FROM usernames")
    id = cursor.fetchall()[0][0]
    return id

def set_connection():
    connection = psycopg2.connect(
    dbname = config.db_name,
    user = config.postgres_user,
    password = config.postgres_password,
    host = config.host_name,
    port = config.port
    )
    cursor = connection.cursor()
    return cursor, connection

def close_connection(connection, cursor):
    cursor.close()
    connection.close()

#Functions don't close connection automatically, it has to be closed manually
def add_user(username, connection, cursor):
    cursor.execute("INSERT INTO usernames VALUES (%s, %s);", (get_last_id(cursor) + 1, username))
    connection.commit()
    
def delete_user(username, connection, cursor):
    cursor.execute("DELETE FROM usernames WHERE username = %s;", (username,))
    connection.commit()

def change_name(old_username, new_username, connection, cursor):
    cursor.execute("UPDATE usernames SET username = %s WHERE username = %s;", (new_username, old_username))
    connection.commit()

def get_user(id, cursor):
    cursor.execute("SELECT username FROM usernames WHERE id = %s", (id,))
    username = cursor.fetchall()[0][0]
    return username
