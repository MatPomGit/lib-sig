# Komponenty lib-sig

| Moduł | Odpowiedzialność | Status |
| --- | --- | --- |
| `lib_sig.core` | Sygnały wielokanałowe, czas, jednostki | IMPLEMENTED EXPERIMENTAL |
| `lib_sig.filters` | Causal FIR i średnia ruchoma (bez resamplingu) | IMPLEMENTED EXPERIMENTAL (PR #3) |
| `lib_sig.io` | Import/eksport i pochodzenie danych | PLANNED |
| `lib_sig.spectral` | RFFT i jednostronny periodogram PSD | IMPLEMENTED EXPERIMENTAL (PR #4) |
| `lib_sig.events` | Markery, epoki i korelacja czasu | PLANNED |
| `lib_sig.quality` | Braki, artefakty, nasycenie, kompletność | PLANNED |
| `lib_sig.features` | Statystyki i uniwersalne deskryptory | PLANNED |

`lib-sig` obejmuje DSP sygnałów akustycznych, mechanicznych, elektrycznych, biologicznych i symulowanych. Nie obejmuje akwizycji aparatury, ASR/TTS, detekcji obiektów, trackingu ani diagnostyki medycznej.

Filtr `valid` zmniejsza długość sygnału; zachowana jest oś regularna, a pierwszy timestamp odpowiada najnowszej próbce pierwszego pełnego okna. [Kontrakt](../contracts.md).
