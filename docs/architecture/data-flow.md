# Przepływ sygnałów

Dane z pliku, urządzenia lub symulatora trafiają do `io`, następnie do zwalidowanego `SignalBlock`, opcjonalnych transformacji `filters/spectral/events` i konsumenta.

Wymagane metadane: identyfikator źródła, nazwy kanałów, jednostki, częstotliwość próbkowania lub wektor czasu, wskazanie zegara i historia transformacji. Każda zmiana długości bloku, amplitudy lub osi czasu musi zostać jawnie opisana. Nie wolno wstawiać brakujących próbek bez wybranej metody interpolacji.

Strumienie mogą zawierać wrażliwe dane pomiarowe, dlatego biblioteka nie powinna domyślnie zapisywać surowych próbek do publicznych logów ani GitHub CI. Akwizycja sprzętowa jest własnością jawnie skonfigurowanych adapterów odbiorcy.

**Implementacja i E2E: NOT_RUN.**
