import psycopg2
from config import DATABASE_HOST, DATABASE_USERNAME, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_PORT


def get_connection():
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        dbname=DATABASE_NAME,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        port=DATABASE_PORT
    )

    return conn
