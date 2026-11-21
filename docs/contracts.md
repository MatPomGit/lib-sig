# Proponowany kontrakt sygnałów

**PROPOSED / NOT_IMPLEMENTED.** Brak publicznych symboli; `contracts/api.json:public_entrypoints` pozostaje pusty.

| Typ | Pola / wymagania |
| --- | --- |
| `ChannelDescriptor` | `name`, `unit`, `source_id?`, `calibration_ref?`, `kind?` |
| `TimeAxis` | `kind=regular/irregular`, `start_s?`, `sampling_rate_hz?`, `timestamps_s?`, `timebase` |
| `SignalBlock` | `samples[sample,channel]`, `channels[]`, `time_axis`, `mask?`, `source_id` |
| `SignalEvent` | `event_id`, `onset_s`, `duration_s`, `timebase`, `source_id` |
| `SignalQuality` | `metric`, `value`, `unit`, `window`, `validity` |
| `TransformProvenance` | `operation`, `parameters`, `library_version`, `input_ref` |

Dla regularnej osi `t[i]=start_s+i/sampling_rate_hz`; dla nieregularnej należy dostarczyć uporządkowane timestampy. Liczba rekordów czasu musi zgadzać się z liczbą próbek, a liczba kanałów z deskryptorami. Częstotliwość próbkowania: Hz; czas: s. Jednostki amplitudy zależą od konkretnego czujnika i nie powinny być domyślnie zakładane.

Błędy: `INVALID_SHAPE`, `INVALID_UNITS`, `TIMEBASE_MISMATCH`, `IRREGULAR_SAMPLING`, `UNSUPPORTED_FORMAT`, `DATA_LOSS`. Każda transformacja zmieniająca czas lub amplitudę powinna zachować provenance. Breaking changes wymagają wersjonowania API i testów konsumentów.
