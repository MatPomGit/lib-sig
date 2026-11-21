# Przepływ danych

Plan: **źródło → walidacja schematu → blok/strumień → transformacja → metadane pochodzenia → odbiorca**. Import i eksport powinny być opcjonalne; nie zapisywać domyślnie danych z urządzeń do repo.

czas próbki w sekundach (źródłowy i monotoniczny), częstotliwość w Hz, jednostki fizyczne jawne dla każdego kanału. Dla każdego bloku utrzymać identyfikator, monotoniczny czas, jednostki i źródło. Resampling, segmentacja lub normalizacja powinny pozostawić ślad w metadanych. Nieregularne próbki, brakujące kanały oraz skoki czasu muszą zwracać ostrzeżenia lub błędy.

Nie logować surowych nagrań, próbek biologicznych, transkrypcji ani danych osób badanych do publicznego CI. Adaptery lokalnych usług są osobną granicą zaufania, nawet dla loopback. Stan testów rzeczywistego przetwarzania: **NOT_RUN**.
