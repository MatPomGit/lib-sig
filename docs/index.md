# Dokumentacja lib-sig

Akwizycja i przetwarzanie wielokanałowych sygnałów pomiarowych, w tym EEG, EMG, EDA i PPG.

- [Architektura](architecture/README.md), [moduły](architecture/components.md), [przepływy](architecture/data-flow.md), [dystrybucja](architecture/distribution.md).
- [Kontrakt](contracts.md), [zależności](dependencies.md), [konsumenci](consumers.md), [zgodność](compatibility.md).
- [Testy](testing.md), [roadmap](roadmap.md), [instalacja](installation.md), [prywatność](privacy.md), [ADR-0004](adr/0004-boundaries.md).

Tylko katalog `pages/` jest możliwym źródłem publikowanych stron. `core` i FIR scalono do `main`; eksperymentalne RFFT/PSD znajduje się w PR #4. Brak wydania i automatycznej publikacji.
