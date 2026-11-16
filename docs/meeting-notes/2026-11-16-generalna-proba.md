# Sastanak: Dogovor nakon generalne probe (16.11.2026.)

**Tim:** Git Happens  
**Prisutni:** svi članovi tima

## Dnevni red

1. Povratna informacija s generalne probe
2. Raspored poslova do prve predaje (4 dana)

## Povratna informacija s generalne probe

- Obrasci uporabe nisu dovoljno detaljni.
- Nedostaje UML dijagram razreda.
- Aplikacija mora biti javno dostupna (deployment).
- Treba ostvariti barem jedan filter obrade slike (grayscale) pomoću Pillowa ili OpenCV-a.

## Odluke

- Grayscale filter radimo s **Pillowom**, koji backend već koristi (`backend/app/storage.py`).
- Dijagram razreda crta se prema kodu nakon što se spoji grayscale filter, kako bi sadržavao i nove razrede i metode.
- **Pohrana slika:** u razgovoru s asistentom odlučeno je da do prve predaje slike ne moraju biti pohranjene na vanjskom servisu. Mogu ostati na disku servera i to se neće bodovno umanjiti. Vanjsku pohranu slika zato sada ne implementiramo.

## Ciljevi do prve predaje

| Zadatak | Kriterij gotovosti | Zaduženi |
|---------|--------------------|----------|
| Obrasci uporabe | Svaki UC u docs/3 ima sudionike, preduvjete, osnovni tijek, alternativne tijekove i postuvjete; dodan UC za grayscale filter; ažuriran use case dijagram | Mihaela Miljavac |
| Dijagram razreda | UML dijagram razreda prema stvarnom kodu (modeli, DTO-ovi, routeri i servisi) u docs/4 | Roko Vrdoljak |
| Grayscale filter | Backend ruta koja Pillowom pretvara sliku u sivu; gumb u aplikaciji; test u `backend/tests/` | Feđa Mitić |
| Deployment | Aplikacija javno dostupna; Auth0 podešen za javnu domenu; migracije pokrenute na produkcijskoj bazi; upute i javni URL u docs/6 i README | Leon Ivetić |

## Pitanja za asistenta

- [nema / upisati]
