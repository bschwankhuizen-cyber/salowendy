# Wendy's Schoonheidssalon — www.salonwendy.nl

Statische website voor Wendy's Schoonheidssalon in Oldenzaal, in de eigen huisstijl
(logo, Roboto, mauve `#6D5A64`, roze `#E73B73`, originele foto's in `src/img/`), geserveerd door de
Cloudflare Worker **`salonwendy`** (alleen statische assets, geen servercode).

## Structuur

| Pad | Inhoud |
| --- | --- |
| `build.py` | Alle teksten, prijzen en paginasjablonen. Hier pas je de inhoud aan. |
| `src/style.css`, `src/site.js`, `src/_headers` | Stijl, menu en animaties, HTTP-headers |
| `public/` | Gegenereerde website (wordt meegecommit, zodat er geen buildstap nodig is) |
| `wrangler.jsonc` | Configuratie voor de Cloudflare Worker `salonwendy` |

## Aanpassen

1. Wijzig teksten of prijzen in `build.py` (bijvoorbeeld `HENNA_PRIJS`, `HARSEN`, `GROEPEN`).
2. Draai `python3 build.py` (Python 3.12+, geen extra pakketten nodig).
3. Commit en push. Daarna de site opnieuw uitrollen (zie hieronder).

Lokaal bekijken:

```bash
cd public && python3 -m http.server 8000
```

## Uitrollen naar Cloudflare

Via de Cloudflare-dashboard Git-koppeling van de Worker `salonwendy`
(Settings → Build): deploy command `npx wrangler deploy`, buildcommando leeg laten
(of `python3 build.py`), root directory `/`.

Of handmatig:

```bash
npx wrangler deploy
```

Koppel daarna onder *Settings → Domains & Routes* de domeinen `salonwendy.nl` en
`www.salonwendy.nl` aan de Worker.

De oude URL's van de vorige site (`/gezichtsbehandelingen`, `/overige_behandelingen`,
`/henna-wenkbrauwen`, `/nagels`, `/kadobon`, `/contact`, `/privacy` en de vier
subpagina's van de gezichtsbehandelingen) blijven allemaal werken.
