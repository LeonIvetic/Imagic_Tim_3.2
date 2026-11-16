# A. Pregled aktivnosti grupe

**Cilj:** Zabilježiti aktivnosti tima, doprinose članova i izazove.

## A.1 Sastanci

Bilješke se nalaze u [meeting-notes](meeting-notes/).

| Datum | Tema | Bilješke |
|-------|------|----------|
| 2026-10-26 | Laboratorijska vježba 1 (prezentacija zahtjeva) | [bilješke](meeting-notes/2026-10-26-vjezba-1.md) |
| 2026-10-31 | Pregled rada i dogovor za 5. tjedan | [bilješke](meeting-notes/2026-10-31-tjedan-5.md) |
| 2026-11-09 | Pregled rada i dogovor za 6. tjedan | [bilješke](meeting-notes/2026-11-09-tjedan-6.md) |

## A.2 Doprinosi članova

| Član | Doprinos |
|------|----------|
| Leon Ivetić | Incijalna struktura repozitorija, prva inačica teksta dokumentacije prema predlošku. Koordinacija tima kroz projekt, dodjeljivanje i upravljanje zadatcima ostalih članova. Auth0 postavke (tenant, SPA, API), Issues i milestone, Auth0Provider, apiFetch, spajanje frontenda s backendom, koordinacija. Kostur aplikacije (rute, layout, navigacija), podatkovni sloj src/data/ (localStorage + IndexedDB), ensureUser, seed korisnika, review PR-ova, integracija i provjera na masteru. |
| Feđa Mitić | Backend prijave: provjera Auth0 tokena, get_current_user sa stvaranjem korisnika, ruta za trenutnog korisnika, stvaranje korijenske mape pri stvaranju korisnika, održavanje dokumentacije.|
| Roko Vrdoljak | Dijagram razreda i dijagrami slijeda (UC-001, UC-002), javne stranice drugih korisnika, favoriti, preuzimanje i kopiranje tuđe slike u svoju radnu okolinu. |
| Florijan Blažeka | Login ekran, zaglavlje s imenom i odjavom, stanja učitavanja i greške. Ekran radne okoline: mape (stvori, preimenuj, obriši), upload s provjerom, izbornik slike (preimenuj, premjesti, preuzmi, obriši), prazna stanja. |
| Alan Ivanković | Baza: docker-compose.yml (PostgreSQL), db.py, model User, Alembic migracija, upute u docs/6. Modeli Folder, ImageFile, Post, FavoritePost i FavoriteProfile s kaskadama i CHECK ograničenjem, druga migracija, tablica varijabli u docs/6.2 |
| Lorena Ivanković | ER model cijele aplikacije (PlantUML, opis tablica u docs/4, odluke o brisanju i jedinstvenosti). Integracija Artic API-ja, 3 početne slike pri prvoj prijavi (seedInitialImages), ekran /artic, preglednik slike i panel alata obrade (samo sučelje). |
| Mihaela Miljavac | Obrasci uporabe UC-001 do UC-005, dijagram obrazaca uporabe, tablica sljedivosti 2.6, ekran profila s uređivanjem, postovi (javni/privatni), komponenta PostCard. |


## A.3 Izazovi

[Dopuniti.]
