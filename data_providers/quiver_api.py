import random
import requests
import os
from datetime import datetime, timedelta

class QuiverMockClient:
    """Klient API - przełącza między Mockiem a prawdziwym API na podstawie klucza z .env"""
    def __init__(self):
        self.api_key = os.getenv("QUIVER_API_KEY")
        self.base_url = "https://api.quiverquant.com/beta/live/congresstrading"

    def fetch_recent_trades(self):
        if self.api_key and self.api_key != "opcjonalny_klucz_quiver":
            # Wywołanie prawdziwego API
            try:
                headers = {'accept': 'application/json', 'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhCE', 'Authorization': f'Token {self.api_key}'}
                response = requests.get(self.base_url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Formatowanie zgodnie z oczekiwaniami naszego bota
                formatted = []
                for t in data[:50]: # Ogranicz do 50 ostatnich
                    formatted.append({
                        "name": t.get("Representative", "Nieznany"),
                        "ticker": t.get("Ticker", ""),
                        "type": "Zakup" if t.get("Transaction", "") == "Purchase" else "Sprzedaż",
                        "amount_usd": 50000, # Szacunkowo, API Quiver daje zasięgi a nie kwoty
                        "date": t.get("TransactionDate", "")
                    })
                return formatted
            except Exception as e:
                print(f"[Quiver API] Błąd łączenia z prawdziwym API: {e}. Przechodzę w tryb Mock.")

        # Fallback na dane symulowane (Mock)
        politicians = ["Warren Davidson", "Donald Norcross", "Nancy Pelosi", "Rick Scott", "Alex Padilla"]
        tickers = ["NVDA", "MSFT", "AAPL", "AMD", "GE", "PLTR", "INTC"]
        
        simulated_data = []
        for _ in range(50):
            simulated_data.append({
                "name": random.choice(politicians),
                "ticker": random.choice(tickers),
                "type": random.choice(["Zakup", "Sprzedaż"]),
                "amount_usd": random.randint(10000, 500000),
                "date": (datetime.now() - timedelta(days=random.randint(1, 14))).strftime("%Y-%m-%d")
            })
        return simulated_data
