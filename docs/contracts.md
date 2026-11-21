# Proponowany kontrakt API

**Status: PROPOSED, NOT_IMPLEMENTED.** Publiczne `contracts/api.json:public_entrypoints` pozostaje puste.

| Typ logiczny | Pola / jednostki | Status |
| --- | --- | --- |
| `SignalBlock` | samples[channel,time], sampling_rate_hz, units_per_channel, start_time_s, channel_names | PLANNED |
| `EventMarker` | code, onset_s, duration_s, sample_index?, source_id | PLANNED |
| `SignalQuality` | missing_rate, clipping_fraction, artifact_flags, metric_units | PLANNED |
| `ProcessingProvenance` | transform_chain, parameters, implementation_version, input_hash? | PLANNED |

Kryteria: jawny identyfikator źródła, typ i jednostki, określona reprezentacja timestampu, kontrola dostępu, zdefiniowany model błędu (`INVALID_INPUT`, `UNSUPPORTED_FORMAT`, `UNAVAILABLE`, `TIMEOUT`, `DATA_LOSS`) oraz opis niepewności i obróbki próbek.

Jednostki referencyjne: czas próbki w sekundach (źródłowy i monotoniczny), częstotliwość w Hz, jednostki fizyczne jawne dla każdego kanału. Brak metryki nie jest wartością zero; nie wymyślać współczynników jakości ani confidence. Breaking changes wymagają SemVer i migracji konsumenta.
