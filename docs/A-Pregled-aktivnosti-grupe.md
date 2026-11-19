# A. Pregled aktivnosti grupe

**Cilj:** Prikazati kako je tim organizirao projekt, raspodijelio rad, reagirao na važne probleme i pridonio rezultatu.

## A.1 Evidencija sastanaka

**Cilj:** Voditi kratak zapis projektnih sastanaka i tjedne koordinacije: tko je sudjelovao, što je odlučeno i koja je radnja uslijedila. Detaljne bilješke nalaze se u [meeting-notes](meeting-notes/).

Kratice: `LeI` = Leon Ivetić; `FB` = Florijan Blažeka; `RV` = Roko Vrdoljak; `FM` = Feđa Mitić; `LoI` = Lorena Ivanković; `MM` = Mihaela Miljavac; `AlI` = Alan Ivanković.

| Datum i sudionici | Glavna tema | Donesena odluka ili zadatak | Poveznica na zadatak ili rezultat, ako postoji |
| --- | --- | --- | --- |
| 26.10.2026.; svi članovi, asistent Lovro Bosnar | Laboratorijska vježba 1: prezentacija zahtjeva | Dodati nefunkcijski zahtjev za responzivnost (NF-08); prilagoditi README prema uputama asistenta | [bilješke](meeting-notes/2026-10-26-vjezba-1.md) |
| 31.10.2026.; svi članovi (WhatsApp) | Dogovor za 5. tjedan | Prijava preko Auth0, baza PostgreSQL; prijava se ostvaruje već u 5. tjednu. Zadaci: model podataka (AlI, LoI), prijava – backend (FM), prijava – frontend (LeI, FB), obrasci uporabe (MM), dijagram razreda i dijagrami slijeda (RV) | [bilješke](meeting-notes/2026-10-31-tjedan-5.md) |
| 9.11.2026.; svi članovi | Dogovor za 6. tjedan: klikabilni prototip | Dogovoren prototip cijelog frontenda s podacima u pregledniku; tijekom tjedna plan je promijenjen i frontend je odmah spojen na REST API backenda, pa prototip u pregledniku nije ostvaren. Komponente pristupaju podacima samo kroz `src/data/`; Artic API za početne slike uz rezervne slike. Zadaci: kostur i podatkovni sloj (LeI), radna okolina (FB), Artic i preglednik slike (LoI), profil i postovi (MM), tuđe stranice i favoriti (RV), prijava – backend (FM), modeli i migracija (AlI) | [bilješke](meeting-notes/2026-11-09-tjedan-6.md) |
| 16.11.2026.; svi članovi | Dogovor nakon generalne probe | Filtar grayscale radi se Pillowom; slike do prve predaje ostaju na disku poslužitelja (dogovor s asistentom). Zadaci: obrasci uporabe (MM), dijagram razreda (RV), grayscale (FM), javno postavljanje (LeI) | [bilješke](meeting-notes/2026-11-16-generalna-proba.md) |

## A.2 Plan rada

**Cilj:** Prikazati planirani redoslijed rada i odgovornosti u timu.

**Trenutačni plan:** zadaci se vode u [GitHub Issues](https://github.com/LeonIvetic/Imagic_Tim_3.2/issues) grupirani po milestoneovima, a tjedni plan u tablici ispod. Ažurnost plana održava LeI.

| Razdoblje/Tjedan | Glavni planirani rad | Odgovorni članovi | Poveznica na zadatke |
| --- | --- | --- | --- |
| 5. tjedan (31.10. – 8.11.) | Model podataka i inicijalizacija baze; prijava na backendu i frontendu; obrasci uporabe; dijagram razreda i dijagrami slijeda | AlI, LoI, FM, LeI, FB, MM, RV | [bilješke 31.10.](meeting-notes/2026-10-31-tjedan-5.md) |
| 6. tjedan (9.11. – 15.11.) | Frontend svih ekrana spojen na REST API (radna okolina, preglednik slike, profil i postovi); API radne okoline i pohrana slika na poslužitelju; prijava na backendu; modeli i migracija za cijeli ER model | svi članovi | [bilješke 9.11.](meeting-notes/2026-11-09-tjedan-6.md) |
| 16.11. – prva predaja | Detaljniji obrasci uporabe, dijagram razreda, filtar grayscale, javno postavljanje | MM, RV, FM, LeI | [bilješke 16.11.](meeting-notes/2026-11-16-generalna-proba.md) |

## A.3 Aktivnosti i doprinosi članova

**Cilj:** Prikazati koji su članovi radili na važnim projektnim aktivnostima i približan trud koji prijavljuju. Sati su samoprijavljena procjena uloženog rada.

| Član | Aktivnosti i reprezentativni rezultati | Prijavljeni sati |
| --- | --- | --- |
| Leon Ivetić | Inicijalna struktura repozitorija, prva inačica teksta dokumentacije prema predlošku. Koordinacija tima kroz projekt, dodjeljivanje i upravljanje zadatcima ostalih članova. Auth0 postavke (tenant, SPA, API), Issues i milestone, Auth0Provider, apiFetch, spajanje frontenda s backendom, koordinacija. Kostur aplikacije (rute, layout, navigacija), podatkovni sloj src/data/ (DataProvider) koji poziva REST API backenda, frontend radne okoline (upravljanje mapama i slikama, ImageViewer), poništavanje zadnjeg filtra i prikaz primijenjenih filtara, popravci builda i cachea slika, review PR-ova, integracija i provjera na masteru. Javno postavljanje aplikacije (Dockerfile, Railway, Auth0 za produkcijsku domenu) i upute u docs/6.3. | 50 |
| Feđa Mitić | Backend prijave: provjera Auth0 tokena, get_current_user sa stvaranjem korisnika, ruta za trenutnog korisnika, stvaranje korijenske mape pri stvaranju korisnika. Implementacija svih 5 filtara (greyscale, blur, pixelate, invert, derivative) njihova obrada u backendu i prikaz na stranici (frontend). Održavanje dokumentacije | 50 |
| Roko Vrdoljak | Dijagram razreda i dijagrami slijeda (UC-001, UC-002), javne stranice drugih korisnika, favoriti, preuzimanje i kopiranje tuđe slike u svoju radnu okolinu. | [dopuniti] |
| Florijan Blažeka | Login ekran, zaglavlje s imenom i odjavom, stanja učitavanja i greške. Ekran radne okoline: mape (stvori, preimenuj, obriši), upload s provjerom, izbornik slike (preimenuj, premjesti, preuzmi, obriši), prazna stanja. | [dopuniti] |
| Alan Ivanković | Baza: docker-compose.yml (PostgreSQL), db.py, model User, Alembic migracija, upute za pokretanje baze u docs/6. Modeli Folder, ImageFile, Post, FavoritePost i FavoriteProfile s kaskadnim brisanjem, jedinstvenim i CHECK ograničenjima te djelomičnim indeksom (jedna korijenska mapa po korisniku), druga migracija | 45 |
| Lorena Ivanković | ER model cijele aplikacije (PlantUML, opis tablica u docs/4, odluke o brisanju i jedinstvenosti). Integracija Artic API-ja, 3 početne slike pri prvoj prijavi (seedInitialImages), ekran /artic, preglednik slike i panel alata obrade (samo sučelje). | 40 |
| Mihaela Miljavac | Obrasci uporabe UC-001 do UC-005, UML dijagram obrazaca uporabe, tablica sljedivosti zahtjeva (2.6). Ekran profila s uređivanjem, komponenta PostCard za prikaz slike, opisa i oznake vidljivosti objave (javno/privatno). Seed i tri testne slike. | 25 |

## A.4 Pregled promjena u repozitoriju

**Cilj:** Prikazati kada su promjene napravljene u repozitoriju i tko ih je napravio, uz napomenu da sam broj zapisa promjena ne mjeri kvalitetu doprinosa.

**Prikaz aktivnosti repozitorija:** [GitHub Contributors](https://github.com/LeonIvetic/Imagic_Tim_3.2/graphs/contributors) za cijelo trajanje projekta.

Graf prikazuje samo commitove na glavnoj grani. Promjene se u nju spajaju preko Pull Requestova, pa dio tuđeg rada može biti zabilježen pod članom koji je spojio ili integrirao promjene. Rad na oblikovanju, pregledu i dokumentaciji vidljiv je u tablici A.3.

## A.5 Ključni inženjerski izazovi i rješenja

**Cilj:** Dokumentirati stvarne tehničke i organizacijske prepreke s kojima se tim suočio, poduzete korektivne korake te konačni ishod.

| Izazov | Poduzeta radnja | Ishod ili preostalo ograničenje |
| --- | --- | --- |
| Javno postavljanje uz trajnu pohranu slika i prijavu preko Auth0 | Odabran Railway s volumeom za slike; frontend i backend zapakirani u jedan Docker image na istoj domeni; produkcijska domena upisana u Auth0 | Aplikacija je javno dostupna i automatski se postavlja s grane `master`; trenutno radi na probnom planu |
| Prototip s podacima u pregledniku značio bi dvostruki rad na podatkovnom sloju | Backend API radne okoline napravljen u istom tjednu, a frontend odmah spojen na REST API | Nije bilo migracije iz localStoragea/IndexedDB-a; sloj `src/data/` i dalje odvaja komponente od API-ja |
| Prikaz slika koje traže autorizaciju (`<img>` ne šalje token) | Slike se dohvaćaju kao Blob i prikazuju preko privremene `blob:` adrese (`frontend/src/data/images.js`) | Radi i za tuđe javne postove; nakon primjene filtra slika se ponovno dohvaća prema `updated_at` |
