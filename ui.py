from bank import Bank
import re
from datetime import datetime


class UI:
    def __init__(self):
        self.bank = Bank()

    def run(self):
        while True:
            print("Bank Management System")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Close Account")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.create_account()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.check_balance()
            elif choice == "5":
                self.close_account()
            elif choice == "6":
                self.bank.db.close()
                break
            else:
                print("Invalid choice. Please try again.")

    def create_account(self):
        print("Create a New Account")
        full_name = input("Enter your full name: ")
        address = input("Enter your address: ")

        while True:
            phone_number = input("Enter your phone number (format: XXX-XXX-XXXX): ")
            if re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number):
                break
            else:
                print("Invalid phone number format. Please enter a valid phone number.")

        while True:
            birth_date = input("Enter your birth date (format: DD-MM-YYYY): ")
            try:
                date_obj = datetime.strptime(birth_date, "%d-%m-%Y")
                if 1900 <= date_obj.year <= datetime.now().year - 16:
                    break
                else:
                    print("Invalid birth date. You must be at least 16 years old to create an account.")
            except ValueError:
                print("Invalid date format. Please enter a valid birth date (DD-MM-YYYY).")

        while True:
            email = input("Enter your email address(format: username@example.com) : ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", email):
                break
            else:
                print("Invalid email format. Please enter a valid email address.")

        if not full_name or not address:
            print("All fields are required. Please try again.")
            return

        account = self.bank.create_account(full_name, email, address, phone_number, birth_date)
        print(f"Account created successfully! Account number: {account.account_number}")
        print(f"PIN: {account.pin}")

    def deposit(self):
        print("Deposit Money")
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")
        account = self.bank.get_account_by_number(account_number)

        if account and self.bank.verify_pin(account_number, pin):
            amount = float(input("Enter the deposit amount: "))
            if amount > 0:
                account.update_balance(amount, self.bank.db.cursor)
                self.bank.commit_changes()
                print(
                    f"Deposit of ${amount:.2f} successful. New balance: ${account.check_balance(self.bank.db.cursor):.2f}")
            else:
                print("Invalid amount. Please enter a positive value.")
        else:
            print("Invalid account number or PIN. Please try again.")

    def withdraw(self):
        print("Withdraw Money")
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        if self.bank.verify_pin(account_number, pin):
            account = self.bank.get_account_by_number(account_number)
            amount = float(input("Enter the withdrawal amount: "))

            if amount > 0:
                if account.withdraw(amount, self.bank.db.cursor):
                    self.bank.commit_changes()
                    print(f"Withdrawal of ${amount:.2f} successful. New balance: ${account.check_balance(self.bank.db.cursor):.2f}")
                else:
                    print("Insufficient funds. Withdrawal failed.")
            else:
                print("Invalid amount. Please enter a positive value.")
        else:
            print("Invalid account number or PIN. Please try again.")

    def check_balance(self):
        print("Check Account Balance")
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")

        if self.bank.verify_pin(account_number, pin):
            account = self.bank.get_account_by_number(account_number)
            if account:
                balance = account.check_balance(self.bank.db.cursor)
                if balance is not None:
                    print(f"Current balance for account {account_number}: ${balance:.2f}")
                else:
                    print("Failed to retrieve balance.")
            else:
                print("Account not found.")
        else:
            print("Invalid account number or PIN. Please try again.")

    def close_account(self):
        print("Close Account")
        account_number = input("Enter your account number: ")
        confirmation = input("Are you sure you want to close this account? (yes/no): ").lower()

        if confirmation == "yes":
            if self.bank.close_account(account_number):
                print(f"Account {account_number} has been closed.")
            else:
                print("Account not found or unable to close.")
        else:
            print("Account closure canceled.")
