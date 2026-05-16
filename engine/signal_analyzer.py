class SignalAnalyzer:
    def __init__(self):
        self.tracked_tickers = set()

    def analyze(self, transactions_data: list):
        """
        Analizuje surowe dane w poszukiwaniu "sygnałów" do kupna.
        """
        signals = []
        # Grupowanie transakcji po tickerze
        ticker_groups = {}
        for t in transactions_data:
            if t['type'] == 'Zakup':
                ticker = t['ticker']
                if ticker not in ticker_groups:
                    ticker_groups[ticker] = []
                ticker_groups[ticker].append(t)

        # Ocena sygnałów
        for ticker, trades in ticker_groups.items():
            if len(trades) >= 2:  # Przynajmniej 2 insiderów kupiło
                score = len(trades) * 10  # Prosty scoring
                signals.append({
                    'ticker': ticker,
                    'score': score,
                    'trades': trades
                })
        return signals
