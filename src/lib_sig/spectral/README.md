# spectral: FFT i periodogram PSD

**Status: IMPLEMENTED (EXPERIMENTAL) w zależnym PR #4; bez wydania.** Implementacja wykorzystuje `numpy.fft.rfft`, nie własny silnik FFT. `NumPy 2.3.5` to przypięta zależność modułu widmowego. `core` i `filters` mogą być importowane bez NumPy; moduł ładuje backend dopiero przy analizie.

Dostępne funkcje:

- `rfft_spectrum(block, window="boxcar", detrend="none")`: nienormalizowane współczynniki zespolone rzeczywistego FFT, jednostka amplitudy kanału.
- `periodogram_psd(block, window="boxcar", detrend="constant")`: jednostronna gęstość widmowa mocy (PSD) w `unit²/Hz`.
- `SpectralEstimate`: `frequencies_hz`, `values[frequency][channel]`, `units`, `kind`, okno, detrend, liczba próbek, sampling rate i identyfikatory pochodzenia.

Wymagane jest regularne próbkowanie, co najmniej dwie próbki i kompletność danych. Dane zamaskowane nie są interpolowane; sygnał z brakującą próbką jest odrzucany jako `DATA_LOSS`. Nie ma automatycznego resamplingu ani detekcji artyfaktów.

Okna: prostokątne `boxcar` oraz **periodyczne Hann**, odpowiednie do FFT. Detrend: `none` lub odjęcie średniej `constant`, wykonywane przed oknem. Skala jednostronnego periodogramu:

```text
P[k] = |RFFT(x_detrended · window)[k]|² / (fs · Σ window²)
P[k] *= 2 dla dodatnich częstotliwości poza Nyquistem
```

DC oraz Nyquist (dla parzystej liczby próbek) nie są mnożone przez 2. Rozdzielczość częstotliwości `Δf=fs/N`; suma PSD · Δf odpowiada odpowiednio znormalizowanej mocy sygnału w oknie. FFT zwraca *nieznormalizowany* wynik zespolony, bez jednostronnego podwojenia.

**Niezrealizowane:** Welch PSD, spektrogram, testy urządzeń i wydanie. [Kontrakt](../../../docs/contracts.md), [Testy](../../../docs/testing.md).
