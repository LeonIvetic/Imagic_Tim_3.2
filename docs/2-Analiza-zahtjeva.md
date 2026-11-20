# 2. Analiza zahtjeva

**Cilj:** Iz odobrenog opsega projekta izvesti prepoznatljive, prioritetizirane i provjerljive zahtjeve. Zahtjevi se mogu mijenjati; pri završnoj predaji moraju odražavati dogovorenu aplikaciju. Značajne promjene zabilježite u odjeljku 2.5.

## 2.1 Funkcijski zahtjevi

**Cilj:** Navesti što aplikacija mora omogućiti korisnicima, odakle pojedina mogućnost proizlazi i koji se opažljivi rezultat smatra prihvaćanjem.

| ID | Opis | Prioritet | Izvor | Kriteriji prihvaćanja |
|----|------|-----------|-------|-----------------------|
| F-001 | Korisnici se prijavljuju i registriraju putem OAuth 2.0 pružatelja identiteta. | Visok | Odobreni zadatak | Uspješna prijava otvara radnu okolinu i javnu stranicu korisnika; pri prvoj prijavi račun se automatski stvara; odustajanje od prijave ostavlja zaštićene radnje nedostupnima. |
| F-002 | Korisnik može učitati (upload) i preuzeti (download) rasterske slike u najmanje 3 formata. Podržani su JPEG, PNG, TIFF i WebP. | Visok | Odobreni zadatak | Slika u svakom podržanom formatu može se učitati i pojavljuje se u radnoj okolini; preuzeta datoteka otvara se u standardnom pregledniku slika. |
| F-003 | Radna okolina pohranjuje slike u strukturi mapa; korisnik može stvarati, preimenovati i brisati mape te imenovati i preimenovati datoteke. | Visok | Odobreni zadatak | Korisnik stvara ugniježđenu mapu, premješta u nju sliku, preimenuje mapu i datoteku; promjene su vidljive nakon ponovnog učitavanja. |
| F-004 | Korisnik može prikazati odabranu sliku u radnoj okolini. | Visok | Odobreni zadatak | Odabirom datoteke slika se prikazuje u pregledniku slike. |
| F-005 | Korisnik može primijeniti najmanje 5 filtara (npr. invert, grayscale, pixelate, blur, derivative). | Visok | Odobreni zadatak | Za svaki filtar vidljiv je promijenjeni rezultat na odabranoj slici. |
| F-006 | Korisnik može primijeniti najmanje 4 morfološka operatora (erosion, dilation, opening, closing). | Visok | Odobreni zadatak | Za svaki operator vidljiv je promijenjeni rezultat na odabranoj slici. |
| F-007 | Korisnik može primijeniti najmanje 3 geometrijske transformacije (npr. resize, rotate, flip). | Visok | Odobreni zadatak | Za svaku transformaciju rezultat odgovara zadanim parametrima (dimenzije, kut, os zrcaljenja). |
| F-008 | Korisnik može primijeniti najmanje jedan algoritam segmentacije slike. | Visok | Odobreni zadatak | Rezultat segmentacije prikazuje se kao nova slika. |
| F-009 | Rezultat obrade korisnik sprema kao novu datoteku ili prepisuje izvornu. | Visok | Odobreni zadatak | Nakon spremanja kao nova datoteka postoje original i rezultat; nakon prepisivanja postoji samo izmijenjena datoteka. |
| F-010 | Korisnik ima javnu stranicu s korisničkim imenom, slikom i kratkim opisom koje samo on može uređivati. | Visok | Odobreni zadatak | Vlasnik može urediti podatke; drugi korisnici ih vide, ali ne mogu mijenjati. |
| F-011 | Korisnik može dodavati, uređivati i brisati postove (rasterska slika s tekstualnim opisom) na svojoj javnoj stranici. | Visok | Odobreni zadatak | Novi post prikazuje se na stranici; nakon uređivanja prikazuje novi sadržaj; nakon brisanja više nije vidljiv. |
| F-012 | Korisnik može označiti svaki post kao privatan ili javan. | Visok | Odobreni zadatak | Privatni post vidljiv je samo vlasniku; javni post vide svi prijavljeni korisnici. |
| F-013 | Prijavljeni korisnici mogu pregledavati javne stranice drugih korisnika. | Visok | Odobreni zadatak | Prijavljeni korisnik otvara tuđu javnu stranicu i vidi samo javne postove. |
| F-014 | Korisnik može dodati u favorite pojedini post ili cijelu javnu stranicu drugog korisnika. | Srednji | Odobreni zadatak | Odabrani post ili stranica pojavljuje se na popisu favorita i može se ukloniti. |
| F-015 | Korisnik može sliku s tuđe javne stranice preuzeti lokalno ili dodati u svoju radnu okolinu. | Srednji | Odobreni zadatak | Preuzeta slika otvara se lokalno; dodana slika pojavljuje se u radnoj okolini korisnika. |
| F-016 | Radna okolina je privatna: njezin sadržaj vidljiv je samo vlasniku. | Visok | Odobreni zadatak | Drugi prijavljeni korisnik ne može dohvatiti slike ni mape tuđe radne okoline. |
| F-017 | Korisnik može pretraživati djela iz javne domene u Artic galeriji (Art Institute of Chicago) i odabrano djelo dodati u svoju radnu okolinu. | Srednji | Odluka tima | Pretraga po pojmu prikazuje popis djela s pregledom slike; dodano djelo pojavljuje se u radnoj okolini korisnika. |

## 2.2 Nefunkcijski zahtjevi

**Cilj:** Odrediti važna svojstva kvalitete i uvjete rada odobrene aplikacije na način koji tim može razumno provjeriti.

| ID | Opis | Prioritet | Izvor | Način provjere |
|----|------|-----------|-------|----------------|
| NF-01 | Aplikacija ne pohranjuje korisničke lozinke; autentifikacija se provodi isključivo vanjskim OAuth 2.0 pružateljem. | Visok | Odobreni zadatak | Pregled baze i koda: nema polja za lozinke; prijava radi samo preko OAuth-a. |
| NF-02 | Pristup zaštićenim resursima (radna okolina, privatni postovi, uređivanje profila) dopušten je samo ovlaštenom korisniku. | Visok | Odobreni zadatak | Testni scenarij: neautorizirani i tuđi zahtjevi vraćaju grešku. |
| NF-03 | Aplikacija se koristi u suvremenom web-pregledniku (Chrome, Firefox) bez dodatne instalacije. | Srednji | Procjena tima | Ručni test u najmanje dva preglednika. |
| NF-04 | Obrada slike tipične veličine (do oko 5 MP) vraća rezultat u razumnom vremenu (cilj: unutar nekoliko sekundi). | Srednji | Procjena tima | Mjerenje vremena obrade na uzorku slika; granica se potvrđuje s asistentom. |
| NF-05 | Učitane datoteke validiraju se po stvarnom sadržaju (ne po nastavku imena) i veličini (najviše 10 MB); nepodržani formati i prevelike datoteke odbijaju se uz razumljivu poruku. | Srednji | Procjena tima | Testni scenarij: upload nepodržane i prevelike datoteke. |
| NF-06 | Tajne (OAuth ključevi, pristupni podaci) ne nalaze se u repozitoriju, već u varijablama okruženja. | Visok | Pravila kolegija | Pregled repozitorija; datoteke `.env.example` sadrže samo javne vrijednosti (Auth0 domena, client ID, audience) i lozinku lokalne Docker baze, a produkcijske vrijednosti postavljene su kao varijable na Railwayu. |
| NF-07 | Izvorni kod održava se na GitHubu uz Pull Requeste, Issues i verzioniranje. | Srednji | Pravila kolegija | Pregled povijesti repozitorija. |
| NF-08 | Web aplikacija mora biti responzivna, tj. prilagoditi raspored i veličinu elemenata različitim dimenzijama zaslona (mobitel, tablet, desktop - minimalna širina 360px) bez horizontalnog skrolanja i gubitka funkcionalnosti. | Srednji | Procjena tima | Ručno testiranje u Chrome DevTools na različitim širinama ekrana. |
| NF-09 | Aplikacija je javno dostupna putem HTTPS-a bez lokalne instalacije. | Visok | Generalna proba (16.11.2026.) | Otvaranje <https://imagictim32-production.up.railway.app> i prijava s uređaja izvan razvojnog okruženja. |

## 2.3 Dionici i akteri

**Cilj:** Utvrditi uloge koje utječu na zahtjeve i razlikovati dionike od aktera koji komuniciraju s aplikacijom.

| ID uloge ili aktera | Odnos prema sustavu | Relevantni zahtjevi |
|---------------------|---------------------|---------------------|
| A-01 Neprijavljeni posjetitelj | Akter: može pokrenuti prijavu putem OAuth-a; nema pristup ostalim sadržajima. | F-001 |
| A-02 Prijavljeni korisnik | Akter: koristi radnu okolinu, obrađuje slike, uređuje svoju javnu stranicu i postove, pregledava tuđe javne stranice i postove, upravlja favoritima, preuzima tuđe javne slike te dodaje djela iz Artic galerije u svoju radnu okolinu. | F-002 – F-017 |
| S-01 Auth0 | Vanjski sustav (sekundarni akter): pružatelj identiteta koji provodi prijavu i izdaje pristupni token. | F-001 |
| S-02 Artic API | Vanjski sustav (sekundarni akter): izvor djela iz javne domene za Artic galeriju i za početne slike pri prvoj prijavi. | F-001, F-017 |
| D-01 Nositelj kolegija i asistent | Dionici (nisu akteri): zadaju opseg i ocjenjuju rad. | Cijeli opseg |

## 2.4 Ograničenja i pretpostavke

**Cilj:** Zabilježiti projektno specifične granice i pretpostavke koje utječu na zahtjeve ili oblikovanje, zajedno s njihovim izvorom i praktičnom posljedicom.

| ID | Tip | Opis ograničenja ili pretpostavke | Izvor | Inženjerska posljedica / Provjera |
|----|-----|-----------------------------------|-------|-----------------------------------|
| C-01 | Ograničenje | Prijava i registracija moraju se ostvariti vanjskim servisima za autentifikaciju putem OAuth 2.0. | Zadatak | Autentifikacija se projektira oko odabranog pružatelja; nema lokalnih lozinki. |
| C-02 | Ograničenje | Tim koristi React + JavaScript za frontend i FastAPI (Python) za backend. | Odluka tima | Komunikacija preko REST API-ja; obrada slike izvodi se na backendu (vidi AS-01). |
| C-03 | Ograničenje | Radna okolina je privatna, a javna stranica vidljiva svim prijavljenim korisnicima i uređuje je samo vlasnik. | Zadatak | Provjera vlasništva na svakom zahtjevu. |
| C-04 | Ograničenje | Minimalni opseg obrade: 5 filtara, 4 morfološka operatora, 3 geometrijske transformacije, 1 algoritam segmentacije; najmanje 3 formata datoteka. | Zadatak | Ostvariti sve navedene alate; provjeriti u ispitivanju. |
| AS-01 | Pretpostavka | Obrada slika izvodi se na backendu (Pillow/OpenCV). | Odluka tima | Odluka zabilježena u 2.5 i docs/4. |
| AS-02 | Pretpostavka | Za prijavu je dovoljan jedan pružatelj identiteta; tim koristi Auth0 (OAuth 2.0). | Odluka tima | Odluka zabilježena u 2.5 i docs/4. |
| AS-03 | Pretpostavka | Artic API dostupan je za dohvat početnih slika i za Artic galeriju (F-017); ako nije, za početne slike koriste se ugrađene slike. | Procjena tima | Ostvareno za početne slike: ugrađene slike nalaze se u `backend/app/seed/`, a prijava ne pada ako Artic ne odgovori (test `test_bez_artica_koriste_se_ugradene_slike`). Ponašanje galerije kad Artic nije dostupan opisano je u UC-011 (2a). |
| AS-04 | Pretpostavka | Slike se pohranjuju na disku poslužitelja (Railway volume), a ne na vanjskom servisu za pohranu. | Dogovor s asistentom | Vrijedi do prve predaje; baza čuva samo putanju do datoteke, pa je kasniji prelazak na vanjsku pohranu ograničen na `backend/app/storage.py`. |

## 2.5 Značajne promjene zahtjeva

**Cilj:** Sačuvati razlog promjena koje mijenjaju dogovoreni opseg, prioritet ili kriterije prihvaćanja.

| Datum | ID zahtjeva | Promjena i razlog | Dogovoreno s / dokaz |
|-------|-------------|-------------------|----------------------|
| 30.10.2026. | NF-08 | Dodan novi nefunkcijski zahtjev za responzivnost stranice. Razlog: Korisnici će aplikaciji pristupati s različitih uređaja, a zadatak ne propisuje podržane veličine zaslona, pa ih je tim definirao. | Dogovor s asistentom na [vježbi 26.10.](meeting-notes/2026-10-26-vjezba-1.md) |
| 31.10.2026. | AS-01, C-02 | Obrada slika izvodi se na backendu (Pillow/OpenCV). Razlog: jedna implementacija alata na poslužitelju, neovisna o pregledniku. | Odluka tima ([sastanak 31.10.](meeting-notes/2026-10-31-tjedan-5.md)) |
| 31.10.2026. | AS-02, F-001 | Za prijavu se koristi Auth0 (OAuth 2.0), a za pohranu podataka PostgreSQL. | Odluka tima ([sastanak 31.10.](meeting-notes/2026-10-31-tjedan-5.md)) |
| 9.11.2026. | F-002, NF-05 | Podržani formati utvrđeni su kao JPEG, PNG i WebP, a TIFF uz backend jer ga preglednici ne prikazuju (za prikaz se pretvara u PNG). Najveća veličina datoteke je 10 MB. | Odluka tima ([sastanak 9.11.](meeting-notes/2026-11-09-tjedan-6.md)) |
| 16.11.2026. | NF-09, AS-04 | Dodan zahtjev za javnu dostupnost aplikacije; slike do prve predaje ostaju na disku poslužitelja. | Generalna proba i dogovor s asistentom ([sastanak 16.11.](meeting-notes/2026-11-16-generalna-proba.md)) |
| 18.11.2026. | F-017, A-02, S-01, S-02 | Dodan zahtjev za Artic galeriju (UC-011). Obrasci uporabe razrađeni su vezama `<<include>>` (UC-010 Spremanje slike u radnu okolinu) i `<<extend>>`. Akter A-03 spojen je u A-02 jer aplikacija ne razlikuje ulogu posjetitelja od prijavljenog korisnika. Auth0 i Artic API navedeni su kao vanjski sustavi. Razlog: generalna proba pokazala je da obrasci uporabe nisu dovoljno detaljni. | Odluka tima |

## 2.6 Sljedivost zahtjeva

**Cilj:** Osigurati dvosmjernu sljedivost — povezati zahtjeve s opisanim ponašanjem, dijelovima sustava koji ih ostvaruju te ispitivanjem ili drugom provjerom.

| ID zahtjeva | Obrazac uporabe / modul | Arhitekturna realizacija | Ispitivanje ili provjera |
|-------------|-------------------------|--------------------------|--------------------------|
| F-001 | UC-001 | `backend/app/auth.py` (provjera Auth0 tokena, stvaranje korisnika), `backend/app/seed.py` (početne slike) | `test_auth.py`, `test_seed.py` |
| F-002 | UC-002, UC-006, UC-010 | `backend/app/workspace.py` (učitavanje i preuzimanje slika), `backend/app/storage.py` (pohrana i provjera formata) | `test_workspace.py` |
| F-003 | UC-006 | `backend/app/workspace.py` (organizacija mapa i slika) | `test_workspace.py` |
| F-004 | UC-006 | Preglednik slike u radnoj okolini | Ručna provjera prikaza odabrane slike |
| F-005 | UC-003 | `backend/app/filters.py` (5 filtara u Pillowu: grayscale, invert, pixelate, blur, derivative), `POST /api/images/{id}/filters` u `backend/app/workspace.py`, odabir i pregled filtara u `frontend/src/pages/ImageViewer.jsx` | `test_filter_preview` (`test_workspace.py`) |
| F-006 – F-008 | UC-003 | Morfološki operatori, geometrijske transformacije i segmentacija (u izradi) | na čekanju |
| F-009 | UC-003, UC-010 | `POST /api/images/{id}/filters` (`action`: `copy` ili `overwrite`) u `backend/app/workspace.py`, `backend/app/storage.py` (pohrana rezultata) | `test_filter_copy_and_overwrite` (`test_workspace.py`) |
| F-010 | UC-007 | `backend/app/users.py` (`PATCH /api/users/me`) | `test_profile_posts.py` |
| F-011 – F-012 | UC-004 | `backend/app/posts.py` (postovi i kontrola vidljivosti) | `test_profile_posts.py`, `test_slika_privatnog_posta_vidi_samo_vlasnik` |
| F-013 | UC-005 | Pregled javnih profila i postova (u izradi) | na čekanju |
| F-014 | UC-008 | API za favorite (u izradi) | na čekanju |
| F-015 | UC-009 | Preuzimanje tuđe javne slike i dodavanje u vlastitu radnu okolinu (u izradi) | na čekanju |
| F-016 | UC-002, UC-003, UC-006, UC-010 | Provjera vlasništva u `backend/app/workspace.py` (`own_folder`, `own_image`) | `test_tudja_radna_okolina_nedostupna` |
| F-017 | UC-011, UC-010 | Artic galerija (u izradi; stranica `frontend/src/pages/ArticGallery.jsx`) | na čekanju |
| NF-09 | — | Docker image na Railwayu ([6.3](6-Postavljanje-instalacija-i-konfiguracija.md#63-javno-postavljanje-i-administracija)) | ručna provjera na javnoj domeni |

Stavke označene „na čekanju” dopunit će se nakon realizacije morfoloških operatora, geometrijskih transformacija i segmentacije (UC-003), pregleda tuđeg javnog profila i objava (UC-005), upravljanja favoritima (UC-008), preuzimanja tuđe javne slike (UC-009) i Artic galerije (UC-011).

## 2.7 Pregled zahtjeva

**Cilj:** Zabilježiti važne povratne informacije o zahtjevima i odluke koje iz njih proizlaze na formalnim kontrolnim točkama projekta.

| Kontrolna točka | Povratna informacija ili nalaz | Odluka o zahtjevu ili opsegu |
|-----------------|--------------------------------|------------------------------|
| Generalna proba (16.11.2026.) | Obrasci uporabe nisu dovoljno detaljni; nedostaje dijagram razreda; aplikacija nije javno dostupna; nije ostvaren nijedan filtar obrade slike. | Dodan NF-09; do prve predaje ostvaruje se filtar grayscale, a slike ostaju na disku poslužitelja (AS-04). Do prve predaje ostvareno je svih 5 filtara iz F-005 sa spremanjem rezultata kao nove datoteke ili prepisivanjem izvorne (F-009), a aplikacija je javno dostupna (NF-09). Vidi [bilješke](meeting-notes/2026-11-16-generalna-proba.md). |
| Iteracija 1 | | |
| Demo 2 | | |
| Završni pregled | | |

---

> **Završna provjera:** Zahtjevi su aktualni, provjerljivi i povezani. Svaki važan zahtjev moguće je pratiti od njegova opisa i ponašanja preko mjesta realizacije u sustavu do odgovarajućeg ispitivanja ili druge provjere.
