import random
import string


class Account:
    def __init__(self, full_name, email, address, phone_number, birth_date):
        self.account_number = self.generate_account_number()
        self.full_name = full_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.balance = 0.0
        self.pin = self.generate_pin()

    def generate_account_number(self):
        return ''.join(random.choice(string.digits) for _ in range(5))

    def generate_pin(self):
        return ''.join(random.choice(string.digits) for _ in range(4))

    def deposit(self, amount, db_cursor):
        self.balance += amount
        db_cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                          (self.balance, self.account_number))

    def withdraw(self, amount, db_cursor):
        if amount <= self.balance:
            self.balance -= amount
            db_cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                              (self.balance, self.account_number))
            return True
        else:
            return False

    def check_balance(self, db_cursor):
        db_cursor.execute("SELECT balance FROM accounts WHERE account_number = ?",
                          (self.account_number,))
        balance_data = db_cursor.fetchone()

        if balance_data:
            return balance_data[0]
        return None

    def update_balance(self, amount, db_cursor):
        self.balance += amount
        db_cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?",
                          [self.balance, self.account_number])
