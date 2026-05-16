from core.bot import TradingBot

if __name__ == "__main__":
    bot = TradingBot()
    print("Uruchamianie testowej iteracji bota...")
    bot.step()
    print("Testowa iteracja zakończona. Sprawdź bazę danych 'bot_data.db'.")
