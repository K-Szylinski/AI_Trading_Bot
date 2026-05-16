from .base_broker import BaseBroker
from database.db_manager import DatabaseManager

class DemoBroker(BaseBroker):
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
        print("[DemoBroker] Zainicjalizowano lokalnego brokera (Konto Demo)")

    def buy(self, ticker: str, quantity: int, price: float) -> bool:
        cost = quantity * price
        balance = self.db.get_balance()
        
        if balance >= cost:
            # Wystarczająco gotówki, potrącamy kwotę
            self.db.update_balance(-cost)
            print(f"[DemoBroker] KUPNO: {quantity}x {ticker} po cenie ${price:.2f} (Koszt: ${cost:.2f})")
            return True
        else:
            print(f"[DemoBroker] ODRZUCONO ZAKUP {ticker}: Brak gotówki (Wymagane: ${cost:.2f}, Dostępne: ${balance:.2f})")
            return False

    def sell(self, ticker: str, quantity: int, price: float) -> bool:
        revenue = quantity * price
        self.db.update_balance(revenue)
        print(f"[DemoBroker] SPRZEDAŻ: {quantity}x {ticker} po cenie ${price:.2f} (Wpływ: ${revenue:.2f})")
        return True

    def get_positions(self):
        return self.db.get_open_positions()
