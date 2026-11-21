# API sygnałów: stan rzeczywisty i planowany

**IMPLEMENTED (EXPERIMENTAL):** import `from lib_sig import ChannelDescriptor, TimeAxis, SignalBlock, SignalValidationError`. Implementacja znajduje się w `src/lib_sig/core/models.py`. API nie jest wydane ani objęte gwarancją kompatybilności.

| Typ | Obecne pola / zachowanie | Status |
| --- | --- | --- |
| `ChannelDescriptor` | `name: str`, `unit: str`, opcjonalnie `source_id`, `calibration_ref`, `kind` | IMPLEMENTED |
| `TimeAxis` | `kind=regular/irregular`, `timebase`, `start_s?`, `sampling_rate_hz?`, `timestamps_s?`, `timestamp_at(index)` | IMPLEMENTED |
| `SignalBlock` | `samples[sample,channel]`, `channels[]`, `time_axis`, `source_id`, `mask?`, `sample_count`, `channel_count`, `timestamp_at(index)` | IMPLEMENTED |
| `SignalValidationError` | `code` i tekst błędu, klasa pochodna `ValueError` | IMPLEMENTED |
| `SignalEvent`, `SignalQuality`, `TransformProvenance` | Schematy niezatwierdzone, bez implementacji | PLANNED |

Dla osi regularnej `t[i] = start_s + i/sampling_rate_hz`, a nieregularna wymaga rosnącej krotki `timestamps_s` o długości równej liczbie próbek. Czas jest wyrażony w sekundach, częstotliwość w Hz; amplitudy mają jednostki z `ChannelDescriptor.unit`. Wiersze i kolumny danych muszą być krotkami; obiekty są niemodyfikowalne.

`mask=True` oznacza pomiar ważny. Wartości NaN/Inf są tolerowane wyłącznie przy `False`; nie są interpolowane. Błędy używane przez bieżącą implementację to `INVALID_SHAPE`, `INVALID_UNITS`, `TIMEBASE_MISMATCH`, `IRREGULAR_SAMPLING` i `DATA_LOSS`. `public_entrypoints` w `contracts/api.json` zawiera tylko rzeczywiście dostępne importy.

Filtrowanie, resampling, FFT/PSD, akwizycja, eksport i przetwarzanie strumieni nie należą do obecnego API. Przed wydaniem wymagane są testy integracyjne, licencja, packaging i niezależna recenzja.
