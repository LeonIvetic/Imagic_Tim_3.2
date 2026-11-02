# 3. Obrasci uporabe

**Cilj:** Opisati aktere i reprezentativne interakcije korisnika sa sustavom.

>UML dijagrami izrađuju se u PlantUML-u (izvor `.puml` + slika).

## 3.1 Akteri

Vidi [2.3 Dionici i akteri](2-Analiza-zahtjeva.md#23-dionici-i-akteri).

## 3.2 Popis obrazaca uporabe

| ID | Naziv | Akter | Povezani zahtjevi |
|----|-------|-------|-------------------|
| UC-001 | Prijava putem OAuth 2.0 | Neprijavljeni posjetitelj | F-001 |
| UC-002 | Upload i organizacija slika | Prijavljeni korisnik | F-002 – F-004, F-016 |
| UC-003 | Obrada slike | Prijavljeni korisnik | F-005 – F-009 |
| UC-004 | Objava posta | Prijavljeni korisnik | F-010 – F-012 |
| UC-005 | Pregled tuđe stranice i favoriti | Prijavljeni korisnik | F-013 – F-016 |

## 3.3 Opisi obrazaca uporabe

### UC-001 Prijava putem OAuth 2.0

**Preduvjeti:**
- korisnik je otvorio aplikaciju Imagic
- korisnik nije prijavljen

**Glavni tijek:**
1. Korisnik odabire opciju „Prijava”.
2. Sustav preusmjerava korisnika na Auth0 stranicu za prijavu.
3. Korisnik unosi svoje podatke za prijavu ili odabire prijavu putem Google računa.
4. Auth0 provjerava identitet korisnika.
5. Nakon uspješne autentifikacije korisnik se preusmjerava natrag u aplikaciju Imagic.
6. Aplikacija dohvaća pristupni token i šalje ga backendu radi provjere.
7. Backend provjerava valjanost tokena i traži korisnika u bazi podataka.
8. Ako korisnik ne postoji u bazi, sustav stvara njegov korisnički zapis i dodjeljuje mu tri početne slike.
9. Sustav prikazuje prijavljenom korisniku njegovu radnu okolinu.

**Alternativni tijekovi:**

A1 - Korisnik odustaje od prijave
1. Korisnik odustaje od prijave na Auth0 stranici.
2. Korisnik ostaje neprijavljen i nema pristup zaštićenim funkcionalnostima.

A2 - Auth0 nije dostupan
1. Sustav ne može uspostaviti vezu s Auth0 uslugom.
2. Prijava se ne može dovršiti pa korisnik ostaje neprijavljen.

A3 - Korisnički račun već postoji
1. Sustav pronalazi postojeći korisnički račun u bazi podataka.
2. Korisnik se uspješno prijavljuje i pristupa svojoj radnoj okolini.

**Postuvjeti:**
- nakon uspješne prijave korisnik ima pristup svojoj privatnoj radnoj okolini i javnoj stranici profila
- ako je riječ o prvoj prijavi, stvoren je korisnički račun te su korisniku dodijeljene tri početne slike
- ako prijava nije uspjela ili je korisnik odustao, ostaje neprijavljen i nema pristup zaštićenim funkcionalnostima

### UC-002 Upload i organizacija slika

**Preduvjeti:**

- korisnik je prijavljen u aplikaciju Imagic
- korisnik je otvorio svoju privatnu radnu okolinu

**Glavni tijek:**

1. Korisnik odabire opciju za učitavanje slike.
2. Korisnik odabire datoteku sa svojeg uređaja i potvrđuje učitavanje.
3. Sustav provjerava tip i veličinu odabrane datoteke.
4. Sustav pohranjuje sliku u korisnikovu privatnu radnu okolinu i prikazuje je u popisu datoteka.
5. Korisnik prema potrebi organizira sadržaj radne okoline stvaranjem ili brisanjem mapa, preimenovanjem datoteka ili mapa te premještanjem slika u mape.
6. Sustav sprema odabrane promjene i ažurira prikaz radne okoline.

**Alternativni tijekovi:**

A1 – Korisnik odustaje od učitavanja

1. Korisnik odustaje prije potvrde učitavanja.
2. Nova datoteka nije dodana u radnu okolinu.

A2 – Nepodržani format ili prevelika datoteka

1. Sustav utvrđuje da format datoteke nije podržan ili da datoteka prelazi dopuštenu veličinu.
2. Sustav odbija učitavanje i prikazuje poruku o razlogu odbijanja.

A3 – Rad s postojećim slikama i mapama

1. Korisnik umjesto učitavanja nove slike odabire rad s postojećim sadržajem svoje radne okoline.
2. Korisnik odabire jednu od radnji:
   - stvara novu mapu unosom naziva i odabirom njezina položaja, uključujući unutar postojeće mape
   - preimenuje odabranu datoteku ili mapu unosom novog naziva
   - premješta odabranu sliku u odredišnu mapu
   - briše odabranu mapu
   - odabire sliku za prikaz, nakon čega je sustav prikazuje u pregledniku slike
   - odabire sliku za preuzimanje, nakon čega sustav omogućuje njezino preuzimanje na korisnikov uređaj u podržanom formatu.
3. Ako odabrana radnja mijenja sadržaj radne okoline, sustav sprema promjene i ažurira prikaz.
4. Korisnik prema potrebi ponavlja postupak.

**Postuvjeti:**

- nakon uspješnog učitavanja slika je pohranjena u korisnikovoj privatnoj radnoj okolini
- provedene promjene u strukturi mapa, nazivima i položaju slika spremljene su i vidljive nakon ponovnog učitavanja
- nakon uspješnog prikaza odabrana slika prikazana je u pregledniku slike
- nakon uspješnog preuzimanja korisnik ima lokalnu kopiju slike
- ako korisnik odustane od učitavanja ili sustav odbije datoteku, nova datoteka nije pohranjena
- sadržaj radne okoline dostupan je samo njezinu vlasniku


### UC-003 Obrada slike

**Preduvjeti:**

- korisnik je prijavljen u aplikaciju Imagic
- korisnik je odabrao sliku u svojoj privatnoj radnoj okolini

**Glavni tijek:**

1. Korisnik odabire postupak obrade slike: filtar, morfološki operator, geometrijsku transformaciju ili segmentaciju.
2. Korisnik prema potrebi zadaje parametre odabranog postupka.
3. Sustav primjenjuje odabrani postupak i prikazuje rezultat obrade.
4. Korisnik prema potrebi nastavlja obrađivati sliku ponavljanjem koraka 1. – 3.
5. Korisnik odabire spremanje rezultata kao nove datoteke i unosi njezin naziv.
6. Sustav pohranjuje rezultat kao novu datoteku u korisnikovoj radnoj okolini, uz očuvanje izvorne slike.

**Alternativni tijekovi:**

A1 – Prepisivanje izvorne slike

1. U 5. koraku korisnik umjesto spremanja u novu datoteku odabire prepisivanje izvorne slike.
2. Sustav sprema rezultat obrade umjesto izvorne slike.

A2 – Odustajanje od spremanja

1. Korisnik završava obradu bez spremanja rezultata.
2. Izvorna datoteka ostaje nepromijenjena, a rezultat obrade nije pohranjen.

**Postuvjeti:**

- nakon spremanja u novu datoteku u radnoj okolini postoje izvorna slika i rezultat obrade
- nakon prepisivanja izvorna datoteka zamijenjena je rezultatom obrade
- ako korisnik ne spremi rezultat, pohranjena izvorna datoteka ostaje nepromijenjena
- rezultat obrade u privatnoj radnoj okolini dostupan je samo vlasniku

### UC-004 Objava posta

**Preduvjeti:**

- korisnik je prijavljen u aplikaciju Imagic
- korisnik je otvorio svoju javnu stranicu
- za objavu novog posta korisnik ima sliku u svojoj radnoj okolini

**Glavni tijek:**

1. Korisnik odabire opciju za dodavanje novog posta.
2. Korisnik odabire sliku iz svoje radne okoline i unosi tekstualni opis.
3. Korisnik određuje hoće li post biti javan ili privatan.
4. Korisnik potvrđuje objavu.
5. Sustav sprema post i prikazuje ga na korisnikovoj stranici.
6. Javni post dostupan je svim prijavljenim korisnicima, a privatni samo vlasniku.

**Alternativni tijekovi:**

A1 – Korisnik odustaje od objave

1. Korisnik odustaje prije potvrde objave.
2. Sustav ne stvara novi post.

A2 – Uređivanje postojećeg posta

1. Korisnik umjesto dodavanja novog posta odabire vlastiti postojeći post i opciju za uređivanje.
2. Korisnik uređuje sadržaj posta ili mijenja njegovu oznaku javnosti.
3. Korisnik potvrđuje promjene.
4. Sustav sprema promjene i prikazuje ažurirani post uz odgovarajuću vidljivost.

A3 – Brisanje postojećeg posta

1. Korisnik umjesto dodavanja novog posta odabire vlastiti postojeći post i opciju za brisanje.
2. Sustav briše post i uklanja ga s korisnikove stranice.

A4 – Uređivanje vlastitog profila bez objave novog posta

1. Korisnik umjesto dodavanja novog posta odabire opciju za uređivanje vlastitog profila.
2. Korisnik mijenja korisničko ime, sliku ili kratki opis.
3. Korisnik potvrđuje promjene.
4. Sustav sprema promjene i prikazuje ažurirane podatke na korisnikovoj javnoj stranici.

**Postuvjeti:**

- nakon uspješne objave novi post prikazan je na korisnikovoj stranici
- nakon uspješnog uređivanja post prikazuje spremljeni sadržaj i ima odabranu vidljivost
- nakon brisanja post više nije vidljiv na korisnikovoj stranici
- javni postovi vidljivi su svim prijavljenim korisnicima, a privatni samo vlasniku
- ako korisnik odustane od objave, novi post nije stvoren
- nakon uspješnog uređivanja profila ažurirani podaci prikazani su na korisnikovoj javnoj stranici
- podatke profila može uređivati samo njegov vlasnik

### UC-005 Pregled tuđe stranice i favoriti

**Preduvjeti:**

- korisnik je prijavljen u aplikaciju Imagic
- postoji javna stranica drugog korisnika

**Glavni tijek:**

1. Korisnik otvara javnu stranicu drugog korisnika.
2. Sustav prikazuje korisničko ime, sliku i kratki opis vlasnika stranice te njegove javne postove.
3. Korisnik pregledava prikazani sadržaj.
4. Korisnik odabire pojedini javni post ili cijelu javnu stranicu i dodaje ih u favorite.
5. Sustav sprema odabir i prikazuje post ili stranicu na korisnikovu popisu favorita.

**Alternativni tijekovi:**

A1 – Pregled bez dodavanja u favorite

1. Korisnik pregledava javnu stranicu i postove bez dodavanja u favorite.
2. Popis favorita ostaje nepromijenjen.

A2 – Uklanjanje iz favorita

1. Korisnik odabire post ili javnu stranicu koji se već nalaze u njegovim favoritima.
2. Korisnik odabire uklanjanje iz favorita.
3. Sustav uklanja odabrani post ili stranicu s korisnikova popisa favorita.

A3 – Preuzimanje slike na uređaj

1. Tijekom pregleda korisnik odabire sliku iz javnog posta i opciju za preuzimanje na svoj uređaj.
2. Sustav omogućuje preuzimanje odabrane slike.

A4 – Dodavanje slike u vlastitu radnu okolinu

1. Tijekom pregleda korisnik odabire sliku iz javnog posta i opciju za dodavanje u vlastitu radnu okolinu.
2. Sustav pohranjuje kopiju slike u korisnikovu privatnu radnu okolinu.
3. Dodana slika pojavljuje se u korisnikovoj radnoj okolini.

**Postuvjeti:**

- korisniku su prikazani javni podaci profila i javni postovi drugog korisnika, dok privatni postovi nisu dostupni
- nakon dodavanja u favorite odabrani post ili stranica nalaze se na korisnikovu popisu favorita
- nakon uklanjanja iz favorita odabrani post ili stranica više se ne nalaze na tom popisu
- nakon uspješnog preuzimanja korisnik ima lokalnu kopiju slike
- nakon uspješnog dodavanja u radnu okolinu korisnik ima vlastitu kopiju slike u svojoj privatnoj radnoj okolini
- sadržaj izvornog posta i stranice drugog korisnika ostaje nepromijenjen