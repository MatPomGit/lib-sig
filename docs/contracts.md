# Kontrakt API Signal

Wersja `0.1.0` pozostaje **eksperymentalna**, bez wydania. `core` jest scalony do `main`, a `filters` (PR #3) oraz `spectral` (PR #4) pozostają zmianami rozwojowymi.

| API | Semantyka | Status |
| --- | --- | --- |
| `ChannelDescriptor`, `TimeAxis`, `SignalBlock`, `SignalValidationError` | Sygnał wielokanałowy, jednostki, regularny i nieregularny czas, maski | MAIN |
| `fir_filter`, `moving_average` | Causal FIR valid/no padding, jednostka bez zmian | PR #3 |
| `rfft_spectrum` | Współczynniki RFFT bez normalizacji i podwajania | STACKED PR #4 |
| `periodogram_psd` | Jednostronne `unit²/Hz` ze skalą energy okna | STACKED PR #4 |
| `SpectralEstimate` | Immutable `frequencies_hz`, `values[frequency][channel]`, `units`, `window`, `detrend`, `kind`, `sample_count`, `sampling_rate_hz`, `source_id`, `timebase`, `start_s` | STACKED PR #4 |
| Welch PSD, spektrogram, resampling | Brak implementacji | PLANNED |

FFT/PSD: regularny `TimeAxis`, co najmniej dwie próbki, wszystkie maski ważne. Okno `boxcar` lub periodyczny `hann`; detrend `none` lub `constant` przed oknem. `rfft_spectrum` domyślnie nie odejmuje średniej, `periodogram_psd` domyślnie ją odejmuje. PSD: `|X[k]|² / (fs Σw²)`, podwojenie wszystkich dodatnich częstotliwości z wyjątkiem Nyquista dla parzystego N. DC pozostaje bez podwojenia. Częstotliwości w Hz, PSD w jednostka²/Hz. Metadane czasowe i pochodzenie są zachowane.

Funkcje nie imputują braków, nie wykonują resamplingu i nie przyjmują danych o nieregularnym próbkowaniu. Nieprawidłowe argumenty: `INVALID_SPECTRUM`, maski: `DATA_LOSS`, brak NumPy: `DEPENDENCY_UNAVAILABLE`.

Brak gwarancji stabilności API, builda wheel i wyników na aparaturze. Breaking changes po uruchomieniu odbiorców wymagają wersjonowania i planu migracji.
