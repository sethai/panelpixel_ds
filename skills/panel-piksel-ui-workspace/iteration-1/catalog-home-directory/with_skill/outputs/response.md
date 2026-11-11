Strona główna PixelHub jest gotowa w jednym pliku: `index.html` w katalogu outputs. Oba pliki systemu (`tokens.css`, `components.css`) są wklejone do `<style>` bez zmian, więc plik działa samodzielnie. Z zewnątrz ładuje tylko fonty Google: Archivo i Press Start 2P.

**Co jest na ekranie** (przepis nr 1, „Katalog — strona główna”):
- **Wyszukiwarka:** duże pole `.search-main` pod nagłówkiem H1, pod nim chipy z popularnymi frazami (CC0, 16×16, PICO-8, dithering, polskie znaki). Niżej trzy liczniki: 4 529 zasobów, 8 kategorii, 37 nowych w tym tygodniu.
- **Wyróżniony panel „Świeżo dodane”:** `.panel.is-featured`, licznik 37, 7 pozycji z kategorią, trzy pierwsze z żółtym badge „Nowe”. Obok zwykły panel „Znasz darmowy zasób?” z jedynym przyciskiem głównym „Zgłoś zasób” i callout o licencjach.
- **Siatka 8 kategorii** (`.grid-panels`): Edytory 46, Palety 1 280, Fonty 312, Tutoriale 534, Tilesety 2 048, Animacja 87, Społeczności 64, Sklepy z assetami 158. Każda ma `.count`, krótkie motto, 6–7 pozycji z monogramem i liczbą zapisań oraz link „Zobacz wszystkie”. Dane są realistyczne, np. LibreSprite, Pixelorama, Endesga 32, m5x7, Kenney 1-Bit Pack, r/PixelArt.

**Głośny element:** panel „Świeżo dodane”, jedyny `.is-featured` na stronie, z różowym cieniem.

**Elementy spoza systemu** (zbudowane z tokenów, można dopisać do design.md):
- Pod H1 jest duża wyszukiwarka z kolorowym cieniem zamiast tej w nagłówku. To ten sam komponent, tylko w innym miejscu.
- Lista w wyróżnionym panelu ma dwie kolumny (od 1100 px w dół jedną) i małą etykietę kategorii `.fresh-cat`, ukrytą na telefonie.
- Pasek popularnych fraz to chipy jako linki.
- Pasek liczników: liczba w Press Start 2P, podpis w Archivo.
- `a.btn { text-decoration: none }`, bo przyciski zrobione jako linki dostawały podkreślenie.

**Sprawdzenie:**
- `check_screen.py`: „OK — brak uwag”, czyli 0 ERROR i 0 WARN.
- Render obejrzany w headless Chrome w 1280 px i 390 px (w 390 px przez iframe o tej szerokości). W 1280 px kategorie układają się w 4 kolumny po 2 rzędy, a wyróżniony panel stoi obok panelu zgłoszeń. W 390 px wszystko jest w jednej kolumnie i długie nazwy kończą się wielokropkiem. Na zrzutach nic nie wystaje poza szerokość ekranu, ale nie mierzyłem tego skryptem. Polskie znaki renderują się w obu fontach.
- Nie sprawdzałem czytnikiem ekranu ani zmierzonych kontrastów.
