# core: model próbkowanego sygnału

**Status: IMPLEMENTED (EXPERIMENTAL), bez wydania.** Dostępne: `ChannelDescriptor`, `TimeAxis`, `SignalBlock` i `SignalValidationError`. Źródła: [models.py](models.py). Import po umieszczeniu `src/` na ścieżce Pythona: `from lib_sig import TimeAxis, ChannelDescriptor, SignalBlock`.

`SignalBlock.samples` to niepusta, niezmienna krotka wierszy `(sample, channel)`. Każdy kanał wymaga jawnej jednostki. `TimeAxis` obsługuje próbki regularne (`start_s`, `sampling_rate_hz`) i nieregularne (`timestamps_s`), wymagając jawnego `timebase`. Timestamps są w sekundach. Pole `mask` ma `True` dla danych ważnych, `False` dla braków; wartości niekończone są dopuszczalne tylko w pozycjach oznaczonych `False`.

Kod odrzuca niespójne wymiary, zduplikowane kanały, nieprawidłowe jednostki, nieuporządkowany czas i niezamaskowane wartości niekończone. `SignalValidationError.code` zapewnia klasyfikację błędów. Nie ma akwizycji, filtrowania, zapisu na dysk ani zależności od SDK urządzeń.

[Kontrakt](../../../docs/contracts.md) · [Testy](../../../docs/testing.md).
