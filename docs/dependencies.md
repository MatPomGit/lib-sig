# Zależności i łańcuch dostaw

`core` i `filters` korzystają wyłącznie ze standardowej biblioteki Python. **Moduł `spectral` wymaga NumPy**, ładowanego leniwie podczas obliczeń. Testowana, przypięta wersja to `numpy==2.3.5` z [requirements-spectral.txt](../requirements-spectral.txt). CI instaluje wyłącznie koła binarne w izolowanym GitHub-hosted runnerze. Wydanie i lockfile z sumami hash wymagają oddzielnego przeglądu supply-chain.

SciPy 1.16.3 jest przypięte **tylko dla testów porównawczych** w `requirements-spectral-test.txt` (weryfikacja względem `scipy.signal.periodogram` i `scipy.fft.rfft`), nie jest zależnością runtime biblioteki. Welch PSD, filtry i resampling pozostają planowane. MNE, BrainFlow i inne SDK pozostają opcjonalnymi zależnościami odbiorców, nie rdzenia.

Brak `pyproject.toml`, wydania i pakietu produkcyjnego. Weryfikacja licencji zależności przechodnich i hash-based lockfile: **NOT_RUN**.
