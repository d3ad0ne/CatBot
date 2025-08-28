import logging

import psycopg2
from src import config
from loguru import logger


logging_level = config.logging_level
logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level=logging_level
)


def get_last_id(cursor):
    cursor.execute("SELECT MAX(id) FROM Users")
    id = cursor.fetchall()[0][0]
    if id is None:
        return 0
    return id


def set_connection():
    try:
        connection = psycopg2.connect(
        dbname = config.db_name,
        user = config.postgres_user,
        password = config.postgres_password,
        host = config.host_name,
        port = config.port
        )
        cursor = connection.cursor()
        logger.info('Successfully set connection to the PostgreSQL DB')
        return cursor, connection
    except psycopg2.Error as e:
        logger.error(f'Failed to set connection to the PostgreSQL DB: {e.pgerror}')


def close_connection(connection, cursor):
    try:
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        logger.error(f'Failed to close PostgreSQL connection: {e.pgerror}')


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


def get_images_amount(chat_id, cursor):
    cursor.execute('SELECT images_amount FROM Users WHERE chat_id = %s;', (chat_id,))
    images_amount = cursor.fetchall()[0][0]
    return images_amount


def get_chat_id(id, cursor):
    cursor.execute("SELECT chat_id FROM Users WHERE id = %s", (id,))
    chat_id = cursor.fetchall()[0][0]
    return chat_id


def schema_creator(schema_name):
    cur, conn = set_connection()
    try:
        cur.execute(f'CREATE SCHEMA IF NOT EXISTS {schema_name};')
        conn.commit()
        logger.info(f'Successfully created schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logger.error(f'Error during schema creation: {e}')
    finally:
        close_connection(conn, cur)


def table_creator(schema_name, table_name):
    cur, conn = set_connection()
    try:
        cur.execute(f'''
CREATE TABLE IF NOT EXISTS {schema_name}.{table_name}
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    chat_id bigint NOT NULL,
    images_amount bigint,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT chat_id_unique UNIQUE (chat_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS {schema_name}.users
    OWNER to {config.postgres_user};
''')
        conn.commit()
        logger.info(f'Successfully created table {table_name} in schema {schema_name} if it didn\'t exist yet')
    except psycopg2.Error as e:
        logging.error(f'Error during table creation: {e}')
    finally:
        close_connection(conn, cur)