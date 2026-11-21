# Dystrybucja

Preferowana forma docelowa: pakiet Python `lib-sig` z `src/lib_sig/`. Brak `pyproject.toml`, kodu uruchamialnego i opublikowanego artefaktu.

Wydanie wymaga sprawdzonej licencji, wersji i pochodzenia SDK/modeli, minimalnych uprawnień, przejścia testów na konkretnym SHA, audytu zależności oraz clean-install. Integracje sprzętowe muszą mieć własną bramkę E2E. Pages korzystają z osobnego `pages/` i nie są wdrażane przez ten PR.
