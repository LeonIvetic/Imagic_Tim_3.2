# 1. Opseg projekta

**Cilj:** Objasniti odobreni projektni zadatak vlastitim riječima tima. Čitatelj treba razumjeti problem, ciljane korisnike, cilj projekta i njegove granice bez prethodnog čitanja detaljnih zahtjeva.

## 1.1 Problem i cilj projekta

**Cilj:** Jasno razgraničiti problem koji se rješava od predloženog rješenja i stvarne koristi za korisnika.

Osnovnu obradu rasterskih slika (filtri, geometrijske transformacije, morfološki operatori) obično je potrebno raditi u zasebnim alatima, a rezultate dijeliti drugim kanalima. Imagic ima za cilj objediniti na jednom mjestu obradu slika u pregledniku, njihovu pohranu u vlastitu privatnu radnu okolinu i javnu objavu odabranih slika s popratnim opisom. Očekivana je korist da korisnik slike može učitati, obraditi, organizirati i podijeliti bez instalacije dodatnog softvera. Brojčane tvrdnje o uštedi vremena ili učinkovitosti ne navodimo jer ih nismo izmjerili.

## 1.2 Ciljani korisnici i dionici

**Cilj:** Utvrditi osobe, uloge i organizacije čije potrebe i interesi određuju projektni zadatak.

| Skupina korisnika ili dionika | Potreba ili interes relevantan za ovaj projekt |
|-------------------------------|------------------------------------------------|
| Prijavljeni korisnik | Učitati i preuzeti rasterske slike, organizirati ih u mape, obraditi ih alatima te spremiti rezultat; objaviti slike s opisom na vlastitoj javnoj stranici. |
| Drugi prijavljeni korisnik (posjetitelj javne stranice) | Pregledavati javne stranice i postove drugih korisnika, dodavati favorite te preuzeti sliku lokalno ili u svoju radnu okolinu. |
| Vanjski pružatelj identiteta (OAuth 2.0) | Dionik koji ne koristi aplikaciju, ali određuje način prijave i registracije; aplikacija ne pohranjuje lozinke. |
| Nositelj kolegija i asistent | Dionici koji definiraju opseg zadatka i ocjenjuju rezultat; nisu akteri aplikacije. |

## 1.3 Granice projekta

**Cilj:** Jasno definirati granice sustava — što je obuhvaćeno odobrenim zadatkom, što je svjesno izostavljeno ili odgođeno te o kojim vanjskim uslugama sustav izravno ovisi.

**Uključeno:** Prijava putem OAuth 2.0; privatna radna okolina (upload/download u najmanje 3 formata, mape, imenovanje i preimenovanje, prikaz slike); obrada slika (najmanje 5 filtara, 4 morfološka operatora, 3 geometrijske transformacije i 1 algoritam segmentacije) uz spremanje kao nova datoteka ili prepis originala; javna stranica s profilom i postovima (javni/privatni); favoriti te preuzimanje tuđih slika lokalno ili u svoju radnu okolinu; 3 početne testne slike pri prvoj prijavi.

**Izvan opsega ili odgođeno:** Obrada vektorske grafike, komentari i lajkovi, pretraživanje korisnika, undo/redo te dodatni filtri i operatori iznad minimuma. Odgođeno zbog ograničenog vremena semestra; moguće kao budući rad ako ostane kapaciteta.

**Vanjske ovisnosti:** OAuth 2.0 pružatelj identiteta (npr. Google ili GitHub); Artic API (Art Institute of Chicago) za dohvat početnih testnih slika; biblioteka za obradu slika (ImageJS u pregledniku ili Pillow/OpenCV na backendu, odluka čeka potvrdu asistenta).

## 1.4 Postojeći pristupi i opravdanost projekta

**Cilj:** Objasniti kako korisnici trenutačno rješavaju problem i koja preostala potreba opravdava odobreni projekt.

Korisnici danas za obradu slika obično koriste zasebne uređivače slika, a za objavu zasebne društvene mreže ili servise za dijeljenje. Imagic povezuje oba koraka u jednu platformu s privatnom radnom okolinom i javnom stranicom, uz naglasak na alate iz područja obrade slike (npr. morfološki operatori i segmentacija). Ne tvrdimo da postojeća rješenja ne mogu obaviti ove zadatke; cilj je projekta realizirati zadani opseg kao cjelovitu web-aplikaciju. Pregled konkurentskih proizvoda nije obavezan i nije dio ovog opisa.

---

> **Završna provjera:** Opis problema, cilj projekta, korisnici i dionici, granice opsega te postojeći pristupi međusobno su usklađeni. Navedene koristi ne predstavljaju neprovjerene tvrdnje, a uključene i izostavljene funkcionalnosti odgovaraju odobrenom projektnom zadatku.
