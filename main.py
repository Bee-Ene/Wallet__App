from urls import get_paths


class App:
    def __init__(self):
        self.app_active = None
        self.paths = get_paths()
        self.actions = {
            '1': self.signup,
            '2': self.login,
            '0': self.exit
        }

    def signup(self):
        self.paths['signup']()

    def login(self):
        path_dict = get_paths()
        success, name, wall_id = self.paths['login']()
        path_dict['username'] = name
        path_dict['wallet'] = wall_id
        logged_in_active = True
        state = {'logged_in_active': logged_in_active}
        while success and state['logged_in_active']:
            path_dict['logged_in'](path_dict['username'], state, path_dict['wallet'])

    def exit(self):
        print('\nExit.')
        self.app_active = False

    @staticmethod
    def invalid_selection():
        print('Error 404 \nPage not found.')

    def run(self):
        self.app_active = True
        print('Welcome to the wallet app')

        while self.app_active:
            print('Kindly enter the corresponding number to an action.')
            user_choice = str(input("1. Sign Up\n"
                                    "2. Login\n"
                                    "3. View Balance\n"
                                    "4. View all Transactions\n"
                                    "5. View a Transaction\n"
                                    "6. Receive Money\n"
                                    "7. Send Money\n"
                                    "8. View Profile\n"
                                    "9. View Wallet\n"
                                    "10. Logout\n"
                                    "0. Exit\n"))
            action = self.actions.get(user_choice, self.invalid_selection)
            action()


app = App()
app.run()
