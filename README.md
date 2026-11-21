# lib-sig

**Signal:** ogólna biblioteka reprezentacji i przetwarzania próbkowanych sygnałów z robotyki, automatyki, akustyki i biosensorów.

**Stan:** `core` scalony do `main`; `filters` w PR #3, `spectral` (RFFT/PSD) w zależnym PR #4. Nie wydano pakietu ani nie zweryfikowano go na urządzeniach.

| Moduł | Zakres | Status |
| --- | --- | --- |
| [core](src/lib_sig/core/README.md) | Kanały, jednostki, czas i maski | MAIN |
| [filters](src/lib_sig/filters/README.md) | Causal FIR i średnia ruchoma | PR #3 |
| [spectral](src/lib_sig/spectral/README.md) | RFFT, jednostronny periodogram PSD | STACKED PR #4 |
| [io](src/lib_sig/io/README.md) | Import/eksport | PLANNED |
| [events](src/lib_sig/events/README.md) | Markery i epoki | PLANNED |
| [quality](src/lib_sig/quality/README.md) | Jakość sygnału | PLANNED |
| [features](src/lib_sig/features/README.md) | Deskryptory statystyczne | PLANNED |

`lib-sig` nie steruje aparaturą. Rozpoznawanie mowy należy do `lib-audio`, obraz do `lib-vis`, tracking do `lib-track`, a sprzęt do prywatnego rejestru `devices`.

[Architektura](ARCHITECTURE.md) · [Kontrakty](docs/contracts.md) · [Testy](docs/testing.md) · [Zależności](docs/dependencies.md).

Brak finalnej licencji, pakowania, wydania oraz dowodów testów sprzętowych i naukowego benchmarku.
