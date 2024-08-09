from datetime import datetime
import random
from models import User, Wallet, Transaction
from repository import UserSqlRepository, WalletSqlRepository


class UserView:

    @staticmethod
    def signup():
        name = input('Enter your name: ')
        username = input('Enter username: ')
        # password = getpass.getpass('Enter password: ')
        password = str(input('Enter password: '))
        wallet_id = str(random.randint(1, 10000))
        created_at = str(datetime.now().isoformat())
        balance = 0.0

        user = User(name, username, password, created_at)
        if UserSqlRepository.create_user(user):
            wallet = Wallet(wallet_id, balance, username)
            WalletSqlRepository.create_wallet(wallet)

    @staticmethod
    def login():
        username = input('Enter username: ')
        password = input('Enter password: ')
        success, name, wall_id = UserSqlRepository.load_user(username, password)
        if success:
            print('Login Successful!')
        return success, name, wall_id

    @staticmethod
    def logged_in(username, state, wallet_id):
        while state['logged_in_active']:
            user_choice = str(input("1. View Balance\n"
                                    "2. View all Transactions\n"
                                    "3. View a Transaction"
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
            username = WalletSqlRepository.receive_money(wall_id=wall_id_, amount=amount)
            created_at = datetime.now().isoformat()
            transaction_id = str(created_at) + '-' + str(amount)
            recipient = ''
            sender = username
            transaction_type = 'receive'
            transaction = Transaction(transaction_id, created_at, sender, recipient, amount, transaction_type)
            WalletSqlRepository.insert_transaction(transaction)
        except ValueError as e:
            print(f'{e}')

    @staticmethod
    def view_send_money(wallet_id):
        recipient = str(input("Enter recipient's username: "))
        amount = input('Enter amount: ')
        try:
            amount = float(amount)
            username = WalletSqlRepository.send_money(wallet_id, amount, recipient)
            created_at = datetime.now().isoformat()
            transaction_id = str(created_at) + '-' + str(amount)
            recipient = recipient
            sender = username
            transaction_type = 'send'
            transaction = Transaction(transaction_id, created_at, sender, recipient, amount, transaction_type)
            WalletSqlRepository.insert_transaction(transaction)
        except ValueError as e:
            print(f'{e}')

    @staticmethod
    def view_balance(wallet_id):
        WalletSqlRepository.check_balance(wallet_id)

    @staticmethod
    def view_wallet(wallet_id):
        WalletSqlRepository.profile_wallet(wallet_id)

    @staticmethod
    def view_transactions(username):
        return WalletSqlRepository.get_transactions(username)

    @staticmethod
    def view_a_transaction():
        transaction_id = input('Enter the transaction ID: ')
        WalletSqlRepository.get_a_transaction(transaction_id)
