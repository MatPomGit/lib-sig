# ADR-0004: granice lib-sig

Data: 2026-11-21  
Status: proposed

## Kontekst

Akwizycja i przetwarzanie wielokanałowych sygnałów pomiarowych, w tym EEG, EMG, EDA i PPG. Funkcje tego obszaru przenikają przez kilka projektów, przez co łatwo o duplikację.

## Propozycja

Biblioteka odpowiada za wspólną reprezentację sygnału, jakość danych, filtrowanie, synchronizację i ekstrakcję cech; nie steruje hardware i nie wykonuje diagnostyki klinicznej. lib-eye odpowiada za okulografię, lib-audio za semantykę mowy i ASR/TTS, a devices za kontrakty urządzeń.

## Alternatywy

- Duplikowanie kodu w aplikacjach: trudniejsze testy i utrzymanie.
- Jeden megaprojekt sensorów/modeli: nadmierne zależności oraz brak jawnych granic.

## Konsekwencje

Oddzielne kontrakty i testy źródeł. Zamierzone jednostki: czas próbki w sekundach (źródłowy i monotoniczny), częstotliwość w Hz, jednostki fizyczne jawne dla każdego kanału. Nie deklarować wsparcia bez rzeczywistych testów.
