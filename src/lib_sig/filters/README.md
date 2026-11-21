# filters: causal FIR (eksperymentalne)

**Status: IMPLEMENTED (EXPERIMENTAL) w gałęzi rozwojowej.**

Moduł oferuje `fir_filter(block, taps)` oraz `moving_average(block, window)`. Implementacja korzysta tylko ze standardowej biblioteki Pythona. To niewielka, bezpośrednia operacja splotu dla krótkich filtrów, **nie** zamiennik SciPy/FFmpeg ani rozwiązanie dla długich sygnałów.

Konwencja: `y[n] = Σ taps[k] · x[n-k]`, `taps[0]` mnoży najnowszą próbkę. Tryb **valid** bez zerowego paddingu, długość wyniku `N-K+1`. Timestampy wskazują czas **najnowszej próbki wejściowej**, bez automatycznej kompensacji opóźnienia grupowego. Filtr średniej ruchomej ma opóźnienie grupowe `(K-1)/(2·fs)` s względem środka okna. Jednostki i nazwy kanałów pozostają niezmienione. Nie dokonuje się resamplingu, normalizacji amplitudy poza wagami średniej ani automatycznej interpolacji.

Wymagane są **regularne próbki**. Niepoprawny blok, współczynnik NaN/Inf, za długi filtr lub przepełnienie obliczeń skutkują błędem. Jeśli wejście zawiera pozycje z `mask=False`, całe okno dla odpowiedniego kanału zostaje oznaczone `False`, a wynik to `NaN`. Surowe dane nie są modyfikowane.

API i ograniczenia: [kontrakty](../../../docs/contracts.md). Testy syntetyczne: `tests/test_fir_filter.py`. **Brak weryfikacji na urządzeniach i wydania.**
