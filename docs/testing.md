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

Po scaleniu PR #2 zmieniono bazę PR #3 na `main`. [Scaffold CI #44949687674](https://github.com/MatPomGit/lib-sig/actions/runs/44949687674) potwierdził **90/90 PASS na `3e37ec6ee1d11fe351bd5beac67d58d51a9ef313`** (dokładny SHA w logach). To wynik **sprzed E4.0**. Nowe regresje E4.0 obejmują limit obliczeń, łańcuch metadanych i precyzję czasu; po commicie E4.0 aktualny status należy weryfikować w bieżących sprawdzeniach PR #3. Nie deklarować PASS dla SHA bez logów jego uruchomienia.
