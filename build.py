#!/usr/bin/env python3
"""Bouwt de statische website van Wendy's Schoonheidssalon naar ./public.

Gebruik:  python3 build.py
Alle teksten en prijzen staan hieronder in dit bestand; pas ze hier aan en
draai het script opnieuw. Er zijn geen externe pakketten nodig.
"""
from __future__ import annotations

import datetime
import html
import json
import re
import shutil
from pathlib import Path

from PIL import Image  # pip install pillow

ROOT = Path(__file__).parent
OUT = ROOT / "public"
ARCHIEF = ROOT / "archief" / "afbeeldingen"
VANDAAG = datetime.date.today().isoformat()
SITE = "https://www.salonwendy.nl"

# ---------------------------------------------------------------- gegevens
SALON = {
    "naam": "Wendy's Schoonheidssalon",
    "straat": "Uiverstraat 39",
    "postcode": "7574 BA",
    "plaats": "Oldenzaal",
    "tel": "0541 538 153",
    "tel_link": "+31541538153",
    "mail": "info@salonwendy.nl",
    "maps": "https://www.google.com/maps/search/?api=1&query=Uiverstraat+39+7574+BA+Oldenzaal",
}
HENNA_PRIJS = "€ 24,00"
GA4_ID = "G-06DQ66QK3J"  # Google Analytics 4 metings-ID

GROEPEN = [
    {
        "slug": "korte-behandelingen",
        "header": "header-kort.jpg",
        "titel": "Korte behandelingen",
        "kort": "Korte behandeling",
        "hero": "Je huid ziet er na de behandeling <em>stralend</em> uit",
        "intro": "Weinig tijd, wel toe aan een frisse huid? Kies een korte gezichtsbehandeling van 30 of 40 minuten.",
        "kaart": "Een frisse, zuivere huid in 30 of 40 minuten.",
        "vanaf": "€ 32,00",
        "duur": "30 – 40 min",
        "icon": "drop",
        "foto": "card-kort.jpg",
        "items": [
            ("Cucumber treatment", "Mooi, voor de jonge huid", "€ 32,00", "30 minuten", [
                "In deze korte behandeling wordt je huid goed gereinigd. Je wenkbrauwen worden geëpileerd en onzuiverheden en gerstekorrels worden verwijderd.",
                "Tot slot wordt een beschermende en verfrissende 24-uurs crème met komkommerextract aangebracht.",
            ]),
            ("Purifying treatment", "Zuiver, voor de onzuivere / acne huid", "€ 35,50", "40 minuten", [
                "In deze behandeling wordt gewerkt met tea tree producten en er wordt een intensieve peeling gedaan. Wenkbrauwen worden geëpileerd en onzuiverheden worden verwijderd.",
                "Een reinigend en herstellend kleimasker zorgt ervoor dat de huid er weer rustiger uitziet.",
            ]),
        ],
    },
    {
        "slug": "huidverzorgende-behandelingen",
        "header": "header-huidverzorging.jpg",
        "titel": "Huidverzorgende behandelingen",
        "kort": "Huidverzorgend",
        "hero": "Na een huidverzorgende behandeling zie je er weer <em>stralend</em> uit",
        "intro": "Kies uit drie heerlijke huidverzorgende behandelingen van 60 minuten, elk met een ontspannende massage en een masker.",
        "kaart": "Drie verzorgende behandelingen met massage en masker.",
        "vanaf": "€ 51,50",
        "duur": "60 min",
        "icon": "leaf",
        "foto": "card-huidverzorging.jpg",
        "items": [
            ("Aloë Vera treatment", "Hydraterend en herstellend", "€ 51,50", "60 minuten", [
                "Tijdens deze behandeling geniet je van een heerlijke reiniging en een fijne scrub. Je wenkbrauwen worden geëpileerd en onzuiverheden worden verwijderd.",
                "Er wordt gewerkt met producten die een hoge concentratie aloë vera bevatten. Aloë vera werkt sterk hydraterend en herstellend. Na een heerlijke ontspannende massage en een masker ziet je huid er weer stralend uit.",
            ]),
            ("Sensitive & Calming treatment", "Verzachtend en verzorgend", "€ 51,50", "60 minuten", [
                "Deze behandeling begint met een zachte oppervlakte- en dieptereiniging. Wenkbrauwen worden geëpileerd en onzuiverheden worden verwijderd.",
                "Er wordt gewerkt met producten die azuleen bevatten, de actieve werkstof uit kamilleolie. Die werkt verzachtend en ontstekingsremmend en maakt deze behandeling geschikt voor de gevoelige, zeer gevoelige en onzuivere huid. Het masker wordt afgestemd op de huidconditie en natuurlijk krijg je ook een heerlijke ontspannende massage.",
            ]),
            ("Royal Jelly treatment", "Activerend, verbetert de algehele conditie van de huid", "€ 51,50", "60 minuten", [
                "Er wordt gestart met een zachte reiniging gevolgd door een fijne scrub. Vervolgens worden wenkbrauwen geëpileerd en onzuiverheden verwijderd.",
                "De Royal Jelly serie is gebaseerd op natuurlijke gelei royale: de koninginnegelei die de bijenkoningin tot voedsel dient. Dit rijke werkstofcomplex zorgt voor een betere doorbloeding, verbeterde elasticiteit en een gladdere, strakkere huid. Na een ontspannende massage en een masker ziet de huid er gezond en fris uit.",
            ]),
        ],
    },
    {
        "slug": "huidverbeterende-en-ontspannende-behandelingen",
        "header": "header-huidverbetering.jpg",
        "titel": "Huidverbeterende & ontspannende behandelingen",
        "kort": "Huidverbeterend",
        "hero": "Geniet en ontspan van deze <em>heerlijke</em> behandelingen",
        "intro": "Twee uitgebreide behandelingen van 80 minuten die je huid zichtbaar verbeteren én je helemaal tot rust laten komen.",
        "kaart": "Uitgebreid verwennen én zichtbaar resultaat.",
        "vanaf": "€ 61,50",
        "duur": "80 min",
        "icon": "sparkle",
        "foto": "card-huidverbetering.jpg",
        "items": [
            ("Myoxinol anti-wrinkle treatment", "Vermindert rimpels & revitaliseert", "€ 61,50", "80 minuten", [
                "Je geniet van een goede reiniging en een fijne scrub. Nadat je wenkbrauwen zijn geëpileerd en onzuiverheden zijn verwijderd, volgt een heerlijke, ontspannende lomi lomi massage van gelaat, nek, schouders en armen. Een voedend masker wordt aangepast aan je huidtype.",
                "De belangrijkste werkstoffen zijn Myoxinol, hibiscus en verschillende vitaminen. Myoxinol bestrijdt rimpels op een vergelijkbare manier als botox, maar is plantaardig en onschadelijk. De huid wordt gladder en krijgt een jonge, frisse uitstraling.",
            ]),
            ("Caviar Gold treatment", "Hydraterend & herstructurerend", "€ 61,50", "80 minuten", [
                "Deze behandeling begint met een warm voetenbad en een nek- en schoudermassage, eventueel ook van de hoofdhuid. Daarna volgt de gezichtsbehandeling: een zachte reiniging, een heerlijke scrub, epileren van de wenkbrauwen en het verwijderen van onzuiverheden.",
                "Vervolgens geniet je van een ontspannende gelaatsmassage met de ‘precious gold honey’ massagecrème, gevolgd door een voedend masker. Als afsluiting wordt de caviar age defense cream aangebracht. Kaviaarextract, hyaluronzuur en plantaardige extracten activeren de vernieuwing van de huid; hyaluronzuur werkt bovendien sterk hydraterend.",
            ]),
        ],
    },
    {
        "slug": "aromatherapie",
        "header": "header-aroma.jpg",
        "titel": "Aromatherapie",
        "kort": "Aromatherapie",
        "hero": "Geniet van een <em>unieke</em> geurbeleving",
        "intro": "Twee aromatherapiebehandelingen voor het gezicht met de 100% natuurlijke producten van Chi. Geur, warmte en aanraking brengen lichaam en geest in balans.",
        "kaart": "Een bijzondere geurbeleving met warme stenen en Chi-oliën.",
        "vanaf": "€ 51,50",
        "duur": "60 / 85 min",
        "icon": "flower",
        "foto": "card-aroma.jpg",
        "items": [
            ("A touch of Roses, Lavender of Happiness", "Heerlijke geurbeleving en ontspanning", "€ 51,50", "60 minuten", [
                "In deze behandeling staan geurbeleving en ontspanning voorop. Er wordt gereinigd met een zachte olie, gevolgd door een dieptereiniging met honing. Een lange massage met onder andere zachte penselen en warme stenen zorgt voor ultieme ontspanning. Je sluit af met een verzorgend masker.",
                "Je kiest zelf je geur: rozen, lavendel of sinaasappel met mandarijn en vanille.",
            ]),
            ("Special Wellness", "Ontspanning van lichaam en geest, aangepast aan het seizoen", "€ 62,00", "85 minuten", [
                "Een cadeautje voor jezelf! Puur genieten en ontspannen, dat is wat deze behandeling je geeft. Elke twee tot drie maanden wordt de samenstelling aangepast met geuren die bij het seizoen passen.",
                "Er worden verschillende massages gegeven, bijvoorbeeld van rug, hoofdhuid of armen; de gezichtsmassage hoort er altijd bij. Soms is er een heerlijk voetenbad of wordt de rug gescrubd. Alle producten zijn van Chi en worden door Wendy zelf bereid: een basisolie gemengd met etherische oliën die elk een eigen positief effect hebben op lichaam en geest.",
            ]),
        ],
    },
]

GEUREN = [
    ("scent-rose", "rose", "A touch of Roses", "Rozenkwarts",
     "Liefde, zachtheid en een gevoel van harmonie en warmte. Kalmerend en regenererend, ook voor de zeer gevoelige huid. Laat je zorgen los."),
    ("scent-lavender", "lavender", "A touch of Lavender", "Amethist",
     "Zeer rustgevend: lichaam en geest komen in balans. Verzorgend en verzachtend, geschikt voor veel huidtypen, ook de vette huid. Heerlijk bij stress."),
    ("scent-happy", "citrus", "A touch of Happiness", "Oranje calciet",
     "Sinaasappel, mandarijn en vanille laten je de zonnige kant van het leven zien. Stimulerend, verwarmend en ontspannend. Geniet van het leven!"),
]

LOSSE_ONDERDELEN = ["Epileren / harsen wenkbrauwen", "Harsen bovenlip", "Harsen kin / kaakgebied", "Verven wimpers", "Verven wenkbrauwen"]
PRIJS_ONDERDELEN = [("Eén onderdeel", "€ 14,00"), ("Twee onderdelen", "€ 18,00"), ("Drie onderdelen", "€ 21,00"),
                    ("Vier onderdelen", "€ 26,00"), ("Vijf onderdelen", "€ 31,50")]
COMBI = [("Eerste onderdeel", "+ € 5,50"), ("Elk volgend onderdeel", "+ € 1,50")]
HARSEN = [("Onderbenen", "€ 29,50"), ("Hele benen (incl. liezen)", "€ 39,50"), ("Armen", "€ 21,50"),
          ("Oksels", "€ 19,50"), ("Armen en oksels", "€ 35,50")]
NAGELS = [("Gellak", "€ 26,50"), ("Verwijderen gellak", "€ 13,50")]

NAV = [
    ("/gezichtsbehandelingen/", "Gezicht"),
    ("/overige_behandelingen/", "Harsen & verven"),
    ("/henna-wenkbrauwen/", "Henna"),
    ("/nagels/", "Nagels"),
    ("/prijzen/", "Prijzen"),
    ("/kadobon/", "Kadobon"),
    ("/contact/", "Contact"),
]
# uitklapmenu onder "Gezicht" (wordt na GROEPEN gevuld)
NAV_SUB = {}

# ---------------------------------------------------------------- iconen
def svg(body: str, vb: str = "0 0 24 24", extra: str = "") -> str:
    return (f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{body}</svg>')

ICONS = {
    "phone": svg('<path d="M5 3.5h3.2l1.6 4.2-2 1.4a11 11 0 0 0 7.1 7.1l1.4-2 4.2 1.6V19a1.6 1.6 0 0 1-1.7 1.6A16.6 16.6 0 0 1 3.4 5.2 1.6 1.6 0 0 1 5 3.5Z"/>'),
    "mail": svg('<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="m3.5 7 8.5 6.2L20.5 7"/>'),
    "pin": svg('<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/>'),
    "clock": svg('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>'),
    "check": svg('<circle cx="12" cy="12" r="9"/><path d="m8 12.3 2.7 2.7L16 9.6"/>'),
    "heart": svg('<path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.5C19.5 15.4 12 20 12 20Z"/>'),
    "info": svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.8v.2"/>'),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "drop": svg('<path d="M12 3.2s6 6.6 6 11a6 6 0 0 1-12 0c0-4.4 6-11 6-11Z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.6 2.6"/>'),
    "leaf": svg('<path d="M5 19c0-8 5-13.5 14-14 .4 9-5 14.4-13 14"/><path d="M5 19c3-4 6-6.5 9.5-8.5"/>'),
    "sparkle": svg('<path d="M12 3.5c.6 4.2 2.3 5.9 6.5 6.5-4.2.6-5.9 2.3-6.5 6.5-.6-4.2-2.3-5.9-6.5-6.5 4.2-.6 5.9-2.3 6.5-6.5Z"/><path d="M18.5 15.5c.3 1.7 1 2.4 2.5 2.7-1.6.3-2.3 1-2.5 2.6-.3-1.6-1-2.3-2.6-2.6 1.6-.3 2.3-1 2.6-2.7Z"/>'),
    "flower": svg('<circle cx="12" cy="10" r="2"/><path d="M12 8c-1.5-3 0-5 0-5s1.5 2 0 5ZM14 10c3-1.5 5 0 5 0s-2 1.5-5 0ZM10 10c-3-1.5-5 0-5 0s2 1.5 5 0ZM12 12c1.6 2.7.6 4.6.6 4.6M12 12c-1.6 2.7-.6 4.6-.6 4.6"/><path d="M12 16.6V21M12 19c1.8-1.7 3.6-1.8 3.6-1.8M12 19.6c-1.8-1.7-3.6-1.8-3.6-1.8"/>'),
    "wax": svg('<path d="M7 20c-1.5-6 0-11 5-16 5 5 6.5 10 5 16Z"/><path d="M9.5 16.5c.2-2.6 1-4.6 2.5-6.5"/>'),
    "brow": svg('<path d="M3 13c3.5-4.5 10-6 18-3"/><path d="M3 13c4-2.6 10-3.4 18-3"/><path d="M7 17.5c1.6 1.2 3.4 1.8 5 1.8s3.4-.6 5-1.8"/><circle cx="12" cy="17" r="1.3"/>'),
    "nail": svg('<path d="M8 21v-9a4 4 0 0 1 8 0v9"/><path d="M9.5 12a2.5 2.5 0 0 1 5 0v3.5h-5Z"/><path d="M6 21h12"/>'),
    "gift": svg('<rect x="3.5" y="9" width="17" height="11.5" rx="1.5"/><path d="M3 9h18v-3H3ZM12 6v14.5M12 6S10.5 2.5 8 3.2C6 3.8 7 6 12 6ZM12 6s1.5-3.5 4-2.8C18 3.8 17 6 12 6Z"/>'),
    "back": svg('<path d="M5 20c1-6 3.5-9 7-9s6 3 7 9"/><path d="M12 11c-2.4 0-4-2-4-4.2a4 4 0 0 1 8 0C16 9 14.4 11 12 11Z"/><path d="M12 13.5V20"/>'),
    "rose": svg('<path d="M12 13c-3.3 0-5-2.2-5-5 2 .8 3.4.5 5-1.5 1.6 2 3 2.3 5 1.5 0 2.8-1.7 5-5 5Z"/><path d="M12 6.5c-.8-1.2-.6-2.6.3-3.5M9.5 9.2c1 .8 3.6.9 5-.4"/><path d="M12 13v8M12 17c-2-.3-3.6-1.5-4.2-3.2M12 18.5c1.8-.4 3.2-1.6 3.8-3"/>'),
    "lavender": svg('<path d="M12 21V8"/><path d="M12 9c-1.2-.4-1.6-1.6-1-2.6M12 9c1.2-.4 1.6-1.6 1-2.6M12 6.2c-1-.5-1.2-1.6-.5-2.4M12 6.2c1-.5 1.2-1.6.5-2.4M12 3.4V2.6M12 12c-1.3-.3-1.9-1.5-1.3-2.6M12 12c1.3-.3 1.9-1.5 1.3-2.6"/><path d="M12 17c-2.2-.5-3.8-2.2-4-4.5M12 18c2-.6 3.4-2 3.8-4"/>'),
    "citrus": svg('<circle cx="12" cy="13" r="7.5"/><circle cx="12" cy="13" r="5"/><path d="M12 8v10M7 13h10M8.5 9.5l7 7M15.5 9.5l-7 7"/><path d="M12 5.5c.5-2 2-3 4-3"/>'),
    "stone": svg('<path d="M4 15c0-4 3.5-8 8-8s8 3 8 7-3.5 5.5-8 5.5S4 18.5 4 15Z"/><path d="M8 12c1.2-1.6 3-2.3 5-2"/>'),
    "calendar": svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>'),
}

LOGO = svg(
    '<circle cx="24" cy="24" r="22.5" stroke-width="1"/>'
    '<path d="M24 37V20" stroke-width="1.2"/>'
    '<path d="M24 22c-2.6-4.8-1.8-9.2 0-12.4 1.8 3.2 2.6 7.6 0 12.4Z"/>'
    '<path d="M24 26c-4.6-.4-8.2-3.4-9.4-7.6 4.4-.6 8 1.6 9.4 7.6ZM24 26c4.6-.4 8.2-3.4 9.4-7.6-4.4-.6-8 1.6-9.4 7.6Z"/>'
    '<path d="M24 31.5c-3.8.6-7.2-1.2-8.8-4.4 3.6-1.2 7 .2 8.8 4.4ZM24 31.5c3.8.6 7.2-1.2 8.8-4.4-3.6-1.2-7 .2-8.8 4.4Z"/>',
    vb="0 0 48 48", extra=' class="logo-mark"')

BOTANICAL = (
    '<svg class="botanical" viewBox="0 0 400 500" fill="none" stroke="currentColor" stroke-width="1.2" '
    'stroke-linecap="round" aria-hidden="true" preserveAspectRatio="xMidYMax meet">'
    '<path d="M200 500C200 380 196 300 210 180"/>'
    '<path d="M200 430c-40-8-78-40-90-92 50 6 82 40 90 92Z"/>'
    '<path d="M202 380c42-10 74-46 80-96-46 10-74 44-80 96Z"/>'
    '<path d="M203 320c-34-10-60-40-64-82 40 8 62 38 64 82Z"/>'
    '<path d="M206 262c30-12 52-40 54-76-36 10-54 38-54 76Z"/>'
    '<path d="M208 210c-22-12-36-34-34-62 26 10 38 32 34 62Z"/>'
    '<path d="M210 180c4-22 14-38 30-48-2 22-12 38-30 48Z"/>'
    '<path d="M110 500c0-60 6-110 40-160"/>'
    '<path d="M126 430c-30-2-52-22-58-52 30 2 52 22 58 52ZM138 382c24-8 40-28 42-56-26 6-40 28-42 56Z"/>'
    '<path d="M300 500c4-50 0-100-28-150"/>'
    '<path d="M296 440c28-6 46-28 48-58-28 6-46 28-48 58ZM284 392c-24-6-40-26-42-52 24 4 40 24 42 52Z"/>'
    '<circle cx="240" cy="128" r="3"/><circle cx="174" cy="146" r="3"/><circle cx="150" cy="338" r="2.4"/>'
    '</svg>')

ROTATING = (
    '<svg class="spin" viewBox="0 0 120 120" aria-hidden="true" style="color:#e73b73">'
    '<defs><path id="c" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs>'
    '<text font-family="Roboto, sans-serif" font-weight="500" font-size="8" letter-spacing="2.2" fill="currentColor">'
    '<textPath href="#c">GEZICHT · LICHAAM · GEEST · OLDENZAAL ·</textPath></text>'
    '<path d="M60 48c-3 6-3 18 0 24 3-6 3-18 0-24Z" fill="none" stroke="currentColor" stroke-width="1"/></svg>')

e = html.escape

# ---------------------------------------------------------------- afbeeldingen
# naam op de site -> origineel (maximale resolutie) in archief/afbeeldingen
IMAGES = {
    "landschap": "landschap.jpg",
    "header-gezicht": "header-gezichtsbehandelingen.jpg",
    "header-kort": "header-gezichtsbehandeling.jpg",
    "header-huidverzorging": "zuiver-gezichtsbehandeling.jpg",
    "header-huidverbetering": "header-strand.jpg",
    "header-aroma": "lavendel-field.jpg",
    "header-benen": "header-benen-uit-auto.jpg",
    "header-kadobon": "kadobon-salon-wendy.jpg",
    "header-henna": "henna-eyebrow.jpg",
    "header-nagels": "nail-art.jpg",
    "henna-voor-na": "henna-wenkbrauwen-voor-na.jpg",
    "aroma-olie": "essential-oil-aroma.jpg",
    "card-gezicht": "gezicht-beauty.jpg",
    "card-benen": "card-benen.jpg",
    "card-henna": "henna-wenkbrauw.jpg",
    "card-kort": "gezichtsbehandeling_192984281-AS.jpeg",
    "card-huidverzorging": "huidverzorging_288276290-AS.jpeg",
    "card-huidverbetering": "huid_187904763.jpeg",
    "card-aroma": "bloemen-geuren-ruiken_15290929.jpeg",
}
ALT = {
    "landschap": "Lavendelveld bij zonsondergang: genieten van totale ontspanning en heerlijke aroma's",
    "header-gezicht": "Vrouw ontspant tijdens een gezichtsbehandeling in de schoonheidssalon",
    "header-kort": "Korte gezichtsbehandeling met reinigend masker",
    "header-huidverzorging": "Verzorgende gezichtsbehandeling voor een stralende huid",
    "header-huidverbetering": "Ontspannen en stralend na een huidverbeterende behandeling",
    "header-aroma": "Lavendelveld: aromatherapie met lavendel, rozen en citrus",
    "header-benen": "Gladde benen na harsen bij Wendy's Schoonheidssalon",
    "header-kadobon": "Feestelijk verpakte kadobon van Wendy's Schoonheidssalon",
    "header-henna": "Volle, strakke wenkbrauwen met henna",
    "header-nagels": "Mooie nagels met gellak",
    "henna-voor-na": "Wenkbrauwen voor en na de henna wenkbrauwen behandeling",
    "aroma-olie": "Aromatherapie met pure etherische olie en bloemen",
    "card-gezicht": "Ontspannende gezichtsmassage tijdens een gezichtsbehandeling in Oldenzaal",
    "card-benen": "Gladde benen na harsen",
    "card-henna": "Close-up van een mooi gevormde wenkbrauw",
    "card-kort": "Korte gezichtsbehandeling met masker",
    "card-huidverzorging": "Huidverzorgende gezichtsbehandeling met reiniging",
    "card-huidverbetering": "Huidverbeterende gezichtsbehandeling door de schoonheidsspecialiste",
    "card-aroma": "Vrouw geniet van de geur van bloemen tijdens aromatherapie",
}
BREEDTES = (480, 800, 1200, 1600, 1920, 2400)
SIZES = {}  # naam -> (breedte, hoogte, [breedtes])


def make_images() -> None:
    """Maakt WebP-varianten (tot en met de originele resolutie) + een JPG op volle grootte."""
    doel = OUT / "img"
    doel.mkdir(parents=True, exist_ok=True)
    for naam, bron in IMAGES.items():
        im = Image.open(ARCHIEF / bron).convert("RGB")
        w, h = im.size
        ws = sorted({b for b in BREEDTES if b < w} | {w})
        for b in ws:
            v = im if b == w else im.resize((b, round(h * b / w)), Image.LANCZOS)
            v.save(doel / f"{naam}-{b}.webp", "WEBP", quality=82, method=6)
        im.save(doel / f"{naam}.jpg", "JPEG", quality=88, progressive=True, optimize=True)
        SIZES[naam] = (w, h, ws)
    for svg in ("logo.svg", "logo-wit.svg"):
        shutil.copy(ROOT / "src" / "img" / svg, doel / svg)


def _sizes_attr(naam: str, cls: str) -> str:
    if "bg" in cls or naam in ("landschap",) or naam.startswith("header-") and "feature" not in cls:
        return "100vw"
    if naam.startswith("card-"):
        return "(max-width: 760px) 100vw, (max-width: 1200px) 45vw, 360px"
    return "(max-width: 860px) 100vw, 50vw"


def responsive(doc: str) -> str:
    """Zet elke <img src="/img/naam.jpg"> om naar een responsive WebP-afbeelding met srcset."""
    def sub(m):
        tag = m.group(0)
        naam = m.group(1)
        if naam not in SIZES:
            return tag
        w, h, ws = SIZES[naam]
        cls = (re.search(r'class="([^"]*)"', tag) or [None, ""])[1]
        srcset = ", ".join(f"/img/{naam}-{b}.webp {b}w" for b in ws)
        tag = tag.replace(f'src="/img/{naam}.jpg"', f'src="/img/{naam}-{ws[-1]}.webp" srcset="{srcset}" sizes="{_sizes_attr(naam, cls)}"')
        tag = re.sub(r'\s(width|height)="\d+"', "", tag)
        tag = tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
        if 'alt=""' in tag and "bg" not in cls:
            tag = tag.replace('alt=""', f'alt="{e(ALT.get(naam, ""))}"')
        if "decoding=" not in tag:
            tag = tag.replace("<img ", '<img decoding="async" ', 1)
        return tag
    return re.sub(r'<img[^>]*src="/img/([a-z0-9-]+)\.jpg"[^>]*>', sub, doc)


# ---------------------------------------------------------------- structured data / SEO
SALON_LD = {
    "@type": ["BeautySalon", "HealthAndBeautyBusiness"],
    "@id": "https://www.salonwendy.nl/#salon",
    "name": "Wendy's Schoonheidssalon",
    "alternateName": "Salon Wendy",
    "description": "Schoonheidssalon in Oldenzaal (Twente) voor verzorgende en ontspannende gezichtsbehandelingen, aromatherapie, rugbehandeling, harsen, verven, epileren, henna wenkbrauwen en gellak. Uitsluitend op afspraak.",
    "url": "https://www.salonwendy.nl/",
    "logo": "https://www.salonwendy.nl/img/logo.svg",
    "image": "https://www.salonwendy.nl/img/landschap.jpg",
    "telephone": "+31541538153",
    "email": "info@salonwendy.nl",
    "priceRange": "€14 - €62",
    "currenciesAccepted": "EUR",
    "address": {"@type": "PostalAddress", "streetAddress": "Uiverstraat 39", "postalCode": "7574 BA",
                "addressLocality": "Oldenzaal", "addressRegion": "Overijssel", "addressCountry": "NL"},
    "areaServed": [{"@type": "City", "name": n} for n in ("Oldenzaal", "Losser", "Denekamp", "Hengelo", "Enschede", "Dinkelland")],
    "founder": {"@type": "Person", "name": "Wendy Schwankhuizen-Luttikhuis", "jobTitle": "Schoonheidsspecialiste"},
    "knowsAbout": ["gezichtsbehandeling", "aromatherapie", "huidverzorging", "huidverbetering", "harsen", "epileren",
                   "wimpers verven", "wenkbrauwen verven", "henna wenkbrauwen", "gellak", "rugbehandeling"],
}


def euro(prijs: str) -> str:
    return re.sub(r"[^0-9,]", "", prijs).replace(",", ".")


def offer(naam: str, prijs: str, beschrijving: str = "", duur: str = "", url: str = "") -> dict:
    o = {"@type": "Offer", "price": euro(prijs), "priceCurrency": "EUR",
         "itemOffered": {"@type": "Service", "name": naam, "provider": {"@id": SALON_LD["@id"]}}}
    if beschrijving:
        o["itemOffered"]["description"] = beschrijving
    if duur:
        mins = re.search(r"\d+", duur)
        if mins:
            o["itemOffered"]["timeRequired"] = f"PT{mins.group(0)}M"
    if url:
        o["url"] = SITE + url
    return o


def catalog(naam: str, offers: list[dict]) -> dict:
    return {"@type": "OfferCatalog", "name": naam, "itemListElement": offers}


def faq_html(faq: list[tuple[str, str]], titel: str = "Veelgestelde vragen") -> str:
    if not faq:
        return ""
    items = "".join(f'<details class="faq-item"><summary>{e(q)}</summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in faq)
    return f"""
<section class="section section-tint faq">
  <div class="wrap narrow">
    <div class="section-head reveal" style="text-align:center"><span class="eyebrow">Goed om te weten</span><h2>{titel}</h2></div>
    <div class="faq-list reveal">{items}</div>
  </div>
</section>"""


def ld_script(path: str, title: str, desc: str, crumbs: list[tuple[str, str]], extra: list[dict], faq) -> str:
    graph = [SALON_LD,
             {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": SALON["naam"],
              "inLanguage": "nl-NL", "publisher": {"@id": SALON_LD["@id"]}},
             {"@type": "WebPage", "@id": SITE + path + "#webpage", "url": SITE + path, "name": title,
              "description": desc, "inLanguage": "nl-NL", "isPartOf": {"@id": SITE + "/#website"},
              "about": {"@id": SALON_LD["@id"]}, "dateModified": VANDAAG}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]})
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]})
    for x in extra:
        if x.get("@type") == "OfferCatalog":
            graph.append({"@type": "Service", "name": x["name"], "provider": {"@id": SALON_LD["@id"]},
                          "areaServed": "Oldenzaal", "hasOfferCatalog": x})
        else:
            graph.append(x)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'<script type="application/ld+json">\n{data}\n</script>\n'


LLM_PAGES = []  # (titel, pad, beschrijving) voor llms.txt
PAGE_IMAGES = {}  # pad -> afbeeldingsnamen (voor de image-sitemap)
PAGE_TITLES = {}

# "Combineer met": verwante pagina's per pagina (interne links)
KAART = {
    "/gezichtsbehandelingen/korte-behandelingen/": ("Korte behandelingen", "card-kort", "Frisse, zuivere huid in 30 of 40 minuten · vanaf € 32,00"),
    "/gezichtsbehandelingen/huidverzorgende-behandelingen/": ("Huidverzorgende behandelingen", "card-huidverzorging", "Met massage en masker · 60 min · € 51,50"),
    "/gezichtsbehandelingen/huidverbeterende-en-ontspannende-behandelingen/": ("Huidverbeterende behandelingen", "card-huidverbetering", "Zichtbaar resultaat · 80 min · € 61,50"),
    "/gezichtsbehandelingen/aromatherapie/": ("Aromatherapie", "card-aroma", "Geurbeleving met warme stenen · vanaf € 51,50"),
    "/overige_behandelingen/": ("Harsen, epileren & verven", "card-benen", "Benen, armen, oksels, wenkbrauwen en wimpers · vanaf € 14,00"),
    "/henna-wenkbrauwen/": ("Henna wenkbrauwen", "card-henna", "Tot 6 weken volle wenkbrauwen · € 24,00"),
    "/nagels/": ("Gellak nagels", "header-nagels", "Twee weken of langer mooie nagels · € 26,50"),
    "/kadobon/": ("Kadobon", "header-kadobon", "In elk gewenst bedrag, feestelijk verpakt"),
    "/prijzen/": ("Prijslijst", "aroma-olie", "Alle behandelingen en prijzen op één pagina"),
    "/gezichtsbehandelingen/": ("Gezichtsbehandelingen", "card-gezicht", "9 behandelingen + huidtype-wijzer"),
}
RELATED = {
    "/gezichtsbehandelingen/": ["/overige_behandelingen/", "/henna-wenkbrauwen/", "/prijzen/"],
    "/gezichtsbehandelingen/korte-behandelingen/": ["/gezichtsbehandelingen/huidverzorgende-behandelingen/", "/overige_behandelingen/", "/henna-wenkbrauwen/"],
    "/gezichtsbehandelingen/huidverzorgende-behandelingen/": ["/gezichtsbehandelingen/huidverbeterende-en-ontspannende-behandelingen/", "/gezichtsbehandelingen/aromatherapie/", "/overige_behandelingen/"],
    "/gezichtsbehandelingen/huidverbeterende-en-ontspannende-behandelingen/": ["/gezichtsbehandelingen/huidverzorgende-behandelingen/", "/gezichtsbehandelingen/aromatherapie/", "/henna-wenkbrauwen/"],
    "/gezichtsbehandelingen/aromatherapie/": ["/gezichtsbehandelingen/huidverbeterende-en-ontspannende-behandelingen/", "/kadobon/", "/nagels/"],
    "/overige_behandelingen/": ["/henna-wenkbrauwen/", "/gezichtsbehandelingen/korte-behandelingen/", "/nagels/"],
    "/henna-wenkbrauwen/": ["/overige_behandelingen/", "/gezichtsbehandelingen/", "/nagels/"],
    "/nagels/": ["/henna-wenkbrauwen/", "/gezichtsbehandelingen/korte-behandelingen/", "/kadobon/"],
    "/kadobon/": ["/gezichtsbehandelingen/aromatherapie/", "/prijzen/", "/nagels/"],
    "/prijzen/": ["/gezichtsbehandelingen/", "/kadobon/", "/henna-wenkbrauwen/"],
    "/contact/": ["/prijzen/", "/gezichtsbehandelingen/", "/kadobon/"],
}


def related_html(path: str) -> str:
    rel = RELATED.get(path)
    if not rel:
        return ""
    titel = "Ook interessant" if path in ("/prijzen/", "/contact/", "/kadobon/") else "Combineer met"
    cards = "".join(
        f'<a class="card reveal" href="{u}"><span class="card-photo"><img src="/img/{KAART[u][1]}.jpg" alt="" loading="lazy"></span>'
        f'<h3>{e(KAART[u][0])}</h3><p>{e(KAART[u][2])}</p><span class="link">Bekijk</span></a>' for u in rel)
    return f"""
<section class="section related">
  <div class="wrap">
    <div class="section-head reveal"><span class="eyebrow">{titel}</span><h2>Maak het <em>compleet</em></h2></div>
    <div class="cards related-cards">{cards}</div>
  </div>
</section>"""
CUR = ' aria-current="page"'

# ---------------------------------------------------------------- layout
def head(title: str, desc: str, path: str, og: str = "landschap") -> str:
    full = title if title.startswith("Wendy") else f"{title} | {SALON['naam']}"
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:locale" content="nl_NL">
<meta name="theme-color" content="#6d5a64">
<meta property="og:image" content="{SITE}/img/{og}.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM-samenvatting">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">
<script>document.documentElement.classList.add("js")</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA4_ID}');</script>
"""


def header(active: str) -> str:
    def li(href, label):
        cur = CUR if active == href else ""
        sub = NAV_SUB.get(href)
        if not sub:
            return f'<li><a class="navlink" href="{href}"{cur}>{label}</a></li>'
        subs = "".join(f'<li><a href="{h}"{CUR if active == h else ""}>{e(t)}</a></li>' for h, t in sub)
        return (f'<li class="has-sub"><a class="navlink" href="{href}"{cur}>{label}</a>'
                f'<ul class="subnav" aria-label="{label}">{subs}</ul></li>')
    items = "".join(li(h, l) for h, l in NAV)
    return f"""</head>
<body>
<a class="skip" href="#main">Naar de inhoud</a>
<div class="topbar"><div class="wrap">
  <span>{SALON['straat']}, {SALON['plaats']} · Uitsluitend op afspraak</span>
  <a href="tel:{SALON['tel_link']}">Bel voor een afspraak: <strong>{SALON['tel']}</strong></a>
</div></div>
<header class="header" id="top">
  <div class="wrap">
    <a class="logo" href="/" aria-label="{e(SALON['naam'])}, naar de homepage">
      <img src="/img/logo.svg" alt="Wendy's Schoonheidssalon" width="204" height="52">
    </a>
    <button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">
      <ul>{items}</ul>
      <a class="btn btn-primary" href="tel:{SALON['tel_link']}">{ICONS['phone']} Afspraak maken</a>
    </nav>
  </div>
</header>
<main id="main">
"""


def cta_band() -> str:
    return f"""
<section class="section section-plum cta-band">
  <img class="bg" src="/img/landschap.jpg" alt="" loading="lazy">
  <div class="wrap reveal">
    <span class="eyebrow">Tijd voor jezelf</span>
    <h2>Gun jezelf een moment van <em>pure aandacht</em></h2>
    <p>Er wordt uitsluitend op afspraak gewerkt, zodat de tijd helemaal voor jou is. Bel gerust om een afspraak te maken of voor advies over de behandeling die bij jou past.</p>
    <div class="btns">
      <a class="btn btn-light" href="tel:{SALON['tel_link']}">{ICONS['phone']} {SALON['tel']}</a>
      <a class="btn btn-light" href="mailto:{SALON['mail']}">{ICONS['mail']} {SALON['mail']}</a>
    </div>
    <p style="margin:1.6rem 0 0"><a href="/contact/" style="color:#fff">Route &amp; contactgegevens</a> · <a href="/prijzen/" style="color:#fff">Bekijk alle prijzen</a></p>
  </div>
</section>"""


def footer() -> str:
    return f"""
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/"><img src="/img/logo-wit.svg" alt="Wendy's Schoonheidssalon" width="228" height="58" loading="lazy"></a>
        <p style="margin-top:1.4rem;max-width:22em">Verzorgende en ontspannende behandelingen voor gezicht en lichaam, in alle rust in Oldenzaal.</p>
      </div>
      <div>
        <h4>Behandelingen</h4>
        <ul>
          <li><a href="/gezichtsbehandelingen/">Gezichtsbehandelingen</a></li>
          <li><a href="/gezichtsbehandelingen/korte-behandelingen/">Korte behandelingen</a></li>
          <li><a href="/gezichtsbehandelingen/huidverzorgende-behandelingen/">Huidverzorgende behandelingen</a></li>
          <li><a href="/gezichtsbehandelingen/huidverbeterende-en-ontspannende-behandelingen/">Huidverbeterende behandelingen</a></li>
          <li><a href="/gezichtsbehandelingen/aromatherapie/">Aromatherapie</a></li>
          <li><a href="/overige_behandelingen/">Harsen, verven &amp; epileren</a></li>
          <li><a href="/henna-wenkbrauwen/">Henna wenkbrauwen</a></li>
          <li><a href="/nagels/">Gellak nagels</a></li>
        </ul>
      </div>
      <div>
        <h4>Salon</h4>
        <ul>
          <li><a href="/prijzen/">Prijslijst</a></li>
          <li><a href="/kadobon/">Kadobon</a></li>
          <li><a href="/contact/">Contact &amp; afspraak</a></li>
          <li><a href="/privacy/">Privacyverklaring</a></li>
          <li><a href="/sitemap/">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>{SALON['straat']}<br>{SALON['postcode']} {SALON['plaats']}</li>
          <li><a href="tel:{SALON['tel_link']}">{SALON['tel']}</a></li>
          <li><a href="mailto:{SALON['mail']}">{SALON['mail']}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> {e(SALON['naam'])}</span>
      <span>Uitsluitend op afspraak · Met liefde verzorgd in Oldenzaal</span>
    </div>
  </div>
</footer>
<a class="fab" href="tel:{SALON['tel_link']}" aria-label="Bel {SALON['tel']}">{ICONS['phone']}</a>
<script src="/site.js" defer></script>
</body>
</html>
"""


def page(path: str, title: str, desc: str, body: str, active: str = "", extra_head: str = "",
         crumbs=None, ld=None, faq=None, og: str = "landschap", llm: bool = True) -> None:
    crumbs = crumbs if crumbs is not None else [("Home", "/")]
    full = title if title.startswith("Wendy") else f"{title} | {SALON['naam']}"
    hdr = header(active or path)
    if active and active != path:  # subpagina: markeer ook het item in het uitklapmenu
        hdr = hdr.replace(f'<a href="{path}">', f'<a href="{path}"{CUR}>')
    doc = (head(title, desc, path, og) + extra_head + ld_script(path, full, desc, crumbs, ld or [], faq)
           + hdr + body + related_html(path) + faq_html(faq or []) + cta_band() + footer())
    target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = responsive(doc)
    target.write_text(doc, encoding="utf-8")
    PAGE_IMAGES[path] = list(dict.fromkeys(re.findall(r'src="/img/([a-z0-9-]+?)-\d+\.webp"', doc)))
    PAGE_TITLES[path] = title
    if llm:
        LLM_PAGES.append((title, path, desc))


def page_hero(eyebrow: str, h1: str, lead: str, crumbs: list[tuple[str, str]], after: str = "", photo: str = "") -> str:
    bg = f'<img class="bg" src="/img/{photo}" alt="" fetchpriority="high">' if photo else ""
    cls = "page-hero has-photo" if photo else "page-hero"
    cr = "".join(f'<a href="{h}">{t}</a><span>/</span>' for h, t in crumbs[:-1]) + f"{crumbs[-1][1]}"
    return f"""
<section class="{cls}">
  {bg}
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad">{cr}</nav>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    {after}
  </div>
</section>"""


def treatment_card(i: int, groep: dict, item: tuple) -> str:
    naam, sub, prijs, duur, tekst = item
    paras = "".join(f"<p>{e(t)}</p>" for t in tekst)
    return f"""
<article class="treatment reveal">
  <div class="treatment-body">
    <span class="treatment-tag">{e(groep['kort'])} · {i:02d}</span>
    <h3>{e(naam)}</h3>
    <p class="sub">{e(sub)}</p>
    {paras}
  </div>
  <div class="treatment-price">
    <span class="amount">{prijs}</span>
    <span class="dur">{ICONS['clock']} {duur}</span>
    <a class="btn btn-primary" href="tel:{SALON['tel_link']}">Reserveren</a>
  </div>
</article>"""


def group_block(groep: dict, heading_tag: str = "h2", link: bool = True) -> str:
    cards = "".join(treatment_card(i + 1, groep, it) for i, it in enumerate(groep["items"]))
    titel = groep["titel"]
    if link:
        titel = f'<a href="/gezichtsbehandelingen/{groep["slug"]}/" style="text-decoration:none">{e(titel)}</a>'
    else:
        titel = e(titel)
    extra = scents_html() if groep["slug"] == "aromatherapie" else ""
    return f"""
<div class="group" id="{groep['slug']}">
  <div class="group-head reveal">
    <{heading_tag}>{titel}</{heading_tag}>
    <p>{e(groep['intro'])}</p>
  </div>
  <div class="treatments">{cards}</div>
  {extra}
</div>"""


def scents_html(style: str = ' style="margin-top:22px"') -> str:
    return f'<div class="aroma"{style}>' + "".join(
        f"""<div class="scent {cls} reveal">{ICONS[ic]}<h3>{e(t)}</h3><span class="stone">Edelsteen: {e(st)}</span><p>{e(txt)}</p></div>"""
        for cls, ic, t, st, txt in GEUREN) + "</div>"


CALLOUT = f"""<div class="callout reveal">{ICONS['info']}<p>Tijdens alle gezichtsbehandelingen worden de wenkbrauwen geëpileerd of geharst en worden onzuiverheden verwijderd. Wil je ook je wimpers of wenkbrauwen laten verven, of je bovenlip en/of kin laten harsen? Geef dit dan even door bij het maken van je afspraak, zodat de extra tijd gereserveerd kan worden.</p></div>"""


def pricelist(rows) -> str:
    return '<ul class="pricelist">' + "".join(
        f'<li><span>{e(a)}</span><span class="dots"></span><span class="p">{b}</span></li>' for a, b in rows) + "</ul>"



# ---------------------------------------------------------------- veelgestelde vragen (gebaseerd op bestaande info)
TEL_A = f'<a href="tel:{SALON["tel_link"]}">{SALON["tel"]}</a>'
NAV_SUB["/gezichtsbehandelingen/"] = [("/gezichtsbehandelingen/", "Alle gezichtsbehandelingen")] + [
    (f"/gezichtsbehandelingen/{g['slug']}/", g["titel"].replace(" & ontspannende", "")) for g in GROEPEN]

FAQ_ALGEMEEN = [
    ("Hoe maak ik een afspraak bij Wendy's Schoonheidssalon?",
     f"Afspraken maak je telefonisch via {TEL_A}. Er wordt uitsluitend op afspraak gewerkt, zodat de tijd speciaal voor jou gereserveerd is. Voor algemene vragen kun je ook mailen naar <a href=\"mailto:info@salonwendy.nl\">info@salonwendy.nl</a>."),
    ("Waar zit de salon?",
     "Wendy's Schoonheidssalon zit aan de Uiverstraat 39, 7574 BA Oldenzaal, in Twente. De salon is goed bereikbaar vanuit onder andere Losser, Denekamp, Hengelo en Enschede."),
    ("Welke behandelingen kan ik boeken?",
     "Je kunt kiezen uit 9 gezichtsbehandelingen (kort, huidverzorgend, huidverbeterend en aromatherapie), een uitgebreide rugbehandeling, harsen van benen, armen en oksels, epileren en verven van wenkbrauwen en wimpers, henna wenkbrauwen en gellak voor de nagels."),
    ("Wat kost een gezichtsbehandeling?",
     "Een korte gezichtsbehandeling begint bij € 32,00 (30 minuten). Huidverzorgende behandelingen en de aromatherapie A touch of… kosten € 51,50 (60 minuten), de huidverbeterende behandelingen € 61,50 (80 minuten) en de Special Wellness € 62,00 (85 minuten)."),
    ("Wat als ik verhinderd ben?",
     "Zeg je afspraak dan tijdig af. Niet nagekomen afspraken worden in rekening gebracht."),
    ("Kan ik een kadobon kopen?",
     f"Ja, een kadobon is verkrijgbaar in elk gewenst bedrag. Bel {TEL_A}, dan wordt de kadobon feestelijk voor je verpakt."),
]
FAQ_GEZICHT = [
    ("Welke gezichtsbehandeling past bij mijn huid?",
     "Voor de jonge huid is de Cucumber treatment ideaal; voor de onzuivere of acne-huid de Purifying treatment. Een droge of vochtarme huid geniet van de Aloë Vera of Caviar Gold treatment, een gevoelige huid van de Sensitive &amp; Calming treatment of A touch of Roses. Voor de rijpere huid en rimpels zijn de Myoxinol anti-wrinkle en Royal Jelly treatment geschikt. Twijfel je? Wendy adviseert je graag."),
    ("Wat zit er standaard in elke gezichtsbehandeling?",
     "Tijdens alle gezichtsbehandelingen worden de wenkbrauwen geëpileerd of geharst en worden onzuiverheden verwijderd."),
    ("Kan ik wimpers verven of bovenlip harsen combineren met een gezichtsbehandeling?",
     "Ja. Geef het even door bij het maken van de afspraak, zodat er extra tijd gereserveerd wordt. In combinatie met een gezichtsbehandeling kost het eerste losse onderdeel € 5,50 extra en elk volgend onderdeel € 1,50."),
    ("Met welke producten wordt gewerkt?",
     "Er wordt gewerkt met de producten van Webecos, aangevuld met pure aromatherapie. Bij de aromatherapiebehandelingen worden de 100% natuurlijke producten van Chi gebruikt."),
    ("Hoe lang duurt een gezichtsbehandeling?",
     "Van 30 minuten (Cucumber treatment) tot 85 minuten (Special Wellness). De huidverzorgende behandelingen duren 60 minuten, de huidverbeterende behandelingen 80 minuten."),
]
FAQ_AROMA = [
    ("Wat is het verschil tussen de drie geuren?",
     "A touch of Roses werkt kalmerend en is ook geschikt voor de zeer gevoelige huid. A touch of Lavender is zeer rustgevend en geschikt voor veel huidtypen, ook de vette huid. A touch of Happiness (sinaasappel, mandarijn en vanille) werkt stimulerend, verwarmend en ontspannend en is geschikt voor alle huidtypen."),
    ("Wat is de Special Wellness?",
     "Een behandeling van 85 minuten (€ 62,00) die elke 2 tot 3 maanden wordt aangepast aan het seizoen. Naast de gezichtsmassage krijg je bijvoorbeeld een massage van rug, hoofdhuid of armen, soms een voetenbad of rugscrub."),
    ("Worden er edelstenen gebruikt?",
     "Ja. Tijdens de massage worden bij Roses rozenkwarts, bij Lavender amethist en bij Happiness oranje calciet gebruikt."),
]
FAQ_HARSEN = [
    ("Wat kost harsen van de benen?",
     "Onderbenen harsen kost € 29,50 en hele benen (inclusief liezen) € 39,50."),
    ("Hoe werken de prijzen van de losse onderdelen?",
     "Voor epileren of harsen van de wenkbrauwen, harsen van bovenlip of kin en verven van wimpers of wenkbrauwen betaal je € 14,00 voor één onderdeel, oplopend tot € 31,50 voor vijf onderdelen."),
]
FAQ_HENNA = [
    ("Hoe lang blijven henna wenkbrauwen mooi?",
     "Gemiddeld blijft de henna 5 tot 6 weken op de haartjes zitten en tot wel 2 weken op de huid."),
    ("Wat is het verschil tussen henna en gewoon verven?",
     "Bij henna worden niet alleen de haartjes maar ook de huid gekleurd. Daardoor lijken de wenkbrauwen voller."),
    ("Is henna natuurlijk?",
     "Ja. Henna is afkomstig van een struik: plantaardig en een zuiver natuurproduct. De henna komt uit Brazilië."),
]
FAQ_NAGELS = [
    ("Hoe lang blijft gellak mooi?",
     "Twee weken, soms ook langer. Dat hangt af van hoe snel je nagels groeien en van je werk en hobby's."),
    ("Is gellak hetzelfde als shellac?",
     "Gellak wordt ook wel gel-nagellak of shellac genoemd. Het is een tussenweg tussen gewone nagellak en gelnagels."),
    ("Wat kost gellak?",
     "Gellak kost € 26,50. Het verwijderen van gellak kost € 13,50."),
]
FAQ_KADOBON = [
    ("Voor welk bedrag kan ik een kadobon kopen?",
     "De kadobon is verkrijgbaar in elk gewenst bedrag."),
    ("Hoe bestel ik een kadobon?",
     f"Bel {TEL_A}. De kadobon wordt dan feestelijk voor je verpakt."),
]

# huidtype-wijzer op basis van de behandelbeschrijvingen
HUIDWIJZER = [
    ("Jonge huid", "Cucumber treatment", "korte-behandelingen", "€ 32,00 · 30 min"),
    ("Onzuivere of acne huid", "Purifying treatment", "korte-behandelingen", "€ 35,50 · 40 min"),
    ("Droge of vochtarme huid", "Aloë Vera of Caviar Gold treatment", "huidverzorgende-behandelingen", "vanaf € 51,50"),
    ("Gevoelige huid", "Sensitive &amp; Calming treatment", "huidverzorgende-behandelingen", "€ 51,50 · 60 min"),
    ("Rijpere huid en rimpels", "Myoxinol anti-wrinkle treatment", "huidverbeterende-en-ontspannende-behandelingen", "€ 61,50 · 80 min"),
    ("Toe aan totale ontspanning", "Aromatherapie of Special Wellness", "aromatherapie", "vanaf € 51,50"),
]

# ---------------------------------------------------------------- pagina's
def group_offers(g: dict) -> list[dict]:
    return [offer(n, pr, f"{sub}. " + " ".join(t), du, f"/gezichtsbehandelingen/{g['slug']}/") for n, sub, pr, du, t in g["items"]]


def build_home() -> None:
    cards = []
    for g in GROEPEN:
        cards.append(f"""
<a class="card reveal" href="/gezichtsbehandelingen/{g['slug']}/">
  <span class="card-photo"><img src="/img/{g['foto']}" alt="" loading="lazy" width="800" height="533"></span>
  <h3>{e(g['titel'].replace(' & ontspannende', ''))}</h3>
  <p>{e(g['kaart'])}</p>
  <div class="card-meta"><span>{g['duur']}</span><span>vanaf <b>{g['vanaf']}</b></span></div>
</a>""")
    extra_cards = [
        ("/overige_behandelingen/", "card-benen.jpg", "Harsen &amp; epileren", "Benen, armen en oksels harsen; wenkbrauwen epileren en wimpers verven.", "losse onderdelen", "€ 14,00"),
        ("/henna-wenkbrauwen/", "card-henna.jpg", "Henna wenkbrauwen", "Tot wel 6 weken volle, strakke wenkbrauwen met natuurlijke henna.", "20 min", HENNA_PRIJS),
        ("/nagels/", "header-nagels.jpg", "Gellak nagels", "Twee weken (of langer) prachtige, stevige nagels voor elk moment.", "gellak", "€ 26,50"),
    ]
    for href, ic, t, p, l, pr in extra_cards:
        cards.append(f"""
<a class="card reveal" href="{href}">
  <span class="card-photo"><img src="/img/{ic}" alt="" loading="lazy"></span>
  <h3>{t}</h3>
  <p>{p}</p>
  <div class="card-meta"><span>{l}</span><span>vanaf <b>{pr}</b></span></div>
</a>""")
    cards.append(f"""
<a class="card reveal" href="/kadobon/" style="background:var(--plum);color:#fff;border-color:var(--plum)">
  <span class="card-photo"><img src="/img/header-kadobon.jpg" alt="" loading="lazy"></span>
  <h3 style="color:#fff">Kadobon</h3>
  <p style="color:rgba(255,255,255,.8)">Verras iemand die je liefhebt met een moment van ontspanning, in elk gewenst bedrag.</p>
  <div class="card-meta" style="border-color:rgba(255,255,255,.2);color:rgba(255,255,255,.75)"><span>feestelijk verpakt</span><span class="link" style="color:#ffb3cc">Bekijk</span></div>
</a>""")

    body = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="reveal">
      <span class="eyebrow">Schoonheidssalon in Oldenzaal</span>
      <h1><span class="script">Gezicht, lichaam en geest</span><span class="line">Tijd om <em>helemaal</em> tot rust te komen</span></h1>
      <p class="lead">Geniet van verzorgende gezichtsbehandelingen, heerlijke aroma's en een massage waarbij je alles even loslaat. Bij Wendy's Schoonheidssalon word je volledig in de watten gelegd.</p>
      <div class="btns">
        <a class="btn btn-primary" href="tel:{SALON['tel_link']}">{ICONS['phone']} Bel voor een afspraak</a>
        <a class="btn btn-ghost" href="/gezichtsbehandelingen/">Bekijk behandelingen</a>
      </div>
      <ul class="hero-facts">
        <li>{ICONS['check']} Uitsluitend op afspraak</li>
        <li>{ICONS['check']} Webecos &amp; pure aromatherapie</li>
        <li>{ICONS['check']} Behandelingen 30 tot 85 min</li>
      </ul>
    </div>
    <div class="hero-visual reveal">
      <div class="arch"><img src="/img/card-gezicht.jpg" alt="Ontspannende gezichtsbehandeling met massage" width="800" height="533"></div>
      {ROTATING}
      <div class="badge">{ICONS['flower']}<div><strong>Aromatherapie</strong><small>Rozen, lavendel of een vleugje happiness</small></div></div>
    </div>
  </div>
</section>

<section class="band">
  <img src="/img/landschap.jpg" alt="Lavendelveld bij zonsondergang" width="1600" height="450" loading="lazy">
  <div class="wrap reveal">
    <span class="eyebrow" style="color:#ffb3cc">Aromatherapie</span>
    <h2>Geniet van totale ontspanning en heerlijke aroma's</h2>
    <p>Kies uit maar liefst 9 behandelingen voor de verzorging van je huid, voor huidverbetering of voor pure ontspanning.</p>
    <a class="btn btn-primary" href="/gezichtsbehandelingen/">Bekijk de behandelingen</a>
  </div>
</section>

<section class="section section-tint">
  <div class="wrap welcome">
    <div class="reveal"><div class="welcome-photo"><img src="/img/aroma-olie.jpg" alt="Aromatherapie met pure etherische olie" width="1500" height="1000" loading="lazy"></div>
    <blockquote class="welcome-quote">Met de producten van Webecos, aangevuld met pure aromatherapie, geniet je optimaal en halen we het beste in je naar boven.<cite>Wendy</cite></blockquote></div>
    <div class="reveal">
      <span class="eyebrow">Welkom</span>
      <h2>Welkom bij <em>Wendy's</em> Schoonheidssalon</h2>
      <p>Bij Wendy's Schoonheidssalon in Oldenzaal geniet je van verzorgende en ontspannende gezichtsbehandelingen. Of kom heerlijk relaxen tijdens een uitgebreide rugbehandeling. Epileren en harsen van gelaat, armen of benen behoren natuurlijk ook tot de mogelijkheden.</p>
      <p>Kies voor huidverzorging, huidverbetering of een aromatherapiebehandeling om helemaal tot rust te komen: van een korte behandeling van 30 minuten tot een lange verwenbehandeling van 85 minuten.</p>
      <div class="welcome-sig">
        <div><b>9</b><span>gezichtsbehandelingen</span></div>
        <div><b>85</b><span>minuten puur genieten</span></div>
        <div><b>100%</b><span>tijd voor jou</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><span class="eyebrow">Behandelingen</span><h2>Kies wat <em>jij</em> nodig hebt</h2></div>
      <p>Van een frisse, zuivere huid tot een complete verwenbehandeling voor lichaam en geest: er is altijd een behandeling die bij je past.</p>
    </div>
    <div class="cards">{''.join(cards)}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="wrap">
    <div class="section-head center reveal" style="text-align:center">
      <span class="eyebrow">Aromatherapie</span>
      <h2>Welke geur kies <em>jij</em> vandaag?</h2>
      <p class="lead narrow center">Elke geur heeft zijn eigen werking. Tijdens de massage worden bijpassende edelstenen gebruikt.</p>
    </div>
    {scents_html("")}
    <p class="center" style="text-align:center;margin-top:40px"><a class="link" href="/gezichtsbehandelingen/aromatherapie/">Ontdek de aromatherapiebehandelingen</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="gift reveal">
      <div>
        <span class="eyebrow">Kadobon</span>
        <h2>Verras iemand met een <em>moment voor zichzelf</em></h2>
        <p>Een kadobon van Wendy's Schoonheidssalon is verkrijgbaar in elk gewenst bedrag. Bel even, dan wordt de bon feestelijk voor je verpakt.</p>
        <div class="btns" style="margin-top:1.8rem"><a class="btn btn-primary" href="/kadobon/">Meer over de kadobon</a></div>
      </div>
      <div class="gift-art">{ICONS['gift'].replace('stroke-width="1.4"', 'stroke-width=".7"')}</div>
    </div>
  </div>
</section>

<section class="section section-tint">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><span class="eyebrow">Zo werkt het</span><h2>In drie stappen <em>ontspannen</em></h2></div>
      <p>Persoonlijk, rustig en met alle aandacht voor jou.</p>
    </div>
    <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
      <div class="card reveal"><span class="card-icon">{ICONS['phone']}</span><h3>Bel voor een afspraak</h3><p>Afspraken maak je telefonisch via {SALON['tel']}. Twijfel je welke behandeling bij je past? Wendy adviseert je graag.</p></div>
      <div class="card reveal"><span class="card-icon">{ICONS['calendar']}</span><h3>Jouw tijd, gereserveerd</h3><p>Er wordt uitsluitend op afspraak gewerkt. Je tijd wordt speciaal voor jou vrijgehouden: geen haast, geen wachtrij.</p></div>
      <div class="card reveal"><span class="card-icon">{ICONS['heart']}</span><h3>Genieten</h3><p>Laat je verwennen met zachte producten, warme handen en heerlijke geuren, en ga stralend weer naar huis.</p></div>
    </div>
  </div>
</section>
"""
    page("/", f"{SALON['naam']} in Oldenzaal | Gezichtsbehandelingen & aromatherapie",
         "Schoonheidssalon in Oldenzaal: ontspannende gezichtsbehandelingen, aromatherapie, harsen, henna wenkbrauwen en gellak. Bel 0541 538 153 voor een afspraak.",
         body, active="/", crumbs=[("Home", "/")], faq=FAQ_ALGEMEEN,
         ld=[catalog("Gezichtsbehandelingen", [o for g in GROEPEN for o in group_offers(g)])])


def build_gezicht() -> None:
    pills = '<div class="pills">' + "".join(
        f'<a href="#{g["slug"]}">{e(g["kort"])}</a>' for g in GROEPEN) + "</div>"
    body = page_hero("Gezichtsbehandelingen", "Stralend <em>de dag</em> door",
                     "Kies de gezichtsbehandeling die het beste bij jou past: van een korte frisse behandeling tot een uitgebreid moment voor lichaam en geest.",
                     [("/", "Home"), ("", "Gezichtsbehandelingen")], pills, photo="header-gezicht.jpg")
    gids = "".join(f'<a class="skin reveal" href="/gezichtsbehandelingen/{sl}/"><span class="skin-type">{t}</span><strong>{b}</strong><span class="skin-meta">{m}</span></a>'
                   for t, b, sl, m in HUIDWIJZER)
    body += f"""
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <div class="section-head split reveal"><div><span class="eyebrow">Huidtype-wijzer</span><h2>Welke behandeling past bij <em>jouw huid</em>?</h2></div>
    <p>Kies je huidtype of wens en ontdek welke gezichtsbehandeling het beste bij je past. Twijfel je? Wendy adviseert je graag.</p></div>
    <div class="skins">{gids}</div>
  </div>
</section>"""
    body += f'<section class="section"><div class="wrap">{CALLOUT}' + \
            "".join(group_block(g) for g in GROEPEN) + "</div></section>"
    page("/gezichtsbehandelingen/", "Gezichtsbehandelingen in Oldenzaal",
         "9 gezichtsbehandelingen in Oldenzaal: kort, huidverzorgend, huidverbeterend en aromatherapie, van € 32,00 tot € 62,00. Vind de behandeling voor jouw huid.",
         body, crumbs=[("Home", "/"), ("Gezichtsbehandelingen", "/gezichtsbehandelingen/")], faq=FAQ_GEZICHT,
         og="header-gezicht", ld=[catalog("Gezichtsbehandelingen", [o for g in GROEPEN for o in group_offers(g)])])

    for g in GROEPEN:
        pills = '<div class="pills">' + "".join(
            f'<a href="/gezichtsbehandelingen/{o["slug"]}/"{CUR if o is g else ""}>{e(o["kort"])}</a>'
            for o in GROEPEN) + "</div>"
        body = page_hero("Gezichtsbehandelingen", g["hero"], g["intro"],
                         [("/", "Home"), ("/gezichtsbehandelingen/", "Gezichtsbehandelingen"), ("", g["titel"])], pills, photo=g["header"])
        block = group_block(g, link=False).replace('<div class="group-head reveal">', '<div class="group-head reveal" hidden>', 1)
        body += f'<section class="section" style="padding-top:20px"><div class="wrap">{CALLOUT}{block}</div></section>'
        prijzen = sorted({it[2] for it in g["items"]}, key=lambda x: float(euro(x)))
        kort_titel = g["titel"].replace(" & ontspannende", "")
        desc = f"{kort_titel} in Oldenzaal: " + " en ".join(it[0] for it in g["items"]) + f". Vanaf {prijzen[0]}."
        if len(desc) < 125:
            desc += " Bel 0541 538 153 voor een afspraak."
        page(f"/gezichtsbehandelingen/{g['slug']}/", f"{kort_titel} in Oldenzaal", desc, body,
             active="/gezichtsbehandelingen/", og=g["header"].replace(".jpg", ""),
             crumbs=[("Home", "/"), ("Gezichtsbehandelingen", "/gezichtsbehandelingen/"), (g["titel"], f"/gezichtsbehandelingen/{g['slug']}/")],
             faq=FAQ_AROMA if g["slug"] == "aromatherapie" else FAQ_GEZICHT[:2],
             ld=[catalog(g["titel"], group_offers(g))])


def build_overig() -> None:
    body = page_hero("Harsen · verven · epileren", "De <em>finishing touch</em>",
                     "Strak gevormde wenkbrauwen, sprekende wimpers en zijdezachte benen. Los te boeken of als aanvulling op je gezichtsbehandeling.",
                     [("/", "Home"), ("", "Harsen, verven & epileren")], photo="header-benen.jpg")
    chips = "".join(f"<li>{e(x)}</li>" for x in LOSSE_ONDERDELEN)
    body += f"""
<section class="section" style="padding-top:20px">
  <div class="wrap">
    <div class="pricegrid">
      <div class="pricebox reveal">
        <span class="treatment-tag">Gezicht</span>
        <h3>Losse onderdelen</h3>
        <p>Combineer zoveel onderdelen als je wilt:</p>
        <ul class="chips">{chips}</ul>
        {pricelist(PRIJS_ONDERDELEN)}
      </div>
      <div style="display:grid;gap:22px">
        <div class="pricebox reveal">
          <span class="treatment-tag">Lichaam</span>
          <h3>Harsen</h3>
          <p>Gladde huid voor weken.</p>
          {pricelist(HARSEN)}
        </div>
        <div class="pricebox reveal">
          <span class="treatment-tag">In combinatie</span>
          <h3>Bij een gezichtsbehandeling</h3>
          <p>Voeg een of meer losse onderdelen toe aan je gezichtsbehandeling.</p>
          {pricelist(COMBI)}
        </div>
      </div>
    </div>
    <a class="card reveal" href="/henna-wenkbrauwen/" style="margin-top:22px;flex-direction:row;align-items:center;gap:24px;flex-wrap:wrap">
      <span style="width:110px;height:74px;border-radius:8px;overflow:hidden;flex:none"><img src="/img/card-henna.jpg" alt="" loading="lazy" style="width:100%;height:100%;object-fit:cover"></span>
      <div style="flex:1;min-width:220px"><h3 style="margin:0">Henna wenkbrauwen</h3><p style="margin:0">Tot wel 6 weken volle en strakke wenkbrauwen · {HENNA_PRIJS} · 20 min.</p></div>
      <span class="link">Bekijk</span>
    </a>
  </div>
</section>"""
    page("/overige_behandelingen/", "Harsen, epileren & verven in Oldenzaal",
         "Harsen van benen, armen en oksels, epileren en verven van wenkbrauwen en wimpers in Oldenzaal. Losse onderdelen vanaf € 14,00, onderbenen harsen € 29,50.",
         body, og="header-benen", faq=FAQ_HARSEN,
         crumbs=[("Home", "/"), ("Harsen, epileren & verven", "/overige_behandelingen/")],
         ld=[catalog("Harsen, epileren en verven", [offer(f"Losse onderdelen gezicht: {a.lower()}", b) for a, b in PRIJS_ONDERDELEN]
                     + [offer(f"Harsen {a.lower()}", b) for a, b in HARSEN])])


def feature_page(path, title, desc, eyebrow, h1, lead, crumb, art_icon, h2, paras, checks, price_html, extra="", photo="", hero_photo="", faq=None, ld=None):
    ch = "".join(f"<li>{ICONS['check']}<span>{c}</span></li>" for c in checks)
    ps = "".join(f"<p>{p}</p>" for p in paras)
    body = page_hero(eyebrow, h1, lead, [("/", "Home"), ("", crumb)], photo=hero_photo)
    art = f'<div class="feature-art photo reveal"><span class="ring"></span><img src="/img/{photo}" alt="" loading="lazy"></div>' if photo else \
        f'<div class="feature-art reveal"><span class="ring"></span>{ICONS[art_icon]}</div>'
    body += f"""
<section class="section">
  <div class="wrap feature">
    {art}
    <div class="reveal">
      <h2>{h2}</h2>
      {ps}
      <ul class="checks">{ch}</ul>
      {price_html}
      <div class="btns"><a class="btn btn-primary" href="tel:{SALON['tel_link']}">{ICONS['phone']} Afspraak maken</a></div>
    </div>
  </div>
  {extra}
</section>"""
    page(path, title, desc, body, faq=faq, ld=ld, og=(hero_photo or "landschap.jpg").replace(".jpg", ""),
         crumbs=[("Home", "/"), (crumb, path)])


def build_henna() -> None:
    feature_page(
        "/henna-wenkbrauwen/", "Henna wenkbrauwen in Oldenzaal",
        f"Henna wenkbrauwen in Oldenzaal: tot wel 6 weken volle en strakke wenkbrauwen met natuurlijke henna. {HENNA_PRIJS}, ca. 20 minuten. Bekijk voor- en na-foto's.",
        "Henna wenkbrauwen", "Voller, strakker <em>en mooier</em>",
        "Tot wel 6 weken mooie, volle en strakke wenkbrauwen, met een zuiver natuurproduct.",
        "Henna wenkbrauwen", "brow", "Wat maakt henna <em>anders</em>?",
        ["Henna is anders dan gewoon verven: je verft niet alleen de haartjes maar ook de huid. Daardoor lijken je wenkbrauwen voller en mooier gevormd.",
         "De henna komt uit Brazilië, waar het een van de populairste salonbehandelingen is. Henna is afkomstig van een struik: plantaardig dus, en een zuiver natuurproduct."],
        ["Natuurlijke henna voor wenkbrauwen", "Voor mooie, strakke en volle wenkbrauwen",
         "Tot wel 6 weken resultaat op de haartjes", "Tot wel 2 weken resultaat op de huid"],
        f'<div class="pricetag"><b>{HENNA_PRIJS}</b><span>· ca. 20 minuten</span></div>',
        extra='<div class="wrap"><figure class="voorna reveal" style="margin-left:0;margin-right:0"><img src="/img/henna-voor-na.jpg" alt="Wenkbrauwen voor en na de henna behandeling" width="1490" height="364" loading="lazy"></figure></div>',
        photo="card-henna.jpg", hero_photo="header-henna.jpg", faq=FAQ_HENNA,
        ld=[catalog("Henna wenkbrauwen", [offer("Henna wenkbrauwen", HENNA_PRIJS, "Natuurlijke henna voor volle, strakke wenkbrauwen; tot 6 weken resultaat op de haartjes en tot 2 weken op de huid.", "20 min", "/henna-wenkbrauwen/")])])


def build_nagels() -> None:
    feature_page(
        "/nagels/", "Gellak nagels in Oldenzaal",
        "Gellak (shellac) in Oldenzaal: twee weken of langer prachtige, stevige nagels. Gellak € 26,50, verwijderen € 13,50. Bel 0541 538 153 voor een afspraak.",
        "Nagels", "De mooiste nagels voor <em>speciale momenten</em>",
        "Glanzende, stevige nagels die er twee weken of langer prachtig uitzien.",
        "Nagels", "nail", "Wat is <em>gellak</em> precies?",
        ["Gellak wordt ook wel gel-nagellak of shellac genoemd. Het is een tussenweg tussen gewone nagellak en gelnagels: het combineert de eigenschappen van een gel met die van nagellak.",
         "Je nagels zien er twee weken mooi uit, soms ook langer. Dat hangt af van hoe snel je nagels groeien en van je werk en hobby's."],
        ["Twee weken of langer mooie nagels", "Extra stevigheid: minder scheuren en afbreken", "Hoogglanzend resultaat"],
        f'<div style="max-width:420px;margin-bottom:1.8rem">{pricelist(NAGELS)}</div>',
        photo="header-nagels.jpg", hero_photo="header-nagels.jpg", faq=FAQ_NAGELS,
        ld=[catalog("Nagels", [offer(f"{a}", b, url="/nagels/") for a, b in NAGELS])])


def build_kadobon() -> None:
    feature_page(
        "/kadobon/", "Kadobon schoonheidssalon Oldenzaal",
        "Verras iemand met een kadobon van Wendy's Schoonheidssalon in Oldenzaal: in elk gewenst bedrag, te besteden aan alle behandelingen en feestelijk verpakt.",
        "Kadobon", "Verras iemand die je <em>liefhebt</em>",
        "Een moment van ontspanning is het mooiste cadeau. Voor een verjaardag, Moederdag, als bedankje, of zomaar.",
        "Kadobon", "gift", "Een cadeau vol <em>aandacht</em>",
        ["Verras vrienden of familie eens met een kadobon van Wendy's Schoonheidssalon. De bon is verkrijgbaar in elk gewenst bedrag, of voor een specifieke behandeling.",
         f"Neem telefonisch contact op via <a href=\"tel:{SALON['tel_link']}\">{SALON['tel']}</a>, dan wordt de kadobon feestelijk voor je verpakt."],
        ["In elk gewenst bedrag", "Feestelijk verpakt", "Te besteden aan alle behandelingen"],
        "", photo="header-kadobon.jpg", hero_photo="header-kadobon.jpg", faq=FAQ_KADOBON)


def build_contact() -> None:
    body = page_hero("Contact", "The art of <em>beauty</em>",
                     "Voor het maken van een afspraak bel je gewoon even. Voor algemene informatie over de behandelingen kun je ook mailen.",
                     [("/", "Home"), ("", "Contact")], photo="landschap.jpg")
    body += f"""
<section class="section" style="padding-top:20px">
  <div class="wrap">
    <div class="contact-grid">
      <div class="contact-card reveal">
        <h2 style="font-size:2.2rem">Afspraak maken</h2>
        <p style="color:var(--muted)">Er wordt uitsluitend op afspraak gewerkt: deze tijd wordt speciaal voor jou gereserveerd. Ben je verhinderd? Zeg je afspraak dan tijdig af. Niet nagekomen afspraken worden in rekening gebracht.</p>
        <ul class="contact-list" style="margin-top:2rem">
          <li><span class="ic">{ICONS['phone']}</span><div><small>Telefoon</small><a href="tel:{SALON['tel_link']}">{SALON['tel']}</a></div></li>
          <li><span class="ic">{ICONS['mail']}</span><div><small>E-mail</small><a href="mailto:{SALON['mail']}">{SALON['mail']}</a></div></li>
          <li><span class="ic">{ICONS['pin']}</span><div><small>Adres</small><span>{SALON['straat']}<br>{SALON['postcode']} {SALON['plaats']}</span></div></li>
        </ul>
      </div>
      <div class="map reveal">
        <iframe class="map-frame" title="Kaart: {SALON['naam']}, {SALON['straat']}, {SALON['plaats']}"
          src="https://maps.google.com/maps?q={SALON['straat'].replace(' ', '+')},+{SALON['postcode'].replace(' ', '+')}+{SALON['plaats']}&amp;hl=nl&amp;z=16&amp;output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <div class="map-inner"><div><b>{SALON['straat']}</b><span>{SALON['postcode']} {SALON['plaats']}</span></div>
          <a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&amp;destination={SALON['straat'].replace(' ', '+')},+{SALON['postcode'].replace(' ', '+')}+{SALON['plaats']}" target="_blank" rel="noopener">Route plannen</a></div>
      </div>
    </div>
  </div>
</section>"""
    page("/contact/", "Contact & afspraak maken",
         f"Maak een afspraak bij Wendy's Schoonheidssalon, {SALON['straat']}, {SALON['postcode']} {SALON['plaats']}. Bel {SALON['tel']} of mail {SALON['mail']}. Uitsluitend op afspraak.",
         body, crumbs=[("Home", "/"), ("Contact", "/contact/")], faq=FAQ_ALGEMEEN[:2] + FAQ_ALGEMEEN[4:5],
         ld=[{"@type": "ContactPage", "url": SITE + "/contact/", "mainEntity": {"@id": SALON_LD["@id"]}}])


def build_privacy() -> None:
    n = SALON["naam"]
    m = f'<a href="mailto:{SALON["mail"]}">{SALON["mail"]}</a>'
    secties = [
        ("", [f"{n}, gevestigd aan {SALON['straat']} {SALON['postcode']} {SALON['plaats']}, is verantwoordelijk voor de verwerking van persoonsgegevens zoals weergegeven in deze privacyverklaring."]),
        ("Contactgegevens", [f"{SITE}/<br>{SALON['straat']}, {SALON['postcode']} {SALON['plaats']}<br>+31 {SALON['tel']}",
                             f"Wendy Schwankhuizen-Luttikhuis is de Functionaris Gegevensbescherming van {n}. Zij is te bereiken via {m}."]),
        ("Persoonsgegevens die wij verwerken", [f"{n} verwerkt uw persoonsgegevens doordat u gebruik maakt van onze diensten en/of omdat u deze zelf aan ons verstrekt.",
                                                "Hieronder vindt u een overzicht van de persoonsgegevens die wij verwerken:",
                                                "<ul><li>Voor- en achternaam</li><li>Geboortedatum</li><li>Adresgegevens</li><li>Telefoonnummer</li><li>E-mailadres</li></ul>"]),
        ("Bijzondere en/of gevoelige persoonsgegevens die wij verwerken", [f"Onze website en/of dienst heeft niet de intentie gegevens te verzamelen over websitebezoekers die jonger zijn dan 16 jaar. Tenzij ze toestemming hebben van ouders of voogd. We kunnen echter niet controleren of een bezoeker ouder dan 16 is. Wij raden ouders dan ook aan betrokken te zijn bij de online activiteiten van hun kinderen, om zo te voorkomen dat er gegevens over kinderen verzameld worden zonder ouderlijke toestemming. Als u er van overtuigd bent dat wij zonder die toestemming persoonlijke gegevens hebben verzameld over een minderjarige, neem dan contact met ons op via {m}, dan verwijderen wij deze informatie."]),
        ("Met welk doel en op basis van welke grondslag wij persoonsgegevens verwerken", [f"{n} verwerkt uw persoonsgegevens voor de volgende doelen:",
                               "<ul><li>Verzenden van onze nieuwsbrief en/of reclamefolder</li><li>U te kunnen bellen of e-mailen indien dit nodig is om onze dienstverlening uit te kunnen voeren</li><li>U te informeren over wijzigingen van onze diensten en producten</li></ul>"]),
        ("Geautomatiseerde besluitvorming", [f"{n} neemt niet op basis van geautomatiseerde verwerkingen besluiten over zaken die (aanzienlijke) gevolgen kunnen hebben voor personen. Het gaat hier om besluiten die worden genomen door computerprogramma's of -systemen, zonder dat daar een mens (bijvoorbeeld een medewerker van {n}) tussen zit. {n} gebruikt de volgende computerprogramma's of -systemen: administratieve software voor schoonheidssalons."]),
        ("Hoe lang we persoonsgegevens bewaren", [f"{n} bewaart uw persoonsgegevens niet langer dan strikt nodig is om de doelen te realiseren waarvoor uw gegevens worden verzameld."]),
        ("Delen van persoonsgegevens met derden", [f"{n} verstrekt nooit uw persoonsgegevens aan derden, alleen als dit nodig is voor de uitvoering van onze overeenkomst met u of om te voldoen aan een wettelijke verplichting."]),
        ("Cookies, of vergelijkbare technieken, die wij gebruiken", [f"{n} gebruikt technische en functionele cookies en analytische cookies van Google Analytics. Een cookie is een klein tekstbestand dat bij het eerste bezoek aan deze website wordt opgeslagen op uw computer, tablet of smartphone. Met Google Analytics houden wij bij hoe bezoekers de website gebruiken, zodat wij de website kunnen optimaliseren. U kunt zich afmelden voor cookies door uw internetbrowser zo in te stellen dat deze geen cookies meer opslaat. Daarnaast kunt u ook alle informatie die eerder is opgeslagen via de instellingen van uw browser verwijderen.", "Op de contactpagina is een kaart van Google Maps ingebouwd. Google kan daarbij cookies plaatsen."]),
        ("Gegevens inzien, aanpassen of verwijderen", [f"U heeft het recht om uw persoonsgegevens in te zien, te corrigeren of te verwijderen. Daarnaast heeft u het recht om uw eventuele toestemming voor de gegevensverwerking in te trekken of bezwaar te maken tegen de verwerking van uw persoonsgegevens door {n} en heeft u het recht op gegevensoverdraagbaarheid. Dat betekent dat u bij ons een verzoek kunt indienen om de persoonsgegevens die wij van u beschikken in een computerbestand naar u of een ander, door u genoemde organisatie, te sturen.",
                                                       f"U kunt een verzoek tot inzage, correctie, verwijdering, gegevensoverdraging van uw persoonsgegevens of verzoek tot intrekking van uw toestemming of bezwaar op de verwerking van uw persoonsgegevens sturen naar {m}.",
                                                       "Om er zeker van te zijn dat het verzoek tot inzage door u is gedaan, vragen wij u een kopie van uw identiteitsbewijs met het verzoek mee te sturen. Maak in deze kopie uw pasfoto, MRZ (machine readable zone, de strook met nummers onderaan het paspoort), paspoortnummer en Burgerservicenummer (BSN) zwart. Dit ter bescherming van uw privacy. We reageren zo snel mogelijk, maar binnen vier weken, op uw verzoek.",
                                                       f"{n} wil u er tevens op wijzen dat u de mogelijkheid heeft om een klacht in te dienen bij de nationale toezichthouder, de Autoriteit Persoonsgegevens. Dat kan via <a href=\"https://autoriteitpersoonsgegevens.nl/nl/contact-met-de-autoriteit-persoonsgegevens/tip-ons\" rel=\"noopener\">autoriteitpersoonsgegevens.nl</a>."]),
        ("Hoe wij persoonsgegevens beveiligen", [f"{n} neemt de bescherming van uw gegevens serieus en neemt passende maatregelen om misbruik, verlies, onbevoegde toegang, ongewenste openbaarmaking en ongeoorloofde wijziging tegen te gaan. Als u de indruk heeft dat uw gegevens niet goed beveiligd zijn of er aanwijzingen zijn van misbruik, neem dan contact op via {m}."]),
    ]
    inner = "".join((f"<h2>{t}</h2>" if t else "") + "".join(p if p.startswith("<ul") else f"<p>{p}</p>" for p in ps)
                    for t, ps in secties)
    body = page_hero("Privacy", "Privacy<em>verklaring</em>", "Zo gaan wij om met uw persoonsgegevens.",
                     [("/", "Home"), ("", "Privacyverklaring")], photo="header-aroma.jpg")
    body += f'<section class="section"><div class="wrap prose">{inner}</div></section>'
    page("/privacy/", "Privacyverklaring", f"Privacyverklaring van {n} in {SALON['plaats']}.", body,
         crumbs=[("Home", "/"), ("Privacyverklaring", "/privacy/")], og="header-aroma", llm=False)


def build_prijzen() -> None:
    def blok(titel, link, rows, tag=""):
        return f"""
<div class="pricebox reveal">
  <span class="treatment-tag">{tag}</span>
  <h3><a href="{link}" style="text-decoration:none">{e(titel)}</a></h3>
  {pricelist(rows)}
  <a class="link" href="{link}">Meer over {e(titel.lower())}</a>
</div>"""
    blokken = [blok(g["titel"].replace(" & ontspannende", ""), f"/gezichtsbehandelingen/{g['slug']}/",
                    [(f"{n} · {du}", pr) for n, _, pr, du, _ in g["items"]], "Gezicht") for g in GROEPEN]
    blokken += [
        blok("Losse onderdelen gezicht", "/overige_behandelingen/", PRIJS_ONDERDELEN + [(f"Bij gezichtsbehandeling: {a.lower()}", b) for a, b in COMBI], "Epileren · harsen · verven"),
        blok("Harsen lichaam", "/overige_behandelingen/", HARSEN, "Lichaam"),
        blok("Henna wenkbrauwen", "/henna-wenkbrauwen/", [("Henna wenkbrauwen · ca. 20 min", HENNA_PRIJS)], "Wenkbrauwen"),
        blok("Gellak nagels", "/nagels/", NAGELS, "Nagels"),
    ]
    body = page_hero("Prijzen", "Prijslijst <em>behandelingen</em>",
                     "Alle behandelingen en prijzen van Wendy's Schoonheidssalon in Oldenzaal op één overzicht. Een kadobon is verkrijgbaar in elk gewenst bedrag.",
                     [("/", "Home"), ("", "Prijzen")], photo="header-aroma.jpg")
    body += f'<section class="section"><div class="wrap"><div class="pricegrid">{"".join(blokken)}</div>' \
            f'<p class="center" style="text-align:center;margin-top:36px;color:var(--muted)">Uitsluitend op afspraak. Afspraak maken: <a class="link" href="tel:{SALON["tel_link"]}">{SALON["tel"]}</a></p></div></section>'
    alle = [o for g in GROEPEN for o in group_offers(g)] + [offer(f"Losse onderdelen: {a.lower()}", b, url="/overige_behandelingen/") for a, b in PRIJS_ONDERDELEN] \
        + [offer(f"Harsen {a.lower()}", b, url="/overige_behandelingen/") for a, b in HARSEN] \
        + [offer("Henna wenkbrauwen", HENNA_PRIJS, duur="20 min", url="/henna-wenkbrauwen/")] + [offer(a, b, url="/nagels/") for a, b in NAGELS]
    page("/prijzen/", "Prijzen schoonheidssalon Oldenzaal",
         "Prijslijst van Wendy's Schoonheidssalon in Oldenzaal: gezichtsbehandelingen vanaf € 32,00, harsen vanaf € 19,50, henna € 24,00, gellak € 26,50.",
         body, crumbs=[("Home", "/"), ("Prijzen", "/prijzen/")], og="header-aroma",
         faq=[FAQ_ALGEMEEN[3], FAQ_HARSEN[1], FAQ_GEZICHT[2]], ld=[catalog("Prijslijst Wendy's Schoonheidssalon", alle)])


def build_sitemap_page() -> None:
    def a(u):
        return f'<a href="{u}">{e(PAGE_TITLES.get(u, u))}</a>'
    gz = "".join(f"<li>{a('/gezichtsbehandelingen/' + g['slug'] + '/')}<ul>" +
                 "".join(f"<li>{e(n)} · {pr}</li>" for n, _, pr, _, _ in g["items"]) + "</ul></li>" for g in GROEPEN)
    body = page_hero("Sitemap", "Alle <em>pagina's</em>", "Een overzicht van alle pagina's en behandelingen op deze website.",
                     [("/", "Home"), ("", "Sitemap")])
    body += f"""
<section class="section" style="padding-top:20px"><div class="wrap prose sitemap-list">
<ul>
  <li>{a('/')}</li>
  <li>{a('/gezichtsbehandelingen/')}<ul>{gz}</ul></li>
  <li>{a('/overige_behandelingen/')}</li>
  <li>{a('/henna-wenkbrauwen/')}</li>
  <li>{a('/nagels/')}</li>
  <li>{a('/prijzen/')}</li>
  <li>{a('/kadobon/')}</li>
  <li>{a('/contact/')}</li>
  <li>{a('/privacy/')}</li>
</ul>
<p>Voor zoekmachines: <a href="/sitemap.xml">sitemap.xml</a> · Voor AI-assistenten: <a href="/llms.txt">llms.txt</a></p>
</div></section>"""
    page("/sitemap/", "Sitemap", "Overzicht van alle pagina's en behandelingen van Wendy's Schoonheidssalon in Oldenzaal.", body,
         crumbs=[("Home", "/"), ("Sitemap", "/sitemap/")], llm=False)


def build_404() -> None:
    body = page_hero("Oeps", "Deze pagina is even <em>op adem</em> aan het komen",
                     "De pagina die je zoekt bestaat niet (meer). Bekijk de behandelingen of ga terug naar de homepage.",
                     [("/", "Home"), ("", "Niet gevonden")],
                     '<div class="btns" style="justify-content:center;margin-top:2rem"><a class="btn btn-primary" href="/">Naar de homepage</a><a class="btn btn-ghost" href="/gezichtsbehandelingen/">Behandelingen</a></div>')
    doc = head("Pagina niet gevonden", "Pagina niet gevonden.", "/404") + header("") + body + footer()
    (OUT / "404.html").write_text(responsive(doc).replace('<link rel="canonical" href="https://www.salonwendy.nl/404">',
                                              '<meta name="robots" content="noindex">'), encoding="utf-8")


def build_static() -> None:
    shutil.copy(ROOT / "src" / "style.css", OUT / "style.css")
    shutil.copy(ROOT / "src" / "site.js", OUT / "site.js")
    shutil.copy(ROOT / "src" / "_headers", OUT / "_headers")
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="32" fill="#6d5a64"/>'
        '<text x="32" y="44" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="36" fill="#fff">W</text>'
        '<circle cx="47" cy="17" r="4" fill="#e73b73"/></svg>', encoding="utf-8")
    # oude URL's zonder slash en verborgen pagina's van de oude site netjes doorsturen
    (OUT / "_redirects").write_text(
        "/gezichtsbehandelingen/mooi /gezichtsbehandelingen/korte-behandelingen/ 301\n"
        "/gezichtsbehandelingen/special /gezichtsbehandelingen/aromatherapie/ 301\n"
        "/thuispakketten /contact/ 301\n"
        "/node/* / 301\n"
        "/user/* / 301\n", encoding="utf-8")


def build_seo_files() -> None:
    volgorde = ["/", "/gezichtsbehandelingen/"] + [f"/gezichtsbehandelingen/{g['slug']}/" for g in GROEPEN] + \
        ["/overige_behandelingen/", "/henna-wenkbrauwen/", "/nagels/", "/prijzen/", "/kadobon/", "/contact/", "/privacy/", "/sitemap/"]
    regels = []
    for u in volgorde:
        imgs = "".join(f"\n    <image:image><image:loc>{SITE}/img/{n}.jpg</image:loc></image:image>"
                       for n in PAGE_IMAGES.get(u, []))
        regels.append(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{VANDAAG}</lastmod>{imgs}\n  </url>\n")
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + "".join(regels) + "</urlset>\n", encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot",
            "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot", "CCBot", "meta-externalagent"]
    (OUT / "robots.txt").write_text(
        "# Alle zoekmachines en AI-assistenten zijn welkom\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
        + f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

    # llms.txt: compacte, feitelijke samenvatting voor AI-assistenten (https://llmstxt.org)
    lijst = "\n".join(f"- [{t}]({SITE}{p}): {d}" for t, p, d in LLM_PAGES)
    behandelingen = []
    for g in GROEPEN:
        behandelingen.append(f"\n### {g['titel']}\n")
        for n_, sub, pr, du, tekst in g["items"]:
            behandelingen.append(f"- **{n_}** ({sub}): {pr}, {du}. {' '.join(tekst)}")
    overig = "\n".join([f"- {a}: {b}" for a, b in PRIJS_ONDERDELEN] + [f"- In combinatie met gezichtsbehandeling, {a.lower()}: {b}" for a, b in COMBI]
                       + [f"- Harsen {a.lower()}: {b}" for a, b in HARSEN] + [f"- Henna wenkbrauwen: {HENNA_PRIJS} (ca. 20 min)"]
                       + [f"- {a}: {b}" for a, b in NAGELS])
    faq = "\n".join(f"**{q}**\n{re.sub(r'<[^>]+>', '', a)}\n" for q, a in FAQ_ALGEMEEN + FAQ_GEZICHT + FAQ_HENNA + FAQ_NAGELS)
    kort = f"""# {SALON['naam']}

> Schoonheidssalon in Oldenzaal (Twente, Overijssel) van schoonheidsspecialiste Wendy Schwankhuizen-Luttikhuis. Verzorgende en ontspannende gezichtsbehandelingen, aromatherapie, rugbehandeling, harsen, epileren, verven, henna wenkbrauwen en gellak. Uitsluitend op afspraak; afspraken telefonisch.

- Adres: {SALON['straat']}, {SALON['postcode']} {SALON['plaats']}, Nederland
- Telefoon (afspraken): {SALON['tel']} (+31 541 538 153)
- E-mail: {SALON['mail']}
- Website: {SITE}/
- Producten: Webecos huidverzorging, Chi aromatherapie (100% natuurlijk)
- Prijzen: van € 14,00 (los onderdeel) tot € 62,00 (Special Wellness, 85 min)

## Pagina's

{lijst}

## Optioneel

- [Volledige inhoud met alle behandelingen en prijzen]({SITE}/llms-full.txt)
- [Privacyverklaring]({SITE}/privacy/)
"""
    (OUT / "llms.txt").write_text(kort, encoding="utf-8")
    vol = kort + f"""
## Gezichtsbehandelingen

Tijdens alle gezichtsbehandelingen worden de wenkbrauwen geëpileerd of geharst en worden onzuiverheden verwijderd.
{chr(10).join(behandelingen)}

### Aromatherapie: geuren en edelstenen
""" + "\n".join(f"- **{t}** (edelsteen: {st}): {txt}" for _, _, t, st, txt in GEUREN) + f"""

## Harsen, epileren, verven, henna en nagels

Losse onderdelen gezicht: {", ".join(LOSSE_ONDERDELEN).lower()}.

{overig}

## Kadobon

Verkrijgbaar in elk gewenst bedrag, feestelijk verpakt. Bestellen via {SALON['tel']}.

## Afspraken

Er wordt uitsluitend op afspraak gewerkt. Niet nagekomen afspraken worden in rekening gebracht.

## Veelgestelde vragen

{faq}"""
    (OUT / "llms-full.txt").write_text(vol, encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_static()
    make_images()
    build_home()
    build_gezicht()
    build_overig()
    build_henna()
    build_nagels()
    build_kadobon()
    build_contact()
    build_privacy()
    build_prijzen()
    build_sitemap_page()
    build_404()
    build_seo_files()
    print("Klaar:", sum(1 for _ in OUT.rglob("*.html")), "pagina's in", OUT)


if __name__ == "__main__":
    main()
