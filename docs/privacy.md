# Prywatność i retencja danych sygnałowych

Próbki mogą pochodzić z biosensorów, mikrofonów, czujników ruchu, maszyn i systemów robotycznych. Zależnie od źródła mogą ujawniać dane osobowe, zdrowotne, lokalizację albo informacje o infrastrukturze. Ryzyko i uprawnienia ocenia się **dla konkretnego zastosowania**, a nie na podstawie nazwy biblioteki.

Biblioteka nie przechowuje domyślnie surowych próbek ani historii analiz, nie publikuje ich w GitHub Issues, PR, CI lub Pages. Rejestrowanie metadanych ma być minimalne: SHA kodu, opis operacji, typ danych i wynik kontroli; bez payloadów pomiarowych.

Kontrakty urządzeń i dane dostępowe należą do prywatnego repo `devices`. W publicznym repozytorium wykorzystywać wyłącznie dane syntetyczne oraz nieidentyfikujące metadane.
