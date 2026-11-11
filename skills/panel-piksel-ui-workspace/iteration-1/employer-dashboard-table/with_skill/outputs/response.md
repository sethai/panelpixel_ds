Panel pracodawcy jest gotowy jako jeden plik HTML: `panel-pracodawcy.html` (w tym folderze). Style systemu (`tokens.css` i `components.css`) są wklejone do pliku bez zmian, więc nie ma osobnych plików CSS.

**Co jest na ekranie**
- **Nagłówek strony:** tytuł „Moje ogłoszenia” i przycisk **+ Dodaj ofertę**. To jedyny przycisk główny na stronie, akcje w tabeli są drugorzędne.
- **Pasek podsumowania** z liczbami za ostatnie 30 dni (oferty, wyświetlenia, aplikacje, oferty wygasające).
- **Callout:** „2 oferty wygasają w tym tygodniu” z nazwami i datami (11.11 i 14.11) oraz przyciskiem „Przedłuż obie”. To jedyny wyróżniający się element ekranu.
- **Zakładki** Aktywne 19 / Szkice 3 / Wygasłe 12. Zakładki przełączają się kliknięciem albo strzałkami, Home i End.
- **Tabela:** stanowisko z lokalizacją i widełkami, status, pakiet, wyświetlenia, aplikacje, data wygaśnięcia i akcje. Liczby i daty są w foncie pikselowym i wyrównane do prawej.
  - Oferty wygasające w tym tygodniu mają czerwoną krawędź wiersza, dopisek „za 2 dni” i przycisk „Przedłuż”.
  - Szkice mają akcje „Podgląd” i „Dokończ”, a wygasłe oferty „Aplikacje” i „Wznów”.
- **Paginacja** z opisem „Oferty 1–8 z 19”.
- **Legenda pakietów:** cztery pakiety z cenami, żeby było jasne, co oznacza każdy kolor.

**Pakiety jako tiery rzadkości:** Legendarny, Epicki, Rzadki i Zwykły, w kolorach pakietów z design systemu. Kolor zawsze idzie w parze z nazwą, więc nie jest jedyną informacją.

**Elementy dodane poza design systemem** (warto dopisać je do design.md):
- **`.tier-tag`:** mały znacznik pakietu do wiersza tabeli. Ma wysokość 24 px, ramkę 2 px i lewą krawędź 10 px w kolorze pakietu. Pełna karta pakietu jest za duża do komórki tabeli.
- **Status jako badge z kolorowym kwadratem:** zielony dla aktywnej, szary dla szkicu, czerwony dla wygasłej. Tekst statusu jest zawsze widoczny.
- **Oznaczenie wygasającej oferty:** czerwona krawędź wiersza i dopisek w kolorze błędu.

Użyłem przepisu nr 10 „Panel użytkownika” z `screen-recipes.md`, uzupełnionego o tiery z przepisu nr 6.

**Sprawdzenie**
- `check_screen.py`: OK, bez błędów i ostrzeżeń.
- Render obejrzałem w Chrome headless w szerokościach 1280 px i 390 px.
  - Przy 390 px strona nie przewija się w poziomie (zmierzyłem szerokość strony: 390 px).
  - Tabela przewija się w swojej ramce, a długie nazwy stanowisk kończą się wielokropkiem.
  - Polskie znaki wyświetlają się poprawnie w obu fontach.
- Przełączania zakładek nie klikałem w przeglądarce. Sprawdziłem tylko kod.
- Strona używa Google Fonts, więc bez internetu fonty zastąpi font systemowy.
