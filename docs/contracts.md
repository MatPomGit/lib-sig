# Kontrakt API Signal: core, FIR i analiza widmowa

**Status: IMPLEMENTED (EXPERIMENTAL), bez wydania.** `core` i `filters` są scalone do `main`; `spectral` jest implementowany w PR #4 i podlega osobnej recenzji R2.

| Typ/funkcja | Obecne pola lub semantyka | Status |
| --- | --- | --- |
| `ChannelDescriptor` | nazwa, jednostka, źródło i opcjonalna kalibracja | CORE |
| `TimeAxis` | regular/irregular, jawny timebase, timestamp_at | CORE |
| `SignalBlock` | `samples[sample,channel]`, kanały, oś czasu, maska i historia `provenance` | CORE |
| `TransformProvenance` | niezmienny rekord operacji, parametrów JSON, osi i braków | EXPERIMENTAL |
| `SignalValidationError` | `code` i opis, pochodna `ValueError` | CORE |
| `fir_filter(block, taps)` | causal FIR, kolejność od najnowszej próbki, valid/no padding | EXPERIMENTAL |
| `moving_average(block, window)` | równoważny FIR z wagami `1/window` | EXPERIMENTAL |
| `rfft_spectrum(block, *, window, detrend)` | nieznormalizowane zespolone RFFT | EXPERIMENTAL (PR #4) |
| `periodogram_psd(block, *, window, detrend)` | jednostronna PSD w jednostka²/Hz | EXPERIMENTAL (PR #4) |
| `SpectralEstimate` | niezmienny wynik z `values[frequency][channel]` i historią `provenance` | EXPERIMENTAL (PR #4) |
| `SignalEvent`, `SignalQuality` | planowane, niezaimplementowane | PLANNED |

Wymagane regularne próbkowanie i niepusty `tuple` skończonych rzeczywistych współczynników o długości nie większej niż liczba próbek. Dla `N` próbek i `K` współczynników wynik ma `N-K+1` próbek. Używana konwencja `y[n] = Σ_{k=0}^{K-1} taps[k]·x[n-k]` od `n=K-1`. Timestamp reprezentuje czas najnowszej próbki, nie środek okna. Filtr nie kompensuje opóźnienia grupowego.

Jednostki amplitudy i `source_id` są zachowywane. Przy masce wejścia `False` dowolny brak w oknie daje wynik `NaN` z maską `False`, ale niezależne kanały pozostają ważne. Przepełnienie wyniku daje `DATA_LOSS`, a błędne współczynniki `INVALID_FILTER`. Przy nieregularnym próbkowaniu zgłaszany jest `IRREGULAR_SAMPLING`. Nie następuje interpolacja, padding, resampling ani przekształcanie jednostek.

Bezpośredni splot jest ograniczony do **1 000 000 multiply-accumulates** na wywołanie, licząc `(N-K+1)*K*C`; przekroczenie zgłasza `RESOURCE_LIMIT` przed kosztowną pętlą. `fir_filter` sprawdza budżet na podstawie długości `taps` przed konwersją współczynników; gdy jednocześnie przekroczony jest budżet i współczynniki są nieprawidłowe, pierwszeństwo ma `RESOURCE_LIMIT`. `moving_average` sprawdza limit przed utworzeniem wektora wag. Ograniczenie dotyczy wersji referencyjnej w Pythonie i nie stanowi benchmarku wydajności.

Każdy wynik dołącza `TransformProvenance` do `SignalBlock.provenance`, nie nadpisując historii wejściowej. `parameters_json` przechowuje dokładne współczynniki `taps` (oraz `window` dla średniej), `input_sample_count`, `output_sample_count`, `timestamp_policy=newest_input_sample`, `missing_policy=invalidate_complete_window_per_channel`. `group_delay_s` jest określone tylko dla średniej ruchomej; dla dowolnego FIR pozostaje `None`. `source_id` identyfikuje źródło, a nie cały rodowód danych. Historia nie zawiera sum kontrolnych wejścia i nie zastępuje archiwalnej ewidencji eksperymentu.

Znaczniki czasu podlegają zaokrągleniom IEEE-754. Zachowanie zgodności oznacza zgodność numeryczną z `block.timestamp_at(i+K-1)` w tolerancji zmiennoprzecinkowej, **nie** identyczność bitową.

FIR z bezpośrednim splotem jest przeznaczony do krótkich filtrów i syntetycznej walidacji, a nie produkcyjnego przetwarzania długich strumieni. Brak clean-install, zweryfikowanej licencji, benchmarków i E2E; `release_status: not_released`.

## Kontrakt widmowy (PR #4)

FFT/PSD wymagają regularnej osi czasu, co najmniej dwóch próbek i pełnej maski. Okno `boxcar` albo periodyczny `hann` oraz detrend `none` lub `constant` (odjęcie średniej przed oknem). `rfft_spectrum` zwraca nieznormalizowane współczynniki zespolone RFFT w jednostkach kanału, bez podwojenia. `periodogram_psd` zwraca `abs(RFFT)^2/(fs*sum(window^2))`, podwajając dodatnie biny z wyjątkiem Nyquista przy parzystym N; DC nie jest podwajane. Wartości wyjściowe indeksuje się jako `values[frequency][channel]`, częstotliwości są wyrażone w Hz, PSD w `unit²/Hz`.

`SpectralEstimate.provenance` zachowuje krotkę `SignalBlock.provenance` i dołącza rekord `TransformProvenance` z operacją `rfft_spectrum` albo `periodogram_psd`, rozmiarem wejścia/wyjścia, `window`, `detrend`, `normalization`, `sampling_rate_hz`, `backend_version`, a dla PSD także energią okna oraz regułą podwojenia. Zachowana historia nie zawiera sum kontrolnych surowych danych i nie zastępuje ewidencji eksperymentu.

Przed konwersją do NumPy wymuszany jest limit szacowanych buforów i obiektów wyniku **64 MiB**; przekroczenie lub `MemoryError` zgłasza `RESOURCE_LIMIT`. Jest to oszacowanie, nie twardy limit RSS podczas FFT. Błędne parametry zgłaszają `INVALID_SPECTRUM`, braki/nieskończoności `DATA_LOSS`, brak NumPy `DEPENDENCY_UNAVAILABLE`. SciPy jest zależnością tylko testów porównawczych, nie publicznego runtime.
