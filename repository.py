import bcrypt
import psycopg2
import psycopg2.extras
from index import get_connection
from models import User, Wallet, Transaction


class WalletSqlRepository:
    @classmethod
    def create_wallet(cls, wallet_db: Wallet):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            insert_clause = '''
                INSERT INTO wallet_db (wallet_id, username, created_at, updated_at)
                VALUES (%s, %s, %s, %s)
            '''

            values = (
                wallet_db.wallet_id,
                wallet_db.username,
                wallet_db.created_at,
                wallet_db.updated_at
            )

            cur.execute(insert_clause, values)
            conn.commit()
            print(f'Wallet created successfully, with username {wallet_db.username} '
                  f'and wallet ID {wallet_db.wallet_id}')
        except Exception as error:
            print(f'{error}')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def insert_transaction(cls, transaction_db: Transaction):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            insert_clause = '''
                INSERT INTO transaction_db(transaction_id,created_at,sender,recipient,amount,transaction_type)
                VALUES(%s, %s, %s, %s, %s, %s)
            '''
            values = (
                transaction_db.transaction_id,
                transaction_db.created_at,
                transaction_db.sender,
                transaction_db.recipient,
                transaction_db.amount,
                transaction_db.transaction_type
            )
            cur.execute(insert_clause, values)
            conn.commit()
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def check_balance(cls, wall_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #get username associated with the wallet id
            cur.execute('''SELECT username FROM wallet_db WHERE wallet_id= %s''', (wall_id,))
            user_row = cur.fetchone()
            if user_row is None:
                print('Wallet ID not found')
                return
            username = user_row[0]
            #calculate balance based on transactions
            cur.execute('''SELECT SUM(CASE WHEN transaction_type = 'receive' THEN amount ELSE -amount END) AS balance
                            FROM transaction_db
                            WHERE sender = %s OR recipient = %s''', (username, username))
            balance = cur.fetchone()[0] or 0.0
            print(f'Balance: {balance}')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def profile_wallet(cls, wall_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT * FROM wallet_db WHERE wallet_id = %s''', (wall_id,))
            wallet_row = cur.fetchone()
            if wallet_row:
                for key, value in wallet_row.items():
                    print(f'{key} : {value}')
            else:
                print('Wallet not found')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()


class UserSqlRepository:
    '''
    @staticmethod
    def get_by_username(username):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('SELECT * FROM user_db WHERE username=%s', (username,))
            result = cur.fetchone()
            if result is None:
                print('User not found.')
            else:
                print(result)
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(f'Error {error}')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
    '''
    @classmethod
    def username_exists(cls, username: str) -> bool:
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT EXISTS (SELECT 1 FROM user_db WHERE username=%s)''', (username,))
            result = cur.fetchone()[0]
            return result
        except Exception as error:
            print(f'Error: {error}')
            return False
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def create_user(cls, user: User):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            insert_clause = ''' 
                INSERT INTO user_db(name,username,password,created_at) 
                VALUES(%s,%s,%s,%s)
            '''
            insert_values = (
                user.name,
                user.username,
                hashed_password.decode('utf-8'),
                user.created_at
            )
            cur.execute(insert_clause, insert_values)
            conn.commit()
            return True
        except Exception as error:
            raise error
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def profile_user(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('SELECT * FROM wallet_db WHERE username = %s', (username,))
            user_row = cur.fetchone()
            if user_row:
                for key, value in user_row.items():
                    print(f'{key} : {value}')
            else:
                print(f'\nUser not found')
        finally:
            print('\n\n')
            cur.close()
            conn.close()

