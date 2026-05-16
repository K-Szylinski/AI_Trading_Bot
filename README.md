# Dokumentacja Projektu: Capitol Tracker (Bot Inwestycyjny)

Ten dokument zawiera wszystkie najważniejsze informacje dotyczące obecnego stanu projektu, jego architektury, sposobu działania oraz instrukcji obsługi.

> [!WARNING]
> **Zastrzeżenie (Disclaimer)**
> Aplikacja w obecnym kształcie to prototyp (Proof of Concept). Operuje na wirtualnych danych i wirtualnym brokerze (tzw. Paper Trading). Zanim podłączysz pod nią prawdziwy kapitał giełdowy, system wymaga rygorystycznych testów, wdrożenia testów jednostkowych i solidnego modułu zarządzania ryzykiem (np. Stop-Loss).

---

## 1. Architektura Systemu

Aplikacja została przebudowana na architekturę modułową. Zamiast jednego dużego skryptu, projekt dzieli się na logiczne pakiety, co pozwala na łatwą rozbudowę w przyszłości.

Oto kluczowe katalogi i ich przeznaczenie:

* **`core/`**: Serce bota.
  * `bot.py`: Znajduje się tu główna pętla logiczna `TradingBot`. Łączy ona wszystkie inne moduły w spójny proces (pobierz dane -> analizuj -> kup/sprzedaj).
* **`data_providers/`**: Moduły odpowiedzialne za pobieranie danych ze świata zewnętrznego.
  * `quiver_api.py`: Obecnie znajduje się tu mock (symulator), który na bieżąco generuje sztuczne transakcje kongresmenów. W przyszłości zostanie zastąpiony prawdziwymi zapytaniami sieciowymi do API.
  * `market_data.py`: Moduł odpowiedzialny za pobieranie **prawdziwych cen akcji na żywo** za pośrednictwem biblioteki `yfinance`. Posiada wbudowany cache.
* **`engine/`**: Logika decyzyjna ("mózg").
  * `signal_analyzer.py`: Moduł, który ocenia "siłę" transakcji. Aktualnie poszukuje zjawiska "klastrowania" – jeśli minimum 2 osoby kupią akcje tej samej spółki, aplikacja generuje `Sygnał`.
  * `risk_manager.py`: Moduł odpowiedzialny za zarządzanie ryzykiem inwestycji, decydujący m.in. o realizacji zysków (Take-Profit) i cięciu strat (Stop-Loss).
* **`broker/`**: Zewnętrzny świat giełdowy.
  * `base_broker.py`: Czysty interfejs (szablon).
  * `demo_broker.py`: Wbudowany symulator brokera (Konto Demo), operujący na wirtualnym kapitale zapisywanym w lokalnej bazie danych. Chroni przed inwestowaniem realnych pieniędzy.
  * `alpaca_client.py`: (Przyszłościowy) Klient brokera Alpaca do prawdziwych rynków.
* **`database/`**: Pamięć długotrwała.
  * `db_manager.py`: Odpowiada za tworzenie bazy SQLite (`bot_data.db`) i zapisywanie tam historii. Przechowuje logi sygnałów, aktualnie otwarte pozycje oraz saldo Twojego **konta demo** (wirtualną gotówkę).

Oprócz tego na zewnątrz mamy:
* **`main.py`**: Interfejs Graficzny (Dashboard). Panel sterowania botem.
* **`run_bot.py`**: Lekki skrypt pozwalający uruchomić bota z konsoli, całkowicie z pominięciem GUI.

---

## 2. Jak działa cykl życia Bota?

Podczas pojedynczego cyklu (tzw. _kroku_), zachodzi następująca sekwencja zdarzeń (możesz to prześledzić w pliku `core/bot.py`):

0. **Zarządzanie Pozycjami:** Bot sprawdza aktualne ceny dla wszystkich akcji, które posiada w wirtualnym portfelu (poprzez `yfinance`). Przesyła ceny do `RiskManager`, który decyduje czy zamknąć pozycję (Take-Profit / Stop-Loss) aktualizując przy tym Twoje saldo gotówki.
1. **Zbieranie danych:** Bot pyta `QuiverMockClient` o najnowsze zadeklarowane transakcje.
2. **Poszukiwanie sygnału:** Surowe dane wędrują do `SignalAnalyzer`. Jeżeli wykryje on "klastrowanie" zakupów dla danej spółki, generuje silny `Sygnał`.
3. **Decyzja Brokerska:** Wykryty sygnał skutkuje próbą zakupu. Bot pobiera rzeczywistą cenę rynkową akcji (`yfinance`) i odpytuje `DemoBroker`, czy posiada wystarczające środki wirtualne.
4. **Zapis do bazy (Logowanie):** Przy pozytywnej weryfikacji zlecenie zostaje zrealizowane (potrącenie gotówki i zapis do `positions`). Wszelkie zdarzenia zapisywane są trwale na dysku w pliku `bot_data.db`.

---

## 3. Jak korzystać z Dashboardu (`main.py`)?

Aplikacja graficzna (Dashboard) to nakładka, która co pewien czas wywołuje powyższy cykl i wyświetla to, co znajduje się w bazie danych.

**Elementy interfejsu:**
* **Górny Pasek:** Wyświetla aktualny **Status Bota**, dostępną wirtualną **Gotówkę (Cash)** oraz szacowaną całkowitą **Wartość Portfela** z uwzględnieniem prawdziwych aktualnych cen z giełdy.
* **Tabela Wykryte Sygnały (u góry):** Wyświetla historyczne sygnały, które zostały zidentyfikowane przez analizator. Rekordy ze "Score" powyżej 20 pkt podświetlają się na zielono.
* **Tabela Otwarte Pozycje (na dole):** Pokazuje wirtualny portfel akcji. Zobaczysz w nim m.in. Cenę Zakupu, **Aktualną Cenę** (na żywo z rynku) oraz niezrealizowany **PnL (Zysk/Stratę w %)** z odpowiednim kolorowaniem.
* **Przycisk [Uruchom analizę (1 krok)]:** Wymusza jednorazowe obudzenie bota. Powoduje odpalenie pojedynczego cyklu analitycznego. Użyj tego, jeśli chcesz ręcznie kontrolować moment kupna.
* **Przycisk [Start Auto-Bot]:** Uruchamia bota w trybie autonomicznym. Dla celów demonstracyjnych w tym trybie bot wykonuje nowy skan rynku co 3 sekundy.

> [!TIP]
> Najlepszym sposobem na zrozumienie działania jest kliknięcie przycisku **"Start Auto-Bot"** w `main.py` i obserwowanie, jak bazy i tabele same wypełniają się danymi!

---

## 4. Dalsza Mapa Drogowa (Roadmap)

To, co udało nam się zrealizować, to dopiero szkielet systemu. Zgodnie z wygenerowanym wcześniej Task List, czekają nas kolejne istotne zadania:

* **Prawdziwe Dane API (Krok 2):** Zastąpienie funkcji losujących prawdziwymi zapytaniami REST do darmowych źródeł raportujących działania z SEC lub z Kongresu.
* **Zarządzanie Pozycją (Zrealizowane ✓):** Wbudowany silnik `RiskManager` potrafi zamykać pozycje przy ustalonym zysku (Take-Profit) i stracie (Stop-Loss). Wymaga tylko kalibracji parametrów.
* **Integracja z prawdziwą giełdą (Krok 4):** Gdy silnik analityczny będzie wysoce skuteczny na koncie demo, ostatecznym etapem jest zarejestrowanie konta u brokera giełdowego (np. Alpaca), wpisanie prawdziwych kluczy API do aplikacji i przesiadka z `DemoBroker` na prawdziwy system egzekucyjny.
