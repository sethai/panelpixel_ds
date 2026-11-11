# Sklep z przedmiotami — Panel & Piksel

**Plik:** `sklep.html` — jeden przenośny plik. CSS i skrypty systemu są wklejone przez `scripts/inline_css.py`. Fonty ładują się z Google Fonts, więc potrzebny jest internet. Katalog `panel-piksel/` obok był potrzebny tylko w trakcie budowania i można go usunąć.

## Co jest na ekranie

- **Nagłówek:** portfel „Twoje monety 1 250” oraz link „Koszyk” z liczbą sztuk. Link przewija stronę do koszyka, co przydaje się na telefonie, gdzie koszyk jest pod listą.
- **Filtry nad siatką:** szukanie po nazwie, kategoria (Broń / Pancerze / Mikstury / Skórki / Inne) i rzadkość. Liczby przy opcjach wylicza `list-controls.js`. Są też chipy aktywnych filtrów, przycisk „Wyczyść filtry” i pusty stan, gdy nic nie pasuje.
- **Sortowanie:** grupa przycisków z `aria-pressed`, czyli Popularne / Najtańsze / Najdroższe / Najrzadsze. Licznik nad listą odmienia słowo („1 przedmiot / 3 przedmioty / 12 przedmiotów”).
- **Siatka 12 przedmiotów:** miecze, tarcza, mikstury, skórki, klucz, zwój, skrzynia i klejnot. Każda karta ma:
  - pikselową ikonę z `icons.css`,
  - rzadkość jako `.tier-tag` (Legendarny / Epicki / Rzadki / Zwykły, zawsze kolor razem z nazwą),
  - atrybuty w `.card-meta`,
  - cenę w monetach w pixel-foncie,
  - stopkę `.card-foot` z przyciskiem `.btn-compact` „Do koszyka”. Gdy przedmiot jest już w koszyku, przycisk zmienia się na „Dodaj jeszcze”, a stopka pokazuje „w koszyku: N szt.”.
- **Boczny koszyk** jest złożony z klocków systemu według design.md §6.23:
  - wiersze z nazwą i `.tier-tag`, pod nimi `.stepper` −/+, cena pozycji i przycisk „Usuń”,
  - `.facts` z wartością koszyka, Twoimi monetami i polem „Brakuje 860” w `--danger`,
  - `.progress` z napisem „Masz potrzebnych monet 59%”,
  - przycisk „Kup za 2 110 monet”, zablokowany przez `aria-disabled`, z `.lock` i powodem w `.btn-reason`: „Brakuje Ci 860 monet. Usuń część przedmiotów albo zdobądź monety w grze.”
- **Koszyk działa naprawdę:**
  - dodawanie, zmiana liczby sztuk i usuwanie przeliczają sumę, brakującą kwotę, pasek postępu i odmianę „monetę/monety/monet”,
  - gdy monet wystarczy, przycisk się odblokowuje, a po zakupie odejmuje monety, opróżnia koszyk i pokazuje powiadomienie `ppToast` „Kupiono przedmioty”,
  - zmiany w koszyku są ogłaszane czytnikom ekranu (`aria-live`).

## Przepis i głośny element

- **Przepis:** „Wyniki z filtrami” (§3) połączony z „Sklep / koszyk” (§11, design.md §6.23), w układzie `.layout-main-side`. Na telefonie jest jedna kolumna, a koszyk trafia pod listę.
- **Głośny element:** koszyk, czyli `.panel.is-featured` z różowym cieniem. To jedyny akcent na ekranie. Akcenty NES pojawiają się tylko w tierach i w zablokowanym przycisku.

## Poza gotowymi komponentami (kandydaci do zgłoszenia, design.md §0.5)

Wszystkie są zbudowane z prymitywów i tokenów systemu. Nie dodawałem ich do `components.css`.

1. **Pionowa karta produktu.** To `.card` z `flex-direction: column` i polem ilustracji `.item-art`: tło `--paper`, ramka `var(--border)`, wysokość 88 px (na telefonie 64 px), ikona `.sprite-xl` na środku. Siatka to `repeat(auto-fill, minmax(min(250px,100%),1fr))`. Propozycja: wariant `.card.card-product`.
2. **Poziomy panel filtrów nad siatką.** To `.panel-filters` z układem grid: wyszukiwarka i dwie grupy opcji w rzędzie, opcje zawijają się w poziomie, a stopka zawiera aktywne filtry i „Wyczyść”. Propozycja: wariant `.panel-filters.is-horizontal`.
3. **Portfel w nagłówku.** To `.badge-seg` z ikoną monety, a kwota jest w pixel-foncie. Propozycja: `.wallet`.
4. **Układ wiersza koszyka** (`.cart-row`). Pierwsza linia to ikona, nazwa z wielokropkiem i tier. Druga linia to `.stepper`, cena wyrównana do prawej i przycisk usuwania. §6.23 opisuje to tylko słownie, więc warto dopisać gotowy kod.

## Wyniki sprawdzeń

- `check_screen.py`: **OK — brak uwag** (0 ERROR, 0 WARN).
- `render_check.py`:
  - 1280 px: szerokość dokumentu 1280 px (OK).
  - 390 px: szerokość dokumentu 390 px (OK). Wcześniej było 416 px, bo przewijany pasek sortowania rozpychał kolumnę; poprawione przez `min-width: 0`.
  - Fonty Archivo i Press Start 2P z polskimi znakami ładują się.
  - Test klikania: kliknięto 33 z 37 kontrolek, martwych 0.
  - 4 kontrolki test pominął jako niewidoczne po załadowaniu. Przycisk „Wyczyść filtry” w pustym stanie jest ukryty, dopóki filtry niczego nie zwracają.
  - Zrzuty obejrzałem, nic nie nachodzi na siebie. Leżą w `shots/sklep-1280.png` i `shots/sklep-390.png`.
- Ręczny test w przeglądarce:
  - na starcie zakup jest zablokowany z powodem „brakuje 860”,
  - po usunięciu „Ostrza Zmierzchu” przycisk się odblokował i pokazał „Po zakupie zostanie Ci 940 monet”,
  - zakup odjął monety (zostało 940), opróżnił koszyk, pokazał pusty stan i powiadomienie.

## Czego nie sprawdziłem

- Trybu ciemnego. Style ekranu używają wyłącznie tokenów, więc powinien działać, ale go nie oglądałem.
- Działania z czytnikiem ekranu.
- Linki do stron przedmiotów, „Ekwipunku” i „Rankingu” prowadzą do adresów, których nie ma, bo to pojedynczy ekran.
