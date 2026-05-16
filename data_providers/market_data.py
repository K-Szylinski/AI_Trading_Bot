import yfinance as yf
import time

class MarketDataProvider:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 300 # 5 minut w cache

    def get_current_price(self, ticker: str) -> float:
        current_time = time.time()
        
        if ticker in self.cache:
            cached_price, timestamp = self.cache[ticker]
            if current_time - timestamp < self.cache_ttl:
                return cached_price
                
        try:
            ticker_data = yf.Ticker(ticker)
            price = None
            try:
                price = ticker_data.fast_info['lastPrice']
            except Exception:
                hist = ticker_data.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]

            if price and price > 0:
                self.cache[ticker] = (price, current_time)
                return price
            return 0.0
        except Exception as e:
            print(f"[MarketData] Błąd pobierania ceny dla {ticker}: {e}")
            return 0.0
