# Plan Przejścia na Produkcję: W Pełni Autonomiczny Bot Serwerowy

Aby przekształcić ten projekt z prototypu w maszynkę zdolną do działania 24/7 na zewnętrznym serwerze (VPS / Chmura) i zarabiania prawdziwych pieniędzy, konieczne jest wdrożenie szeregu zabezpieczeń, algorytmów oraz integracji. 

Oto kompletna lista kroków (Roadmap) do pełnej autonomii:

## Faza 1: Prawdziwe Dane i Backtesting (Inteligencja)
Zanim zaryzykujesz dolara, musisz wiedzieć, że algorytm jest skuteczny.
- [ ] **Integracja Prawdziwego API:** Podpięcie API z prawdziwymi danymi (np. SEC Edgar dla Form 4 lub płatne API Quiver Quantitative / Capitol Trades). Należy obsłużyć limity odpytań (Rate Limits).
- [ ] **Moduł Backtestingu:** Zbudowanie skryptu, który przepuści algorytm przez dane historyczne z ostatnich 5 lat. Pokaże nam to wirtualny zysk, obsunięcie kapitału (Drawdown) i wskaźnik Sharpe'a.
- [ ] **Filtrowanie Szumu (Signal Tuning):** Odrzucanie transakcji polityków, którzy na giełdzie historycznie tracą. Skupienie się wyłącznie na "najlepszych" graczach i transakcjach na duże kwoty (np. > $100k).

## Faza 2: Zarządzanie Ryzykiem i Portfelem (Bezpieczeństwo Kapitału)
Bot na ten moment tylko "kupuje". Musi wiedzieć, jak chronić kapitał i kiedy realizować zyski.
- [ ] **Take-Profit (Realizacja Zysku):** Algorytm zamykający pozycję, gdy akcja wzrośnie o założony procent.
- [ ] **Stop-Loss / Trailing Stop:** Algorytm zamykający pozycję ze stratą (np. przy spadku o 7%), aby zapobiec wyzerowaniu portfela przy nagłym krachu danej spółki.
- [ ] **Position Sizing (Alokacja):** Bot musi wiedzieć, ile akcji kupić w oparciu o wolną gotówkę na koncie. Złota zasada: nigdy nie inwestuj więcej niż np. 5-10% całego kapitału w jedną spółkę.

## Faza 3: Integracja z Prawdziwym Brokerem
- [ ] **Wybór i Podpięcie Brokera:** Zmiana symulatora na produkcyjne API (np. Interactive Brokers API, Alpaca Live, XTB).
- [ ] **Obsługa Błędów Sieciowych:** Co jeśli giełda odrzuci zlecenie? Co jeśli zerwie się połączenie z internetem w trakcie kupowania? Bot musi posiadać potężny mechanizm tzw. *Retry* (ponawiania zapytań) i łapania wyjątków.
- [ ] **Handel Poza Godzinami (Pre-Market / After-Hours):** Decyzja i implementacja, czy bot może reagować na informacje w nocy.

## Faza 4: Wdrożenie na Serwer (Deployment)
Projekt musi działać 24/7, niezależnie od tego, czy Twój komputer jest włączony.
- [ ] **Dockerization:** Stworzenie pliku `Dockerfile`, który "spakuje" całego bota wraz z bibliotekami do jednego wirtualnego kontenera. Gwarantuje to, że zadziała na każdym serwerze.
- [ ] **Wykupienie Serwera VPS:** Wynajęcie taniego serwera na Linuxie (np. na AWS, DigitalOcean, Hetzner - koszt ok. 5$ miesięcznie).
- [ ] **Proces w tle (Daemonization):** Uruchomienie bota przy użyciu narzędzi takich jak `Systemd` lub `Supervisor`. Dzięki temu, jeśli serwer się zrestartuje, bot automatycznie wstanie sam.
- [ ] **Harmonogram (Cron/APScheduler):** Konfiguracja zadań w tle pobierających dane od brokera, sprawdzających pozycje i szukających sygnałów np. co 5 minut w czasie trwania sesji giełdowej.

## Faza 5: Monitoring i Alerty (Kontrola z Telefonu)
Skoro bot działa na serwerze bez interfejsu graficznego (GUI), musisz wiedzieć, co robi.
- [ ] **Powiadomienia Telegram / Discord:** Bot powinien wysyłać Ci wiadomość na telefon za każdym razem, gdy kupi lub sprzeda akcje. Otrzymasz też powiadomienie (Alert Krytyczny) w razie awarii API.
- [ ] **Bezpieczeństwo Kluczy (Secret Management):** Klucze do API giełdy muszą zostać usunięte z kodu i przeniesione do bezpiecznych zmiennych środowiskowych (`.env`) na serwerze.
- [ ] **Kopia Zapasowa Bazy Danych:** Skrypt codziennie wykonujący backup bazy `bot_data.db` (np. na zewnętrzny dysk S3), żeby w razie awarii serwera nie stracić historii transakcji.

---
**Rekomendowana Kolejność Działania:**
Obecnie najlepiej rozpocząć od **Fazy 1 i 2**, używając konta typu Paper Trading (wirtualne pieniądze u prawdziwego brokera). Taki bot ląduje od razu na serwerze (Faza 4) i pracuje "na sucho" przez 2 miesiące. Po zweryfikowaniu zysków, zdejmujemy zabezpieczenia i podpinamy prawdziwe pieniądze.
