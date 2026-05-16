import time
import schedule
import os
from dotenv import load_dotenv

from core.bot import TradingBot

def run_job():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Uruchamianie zaplanowanego zadania bota...")
    bot = TradingBot()
    bot.step()
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Zadanie zakończone.")

if __name__ == "__main__":
    load_dotenv() # Ładowanie zmiennych środowiskowych z pliku .env
    print("Rozpoczynam pracę w tle (Daemon Mode). Wciśnij Ctrl+C aby zatrzymać.")
    
    # Skonfigurowano uruchamianie co minutę (dla celów testowych). 
    # W produkcji zamień na np. schedule.every().day.at("16:00").do(run_job)
    schedule.every(1).minutes.do(run_job)
    
    # Wywołanie raz na start
    run_job()

    while True:
        schedule.run_pending()
        time.sleep(1)
