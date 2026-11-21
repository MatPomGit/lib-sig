# Etapy realizacji

| Etap | Zadanie | Status |
| --- | --- | --- |
| D0 | Struktura, kontrakty i dokumentacja | IMPLEMENTED (ARCHITECTURE) |
| D1 | Typy danych, walidacja i jednostki | IMPLEMENTED, REVIEW PENDING (PR #2) |
| D2 | Jedna elementarna operacja FIR + testy syntetyczne | IMPLEMENTED IN STACKED BRANCH, CI PENDING |
| D3 | Reużycie SciPy, strumienie i synchronizacja | NOT_STARTED |
| D4 | E2E na uprawnionym host i odbiorca | NOT_STARTED |

Nie mylić `D2` z pełnym DSP: filtry IIR, resampling, analiza widmowa i testy fizyczne nadal wymagają osobnej implementacji i dowodów. Merge, wydanie oraz Pages pozostają oddzielnymi bramkami.
