class Account:
    def __init__(self, a_id, a_type, a_balance, username):
        self.id = a_id
        self.type = a_type
        self.balance = a_balance
        self.username = username

    def to_dict(self):
        return {
            "a_id": self.id,
            "a_type": self.type,
            "a_balance": self.balance,
            "username": self.username
        }
