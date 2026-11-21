# core

Planowane typy danych: `SignalBlock`, `TimeAxis`, `ChannelDescriptor`, `SignalEvent` i `TransformProvenance`. Domyślna kolejność danych `samples[sample,channel]`, z jednoznacznym przypisaniem kanałów i jednostek.

Oś czasu może być regularna (start i `sampling_rate_hz > 0`) albo nieregularna (jawny, uporządkowany wektor timestampów). Rzeczywiste i zespolone wartości, maski danych brakujących i kalibracja wymagają osobnej deklaracji. Brak jednostek lub nieregularny sygnał nie może być automatycznie „naprawiany”.

**PLANNED / NOT_IMPLEMENTED.**
