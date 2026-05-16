import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="bot_data.db"):
        self.db_path = db_path
        self.init_db()

    def backup_db(self):
        """Kopia zapasowa bazy danych, używana przez demona przed ważnymi operacjami."""
        if os.path.exists(self.db_path):
            import shutil
            backup_path = self.db_path + ".bak"
            shutil.copy2(self.db_path, backup_path)
            print(f"[Database] Wykonano kopię zapasową bazy do {backup_path}")

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Tabela sygnałów
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    politician TEXT,
                    transaction_date TEXT,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    score REAL
                )
            ''')
            # Tabela otwartych pozycji
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS positions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT,
                    buy_price REAL,
                    quantity INTEGER,
                    buy_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Tabela konta demo
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS account (
                    id INTEGER PRIMARY KEY,
                    cash_balance REAL
                )
            ''')
            # Inicjalizacja konta początkowym kapitałem
            cursor.execute('SELECT COUNT(*) FROM account')
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO account (id, cash_balance) VALUES (1, 100000.0)')
            conn.commit()

    def log_signal(self, ticker, politician, transaction_date, score):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO signals (ticker, politician, transaction_date, score)
                VALUES (?, ?, ?, ?)
            ''', (ticker, politician, transaction_date, score))
            conn.commit()

    def log_position(self, ticker, quantity, buy_price):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO positions (ticker, quantity, buy_price)
                VALUES (?, ?, ?)
            ''', (ticker, quantity, buy_price))
            conn.commit()

    def remove_position(self, position_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM positions WHERE id = ?', (position_id,))
            conn.commit()

    def get_open_positions(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, ticker, quantity, buy_price, buy_time FROM positions')
            return [{"id": row[0], "ticker": row[1], "quantity": row[2], "buy_price": row[3], "buy_time": row[4]} for row in cursor.fetchall()]

    def get_balance(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT cash_balance FROM account WHERE id = 1')
            row = cursor.fetchone()
            return row[0] if row else 0.0

    def update_balance(self, amount):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT cash_balance FROM account WHERE id = 1')
            row = cursor.fetchone()
            if row:
                new_balance = row[0] + amount
                cursor.execute('UPDATE account SET cash_balance = ? WHERE id = 1', (new_balance,))
                conn.commit()
                return new_balance
            return 0.0
