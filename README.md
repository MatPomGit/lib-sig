# lib-sig

Akwizycja i przetwarzanie wielokanałowych sygnałów pomiarowych, w tym EEG, EMG, EDA i PPG.

Status: **ARCHITECTURE_ONLY / NOT_IMPLEMENTED / NOT_RELEASED**. Biblioteka zawiera strukturę planowanych modułów i kontraktów, bez instalowalnego pakietu i rzeczywistego przetwarzania danych.

## Moduły

| Moduł | Zadanie | Status |
| --- | --- | --- |
| [io](src/lib_sig/io/README.md) | Import/eksport sygnałów i metadanych (EDF/BDF/FIF/CSV jako docelowe formaty) | PLANNED |
| [filters](src/lib_sig/filters/README.md) | Filtry cyfrowe, resampling i kontrola aliasingu | PLANNED |
| [events](src/lib_sig/events/README.md) | Zdarzenia, epoki i wyrównanie zegarów | PLANNED |
| [quality](src/lib_sig/quality/README.md) | Kontrola artefaktów, braków i nasycenia kanałów | PLANNED |
| [features](src/lib_sig/features/README.md) | Widma, moc pasmowa, cechy w dziedzinie czasu i częstotliwości | PLANNED |

Biblioteka odpowiada za wspólną reprezentację sygnału, jakość danych, filtrowanie, synchronizację i ekstrakcję cech; nie steruje hardware i nie wykonuje diagnostyki klinicznej. lib-eye odpowiada za okulografię, lib-audio za semantykę mowy i ASR/TTS, a devices za kontrakty urządzeń.

Zobacz [architekturę](ARCHITECTURE.md), [kontrakt](docs/contracts.md), [plan testów](docs/testing.md), [roadmap](docs/roadmap.md) i [prywatność](docs/privacy.md). Publiczne symbole w `contracts/api.json` pozostają puste do czasu implementacji. Nie publikowano Release ani Pages.
