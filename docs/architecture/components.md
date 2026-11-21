# Planowane komponenty

| Moduł | Odpowiedzialność | Ograniczenia | Status |
| --- | --- | --- | --- |
| `lib_sig.io` | Import/eksport sygnałów i metadanych (EDF/BDF/FIF/CSV jako docelowe formaty) | Nie tracić informacji o jednostkach, montażu, kanale i próbkowaniu | PLANNED |
| `lib_sig.filters` | Filtry cyfrowe, resampling i kontrola aliasingu | Jawne pasmo, rząd, faza, kompensacja opóźnienia, znane parametry | PLANNED |
| `lib_sig.events` | Zdarzenia, epoki i wyrównanie zegarów | Jawny timebase i niepewność synchronizacji | PLANNED |
| `lib_sig.quality` | Kontrola artefaktów, braków i nasycenia kanałów | Metryki i progi jako parametry; brak udawania oceny klinicznej | PLANNED |
| `lib_sig.features` | Widma, moc pasmowa, cechy w dziedzinie czasu i częstotliwości | Zachować jednostki, okno, overlap i parametry normalizacji | PLANNED |

Biblioteka odpowiada za wspólną reprezentację sygnału, jakość danych, filtrowanie, synchronizację i ekstrakcję cech; nie steruje hardware i nie wykonuje diagnostyki klinicznej. lib-eye odpowiada za okulografię, lib-audio za semantykę mowy i ASR/TTS, a devices za kontrakty urządzeń.

Publiczne symbole implementować dopiero po teście kontraktowym; `contracts/api.json` rejestruje tylko rzeczywistą implementację.
