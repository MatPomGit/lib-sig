# API Signal: core + elementarny FIR

**Status: IMPLEMENTED (EXPERIMENTAL), bez wydania.** Typy podstawowe i walidatory są przygotowane w `core`; funkcje DSP są dostępne w PR #3 względem `main`, zawierającego już zatwierdzony moduł `core` z PR #2.

| Typ/funkcja | Obecne pola lub semantyka | Status |
| --- | --- | --- |
| `ChannelDescriptor` | nazwa, jednostka, źródło i opcjonalna kalibracja | CORE |
| `TimeAxis` | regular/irregular, jawny timebase, timestamp_at | CORE |
| `SignalBlock` | `samples[sample,channel]`, kanały, oś czasu i opcjonalna maska | CORE |
| `SignalValidationError` | `code` i opis, pochodna `ValueError` | CORE |
| `fir_filter(block, taps)` | causal FIR, kolejność od najnowszej próbki, valid/no padding | EXPERIMENTAL |
| `moving_average(block, window)` | równoważny FIR z wagami `1/window` | EXPERIMENTAL |
| `SignalEvent`, `SignalQuality`, `TransformProvenance` | planowane, niezaimplementowane | PLANNED |

Wymagane regularne próbkowanie i niepusty `tuple` skończonych rzeczywistych współczynników o długości nie większej niż liczba próbek. Dla `N` próbek i `K` współczynników wynik ma `N-K+1` próbek. Używana konwencja `y[n] = Σ_{k=0}^{K-1} taps[k]·x[n-k]` od `n=K-1`. Timestamp reprezentuje czas najnowszej próbki, nie środek okna. Filtr nie kompensuje opóźnienia grupowego.

Jednostki amplitudy i `source_id` są zachowywane. Przy masce wejścia `False` dowolny brak w oknie daje wynik `NaN` z maską `False`, ale niezależne kanały pozostają ważne. Przepełnienie wyniku daje `DATA_LOSS`, a błędne współczynniki `INVALID_FILTER`. Przy nieregularnym próbkowaniu zgłaszany jest `IRREGULAR_SAMPLING`. Nie następuje interpolacja, padding, resampling ani przekształcanie jednostek.

FIR z bezpośrednim splotem jest przeznaczony do krótkich filtrów i syntetycznej walidacji, a nie produkcyjnego przetwarzania długich strumieni. Brak clean-install, zweryfikowanej licencji, benchmarków i E2E; `release_status: not_released`.
