# Etapy realizacji

| Etap | Zadanie | Status |
| --- | --- | --- |
| D0 | Architektura i dokumentacja | IMPLEMENTED |
| D1 | `core`: model danych i czasu | MERGED (PR #2) |
| D2 | `filters`: causal FIR, średnia ruchoma | MERGED TO MAIN (PR #3) |
| D3 | `spectral`: RFFT, periodogram PSD | IMPLEMENTED (PR #4), exact-SHA CI/review PENDING |
| D4 | Welch PSD i dane z rzeczywistego urządzenia | NOT_STARTED |

D2 został scalony; D3 nadal wymaga finalnego CI, odrębnej recenzji i uprawnionego scalenia. Filtry IIR, resampling, analiza strumieniowa i spektrogram pozostają poza bieżącym zakresem. Nie publikować wydania ani Pages na podstawie samego CI.
