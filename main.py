import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, 
                             QPushButton, QLabel, QHeaderView)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

# Importy bota
from core.bot import TradingBot
from database.db_manager import DatabaseManager
import sqlite3

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capitol Tracker - Bot Dashboard")
        self.resize(1000, 700)

        self.bot = TradingBot()
        self.db = DatabaseManager()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Panel górny z kontrolkami bota
        top_panel = QHBoxLayout()
        self.status_label = QLabel("Status: Zatrzymany")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.run_step_btn = QPushButton("Uruchom analizę (1 krok)")
        self.run_step_btn.clicked.connect(self.run_bot_step)
        
        self.auto_btn = QPushButton("Start Auto-Bot")
        self.auto_btn.setCheckable(True)
        self.auto_btn.toggled.connect(self.toggle_auto_bot)

        top_panel.addWidget(self.status_label)
        top_panel.addStretch()
        top_panel.addWidget(self.run_step_btn)
        top_panel.addWidget(self.auto_btn)
        layout.addLayout(top_panel)

        # Tabele
        layout.addWidget(QLabel("<b>Wykryte Sygnały (Sygnały Kupna):</b>"))
        self.signals_table = QTableWidget()
        self.signals_table.setColumnCount(4)
        self.signals_table.setHorizontalHeaderLabels(["Ticker", "Score", "Polityk / Źródło", "Data Wykrycia"])
        self.signals_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.signals_table)

        layout.addWidget(QLabel("<b>Otwarte Pozycje Bota:</b>"))
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(4)
        self.positions_table.setHorizontalHeaderLabels(["Ticker", "Ilość", "Cena Zakupu", "Data Zakupu"])
        self.positions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.positions_table)

        # Timer do auto-bota
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_bot_step)

        # Pierwsze załadowanie
        self.refresh_tables()

    def run_bot_step(self):
        self.status_label.setText("Status: Analizowanie danych...")
        self.status_label.setStyleSheet("color: orange; font-weight: bold; font-size: 14px;")
        QApplication.processEvents() # Wymuszenie odświeżenia UI

        # Uruchom logikę bota
        self.bot.step()

        if self.auto_btn.isChecked():
            self.status_label.setText("Status: Auto-Bot aktywny")
            self.status_label.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")
        else:
            self.status_label.setText("Status: Oczekujący")
            self.status_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")
            
        self.refresh_tables()

    def toggle_auto_bot(self, checked):
        if checked:
            self.auto_btn.setText("Stop Auto-Bot")
            self.auto_btn.setStyleSheet("background-color: darkred; color: white;")
            # Z uruchamianiem co 3 sekundy dla celów testowych
            self.timer.start(3000) 
            self.status_label.setText("Status: Auto-Bot aktywny")
            self.status_label.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")
        else:
            self.auto_btn.setText("Start Auto-Bot")
            self.auto_btn.setStyleSheet("")
            self.timer.stop()
            self.status_label.setText("Status: Zatrzymany")
            self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")

    def refresh_tables(self):
        # Pobieranie z bazy SQLite
        if not os.path.exists(self.db.db_path):
            return

        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.cursor()
            
            # Ładowanie sygnałów
            try:
                cursor.execute("SELECT ticker, score, politician, detected_at FROM signals ORDER BY detected_at DESC LIMIT 50")
                signals = cursor.fetchall()
                self.signals_table.setRowCount(len(signals))
                for i, row in enumerate(signals):
                    self.signals_table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                    
                    score_item = QTableWidgetItem(str(row[1]))
                    if row[1] > 20:
                        score_item.setForeground(QColor("green"))
                    self.signals_table.setItem(i, 1, score_item)
                    
                    self.signals_table.setItem(i, 2, QTableWidgetItem(str(row[2])))
                    self.signals_table.setItem(i, 3, QTableWidgetItem(str(row[3])))
            except sqlite3.OperationalError:
                pass # Tabela może jeszcze nie istnieć

            # Ładowanie pozycji
            try:
                cursor.execute("SELECT ticker, quantity, buy_price, buy_time FROM positions ORDER BY buy_time DESC")
                positions = cursor.fetchall()
                self.positions_table.setRowCount(len(positions))
                for i, row in enumerate(positions):
                    self.positions_table.setItem(i, 0, QTableWidgetItem(str(row[0])))
                    self.positions_table.setItem(i, 1, QTableWidgetItem(str(row[1])))
                    self.positions_table.setItem(i, 2, QTableWidgetItem(f"${row[2]:.2f}"))
                    self.positions_table.setItem(i, 3, QTableWidgetItem(str(row[3])))
            except sqlite3.OperationalError:
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())