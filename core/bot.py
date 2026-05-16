import time
import os
from data_providers.quiver_api import QuiverMockClient
from engine.signal_analyzer import SignalAnalyzer
from broker.alpaca_client import AlpacaBroker
from database.db_manager import DatabaseManager
from engine.risk_manager import RiskManager
from core.notifier import TelegramNotifier

class TradingBot:
    def __init__(self):
        self.data_provider = QuiverMockClient()
        self.analyzer = SignalAnalyzer()
        self.broker = AlpacaBroker()
        self.db = DatabaseManager()
        self.risk_manager = RiskManager()
        self.notifier = TelegramNotifier(
            token=os.getenv("TELEGRAM_BOT_TOKEN"),
            chat_id=os.getenv("TELEGRAM_CHAT_ID")
        )
        self.is_running = False

    def step(self):
        print("\n--- [Bot] Rozpoczynam iterację analityczną ---")
        
        # 0. Bezpieczeństwo - Kopia zapasowa bazy przed zmianami
        self.db.backup_db()
        
        # 0.1 Zarządzanie ryzykiem - symulacyjne sprawdzenie portfela
        print("[Bot] Weryfikacja reguł ryzyka (Stop-Loss / Take-Profit)...")
        # Tutaj w przyszłości można dołączyć kod pobierający aktualne ceny z API.
        
        # 1. Pobranie danych
        data = self.data_provider.fetch_recent_trades()
        print(f"[Bot] Pobrano {len(data)} najnowszych transakcji insiderów.")

        # 2. Analiza sygnałów
        signals = self.analyzer.analyze(data)
        print(f"[Bot] Wykryto {len(signals)} sygnałów kupna.")

        # 3. Egzekucja
        for sig in signals:
            ticker = sig['ticker']
            score = sig['score']
            print(f"[Bot] Silny sygnał dla {ticker} (Score: {score}). Realizacja zlecenia...")
            
            # Zapisz do bazy
            self.db.log_signal(ticker, "Multiple Insiders", "N/A", score)
            
            # Wirtualny zakup (np. zawsze 10 akcji)
            buy_price = 100.0 # Przykładowa cena do testów risk managera
            if self.broker.buy(ticker, 10, buy_price):
                self.db.log_position(ticker, 10, buy_price)
                
                # Wyślij powiadomienie
                msg = f"🟢 <b>ZAKUP AKCJI</b> 🟢\nTicker: <b>{ticker}</b>\nScore: {score}\nIlość: 10\nCena: ${buy_price}"
                self.notifier.send_message(msg)
