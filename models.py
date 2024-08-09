from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    name: str
    username: str
    password: str
    created_at: str

    def write_dict_user(self):
        return {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }


@dataclass
class Wallet:
    wallet_id: str
    balance: float
    username: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def write_dict_wall(self):
        return {
            'wallet_id': self.wallet_id,
            'balance': self.balance,
            'username': self.username,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


@dataclass
class Transaction:
    transaction_id: str
    created_at: str
    sender: str
    recipient: str
    amount: float
    transaction_type: str

    def write_dict_trans(self):
        return {
            'transaction_id': self.transaction_id,
            'created_at': self.created_at,
            'recipient': self.recipient,
            'amount': self.amount,
            'transaction_type': self.transaction_type
        }
