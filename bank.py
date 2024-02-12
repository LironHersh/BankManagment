from database import Database
from account import Account


class Bank:
    def __init__(self):
        self.db = Database()
        self.accounts = []

    def create_account(self, full_name, email, address, phone_number, birth_date):
        account = Account(full_name, email, address, phone_number, birth_date)
        self.accounts.append(account)
        self.db.cursor.execute('''
            INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (account.account_number, account.full_name, account.email, account.address, account.phone_number,
              account.birth_date, account.balance, account.pin))
        self.commit_changes()
        return account

    def close_account(self, account_number):
        self.db.cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
        self.commit_changes()
        if self.db.cursor.rowcount > 0:
            return True
        else:
            return False


    def verify_pin(self, account_number, pin):
        self.db.cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
        account_data = self.db.cursor.fetchone()
        if account_data:
            return True
        return False

    def get_account_by_number(self, account_number):
        # Query the database to get the account based on the account number
        self.db.cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
        account_data = self.db.cursor.fetchone()

        if account_data:
            account = Account(
                account_data[1],  # full_name
                account_data[2],  # email
                account_data[3],  # address
                account_data[4],  # phone_number
                account_data[5],  # birth_date
            )
            account.account_number = account_data[0]
            account.balance = account_data[6]
            account.pin = account_data[7]
            return account
        return None

    def commit_changes(self):
        self.db.conn.commit()

    def deposit(self, account_number, amount):
        account = self.get_account_by_number(account_number)
        if account:
            account.deposit(amount, self.db.cursor)
            self.commit_changes()
            return True
        return False
