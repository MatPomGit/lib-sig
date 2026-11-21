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

Po scaleniu PR #2 zmieniono bazę PR #3 na `main`. [Scaffold CI #44949547334](https://github.com/MatPomGit/lib-sig/actions/runs/44949547334) potwierdził **90/90 PASS na `d1f60245daeb4322dfab9d15ff90dd93a395300b`**, po przeniesieniu bazy na `main`. Kolejna zmiana SHA wymaga ponownego CI.
