# Architektura lib-sig

`lib-sig` zapewni wspólny model **sygnału próbkowanego**, niezależny od dziedziny pomiaru. Dane mogą pochodzić z biosensorów, mikrofonów, IMU, maszyn, robotów lub symulacji.

```text
Źródło / plik / biblioteka urządzenia
                |
               io
                |
     core (próbki, czas, jednostki)
                |
   filters / spectral / events
                |
       quality / features
                |
        aplikacja badawcza
```

Rdzeń nie narzuca jednego SDK, klasy urządzenia ani formatu. Sygnały mogą mieć regularne lub nieregularne próbkowanie; moduły wymagające stałego kroku czasu muszą weryfikować to założenie. Operacje FIR zapisują w niezmiennym `SignalBlock.provenance` kolejność transformacji, współczynniki, politykę braków i kotwiczenie timestampów. Dla średniej ruchomej rejestrowane jest także opóźnienie grupowe; dla ogólnego FIR nie jest ono określane bez znajomości fazy. Wykres charakterystyki częstotliwościowej nie jest jeszcze implementowany. Eksperymentalne RFFT i jednostronny periodogram PSD są realizowane w `spectral` z wykorzystaniem NumPy; `SpectralEstimate.provenance` przenosi historię wejściowych transformacji i zapisuje parametry FFT/PSD. Dane nieregularne lub z brakami są odrzucane, a alokacje podlegają konserwatywnemu budżetowi.

Przetwarzanie sygnału nie obejmuje rozpoznawania mowy (`lib-audio`), obrazu (`lib-vis`), śledzenia tożsamości obiektu (`lib-track`) ani komunikacji ROS2 (`lib-ros`). Warstwy wyższego poziomu mogą wykorzystywać API DSP bez kopiowania implementacji.

Status: **CORE + MINIMAL FIR MERGED / SPECTRAL EXPERIMENTAL (PR #4) / NOT_RELEASED**. `filters` obsługuje przyczynowy FIR i średnią ruchomą; `spectral` RFFT i jednostronną PSD. `io`, `events`, `features` oraz `quality` pozostają planowane. Szczegóły: [komponenty](docs/architecture/components.md), [kontrakty](docs/contracts.md), [przepływ danych](docs/architecture/data-flow.md) i [ADR-0004](docs/adr/0004-boundaries.md).
