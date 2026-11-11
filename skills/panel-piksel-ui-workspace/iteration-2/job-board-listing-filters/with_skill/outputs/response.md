Gotowe — ekran wyników wyszukiwania **LevelUp Jobs** w stylu Panel & Piksel, jeden przenośny plik:

`levelup-jobs-wyniki.html` (CSS systemu i skrypty `list-controls.js` + `ui-controls.js` wklejone przez `inline_css.py`; zewnętrzne są tylko fonty Google)

**Przepis:** `screen-recipes.md` §3 „Wyniki wyszukiwania z filtrami” (`.layout-results`, filtry w prawej kolumnie) + warianty z §11 (`.card-meta`, `.card-foot` z `.btn-compact`, `.opt-n`, `.range`, filtry w szufladzie na telefonie, zwijana nawigacja).

**Co jest na ekranie**
- 8 ofert w kartach `.card` z 8 różnych studiów (Smocza Jama Studio, Kosmiczny Kret, Pikselowa Kuźnia, Żółwie Łamigłówki, 8bit Atelier, Gąszcz Games, Sowa i Smok, Rakietowy Ślimak): monogram, tytuł, firma i miasto, poziom i tryb, kwota w Press Start 2P („24 000–30 000 zł netto B2B”, jedna „brutto UoP”), chipy technologii (max 4 + `.chip-more`), data dodania i przycisk „Zapisz” (przełącznik `aria-pressed`).
- 2 oferty bez widełek — „Widełki nie podane” (`.amount.is-empty`).
- 1 nowa oferta — Senior Unreal Engine Developer z badge „Nowa”.
- Sortowanie: „Najnowsze” / „Najwyższe widełki” (grupa przycisków `aria-pressed`; oferty bez widełek lądują na końcu).
- Panel filtrów po prawej: słowa kluczowe, tryb pracy, poziom (Junior/Mid/Senior/Lead), technologia (Unity, Unreal Engine, Godot, C++, C#), widełki od–do + „Tylko z widełkami”. Filtry działają na żywo, liczby przy opcjach wylicza skrypt, chipy aktywnych filtrów, licznik w nagłówku i w przycisku „Pokaż 8 ofert” z polską odmianą, pusty stan z „Wyczyść filtry”.
- Telefon (< 900 px): filtry chowają się w szufladzie otwieranej przyciskiem „Filtry”, nawigacja zwija się do menu.

**Głośny element:** brak sceny (to ekran pracy) — jedynym akcentem jest wyszukiwarka główna z kolorowym cieniem w nagłówku; badge „Nowa” jest jedyny żółty element.

**Nowe elementy spoza systemu:** brak — wszystko z istniejących klas. Style ekranu to tylko układ (link w tytule karty w kolorze `--ink`, odstępy listy, przewijanie paska sortowania), wyłącznie na tokenach.

**Decyzje:** zrezygnowałem z trzeciej opcji sortowania („Najniższe widełki”), bo na 390 px ucinała się w pasku; paginacji nie dodawałem (8 ofert, brak kolejnych stron). Linki (oferty, nawigacja) prowadzą do przykładowych adresów — to makieta bez backendu.

**Sprawdzenie**
- `check_screen.py`: OK — brak uwag (0 ERROR, 0 WARN).
- `render_check.py`: 1280 px i 390 px — szerokość dokumentu OK (brak poziomego przewijania), Archivo i Press Start 2P z polskimi znakami ładują się; test klikania: 0 martwych kontrolek (31 z 34 klikniętych; za pierwszym razem martwe były linki „#” w okruszkach — poprawione). Oba zrzuty obejrzałem: nic nie nachodzi, karty i chipy zawijają się poprawnie.
- Nie sprawdzałem ręcznie zawartości szuflady filtrów na telefonie po otwarciu (skrypt klika tylko kontrolki widoczne po załadowaniu) ani trybu ciemnego.
