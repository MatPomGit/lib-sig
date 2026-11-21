# Potencjalni odbiorcy lib-sig

| System | Zastosowanie | Status |
| --- | --- | --- |
| `lib-exp` | Synchronizacja markerów i próbkowanych bodźców | PROPOSED |
| `lib-audio` | Uniwersalne FFT, resampling lub filtrowanie audio | PROPOSED |
| `lib-ros` | DSP dla telemetrii czujników i IMU | PROPOSED |
| `lib-track` | Filtracja sekwencji numerycznych jako opcjonalna zależność | PROPOSED |
| `arc-neuro`, `arc-robo`, `arc-xr` | Analizy offline sygnałów z eksperymentów | PROPOSED |

Żaden konsument nie jest jeszcze potwierdzony testem integracyjnym i przypiętą wersją `lib-sig`. Wspólne algorytmy powinny być współdzielone przez pakiet, bez kopiowania ich do konsumentów.
