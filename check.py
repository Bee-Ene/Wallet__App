import psycopg2
import psycopg2.extras

from models import User
from index import get_connection
from datetime import datetime

'''
 name: str
    username: str
    password: str
    created_at: str

'''
name = 'Blessing1'
username = 'Bee1'
password = '123'
created_at = datetime.now().isoformat()

user = User(name, username, password, created_at)
conn = None
cur = None

try:
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    create_script = ''' CREATE TABLE IF NOT EXISTS user_db (
                                name VARCHAR(40),
                                username VARCHAR(15),
                                password VARCHAR(255),
                                created_at VARCHAR(26)

                        )'''
    cur.execute(create_script)

    insert_script = ('INSERT INTO user_db (name, username, password, created_at) VALUES '
                     '(%s, %s, %s, %s)')
    insert_values = (
        user.name,
        user.username,
        user.password,
        user.created_at
    )
    cur.execute(insert_script, insert_values)
    conn.commit()

except Exception as error:
    raise error
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
