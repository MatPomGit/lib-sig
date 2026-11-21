# lib-sig

**Signal:** ogólna biblioteka przetwarzania próbkowanych sygnałów z aparatury badawczej, robotyki, akustyki i biosensorów.

**Status: DEVELOPMENT / NOT_RELEASED.** Dostępny jest `core` (zależny PR #2) i eksperymentalny moduł `filters` w tej gałęzi. Pozostałe moduły są planowane.

| Moduł | Zakres | Status |
| --- | --- | --- |
| [core](src/lib_sig/core/README.md) | Wielokanałowy sygnał, jednostki i czas | IMPLEMENTED (PR #2) |
| [filters](src/lib_sig/filters/README.md) | Krótki causal FIR i średnia ruchoma | IMPLEMENTED (EXPERIMENTAL) |
| [io](src/lib_sig/io/README.md) | Import/eksport | PLANNED |
| [spectral](src/lib_sig/spectral/README.md) | FFT i PSD | PLANNED |
| [events](src/lib_sig/events/README.md) | Markery, epoki i synchronizacja | PLANNED |
| [quality](src/lib_sig/quality/README.md) | Jakość sygnału | PLANNED |
| [features](src/lib_sig/features/README.md) | Deskryptory statystyczne | PLANNED |

`lib-sig` nie steruje urządzeniami. Funkcje mowy/VAD/ASR/TTS należą do `lib-audio`, analiza obrazu do `lib-vis`, tracking do `lib-track`, a metadane aparatury do prywatnego `devices`.

[Architektura](ARCHITECTURE.md) · [Kontrakt](docs/contracts.md) · [Testy](docs/testing.md) · [Roadmap](docs/roadmap.md). Brak licencji, pakietu dystrybucyjnego i wyników sprzętowych. Nie publikowano wydania ani Pages.
