# Walidacja Signal

W repozytorium rozdzielono testy `core`, `filters` (PR #3) i `spectral` (zależny PR #4). Testy widmowe używają sygnałów syntetycznych o znanej odpowiedzi.

Obowiązkowe kontrole widmowe:

1. Przypisana harmoniczna w RFFT: właściwy bin, zespolona amplituda i brak zera dodanego przez padding.
2. Parseval: całka z jednostronnej PSD odpowiada mocy średniej bez detrend.
3. DC i Nyquist bez dwukrotnego skalowania; poprawne podwojenie dodatnich binów.
4. Normalizacja periodycznego okna Hann przez sumę kwadratów wag.
5. Dwa kanały z różnymi jednostkami, zachowane identyfikatory i timebase.
6. Odrzucenie sygnału nieregularnego, zamaskowanych braków, złych argumentów i przepełnienia.

```bash
python -m pip install --only-binary=:all: -r requirements-spectral.txt
PYTHONPATH=src python -m unittest discover -s tests -v
python scripts/validate_repository.py --phase scaffold
python scripts/validate_documentation.py
python scripts/validate_pages.py
```

Po otwarciu PR należy powtórzyć kontrole w GitHub-hosted CI na **dokładnym SHA**. Przed udokumentowaniem wyniku testu nie wpisywać PASS. Testy realnej aparatury, porównanie SciPy, E2E i benchmarki są **NOT_RUN**.
