Sklep z przedmiotami do gry jest gotowy jako jeden plik HTML:
`/Users/sethai/Data/szkolenie_ai_heroes/code/design_system/skills/panel-piksel-ui-workspace/iteration-1/game-item-shop/with_skill/outputs/sklep-przedmiotow.html`

Plik działa sam: `tokens.css` i `components.css` są wklejone bez zmian do `<style>`, a style tego ekranu są w osobnym bloku `<style id="screen">` i korzystają tylko z tokenów. Z zewnątrz ładują się jedynie fonty Google (Archivo i Press Start 2P).

**Co jest na ekranie**
- **Nagłówek:** logo PIKSELBAZAR, nawigacja z linkiem „Koszyk (4)”, wyszukiwarka i portfel z liczbą monet (2 150).
- **Siatka 12 przedmiotów:**
  - przedmioty: 3 miecze, 3 mikstury, zwój, tarcza, hełm i 3 skórki;
  - każdy ma pikselową ikonę 12×12 (SVG z ostrymi krawędziami, kolory SNES, skala ×4);
  - pod nazwą jest typ i statystyka, a cena w monetach jest zapisana fontem Press Start 2P z ikoną monety i dopiskiem „monet”;
  - przycisk „Do koszyka” przełącza się na „W koszyku”.
- **Oznaczenie rzadkości (Legendarny / Epicki / Rzadki / Zwykły):** to zawsze nazwa i kolor razem. Karta ma lewą krawędź 10 px w kolorze rzadkości (`--tier-*`), jak w komponencie `.tier`. Do tego jest badge z nazwą i kwadratem w tym samym kolorze.
- **Pozostałe elementy:** zakładki sortowania i kategorii oraz paginacja.
- **Boczny koszyk (przyklejony przy przewijaniu na desktopie):**
  - pozycje z rzadkością i przyciskami −/+;
  - podsumowanie: przedmioty 3 640, twoje monety 2 150, „Brakuje 1 490” na czerwono i z tym słowem w tekście, do zapłaty 3 640;
  - pasek „Masz 59% potrzebnych monet”.
- **Przycisk „Kup za 3 640 monet” jest zablokowany:**
  - zablokowany jest w wariancie systemu: `aria-disabled="true"`, pikselowa kłódka i powód w `.btn-reason` podpięty przez `aria-describedby` („Brakuje 1 490 monet. Doładuj portfel albo usuń coś z koszyka.”);
  - pod nim jest drugorzędny przycisk „Doładuj monety”.
- **JavaScript na żywo przelicza koszyk.** Przycisk kupna jest zablokowany, dopóki brakuje monet albo koszyk jest pusty. Kliknięcie w zablokowany przycisk niczego nie kupuje, tylko odczytuje powód w regionie `role="status"`.

**Przepis:** połączyłem przepis 3 (wyniki z filtrami: siatka kart i kolumna boczna) z przepisem 4 (blok akcji z ceną i zablokowanym przyciskiem). Kolory rzadkości wziąłem z przepisu 6 (tiery).

**Głośny element:** panel koszyka (`.panel.is-featured`, różowy cień). To jedyne wyróżnienie na ekranie.

**Nowe elementy, których nie ma w systemie** (złożyłem je z prymitywów: ramka 2 px, twarde cienie, `--notch`, tokeny), warto je dopisać do design.md:
1. **Karta przedmiotu:** `.card` ułożona pionowo, z lewą krawędzią tieru 10 px i ramką na ikonę.
2. **Etykieta rzadkości:** `.badge.rarity` z kwadratem 8 px w kolorze tieru.
3. **Wiersz koszyka z licznikiem sztuk:** przyciski −/+ mają 28 px. To mniej niż 44 px wymagane dla przycisków, więc do decyzji.
4. **Podsumowanie koszyka:** `dl` z wierszem „Brakuje” w `--danger`.
5. **Pasek monet:** ramka 2 px i wypełnienie w `--action`.
6. **Portfel w nagłówku.**

**Sprawdzenie**
- `check_screen.py`: OK, brak błędów i ostrzeżeń.
- Render obejrzałem w headless Chrome w 1280 px i 390 px. Na 390 px pokazałem ekran w ramce iframe, bo okno headless Chrome nie zwęża się poniżej ok. 500 px.
- Na desktopie widać 3 kolumny i koszyk obok.
- Na 390 px jest jedna kolumna, a koszyk jest pod siatką (link „Koszyk (4)” w nagłówku do niego przewija). Strona nie przewija się poziomo, tylko zakładki kategorii przewijają się w swojej ramce. Długie nazwy ucinają się wielokropkiem, a polskie znaki wyświetlają się w obu fontach.
- Klikania w −/+ i dodawania do koszyka nie testowałem ręcznie. Widziałem tylko, że skrypt uruchamia się bez błędu i rysuje stan początkowy.
