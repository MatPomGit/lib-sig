# Strategia testowania

Testy offline z danymi syntetycznymi poprzedzają integrację z rzeczywistym urządzeniem, serwisem lub modelem.

1. Próbki syntetyczne z sinusoidami o znanym widmie.
2. Resampling z antyaliasingiem i weryfikacją długości.
3. Filtry: wzmocnienie, opóźnienie grupowe, edge effects.
4. Marker epoch/clock alignment z jitter i utratą danych.
5. Import/eksport testowych plików bez rzeczywistych danych osób badanych.

Wynik testu dokumentować w raporcie z SHA, wersją backendu, jednostkami i konfiguracją źródła. Nie utożsamiać przejścia walidatorów szkieletu z działającym przetwarzaniem sygnału.

Kontrole repozytorium:

```bash
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
python -m unittest discover -s tests -v
```
