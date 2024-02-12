import sqlite3


class Database:
    def __init__(self, db_name='bank.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                account_number TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                balance REAL NOT NULL,
                pin TEXT NOT NULL    
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()
