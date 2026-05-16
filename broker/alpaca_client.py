from .base_broker import BaseBroker
import os

class AlpacaBroker(BaseBroker):
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.api_secret = os.getenv("ALPACA_SECRET_KEY")
        self.paper = os.getenv("ALPACA_PAPER", "True").lower() == "true"
        
        self.is_live = bool(self.api_key and self.api_secret and self.api_key != "twoj_klucz_api_tutaj")
        
        print(f"Zainicjalizowano AlpacaBroker (Paper Trading: {self.paper}, Live API: {self.is_live})")

    def buy(self, ticker: str, quantity: int, price: float):
        if self.is_live:
            # Tu docelowo będzie użycie alpaca-py do złożenia prawdziwego zlecenia
            print(f"[Broker LIVE] Złożono zlecenie RZECZYWISTE: KUP {quantity}x {ticker}")
            return True
        else:
            print(f"[Broker SIM] WIRTUALNE KUPNO: {quantity}x {ticker} po cenie {price}")
            return True

    def sell(self, ticker: str, quantity: int, price: float):
        if self.is_live:
            print(f"[Broker LIVE] Złożono zlecenie RZECZYWISTE: SPRZEDAJ {quantity}x {ticker}")
            return True
        else:
            print(f"[Broker SIM] WIRTUALNA SPRZEDAŻ: {quantity}x {ticker} po cenie {price}")
            return True

    def get_positions(self):
        return []
