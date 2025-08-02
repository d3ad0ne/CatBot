import psycopg2
from src import config


def get_last_id(cursor):
    cursor.execute("SELECT MAX(id) FROM Users")
    id = cursor.fetchall()[0][0]
    if id is None:
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
def add_user(chat_id, connection, cursor):
    cursor.execute("INSERT INTO Users VALUES (%s, %s, %s);", (get_last_id(cursor) + 1, chat_id, 1))
    connection.commit()


def delete_user(chat_id, connection, cursor):
    cursor.execute("DELETE FROM Users WHERE chat_id = %s;", (chat_id,))
    connection.commit()


def change_images_amount(chat_id, amount, connection, cursor):
    cursor.execute('UPDATE Users SET images_amount = %s WHERE chat_id = %s;', (amount, chat_id))
    connection.commit()


def get_images_amount(chat_id, connection, cursor):
    cursor.execute('SELECT images_amount FROM Users WHERE chat_id = %s;', (chat_id,))
    images_amount = cursor.fetchall()[0][0]
    return images_amount


def get_chat_id(id, cursor):
    cursor.execute("SELECT chat_id FROM Users WHERE id = %s", (id,))
    chat_id = cursor.fetchall()[0][0]
    return chat_id
