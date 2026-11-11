# Strona Panel & Piksel na Cloudflare Pages

Strona to czysty HTML/CSS/JS w katalogu `site/` — Cloudflare niczego nie buduje.

## Sposób 1 — przeciągnij i upuść (najprościej)

1. Cloudflare → **Workers & Pages** → **Create** → **Pages** → **Upload assets**.
2. Nazwa projektu, np. `panel-piksel`.
3. Przeciągnij plik `dist/panel-piksel-site-<wersja>.zip` (albo cały katalog `site/`).
4. **Deploy** — strona będzie pod `https://panel-piksel.pages.dev`.

Kolejna wersja: w projekcie → **Create deployment** → wgraj nowy ZIP.

## Sposób 2 — z wiersza poleceń

```bash
npx wrangler pages deploy site --project-name panel-piksel
```

## Sposób 3 — z repozytorium Git

Połącz repozytorium w Cloudflare Pages i ustaw: **Build command**: puste · **Build output directory**: `site`.
Przed każdym commitem odbuduj stronę (patrz niżej) — Cloudflare publikuje to, co jest w `site/`.

## Odbudowanie po zmianach w systemie

```bash
python3 tools/build_all.py   # sync → docs → dist/panel-piksel-<wersja>.zip → site/ → dist/panel-piksel-site-<wersja>.zip
```

W `site/` są też `_headers` (nagłówki bezpieczeństwa i cache), `_redirects` i `404.html` — Cloudflare Pages używa ich automatycznie.
Strona ładuje fonty z Google Fonts; jeśli chcesz mieć wszystko na własnym serwerze, pobierz Archivo i Press Start 2P (licencja OFL) i podmień link w `tools/build_site.py`.
