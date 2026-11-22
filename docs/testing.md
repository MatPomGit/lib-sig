# Walidacja lib-sig

Kontrole `core` zawierają testy osi czasu i danych. Nowe testy `tests/test_fir_filter.py` obejmują splot, średnią ruchomą, tłumienie Nyquista, próbkowanie regularne, maskowanie braków, jednostki i propagację błędów. Wszystkie dane są syntetyczne. [Scaffold CI #44949313509](https://github.com/MatPomGit/lib-sig/actions/runs/44949313509) uruchomił 90 testów na commicie `e1aed637fa13ab3ae5bebafdaa937d6c2a4b0f04` i zakończył się PASS. Po zmianie SHA wymagane jest ponowne CI.

Komendy:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
```

Plan dalszy: porównanie odpowiedzi impulsowej i częstotliwościowej z referencją NumPy/SciPy, benchmark długich wejść, testy antyaliasingu i resamplingu oraz E2E na danych z uprawnionych urządzeń. Te zakresy są **NOT_RUN** do czasu przeprowadzenia testów.

Nie utożsamiać wykonanych syntetycznych testów z walidacją sprzętową lub naukowym benchmarkiem.

Po scaleniu PR #2 zmieniono bazę PR #3 na `main`. [Scaffold CI #44949687674](https://github.com/MatPomGit/lib-sig/actions/runs/44949687674) potwierdził **90/90 PASS na `3e37ec6ee1d11fe351bd5beac67d58d51a9ef313`** (dokładny SHA w logach). To wynik **sprzed E4.0**. [Scaffold CI #45014389661](https://github.com/MatPomGit/lib-sig/actions/runs/45014389661), job `validate`, potwierdził exact-SHA `42ec9b042b931a8c6de25882ef16d9087e8b0cb4`: **94/94 PASS**, scaffold, dokumentacja i Pages PASS. Jest to wynik **sprzed poprawek E4.0 follow-up** (wcześniejsza kontrola zasobów i metadanych). Nowy commit wymaga odrębnego CI na swoim HEAD. Nie deklarować PASS dla SHA bez logów jego uruchomienia.

## PR #4: regresja i odniesienie niezależne

[Scaffold CI #44950563866](https://github.com/MatPomGit/lib-sig/actions/runs/44950563866) potwierdził 103/103 testy dla historycznego `71e0ca6b616f485931e9e4e4371aad7df6e14699` przed integracją najnowszego FIR. To **nie** jest walidacja finalnego E4.0. Po połączeniu historii wymagane jest CI na nowym SHA z zachowaniem testów modułów `core` i `filters`. Testy `tests/test_spectral.py` obejmują szereg FIR → PSD, metadane `provenance`, deterministyczny limit pamięci i mapowanie `MemoryError`; `tests/test_spectral_reference.py` porównują FFT i jednostronną PSD do `scipy.signal.periodogram` dla N parzystego/nieparzystego, `boxcar`/`hann` i obydwu trybów detrend. NumPy 2.3.5 to zależność runtime modułu widmowego, SciPy 1.16.3 służy wyłącznie do testów.

Pełna walidacja lokalna w izolowanym środowisku:

```bash
python -m pip install --only-binary=:all: -r requirements-spectral-test.txt
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
```

Benchmarki długich strumieni, wheel clean-install i testy na urządzeniach: **NOT_RUN**. Nie przypisywać historycznych wyników CI nowym commitom.
