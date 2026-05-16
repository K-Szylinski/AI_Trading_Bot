class RiskManager:
    def __init__(self, take_profit_pct=0.15, stop_loss_pct=-0.07):
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct

    def check_position(self, current_price: float, buy_price: float) -> str:
        """
        Zwraca 'HOLD', 'TAKE_PROFIT' lub 'STOP_LOSS' w zależności od zmiany ceny.
        """
        if buy_price <= 0:
            return "HOLD"
            
        change = (current_price - buy_price) / buy_price
        
        if change >= self.take_profit_pct:
            return "TAKE_PROFIT"
        elif change <= self.stop_loss_pct:
            return "STOP_LOSS"
            
        return "HOLD"
