# Etapy realizacji

| Etap | Zadanie | Status |
| --- | --- | --- |
| D0 | Architektura i dokumentacja | IMPLEMENTED |
| D1 | `core`: model danych i czasu | MERGED (PR #2) |
| D2 | `filters`: causal FIR, średnia ruchoma | IMPLEMENTED (PR #3), REVIEW PENDING |
| D3 | `spectral`: RFFT, periodogram PSD | IMPLEMENTED (stacked PR #4), 103 TESTS PASS ON PREVIOUS SHA |
| D4 | Welch PSD i dane z rzeczywistego urządzenia | NOT_STARTED |

D2 oraz D3 są zależne od formalnej recenzji i właściwego scalenia. Filtry IIR, resampling, analiza strumieniowa i spektrogram pozostają poza bieżącym zakresem. Nie publikować wydania ani Pages na podstawie samego CI.
