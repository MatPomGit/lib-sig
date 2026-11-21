# Walidacja lib-sig

Kontrole `core` zawierają testy osi czasu i danych. Nowe testy `tests/test_fir_filter.py` obejmują splot, średnią ruchomą, tłumienie Nyquista, próbkowanie regularne, maskowanie braków, jednostki i propagację błędów. Wszystkie dane są syntetyczne.

Komendy:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
```

Plan dalszy: porównanie odpowiedzi impulsowej i częstotliwościowej z referencją NumPy/SciPy, benchmark długich wejść, testy antyaliasingu i resamplingu oraz E2E na danych z uprawnionych urządzeń. Te zakresy są **NOT_RUN** do czasu przeprowadzenia testów.

Nie utożsamiać wykonanych syntetycznych testów z walidacją sprzętową lub naukowym benchmarkiem.
