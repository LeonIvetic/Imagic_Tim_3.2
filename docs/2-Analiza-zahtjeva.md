# 2. Analiza zahtjeva

**Cilj:** Iz odobrenog opsega projekta izvesti prepoznatljive, prioritetizirane i provjerljive zahtjeve. Zahtjevi se mogu mijenjati; pri završnoj predaji moraju odražavati dogovorenu aplikaciju. Značajne promjene zabilježite u odjeljku 2.5.

## 2.1 Funkcijski zahtjevi

**Cilj:** Navesti što aplikacija mora omogućiti korisnicima, odakle pojedina mogućnost proizlazi i koji se opažljivi rezultat smatra prihvaćanjem.

| ID | Opis | Prioritet | Izvor | Kriteriji prihvaćanja |
|----|------|-----------|-------|-----------------------|
| F-001 | Korisnici se prijavljuju i registriraju putem OAuth 2.0 pružatelja identiteta. | Visok | Odobreni zadatak | Uspješna prijava otvara radnu okolinu i javnu stranicu korisnika; pri prvoj prijavi račun se automatski stvara; odustajanje od prijave ostavlja zaštićene radnje nedostupnima. |
| F-002 | Pri prvoj prijavi korisnik u radnoj okolini dobiva 3 rasterske slike za testiranje. | Srednji | Odobreni zadatak | Nakon prve prijave u radnoj okolini postoje 3 slike; kod sljedećih prijava se ne dupliciraju. |
| F-003 | Korisnik može učitati (upload) i preuzeti (download) rasterske slike u najmanje 3 formata (npr. JPEG, PNG, TIF). | Visok | Odobreni zadatak | Slika u svakom od 3 formata može se učitati i pojavljuje se u radnoj okolini; preuzeta datoteka otvara se u standardnom pregledniku slika. |
| F-004 | Radna okolina pohranjuje slike u strukturi mapa; korisnik može stvarati, preimenovati i brisati mape te imenovati i preimenovati datoteke. | Visok | Odobreni zadatak | Korisnik stvara ugniježđenu mapu, premješta u nju sliku, preimenuje mapu i datoteku; promjene su vidljive nakon ponovnog učitavanja. |
| F-005 | Korisnik može prikazati odabranu sliku u radnoj okolini. | Visok | Odobreni zadatak | Odabirom datoteke slika se prikazuje u pregledniku slike. |
| F-006 | Korisnik može primijeniti najmanje 5 filtara (npr. invert, grayscale, pixelate, blur, derivative). | Visok | Odobreni zadatak | Za svaki filtar vidljiv je promijenjeni rezultat na odabranoj slici. |
| F-007 | Korisnik može primijeniti najmanje 4 morfološka operatora (erosion, dilation, opening, closing). | Visok | Odobreni zadatak | Za svaki operator vidljiv je promijenjeni rezultat na odabranoj slici. |
| F-008 | Korisnik može primijeniti najmanje 3 geometrijske transformacije (npr. resize, rotate, flip). | Visok | Odobreni zadatak | Za svaku transformaciju rezultat odgovara zadanim parametrima (dimenzije, kut, os zrcaljenja). |
| F-009 | Korisnik može primijeniti najmanje jedan algoritam segmentacije slike. | Visok | Odobreni zadatak | Rezultat segmentacije prikazuje se kao nova slika. |
| F-010 | Rezultat obrade korisnik sprema kao novu datoteku ili prepisuje izvornu. | Visok | Odobreni zadatak | Nakon spremanja kao nova datoteka postoje original i rezultat; nakon prepisivanja postoji samo izmijenjena datoteka. |
| F-011 | Korisnik ima javnu stranicu s korisničkim imenom, slikom i kratkim opisom koje samo on može uređivati. | Visok | Odobreni zadatak | Vlasnik može urediti podatke; drugi korisnici ih vide, ali ne mogu mijenjati. |
| F-012 | Korisnik može dodavati, uređivati i brisati postove (rasterska slika s tekstualnim opisom) na svojoj javnoj stranici. | Visok | Odobreni zadatak | Novi post prikazuje se na stranici; nakon uređivanja prikazuje novi sadržaj; nakon brisanja više nije vidljiv. |
| F-013 | Korisnik može označiti svaki post kao privatan ili javan. | Visok | Odobreni zadatak | Privatni post vidljiv je samo vlasniku; javni post vide svi prijavljeni korisnici. |
| F-014 | Prijavljeni korisnici mogu pregledavati javne stranice drugih korisnika. | Visok | Odobreni zadatak | Prijavljeni korisnik otvara tuđu javnu stranicu i vidi samo javne postove. |
| F-015 | Korisnik može dodati u favorite pojedini post ili cijelu javnu stranicu drugog korisnika. | Srednji | Odobreni zadatak | Odabrani post ili stranica pojavljuje se na popisu favorita i može se ukloniti. |
| F-016 | Korisnik može sliku s tuđe javne stranice preuzeti lokalno ili dodati u svoju radnu okolinu. | Srednji | Odobreni zadatak | Preuzeta slika otvara se lokalno; dodana slika pojavljuje se u radnoj okolini korisnika. |
| F-017 | Radna okolina je privatna: njezin sadržaj vidljiv je samo vlasniku. | Visok | Odobreni zadatak | Drugi prijavljeni korisnik ne može dohvatiti slike ni mape tuđe radne okoline. |

## 2.2 Nefunkcijski zahtjevi

**Cilj:** Odrediti važna svojstva kvalitete i uvjete rada odobrene aplikacije na način koji tim može razumno provjeriti.

| ID | Opis | Prioritet | Izvor | Način provjere |
|----|------|-----------|-------|----------------|
| NF-01 | Aplikacija ne pohranjuje korisničke lozinke; autentifikacija se provodi isključivo vanjskim OAuth 2.0 pružateljem. | Visok | Odobreni zadatak | Pregled baze i koda: nema polja za lozinke; prijava radi samo preko OAuth-a. |
| NF-02 | Pristup zaštićenim resursima (radna okolina, privatni postovi, uređivanje profila) dopušten je samo ovlaštenom korisniku. | Visok | Odobreni zadatak | Testni scenarij: neautorizirani i tuđi zahtjevi vraćaju grešku. |
| NF-03 | Aplikacija se koristi u suvremenom web-pregledniku (Chrome, Firefox) bez dodatne instalacije. | Srednji | Procjena tima | Ručni test u najmanje dva preglednika. |
| NF-04 | Obrada slike tipične veličine (do oko 5 MP) vraća rezultat u razumnom vremenu (cilj: unutar nekoliko sekundi). | Srednji | Procjena tima | Mjerenje vremena obrade na uzorku slika; granica se potvrđuje s asistentom. |
| NF-05 | Učitane datoteke validiraju se po tipu i veličini; nepodržani formati odbijaju se uz razumljivu poruku. | Srednji | Procjena tima | Testni scenarij: upload nepodržane i prevelike datoteke. |
| NF-06 | Tajne (OAuth ključevi, pristupni podaci) ne nalaze se u repozitoriju, već u varijablama okruženja. | Visok | Pravila kolegija | Pregled repozitorija; postoji `.env.example` bez stvarnih vrijednosti. |
| NF-07 | Izvorni kod održava se na GitHubu uz Pull Requeste, Issues i verzioniranje. | Srednji | Pravila kolegija | Pregled povijesti repozitorija. |

## 2.3 Dionici i akteri

**Cilj:** Utvrditi uloge koje utječu na zahtjeve i razlikovati dionike od aktera koji komuniciraju s aplikacijom.

| ID uloge ili aktera | Odnos prema sustavu | Relevantni zahtjevi |
|---------------------|---------------------|---------------------|
| A-01 Neprijavljeni posjetitelj | Akter: može pokrenuti prijavu putem OAuth-a; nema pristup ostalim sadržajima. | F-001 |
| A-02 Prijavljeni korisnik | Akter: koristi radnu okolinu, obrađuje slike, uređuje svoju javnu stranicu i postove. | F-002 – F-013, F-017 |
| A-03 Prijavljeni korisnik kao posjetitelj | Akter: pregledava tuđe javne stranice, dodaje favorite, preuzima slike. | F-014, F-015, F-016 |
| S-01 OAuth 2.0 pružatelj identiteta | Vanjski sustav: provodi autentifikaciju. | F-001, NF-01 |
| S-02 Artic API | Vanjski sustav: izvor početnih testnih slika. | F-002 |
| D-01 Nositelj kolegija i asistent | Dionici (nisu akteri): zadaju opseg i ocjenjuju rad. | Cijeli opseg |

## 2.4 Ograničenja i pretpostavke

**Cilj:** Zabilježiti projektno specifične granice i pretpostavke koje utječu na zahtjeve ili oblikovanje, zajedno s njihovim izvorom i praktičnom posljedicom.

| ID | Tip | Opis ograničenja ili pretpostavke | Izvor | Inženjerska posljedica / Provjera |
|----|-----|-----------------------------------|-------|-----------------------------------|
| C-01 | Ograničenje | Prijava i registracija moraju se ostvariti vanjskim servisima za autentifikaciju putem OAuth 2.0. | Zadatak | Autentifikacija se projektira oko odabranog pružatelja; nema lokalnih lozinki. |
| C-02 | Ograničenje | Tim koristi React + JavaScript za frontend i FastAPI (Python) za backend. | Odluka tima | Komunikacija preko REST API-ja; obrada slike na backendu ili u pregledniku ovisi o odluci (vidi AS-01). |
| C-03 | Ograničenje | Radna okolina je privatna, a javna stranica vidljiva svim prijavljenim korisnicima i uređuje je samo vlasnik. | Zadatak | Provjera vlasništva na svakom zahtjevu. |
| C-04 | Ograničenje | Minimalni opseg obrade: 5 filtara, 4 morfološka operatora, 3 geometrijske transformacije, 1 algoritam segmentacije; najmanje 3 formata datoteka. | Zadatak | Ostvariti sve navedene alate; provjeriti u ispitivanju. |
| AS-01 | Pretpostavka | Obrada slika smije se izvoditi na backendu (Pillow/OpenCV) ili u pregledniku (ImageJS). | Procjena tima | Potvrditi s asistentom na vježbi 26.10.; odluka se bilježi u 2.5. |
| AS-02 | Pretpostavka | Za prijavu je dovoljan jedan OAuth pružatelj. | Procjena tima | Potvrditi s asistentom. |
| AS-03 | Pretpostavka | Artic API dostupan je za dohvat početnih slika; ako nije, koriste se ugrađene slike. | Procjena tima | Provjeriti dostupnost pri implementaciji; predvidjeti rezervno rješenje. |

## 2.5 Značajne promjene zahtjeva

**Cilj:** Sačuvati razlog promjena koje mijenjaju dogovoreni opseg, prioritet ili kriterije prihvaćanja.

| Datum | ID zahtjeva | Promjena i razlog | Dogovoreno s / dokaz |
|-------|-------------|-------------------|----------------------|
| | | | |

## 2.6 Sljedivost zahtjeva

**Cilj:** Osigurati dvosmjernu sljedivost — povezati zahtjeve s opisanim ponašanjem, dijelovima sustava koji ih ostvaruju te ispitivanjem ili drugom provjerom.

| ID zahtjeva | Obrazac uporabe / modul | Arhitekturna realizacija | Ispitivanje ili provjera |
|-------------|-------------------------|--------------------------|--------------------------|
| F-001 | UC-001 (na čekanju) | Modul za autentifikaciju | na čekanju |
| F-003 | UC-002 (na čekanju) | API za datoteke | na čekanju |
| F-006 – F-009 | UC-003 (na čekanju) | Modul za obradu slika | na čekanju |
| F-012 | UC-004 (na čekanju) | API za postove | na čekanju |

Nedostajuće poveznice bit će dopunjene kad nastanu obrasci uporabe, arhitektura i ispitni slučajevi.

## 2.7 Pregled zahtjeva

**Cilj:** Zabilježiti važne povratne informacije o zahtjevima i odluke koje iz njih proizlaze na formalnim kontrolnim točkama projekta.

| Kontrolna točka | Povratna informacija ili nalaz | Odluka o zahtjevu ili opsegu |
|-----------------|--------------------------------|------------------------------|
| Iteracija 1 | | |
| Demo 2 | | |
| Završni pregled | | |

---

> **Završna provjera:** Zahtjevi su aktualni, provjerljivi i povezani. Svaki važan zahtjev moguće je pratiti od njegova opisa i ponašanja preko mjesta realizacije u sustavu do odgovarajućeg ispitivanja ili druge provjere.
