# Walidacja lib-sig

Moduł `core` ma deterministyczne testy jednostkowe w `tests/test_signal_core.py`. Reszta planu DSP pozostaje niewykonana.

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
