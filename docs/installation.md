# Użycie eksperymentalnego modułu Signal

`core` i `filters` działają bez zewnętrznych zależności. Analiza FFT/PSD wymaga przypiętego NumPy 2.3.5. Przykładowa instalacja zależności w izolowanym środowisku deweloperskim:

```bash
python -m pip install --only-binary=:all: -r requirements-spectral.txt
PYTHONPATH=src python -m unittest discover -s tests -p 'test_spectral.py' -v
```

Brak instalowalnego wheel, `pyproject.toml` i zatwierdzonej licencji biblioteki. Jest to wyłącznie dokumentacja pracy na źródłach, nie instrukcja wdrożenia produkcyjnego.
