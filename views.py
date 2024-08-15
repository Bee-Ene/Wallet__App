from datetime import datetime
import random
from index import get_connection
import psycopg2
import psycopg2.extras
import bcrypt
from controllers import WalletFunctions
from models import User, Wallet, Transaction
from repository import UserSqlRepository, WalletSqlRepository


class UserView:

    @staticmethod
    def signup():
        name = input('Enter your name: ')
        username = input('Enter username: ')
        if UserSqlRepository.username_exists(username):
            print('Username already exists.\nTry another username.')
            return
        # password = getpass.getpass('Enter password: ')
        password = str(input('Enter password: '))
        wallet_id = str(random.randint(1, 10000))
        created_at = str(datetime.now().isoformat())

        user = User(name, username, password, created_at)
        if UserSqlRepository.create_user(user):
            wallet = Wallet(wallet_id, username)
            WalletSqlRepository.create_wallet(wallet)

    @staticmethod
    def login():
        username = input('Enter username: ')
        password = input('Enter password: ')
        success, name, wall_id = UserView.load_user(username, password)
        if success:
            print('Login Successful!')
        return success, name, wall_id

    @staticmethod
    def load_user(username: str, password: str):
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('''SELECT password from user_db WHERE username=%s''', (username,))
        result = cur.fetchone()
        if result:
            stored_password = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # get the wallet id of the user from the db
                cur.execute('''SELECT wallet_id FROM wallet_db WHERE username = %s''', (username,))
                wallet_id = cur.fetchone()[0]
                return True, username, wallet_id
            else:
                print('Login failed.')
                return False, None, None
        else:
            print('Login failed.')
            return False, None, None

    @staticmethod
    def logged_in(username, state, wallet_id):
        while state['logged_in_active']:
            user_choice = str(input("1. View Balance\n"
                                    "2. View all Transactions\n"
                                    "3. View a Transaction\n"
                                    "4. Receive Money\n"
                                    "5. Send Money\n"
                                    "6. View Profile\n"
                                    "7. View Wallet\n"
                                    "8. Logout\n"
                                    ))
            if user_choice == '1':
                WalletView.view_balance(wallet_id)
            elif user_choice == '2':
                WalletView.view_transactions(username)
            elif user_choice == '3':
                WalletView.view_a_transaction()
            elif user_choice == '4':
                WalletView.view_receive_money(wallet_id)
            elif user_choice == '5':
                WalletView.view_send_money(wallet_id)
            elif user_choice == '6':
                UserView.view_profile(username)
            elif user_choice == '7':
                WalletView.view_wallet(wallet_id)
            elif user_choice == '8':
                state['logged_in_active'] = False
            else:
                print('\n Input is invalid.')

    @classmethod
    def view_profile(cls, username):
        UserSqlRepository.profile_user(username)


class WalletView:
    wallet = str

    @staticmethod
    def view_receive_money(wall_id_):
        amount = input('Enter amount: ')
        try:
            amount = float(amount)
            WalletFunctions.receive_money(wall_id_, amount)
            #WalletSqlRepository.check_balance(wall_id_)
        except ValueError as e:
            print(f'{e}')

    @staticmethod
    def view_send_money(wallet_id):
        recipient = str(input("Enter recipient's username: "))
        amount = input('Enter amount: ')
        try:
            amount = float(amount)
            WalletFunctions.send_money(wallet_id, amount, recipient)
            WalletSqlRepository.check_balance(wallet_id)
        except ValueError as e:
            print(f'{e}')
        except Exception as e:
            print(f'{e}')

    @staticmethod
    def view_balance(wallet_id):
        WalletSqlRepository.check_balance(wallet_id)

    @staticmethod
    def view_wallet(wallet_id):
        WalletSqlRepository.profile_wallet(wallet_id)

    @staticmethod
    def view_transactions(username):
        return WalletFunctions.get_transactions(username)

    @staticmethod
    def view_a_transaction():
        transaction_id = input('Enter the transaction ID: ')
        WalletFunctions.get_a_transaction(transaction_id)