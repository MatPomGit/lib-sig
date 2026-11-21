# lib-sig

**Signal processing:** uniwersalna biblioteka do reprezentacji, filtrowania, analizy i synchronizacji sygnałów próbkowanych. Obejmuje dane z sensorów przemysłowych i robotycznych, IMU, telemetrię, sygnały akustyczne i biosygnały (EEG, EMG, EDA, PPG). Nie jest ograniczona do biologii.

**Status: ARCHITECTURE_ONLY / NOT_IMPLEMENTED / NOT_RELEASED.** W repozytorium są jedynie specyfikacje i planowane katalogi modułów.

## Moduły

| Moduł | Zadanie | Status |
| --- | --- | --- |
| [core](src/lib_sig/core/README.md) | Wielokanałowe próbki, jednostki i osie czasu | PLANNED |
| [io](src/lib_sig/io/README.md) | Wczytywanie i zapisywanie reprezentacji sygnałów | PLANNED |
| [filters](src/lib_sig/filters/README.md) | DSP, filtracja i resampling | PLANNED |
| [spectral](src/lib_sig/spectral/README.md) | FFT, PSD i analizy czasowo-częstotliwościowe | PLANNED |
| [events](src/lib_sig/events/README.md) | Zdarzenia, okna i synchronizacja strumieni | PLANNED |
| [quality](src/lib_sig/quality/README.md) | Nasycenie, braki i jakość sygnału | PLANNED |
| [features](src/lib_sig/features/README.md) | Deskryptory statystyczne i widmowe | PLANNED |

Biblioteka nie steruje urządzeniami. Funkcje mowy, VAD, ASR i TTS należą do `lib-audio`, obrazy do `lib-vis`, a tracking do `lib-track`. `lib-eye` odpowiada za okulografię. Parametry i identyfikatory aparatury należą do prywatnego katalogu `devices`.

[Architektura](ARCHITECTURE.md) · [Kontrakt](docs/contracts.md) · [Testy](docs/testing.md) · [Roadmap](docs/roadmap.md). Obecnie nie ma implementacji i publicznych symboli API.
