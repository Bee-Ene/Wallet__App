from datetime import datetime
from models import Transaction
import psycopg2
import psycopg2.extras
from index import get_connection
from repository import WalletSqlRepository


class WalletFunctions:

    @classmethod
    def receive_money(cls, wall_id, amount: float):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #cur.execute('''SELECT balance FROM wallet_db WHERE wallet_id =%s''', (wall_id,))
            #balance_atm = cur.fetchone()[0]
            #new_balance = balance_atm + amount
            #cur.execute('''UPDATE wallet_db SET balance = %s WHERE wallet_id =%s''', (new_balance, wall_id))
            #conn.commit()
            # cur.execute('SELECT balance FROM wallet_db WHERE wallet_id = %s', (wall_id,))
            # getting username of wallet_id
            cur.execute('''SELECT username FROM wallet_db WHERE wallet_id = %s''', (wall_id,))
            result = cur.fetchone()
            if not result:
                print('Wallet not found.')
                return
            # conn.commit()
            username = result['username']
            #insert the transaction
            transaction_id = f'{datetime.now().isoformat()} - {amount}'
            transaction = Transaction(transaction_id, datetime.now().isoformat(), username, '', amount, 'receive')
            WalletSqlRepository.insert_transaction(transaction)
            print(f'Successfully deposited {amount} into your wallet.')
            #print available balance after deposit
            WalletSqlRepository.check_balance(wall_id)
        except Exception as error:
            print(error)
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def send_money(cls, wall_id: str, amount: float, recipient: str):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #get sender's username
            cur.execute('''SELECT username FROM wallet_db WHERE wallet_id=%s''', (wall_id,))
            user_row = cur.fetchone()
            if user_row is None:
                print('Sender wallet ID not found.')
                return
            username = user_row[0]
            # checking if recipient's wallet exists
            cur.execute('''SELECT EXISTS (SELECT wallet_id FROM wallet_db WHERE username=%s)''', (recipient,))
            check = cur.fetchone()[0]
            if not check:
                print('Recipient not found')
                return
            # avoid sending money to self
            if username == recipient:
                print("Can't send money to self.")
                return

            # checking for sufficient funds
            cur.execute('''SELECT SUM(CASE WHEN transaction_type = 'receive' THEN amount ELSE -amount END) AS balance
                            FROM transaction_db
                            WHERE sender = %s OR recipient = %s''', (username, username))
            balance = cur.fetchone()[0] or 0.0

            if balance < amount:
                print('Insufficient funds.')
                return

            transaction_id = f'{datetime.now().isoformat()} - {amount}'
            transaction = Transaction(transaction_id, datetime.now().isoformat(), username, recipient, amount, 'send')
            WalletSqlRepository.insert_transaction(transaction)
            print(f'successfully sent {amount} to {recipient}.')
            #print balance
            WalletSqlRepository.check_balance(wall_id)
        except Exception as error:
            conn.rollback()
            print(f'error {error}')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def get_a_transaction(cls, transaction_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT * FROM transaction_db WHERE transaction_id=%s''', (transaction_id,))
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
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()

    @classmethod
    def get_transactions(cls, username):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''SELECT * FROM transaction_db WHERE sender = %s''', (str(username),))
            for result in cur.fetchall():
                print(result)
            print('\n\n')
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
    def check_balance(cls, wall_id):
        conn = None
        cur = None
        try:
            conn = get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('SELECT balance FROM wallet_db WHERE wallet_id = %s', (wall_id,))
            # check = 'SELECT * FROM wallet_db WHERE wallet_id=%s'
            # cur.execute(check,(wall_id,))
            balance = cur.fetchone()[0]
            print(f'Balance: {balance}')
        finally:
            if cur is not None:
                cur.close()
            if conn is not None:
                conn.close()
    @staticmethod
    def check_balance(wall_id):
        WalletSqlRepository.check_balance(wall_id)

    @staticmethod
    def receive_money(wall_id, amount: float):
        username = WalletSqlRepository.receive_money(wall_id, amount)
        created_at = datetime.now().isoformat()
        transaction_id = f'{created_at}-{amount}'
        transaction = Transaction(transaction_id, created_at, username, '', amount, 'receive')
        WalletSqlRepository.insert_transaction(transaction)
        return username

    @staticmethod
    def send_money(wall_id: str, amount: float, recipient: str):
        username = WalletSqlRepository.send_money(wall_id, amount, recipient)
        created_at = datetime.now().isoformat()
        transaction_id = f'{created_at}-{amount}'
        transaction = Transaction(transaction_id, created_at, username, recipient, amount, 'send')
        WalletSqlRepository.insert_transaction(transaction)
        return username

    @staticmethod
    def get_transactions(username):
        WalletSqlRepository.get_transactions(username)

    @staticmethod
    def get_a_transaction(transaction_id):
        WalletSqlRepository.get_a_transaction(transaction_id)
'''
