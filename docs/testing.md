# Walidacja lib-sig

Moduł `core` ma 15 deterministycznych testów jednostkowych w `tests/test_signal_core.py`, w tym wykrywanie nieprzedstawialnych znaczników czasu. Pozostałe kontrole scaffold CI dotyczą struktury i dokumentacji. Testy planowanych algorytmów DSP pozostają niewykonane.

1. Sinusoidy i kombinacje harmoniczne: dokładne piki FFT/PSD, jednostki i normalizacja.
2. Filtry FIR/IIR: odpowiedź częstotliwościowa, opóźnienie, stan początkowy i efekty brzegowe.
3. Resampling, decymacja i aliasing, w tym zapis zmienionej osi czasu.
4. Nieregularne timestampy, jitter, luki, duplikaty i skoki zegara.
5. Test wielokanałowych danych z różnymi jednostkami i maską wartości brakujących.
6. Test import/eksport danych syntetycznych bez przecieku próbek do logów.
7. Docelowe E2E z sygnałem akustycznym, IMU lub EEG po oddzielnym preflight.

Każdy test musi podać SHA, wersję backendu, parametry, jednostki, metrykę i wynik. Testy filtrów, widm, resamplingu i integracji sprzętowej pozostają **NOT_RUN**.

```bash
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
python -m unittest discover -s tests -v
```
