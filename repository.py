import psycopg2
import psycopg2.extras
from index import get_connection
from models import User, Transaction, Wallet


class WalletSqlRepository:
    @classmethod
    def create_wallet(cls, wallet_db: Wallet):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            create_clause = '''CREATE TABLE IF NOT EXISTS wallet_db(
                                                    wallet_id VARCHAR(150),
                                                    balance FLOAT,
                                                    username VARCHAR(255),
                                                    created_at VARCHAR(255),
                                                    updated_at VARCHAR(255)
                                                    )'''
            cur.execute(create_clause)

            insert_clause = (
                '''INSERT INTO wallet_db (wallet_id, balance, username, created_at, updated_at)'''
                '''VALUES (%s, %s, %s, %s, %s)'''
            )
            values = (
                wallet_db.wallet_id,
                wallet_db.balance,
                wallet_db.username,
                wallet_db.created_at,
                wallet_db.updated_at
            )

            cur.execute(insert_clause, values)
            conn.commit()
            print(f'User profile created successfully, with username {wallet_db.username} and wallet ID {wallet_db.wallet_id}.')

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
            create_clause = '''CREATE TABLE IF NOT EXISTS transaction_db (
                                                        transaction_id VARCHAR(150),
                                                        created_at VARCHAR(255),
                                                        sender VARCHAR(255),
                                                        recipient VARCHAR(255),
                                                        amount FLOAT,
                                                        transaction_type VARCHAR(255)
                                                        )'''
            cur.execute(create_clause)
            insert_clause = (
                '''INSERT INTO transaction_db(transaction_id,created_at,sender,recipient,amount,transaction_type)'''
                '''VALUES(%s, %s, %s, %s, %s, %s)''')
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
    def profile_wallet(cls, wall_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''SELECT * FROM wallet_db WHERE wallet_id = %s''', (wall_id,))
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

    @classmethod
    def receive_money(cls, wall_id, amount: float):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''SELECT balance FROM wallet_db WHERE wallet_id =%s''',(wall_id,))
            balance_atm = cur.fetchone()[0]
            amount = float(amount)
            cur.execute('''UPDATE wallet_db SET balance = %s WHERE wallet_id =%s''',(amount + balance_atm, wall_id,))
            conn.commit()
            cur.execute('''SELECT balance FROM wallet_db WHERE wallet_id = %s''',(wall_id,))
            new_balance = cur.fetchone()[0]
            print(f'Successfully deposited {amount} into your wallet. \nYour updated balance is {new_balance}.')

            #getting username of wallet_id
            cur.execute('''SELECT username FROM wallet_db WHERE wallet_id = %s''',(wall_id,))
            result = cur.fetchone()
            conn.commit()
            return result['username']

        except Exception as error:
            print(error)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def send_money(cls, wall_id:str, amount:float, recipient:str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #checking if recipient's wallet exists
        cur.execute('''SELECT EXISTS (SELECT wallet_id FROM wallet_db WHERE username=%s)''',(recipient,))
        check = cur.fetchone()[0]
        if not check:
            print('Recipient not found')
            return
        #avoid sending money to self
        cur.execute('''SELECT username FROM wallet_db WHERE wallet_id=%s''',(wall_id,))
        username = cur.fetchone()[0]
        if username == recipient:
            print("Can't send money to self.")
            return
        try:
            #checking for sufficient funds
            cur.execute('''SELECT balance FROM wallet_db WHERE username = %s''',(username,))
            sender_balance = cur.fetchone()[0]
            if sender_balance >= amount:
                amount = float(amount)
                new_balance = sender_balance - amount
                cur.execute('''UPDATE wallet_db SET balance = %s WHERE username = %s''', (new_balance,username))
                conn.commit()
                #getting recipient's balance
                cur.execute('''SELECT balance FROM wallet_db WHERE username =%s''',(recipient,))
                result = cur.fetchone()
                recipient_balance = result['balance']
                #add money to recipient's wallet
                cur.execute('''UPDATE wallet_db SET balance = %s WHERE username=%s''',(recipient_balance+amount, recipient,))
                #get username of wallet_id
                cur.execute('''SELECT username FROM wallet_db WHERE wallet_id = %s''',(wall_id,))
                result = cur.fetchone()
                conn.commit()
                print(f'{amount} sent to {recipient}\n')
                return result['username']
            else:
                print('Insufficient funds')
                return
        except Exception as error:
            conn.rollback()
            print(f'error {error}')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def check_balance(cls, wall_id):
        conn=get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            check = '''SELECT * FROM wallet_db WHERE wallet_id=%s'''
            cur.execute(check,(wall_id,))
            result = cur.fetchone()
            if result:
                for key, value in result.items():
                    if key == 'balance':
                        print(f'{key}:{value}\n')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_a_transaction(cls, transaction_id):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''SELECT * FROM transaction_db WHERE transaction_id=%s''',(transaction_id))
            result = cur.fetchone()
            if result is None:
                print('Transaction not found')
            else:
                print(result)
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(f'Error {error}')
        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_transactions(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''SELECT * FROM transaction_db WHERE sender = %s''',(str(username),))
            for result in cur.fetchall():
                print(result)
            print('\n\n')
            conn.commit()
        except Exception as error:
            conn.rollback()
            print(f'Error {error}')
        finally:
            cur.close()
            conn.close()


class UserSqlRepository:
    @classmethod
    def create_user(cls, user: User):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            create_clause = '''CREATE TABLE IF NOT EXISTS user_db(
                                                        name VARCHAR(255),
                                                        username VARCHAR(255),
                                                        password VARCHAR(30),
                                                        created_at VARCHAR(150)
                                                        )'''
            cur.execute(create_clause)
            #check if username already exists in the db
            cur.execute('''SELECT EXISTS (SELECT username FROM user_db WHERE username = %s)''',(user.username,))
            result = cur.fetchone()[0]
            if result:
                print('Username already exists.\nTry another username.')
                return False
            else:
                insert_clause = ('''INSERT INTO user_db(name,username,password,created_at) VALUES'''
                                 '''(%s,%s,%s,%s)''')
                insert_values = (
                    user.name,
                    user.username,
                    user.password,
                    user.created_at
                )
                cur.execute(insert_clause,insert_values)
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
    def load_user(cls, username:str, password:str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('''SELECT EXISTS(SELECT * FROM user_db WHERE username=%s AND password=%s)''',
                    (username,password))
        result = cur.fetchall()[0][0]
        if result:
            #get the wallet id of the user from the db
            cur.execute('''SELECT wallet_id FROM wallet_db WHERE username = %s''',(username,))
            wallet_id = cur.fetchone()[0]
            return True, username, wallet_id
        else:
            print('Login failed.')
            return False, None, None

    @classmethod
    def profile_user(cls, username):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute('''SELECT * FROM wallet_db WHERE username = %s''', (username,))
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










