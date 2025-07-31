import psycopg2
from src import config


def get_last_id(cursor):
    cursor.execute("SELECT MAX(id) FROM Users")
    id = cursor.fetchall()[0][0]
    if id == None:
        return 0
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
def add_user(username, chat_id, connection, cursor):
    cursor.execute("INSERT INTO Users VALUES (%s, %s, %s);", (get_last_id(cursor) + 1, username, chat_id))
    connection.commit()
    
def delete_user(username, connection, cursor):
    cursor.execute("DELETE FROM Users WHERE username = %s;", (username,))
    connection.commit()

def change_name(old_username, new_username, connection, cursor):
    cursor.execute("UPDATE Users SET username = %s WHERE username = %s;", (new_username, old_username))
    connection.commit()

def get_chat_id(id, cursor):
    cursor.execute("SELECT chatid FROM Users WHERE id = %s", (id,))
    chat_id = cursor.fetchall()[0][0]
    return chat_id
