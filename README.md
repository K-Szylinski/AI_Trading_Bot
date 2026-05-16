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
* **`engine/`**: Logika decyzyjna ("mózg").
  * `signal_analyzer.py`: Moduł, który ocenia "siłę" transakcji. Aktualnie poszukuje zjawiska "klastrowania" – jeśli minimum 2 osoby kupią akcje tej samej spółki, aplikacja generuje `Sygnał`.
* **`broker/`**: Zewnętrzny świat giełdowy.
  * `base_broker.py`: Czysty interfejs (szablon).
  * `alpaca_client.py`: Klient brokera Alpaca. Na razie operuje w trybie symulacji – przyjmuje zlecenia, nie łącząc się z fizyczną giełdą.
* **`database/`**: Pamięć długotrwała.
  * `db_manager.py`: Odpowiada za tworzenie bazy SQLite (`bot_data.db`) i zapisywanie tam historii. Bot zapisuje tam dwie rzeczy: znalezione sygnały kupna oraz aktualnie otwarte pozycje w portfelu.

Oprócz tego na zewnątrz mamy:
* **`main.py`**: Interfejs Graficzny (Dashboard). Panel sterowania botem.
* **`run_bot.py`**: Lekki skrypt pozwalający uruchomić bota z konsoli, całkowicie z pominięciem GUI.

---

## 2. Jak działa cykl życia Bota?

Podczas pojedynczego cyklu (tzw. _kroku_), zachodzi następująca sekwencja zdarzeń (możesz to prześledzić w pliku `core/bot.py`):

1. **Zbieranie danych:** Bot pyta `QuiverMockClient` o najnowsze zadeklarowane transakcje z ostatnich dwóch tygodni.
2. **Poszukiwanie sygnału:** Surowe dane wędrują do `SignalAnalyzer`. Analizator grupuje je po symbolu spółki (Tickerze). Jeśli zauważy, że np. dla spółki "NVDA" w krótkim czasie zakupu dokonało 2 lub więcej insiderów, nadaje temu zdarzeniu "Score" (np. 20 pkt) i oznacza to jako silny sygnał.
3. **Decyzja Brokerska:** Wykryty sygnał trafia do brokera (`AlpacaBroker`). Generowane jest wirtualne zlecenie "Kup 10 akcji NVDA".
4. **Zapis do bazy (Logowanie):** Zlecenie jest trwale zapisywane na dysku komputera w pliku `bot_data.db`. Zapisywany jest powód (w tabeli `signals`) oraz sam fakt fizycznego posiadania akcji (w tabeli `positions`).

---

## 3. Jak korzystać z Dashboardu (`main.py`)?

Aplikacja graficzna (Dashboard) to nakładka, która co pewien czas wywołuje powyższy cykl i wyświetla to, co znajduje się w bazie danych.

**Elementy interfejsu:**
* **Tabela Wykryte Sygnały (u góry):** Wyświetla historyczne sygnały, które zostały zidentyfikowane przez analizator. Rekordy ze "Score" powyżej 20 pkt podświetlają się na zielono.
* **Tabela Otwarte Pozycje (na dole):** Pokazuje wirtualny portfel akcji, czyli to, co zdołał kupić broker.
* **Przycisk [Uruchom analizę (1 krok)]:** Wymusza jednorazowe obudzenie bota. Powoduje odpalenie pojedynczego cyklu analitycznego. Użyj tego, jeśli chcesz ręcznie kontrolować moment kupna.
* **Przycisk [Start Auto-Bot]:** Uruchamia bota w trybie autonomicznym. Dla celów demonstracyjnych w tym trybie bot wykonuje nowy skan rynku co 3 sekundy.

> [!TIP]
> Najlepszym sposobem na zrozumienie działania jest kliknięcie przycisku **"Start Auto-Bot"** w `main.py` i obserwowanie, jak bazy i tabele same wypełniają się danymi!

---

## 4. Dalsza Mapa Drogowa (Roadmap)

To, co udało nam się zrealizować, to dopiero szkielet systemu. Zgodnie z wygenerowanym wcześniej Task List, czekają nas kolejne istotne zadania:

* **Prawdziwe Dane API (Krok 2):** Zastąpienie funkcji losujących prawdziwymi zapytaniami REST do darmowych źródeł raportujących działania z SEC lub z Kongresu.
* **Zarządzanie Pozycją (Krok 3):** Aktualnie bot "tylko kupuje". Nie wie, kiedy sprzedać. Potrzebujemy zaimplementować tzw. *Take-Profit* (sprzedaj po np. +10% zysku) oraz *Stop-Loss* (sprzedaj, by ciąć straty przy spadku -5%).
* **Integracja z prawdziwą giełdą (Krok 4):** Gdy silnik będzie skuteczny, zarejestrowanie konta u brokera (np. Alpaca, gdzie można mieć za darmo konto Paper Trading ze sztucznymi 100 tys. USD), zdobycie prawdziwych kluczy API, wpisanie ich w `alpaca_client.py` i puszczenie bota na realne rynki bez obawy o utratę realnych pieniędzy (aż do nabrania pewności co do poprawności decyzji bota).
