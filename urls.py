from views import UserView, WalletView


def get_paths():

    return {
        'signup': UserView.signup,
        'wallet': WalletView.wallet,
        'login': UserView.login,
        'logged_in': UserView.logged_in,
        'view_balance': WalletView.view_balance,
        'view_all_transactions': WalletView.view_transactions,
        'view_a_transaction': WalletView.view_a_transaction,
        'receive_money': WalletView.view_receive_money,
        'send money': WalletView.view_send_money,
        'view_profile': UserView.view_profile,
        'view_wallet': WalletView.view_wallet
     }
