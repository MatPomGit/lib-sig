# Komponenty lib-sig

| Moduł | Odpowiedzialność | Status |
| --- | --- | --- |
| `lib_sig.core` | Sygnały wielokanałowe, czas, jednostki | IMPLEMENTED (main) |
| `lib_sig.filters` | Causal FIR i średnia ruchoma | IMPLEMENTED (PR #3) |
| `lib_sig.spectral` | RFFT, jednostronny periodogram PSD | IMPLEMENTED (stacked PR #4) |
| `lib_sig.io` | Import/eksport i pochodzenie | PLANNED |
| `lib_sig.events` | Markery, epoki i korelacja czasu | PLANNED |
| `lib_sig.quality` | Braki, artefakty, kompletność | PLANNED |
| `lib_sig.features` | Deskryptory statystyczne | PLANNED |

Wszystkie operacje wymagają jawnych jednostek i osi czasu. FFT/PSD nie dopuszcza nieregularnych próbek ani braków w danych. Interpretacja kliniczna i urządzenia pozostają u odbiorców. [Kontrakty](../contracts.md).
