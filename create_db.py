#python create_db.py
import psycopg2
import psycopg2.extras
from index import get_connection


def create_tables():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # SQL commands to create tables
        create_wallet_table = '''
        CREATE TABLE IF NOT EXISTS wallet_db (
            wallet_id VARCHAR(150) PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            created_at VARCHAR(255),
            updated_at VARCHAR(255)
        )
        '''

        create_transaction_table = '''
        CREATE TABLE IF NOT EXISTS transaction_db (
            transaction_id VARCHAR(150) PRIMARY KEY,
            created_at VARCHAR(255),
            sender VARCHAR(255),
            recipient VARCHAR(255),
            amount FLOAT,
            transaction_type VARCHAR(255)
        )
        '''

        create_user_table = '''
        CREATE TABLE IF NOT EXISTS user_db (
            name VARCHAR(255),
            username VARCHAR(255) PRIMARY KEY,
            password VARCHAR(150),
            created_at VARCHAR(150)
        )
        '''

        # Execute the create table commands
        cur.execute(create_wallet_table)
        cur.execute(create_transaction_table)
        cur.execute(create_user_table)

        conn.commit()
        print("Tables created successfully.")
    except Exception as error:
        print(f'Error creating tables: {error}')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    create_tables()
