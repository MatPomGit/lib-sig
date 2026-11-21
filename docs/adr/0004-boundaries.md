# ADR-0004: granice biblioteki Signal

Data: 2026-11-21  
Status: proposed

## Kontekst

Próbkowane sygnały z biosensorów, robotów, mikrofonów i aparatury przemysłowej wykorzystują zbliżone operacje DSP. Odrębne, dziedzinowe implementacje filtrów i analizy widmowej zwiększają ryzyko niespójności numerycznych.

## Propozycja

`lib-sig` ma przechowywać ujednolicony model danych czasowych oraz uniwersalne algorytmy DSP: filtrowanie, resampling, FFT/PSD, zdarzenia, jakość i ekstrakcję cech. Biblioteka nie ma być ograniczona do biosygnałów. Akwizycja i interpretacja dziedzinowa pozostają u konsumentów; `lib-audio` realizuje m.in. ASR/TTS, `lib-vis` przetwarza piksele, a `lib-track` zarządza trajektoriami obiektów.

## Alternatywy

- DSP osobno w każdej aplikacji: trudniejsze testowanie i reprodukcja.
- Jeden framework do wszystkiego (audio, obraz, tracking, sensory): nadmierna liczba zależności.

## Konsekwencje

Wspólne kontrakty jednostek i osi czasu, ale konieczność szczegółowych testów numerycznych. Brak deklaracji kompatybilności bez testów na konkretnym SHA.
