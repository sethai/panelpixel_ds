Leaderboard „Kosmicznego Kreta” jest gotowy jako jeden plik:

`/Users/sethai/Data/szkolenie_ai_heroes/code/design_system/skills/panel-piksel-ui-workspace/iteration-1/leaderboard-high-scores/with_skill/outputs/leaderboard.html`

Fonty ładują się z Google Fonts. Pliki `tokens.css` i `components.css` z systemu są wklejone bez zmian do osobnych bloków `<style>`. Style samego ekranu są w trzecim bloku, `<style id="screen">`, i używają wyłącznie tokenów.

**Co jest na ekranie** (oparte na przepisie „5. Ranking / leaderboard”)
- Na górze: nagłówek z logo KOSMICZNYKRET, nawigacją (Ranking jest aktywny) i wyszukiwarką graczy. Pod nim okruszki, tytuł „High scores” z krótkim opisem i przełącznik okresu **Dziś / Ten tydzień / Wszech czasów**. Pod przełącznikiem jest linijka z zakresem dat, np. „Tydzień 3–9 listopada 2026 · reset w poniedziałek o 00:00”.
- **Podium** z miejscami 1–3. Każde miejsce ma monogram, nick, kraj z liczbą gier i wynik (u zwycięzcy w złocie). W kodzie kolejność to 1-2-3, na ekranie 2-1-3.
- **Tabela z miejscami 4–20**. Kolumny: #, Gracz, Kraj, Wynik (posortowany malejąco), Rozgrywki, Zmiana. Zmiana pozycji pokazuje się jako ▲ zielone z liczbą, ▼ czerwone z liczbą, „=” bez zmian albo żółty znaczek „Nowy”. Czytnik ekranu dostaje do tego tekst, np. „awans o 3”. Długie nicki ucinają się wielokropkiem, a pełna nazwa jest w dymku (`title`).
- **Paginacja** wygląda tak: ‹ 1 2 3 … 9 ›, a obok jest licznik „Miejsca 4–20 z 180”. Strona 2 pokazuje miejsca 21–40 i tak dalej. Podium zostaje zawsze widoczne.
- Przełącznik i paginacja działają. Dane są fikcyjne i wpisane w plik: Dziś ma 4 strony, Ten tydzień 9, Wszech czasów 25. Zakładki przełącza się też strzałkami na klawiaturze. Stan widoku trafia do adresu (`#wszech-7`), więc da się wysłać link do konkretnej strony.

**Głośny element:** podium. Na ekranie nie ma wyróżnionego panelu ani ilustracji.

**Nowe elementy, których nie ma w systemie.** Zbudowałam je z istniejących klocków i warto je dopisać do design.md:
1. `.cc`: kod kraju w ramce 2 px, napisany fontem pikselowym, obok pełna nazwa kraju. Kraj nie jest rangą, więc nie ma koloru.
2. `.delta-same`: znak „=” w kolorze `--ink-3` dla graczy bez zmiany pozycji. W systemie są tylko `.delta-up` i `.delta-down`.
3. `.rank` przy liczbach trzycyfrowych (od miejsca 100) rozszerza się w poziomie (`min-width: 28px`). Kwadrat 28 px nie mieści trzech cyfr.
4. Paginacja: wielokropek bez ramki (`.gap`) i wyszarzona strzałka na pierwszej lub ostatniej stronie (`.is-off`).
5. `.podium-meta`: linijka z krajem i liczbą gier pod nickiem na podium.
6. Na telefonie w kolumnie „Kraj” widać tylko kod, a pełna nazwa jest dostępna dla czytnika ekranu. Dzięki temu wynik mieści się w pierwszym widoku tabeli, a resztę przewija się w jej ramce.

**Sprawdzenie**
- `check_screen.py` nie zgłasza żadnych błędów ani ostrzeżeń.
- Render obejrzałam w Chrome bez okna, w szerokości 1280 px (widoki: Ten tydzień str. 1, Dziś str. 4, Wszech czasów str. 7) i 390 px. Przy 390 px szerokość strony to dokładnie 390 px, więc nic nie wychodzi poza ekran.
  - Znalazłam i poprawiłam błąd: ukryte teksty dla czytnika w komórkach tabeli rozpychały stronę do 696 px na telefonie. Pomogło `position: relative` na `.table-wrap`.
  - Polskie znaki wyświetlają się poprawnie w obu fontach.
- Nie testowałam ekranu z czytnikiem ekranu ani w innych przeglądarkach niż Chrome.
