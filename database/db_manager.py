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
