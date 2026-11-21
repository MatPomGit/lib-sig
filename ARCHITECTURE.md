# Architektura lib-sig

Akwizycja i przetwarzanie wielokanałowych sygnałów pomiarowych, w tym EEG, EMG, EDA i PPG. Proponowana warstwa obejmuje format danych i źródła, kontrolę jakości, adaptery istniejących backendów oraz jawne metadane pochodzenia.

Biblioteka odpowiada za wspólną reprezentację sygnału, jakość danych, filtrowanie, synchronizację i ekstrakcję cech; nie steruje hardware i nie wykonuje diagnostyki klinicznej. lib-eye odpowiada za okulografię, lib-audio za semantykę mowy i ASR/TTS, a devices za kontrakty urządzeń.

Jednostki i czas: czas próbki w sekundach (źródłowy i monotoniczny), częstotliwość w Hz, jednostki fizyczne jawne dla każdego kanału. Przetwarzanie nie powinno modyfikować źródłowych danych bez jawnej deklaracji transformacji, a metryki jakości powinny zawierać próg, okno i status ważności.

Opis modułów: [komponenty](docs/architecture/components.md) i [przepływ danych](docs/architecture/data-flow.md); decyzja projektowa: [ADR-0004](docs/adr/0004-boundaries.md). Katalogi `src/lib_sig/*` obecnie zawierają tylko README.

**Brak kodu i testów backendów: NOT_IMPLEMENTED / NOT_RUN.**
