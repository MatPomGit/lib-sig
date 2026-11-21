# Architektura lib-sig

`lib-sig` wspiera ogólne DSP wielokanałowych sygnałów z badań, robotyki, akustyki i biosensorów. Warstwa `core` definiuje niezmienny model danych z jawnie wskazanym czasem i jednostkami.

```text
Źródło danych / plik / aplikacja
            |
        core: SignalBlock
            |
        +---+-----+
        |         |
     filters    spectral
        |         |
 causal FIR    RFFT / PSD
        +----+----+
             |
        odbiorca danych
```

`filters` w PR #3 działa bez zewnętrznych zależności i nie stosuje paddingu. `spectral` w PR #4 korzysta z NumPy, obsługuje regularny czas, okna boxcar/Hann i zwraca jednostronną PSD. Nie interpoluje danych brakujących. Wszelkie obliczenia muszą zachowywać pochodzenie, jednostki i ujawniać normalizację.

Biblioteka nie odpowiada za ASR/TTS (`lib-audio`), przetwarzanie obrazu (`lib-vis`), śledzenie obiektów (`lib-track`) ani transport ROS2 (`lib-ros`). Nie przechowuje danych eksperymentalnych ani identyfikatorów sprzętu.

**Status:** `core` MAIN, `filters` PR #3, `spectral` PR #4. Brak release, E2E i walidacji sprzętu. Szczegóły: [kontrakty](docs/contracts.md), [komponenty](docs/architecture/components.md), [testy](docs/testing.md).
