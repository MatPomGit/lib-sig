# Użycie z katalogu źródłowego

Dostępny jest eksperymentalny, niewydany moduł Python `lib_sig.core`. Weryfikację importu można wykonać lokalnie, bez pobierania zależności:

```bash
PYTHONPATH=src python -c 'from lib_sig import TimeAxis, ChannelDescriptor, SignalBlock'
python -m unittest discover -s tests -p 'test_signal_core.py' -v
```

Nie ma jeszcze instalowalnego pakietu, `pyproject.toml`, opublikowanego wheel ani zatwierdzonej licencji. Nie należy wykorzystywać tego kodu w produkcji lub w badaniach bez niezależnej kontroli kompatybilności i testów.
