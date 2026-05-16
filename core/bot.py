import time
import os
from data_providers.quiver_api import QuiverMockClient
from data_providers.market_data import MarketDataProvider
from engine.signal_analyzer import SignalAnalyzer
from broker.demo_broker import DemoBroker
from database.db_manager import DatabaseManager
from engine.risk_manager import RiskManager
from core.notifier import TelegramNotifier

class TradingBot:
    def __init__(self):
        self.data_provider = QuiverMockClient()
        self.market_data = MarketDataProvider()
        self.analyzer = SignalAnalyzer()
        self.db = DatabaseManager()
        self.broker = DemoBroker(self.db)
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
        positions = self.db.get_open_positions()
        for pos in positions:
            pos_id = pos['id']
            ticker = pos['ticker']
            buy_price = pos['buy_price']
            qty = pos['quantity']
            
            current_price = self.market_data.get_current_price(ticker)
            if current_price > 0:
                action = self.risk_manager.check_position(current_price, buy_price)
                if action in ["TAKE_PROFIT", "STOP_LOSS"]:
                    print(f"[Bot] Sygnał {action} dla {ticker}. Cena: {current_price}, Zakup: {buy_price}")
                    if self.broker.sell(ticker, qty, current_price):
                        self.db.remove_position(pos_id)
                        msg = f"🔵 <b>ZAMKNIĘCIE POZYCJI ({action})</b> 🔵\nTicker: <b>{ticker}</b>\nCena Sprzedaży: ${current_price:.2f}\nZysk/Strata: {((current_price - buy_price)/buy_price)*100:.2f}%"
                        self.notifier.send_message(msg)
        
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
            
            # Pobranie rzeczywistej ceny z API
            buy_price = self.market_data.get_current_price(ticker)
            
            if buy_price > 0:
                # Wirtualny zakup (np. stałe 10 akcji)
                qty = 10 
                if self.broker.buy(ticker, qty, buy_price):
                    self.db.log_position(ticker, qty, buy_price)
                    
                    # Wyślij powiadomienie
                    msg = f"🟢 <b>ZAKUP AKCJI</b> 🟢\nTicker: <b>{ticker}</b>\nScore: {score}\nIlość: {qty}\nCena: ${buy_price:.2f}"
                    self.notifier.send_message(msg)
            else:
                print(f"[Bot] Nie udało się pobrać aktualnej ceny dla {ticker}. Pomijam zakup.")
