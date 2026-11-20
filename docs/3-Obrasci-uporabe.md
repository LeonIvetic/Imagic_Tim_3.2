# 3. Obrasci uporabe

**Cilj:** Prikazati glavne interakcije između aktera aplikacije i sustava. Opisati kako akter ostvaruje cilj i što se događa kada važan korak ne uspije.

## 3.1 Dijagram obrazaca uporabe

**Cilj:** Prikazati granicu sustava, relevantne aktere i njihove glavne ciljeve u preglednom UML dijagramu obrazaca uporabe.

![Dijagram obrazaca uporabe](obrasci-uporabe.png)

**PlantUML izvor:** [obrasci-uporabe.puml](obrasci-uporabe.puml)

Primarni akteri (A-01, A-02) nalaze se lijevo, a vanjski sustavi s kojima Imagic komunicira (Auth0, Artic API) desno. Veza `<<include>>` označava ponašanje koje se uvijek izvodi kao dio osnovnog obrasca. UC-010 Spremanje slike u radnu okolinu zajednički je korak obrazaca UC-002, UC-003 i UC-011. Veza `<<extend>>` označava neobavezno ponašanje koje korisnik može pokrenuti iz osnovnog obrasca. Tako se iz pregleda tuđeg javnog profila (UC-005) profil ili post može dodati u favorite (UC-008), a slika iz javnog posta preuzeti (UC-009).

## 3.2 Specifikacije obrazaca uporabe

**Cilj:** Za svaki obrazac uporabe iz dijagrama objasniti cilj aktera, uobičajenu interakciju s aplikacijom i važne alternative.

Akteri su opisani u [2.3 Dionici i akteri](2-Analiza-zahtjeva.md#23-dionici-i-akteri). Alternativni tokovi označeni su korakom glavnog toka u kojem nastaju (npr. **3a** nastaje u 3. koraku). Obrasci UC-005, UC-008, UC-009 i UC-011 te morfološki operatori, geometrijske transformacije i segmentacija u UC-003 opisuju trenutačno oblikovanje; njihova realizacija je u izradi (vidi [2.6 Sljedivost zahtjeva](2-Analiza-zahtjeva.md#26-sljedivost-zahtjeva)).

### UC-001: Prijava putem OAuth 2.0

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-01 Neprijavljeni posjetitelj |
| **Sekundarni akteri** | S-01 Auth0; S-02 Artic API (samo pri prvoj prijavi) |
| **Povezani zahtjevi** | F-001, NF-01 |
| **Preduvjeti** | Korisnik je otvorio aplikaciju Imagic i nije prijavljen. |
| **Glavni uspješni tok** | 1. Korisnik odabire opciju „Prijava”.<br>2. Sustav preusmjerava korisnika na Auth0 stranicu za prijavu.<br>3. Korisnik unosi podatke za prijavu ili odabire jednog od pružatelja identiteta ponuđenih na Auth0 stranici.<br>4. Auth0 provjerava identitet korisnika i preusmjerava ga natrag u aplikaciju.<br>5. Aplikacija dohvaća pristupni token i šalje ga poslužitelju uz svaki zahtjev.<br>6. Poslužitelj provjerava valjanost tokena i traži korisnika u bazi podataka.<br>7. Budući da se korisnik prijavljuje prvi put, sustav stvara korisnički zapis i korijensku mapu te u nju sprema tri početne slike s Artic API-ja.<br>8. Sustav prikazuje korisnikovu radnu okolinu. |
| **Alternativni tokovi / Iznimke** | **2a — Auth0 nije dostupan:** Prijava se ne može dovršiti i korisnik ostaje neprijavljen.<br>**3a — Korisnik odustaje od prijave:** Korisnik prekida postupak na Auth0 stranici i ostaje neprijavljen.<br>**6a — Korisnički račun već postoji:** Sustav koristi postojeći korisnički zapis; tok se nastavlja u 8. koraku.<br>**7a — Artic API nije dostupan:** Sustav umjesto slika s Artic API-ja sprema tri ugrađene početne slike; prijava se nastavlja normalno. |
| **Posljedice (ishod)** | Korisnik je prijavljen i može pristupiti svojoj privatnoj radnoj okolini i stranici profila; nakon prve prijave u radnoj okolini ima tri početne slike. Ako prijava ne uspije ili korisnik odustane, zaštićene funkcionalnosti ostaju nedostupne. |

### UC-002: Učitavanje slike

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-002, F-016, NF-05 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je mapu u svojoj privatnoj radnoj okolini. |
| **Glavni uspješni tok** | 1. Korisnik odabire opciju „Učitaj slike”.<br>2. Korisnik odabire jednu ili više datoteka sa svojeg uređaja (ili ih povlači u radnu okolinu).<br>3. Sustav provjerava format i veličinu svake datoteke.<br>4. Sustav sprema slike u otvorenu mapu (uključuje UC-010).<br>5. Sustav prikazuje učitane slike u popisu datoteka i poruku o uspješnom učitavanju. |
| **Alternativni tokovi / Iznimke** | **2a — Korisnik odustaje:** Korisnik zatvara dijalog za odabir datoteka; ništa se ne učitava.<br>**3a — Format nije podržan ili datoteka prelazi 10 MB:** Sustav odbija tu datoteku i prikazuje razlog odbijanja; ostale odabrane datoteke učitavaju se normalno. |
| **Posljedice (ishod)** | Učitane slike dostupne su vlasniku u njegovoj privatnoj radnoj okolini. Odbijene datoteke se ne pohranjuju. |

### UC-003: Obrada slike

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-005 – F-009, F-016 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je sliku iz svoje radne okoline u pregledniku slike. |
| **Glavni uspješni tok** | 1. Korisnik odabire postupak obrade: filtar, morfološki operator, geometrijsku transformaciju ili segmentaciju.<br>2. Korisnik prema potrebi zadaje parametre postupka.<br>3. Sustav primjenjuje postupak i prikazuje rezultat; izvorna slika ostaje nepromijenjena.<br>4. Korisnik prema potrebi nastavlja obradu ponavljanjem koraka 1 – 3; sustav prikazuje popis primijenjenih postupaka.<br>5. Korisnik odabire spremanje rezultata kao nove slike i unosi njezin naziv.<br>6. Sustav sprema rezultat kao novu sliku u istu mapu (uključuje UC-010) i otvara je. |
| **Alternativni tokovi / Iznimke** | **3a — Sliku nije moguće obraditi:** Ako slika ima više stranica ili kadrova ili je datoteka oštećena, sustav prikazuje poruku i ne mijenja prikaz.<br>**4a — Poništavanje zadnjeg postupka:** Korisnik poništava zadnji primijenjeni postupak; sustav prikazuje rezultat bez njega, a nakon poništavanja prvog postupka izvornu sliku.<br>**5a — Prepisivanje izvorne slike:** Korisnik odabire prepisivanje izvornika i potvrđuje upozorenje; sustav zamjenjuje izvornu sliku rezultatom obrade, a nova slika prikazuje se i u postojećim objavama koje je koriste.<br>**5b — Odustajanje od obrade:** Korisnik odbacuje obradu; sustav ponovno prikazuje izvornu sliku i ništa ne sprema.<br>**6a — Slika je u međuvremenu izmijenjena:** Ako je izvorna slika prepisana nakon početka obrade (npr. u drugoj kartici), sustav odbija spremanje i traži od korisnika da osvježi stranicu. |
| **Posljedice (ishod)** | Nakon spremanja kao nove slike u radnoj okolini postoje izvorna slika i rezultat obrade; nakon prepisivanja izvorna slika zamijenjena je rezultatom. Ako korisnik odustane, pohranjena slika ostaje nepromijenjena. |

### UC-004: Objava posta

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-011, F-012 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je stranicu vlastitog profila. Za novi post korisnik ima barem jednu sliku u radnoj okolini. |
| **Glavni uspješni tok** | 1. Korisnik odabire opciju „Novi post”.<br>2. Korisnik odabire sliku iz svoje radne okoline i unosi opis.<br>3. Korisnik određuje vidljivost posta; početna postavka je „Privatno”.<br>4. Korisnik potvrđuje spremanje.<br>5. Sustav sprema post i prikazuje ga na stranici profila. |
| **Alternativni tokovi / Iznimke** | **1a — Uređivanje postojećeg posta:** Korisnik odabire „Uredi” na vlastitom postu, mijenja sliku, opis ili vidljivost i potvrđuje promjene; sustav sprema i prikazuje ažurirani post.<br>**1b — Brisanje postojećeg posta:** Korisnik odabire „Obriši” i potvrđuje brisanje; sustav briše post i uklanja ga sa stranice profila.<br>**4a — Korisnik odustaje:** Korisnik zatvara obrazac prije potvrde; sustav ne stvara ni ne mijenja post. |
| **Posljedice (ishod)** | Javni post dostupan je svim prijavljenim korisnicima, a privatni samo vlasniku. Nakon uređivanja prikazuje se spremljeni sadržaj, a nakon brisanja post više nije dostupan. |

### UC-005: Pregled tuđeg javnog profila i objava

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-012, F-013 |
| **Preduvjeti** | Korisnik je prijavljen. |
| **Glavni uspješni tok** | 1. Korisnik otvara popis korisnika i odabire javnu stranicu drugog korisnika.<br>2. Sustav dohvaća javne podatke profila i javne postove vlasnika stranice.<br>3. Sustav prikazuje korisničko ime, profilnu sliku, kratki opis i popis javnih postova.<br>4. Korisnik pregledava prikazani sadržaj. |
| **Alternativni tokovi / Iznimke** | **2a — Profil nije dostupan:** Sustav obavještava korisnika da traženi profil ne postoji.<br>**3a — Profil nema javnih postova:** Sustav prikazuje javne podatke profila i prazan popis postova. |
| **Posljedice (ishod)** | Prikazani su javni podaci profila i javni postovi; privatni postovi ostaju vidljivi samo vlasniku. |

### UC-006: Organizacija slika u radnoj okolini

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-002 – F-004, F-016 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je svoju privatnu radnu okolinu. Za radnju nad postojećom slikom ili mapom ta stavka postoji u radnoj okolini. |
| **Glavni uspješni tok** | 1. Korisnik otvara mapu u kojoj želi stvoriti novu mapu.<br>2. Korisnik odabire „Nova mapa”, upisuje naziv i potvrđuje unos.<br>3. Sustav stvara mapu i ažurira prikaz radne okoline.<br>4. Korisnik odabire sliku i pokreće premještanje.<br>5. Korisnik odabire odredišnu mapu iz stabla mapa i potvrđuje premještanje.<br>6. Sustav sprema novi položaj slike i prikazuje je u odredišnoj mapi. |
| **Alternativni tokovi / Iznimke** | **2a — Mapa istog naziva već postoji:** Sustav odbija stvaranje i prikazuje poruku; korisnik može upisati drugi naziv.<br>**4a — Preimenovanje slike ili mape:** Korisnik unosi novi naziv i potvrđuje promjenu; kod slike se mijenja samo naziv, a nastavak ostaje usklađen s formatom slike.<br>**4b — Premještanje mape:** Korisnik premješta mapu u drugu mapu; sustav ne dopušta premještanje mape u nju samu ili njezinu podmapu.<br>**4c — Brisanje slike:** Korisnik potvrđuje brisanje; sustav briše sliku i postove koji je koriste.<br>**4d — Brisanje mape:** Korisnik potvrđuje brisanje; sustav briše mapu sa svim podmapama i slikama. Korijensku mapu nije moguće obrisati.<br>**4e — Pregled slike:** Korisnik otvara sliku; sustav je prikazuje u pregledniku slike s podacima o formatu, dimenzijama i veličini.<br>**4f — Preuzimanje slike:** Korisnik odabire „Preuzmi”; sustav šalje izvornu datoteku pod nazivom slike.<br>**5a — Slika istog naziva postoji u odredišnoj mapi:** Sustav odbija premještanje ili preimenovanje i prikazuje poruku.<br>**5b — Korisnik odustaje:** Korisnik zatvara dijalog prije potvrde; promjena se ne sprema. |
| **Posljedice (ishod)** | Spremljena struktura mapa, nazivi i položaji slika vidljivi su pri sljedećem otvaranju radne okoline. Nakon preuzimanja korisnik ima lokalnu kopiju slike. |

### UC-007: Uređivanje vlastitog profila

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-010 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je stranicu vlastitog profila. |
| **Glavni uspješni tok** | 1. Korisnik odabire „Uredi profil”.<br>2. Sustav prikazuje obrazac s trenutačnim podacima profila.<br>3. Korisnik mijenja jedan ili više podataka: korisničko ime, ime za prikaz, opis ili URL profilne slike.<br>4. Korisnik potvrđuje spremanje.<br>5. Sustav provjerava i sprema izmjene.<br>6. Sustav prikazuje ažurirane podatke na stranici profila i u zaglavlju aplikacije. |
| **Alternativni tokovi / Iznimke** | **4a — Korisnik odustaje:** Korisnik zatvara obrazac; sustav prikazuje prethodno spremljene podatke.<br>**5a — Korisničko ime je zauzeto:** Sustav prikazuje poruku da je ime zauzeto i ne sprema izmjene; korisnik može unijeti drugo ime i ponoviti 4. korak.<br>**5b — Neispravni podaci:** Ako korisničko ime sadrži nedopuštene znakove ili URL slike ne počinje s `http://` ili `https://`, sustav prikazuje razlog i ne sprema izmjene. |
| **Posljedice (ishod)** | Spremljeni podaci prikazuju se na stranici profila. Podatke profila može mijenjati samo njegov vlasnik. |

### UC-008: Upravljanje favoritima

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-014 |
| **Veza s drugim obrascima** | Proširuje (`<<extend>>`) UC-005: dodavanje u favorite pokreće se tijekom pregleda tuđeg javnog profila ili posta (UC-005, 4. korak). Popisu favorita korisnik može pristupiti i izravno. |
| **Preduvjeti** | Korisnik je prijavljen. Za dodavanje je otvoren javni profil drugog korisnika ili njegov javni post; za uklanjanje stavka je na popisu favorita. |
| **Glavni uspješni tok** | 1. Korisnik otvara javni profil drugog korisnika ili njegov javni post.<br>2. Korisnik odabire dodavanje profila ili posta u favorite.<br>3. Sustav sprema stavku na korisnikov popis favorita.<br>4. Korisnik otvara popis favorita i vidi spremljenu stavku. |
| **Alternativni tokovi / Iznimke** | **3a — Sadržaj više nije javan ili je uklonjen:** Sustav odbija dodavanje i prikazuje obavijest.<br>**4a — Uklanjanje iz favorita:** Korisnik na popisu favorita odabire uklanjanje stavke; sustav je uklanja i ažurira popis. |
| **Posljedice (ishod)** | Nakon dodavanja stavka je na popisu favorita, a nakon uklanjanja više nije. |

### UC-009: Preuzimanje tuđe javne slike

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Povezani zahtjevi** | F-015 |
| **Veza s drugim obrascima** | Proširuje (`<<extend>>`) UC-005: preuzimanje se pokreće tijekom pregleda tuđeg javnog posta (UC-005, 4. korak). Spremanje kopije u radnu okolinu (1a) nije dio glavnog toka, pa obrazac ne uključuje UC-010. |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je javni post drugog korisnika. |
| **Glavni uspješni tok** | 1. Korisnik odabire preuzimanje slike iz javnog posta.<br>2. Sustav provjerava je li post još uvijek javan i je li slika dostupna.<br>3. Sustav šalje datoteku pregledniku.<br>4. Korisnik sprema datoteku na svoj uređaj. |
| **Alternativni tokovi / Iznimke** | **1a — Dodavanje u vlastitu radnu okolinu:** Korisnik odabire dodavanje slike u svoju radnu okolinu; nakon provjere dostupnosti sustav sprema kopiju slike i prikazuje je u korisnikovoj radnoj okolini.<br>**2a — Slika više nije dostupna:** Ako je post obrisan ili je postao privatan, sustav odbija zahtjev i obavještava korisnika. |
| **Posljedice (ishod)** | Korisnik ima lokalnu kopiju slike ili kopiju u svojoj privatnoj radnoj okolini; izvorni post ostaje nepromijenjen. |

### UC-010: Spremanje slike u radnu okolinu

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | Nema izravnog aktera; obrazac je uključen (`<<include>>`) u UC-002, UC-003 i UC-011. |
| **Povezani zahtjevi** | F-002, F-009, F-016, NF-05 |
| **Preduvjeti** | Korisnik je prijavljen. Osnovni obrazac predao je sadržaj slike, njezin naziv i odredišnu mapu. |
| **Glavni uspješni tok** | 1. Sustav provjerava pripada li odredišna mapa prijavljenom korisniku.<br>2. Sustav provjerava format slike prema stvarnom sadržaju datoteke (JPEG, PNG, TIFF ili WebP) te njezinu veličinu.<br>3. Sustav usklađuje nastavak naziva s formatom (npr. `slika.jpg` koja je zapravo PNG sprema se kao `slika.png`); ako u mapi već postoji slika istog naziva, dodaje sufiks (npr. `slika (1).png`).<br>4. Sustav sprema datoteku na disk poslužitelja i u bazi bilježi naziv, format, veličinu i mapu.<br>5. Sustav vraća podatke o spremljenoj slici osnovnom obrascu. |
| **Alternativni tokovi / Iznimke** | **1a — Mapa ne pripada korisniku ili ne postoji:** Sustav odbija spremanje jednako kao za nepostojeću mapu, pa se ne otkriva postoji li tuđa mapa.<br>**2a — Datoteka nije podržana slika, prazna je, veća od 10 MB ili ima previše piksela:** Sustav ne sprema datoteku i osnovnom obrascu vraća razlog odbijanja. |
| **Posljedice (ishod)** | Slika je spremljena i vidljiva samo vlasniku u njegovoj radnoj okolini. Ako spremanje ne uspije, ne nastaje nova slika. |

### UC-011: Dodavanje djela iz Artic galerije

| Element specifikacije | Opis |
| :--- | :--- |
| **Primarni akter** | A-02 Prijavljeni korisnik |
| **Sekundarni akteri** | S-02 Artic API |
| **Povezani zahtjevi** | F-017 |
| **Preduvjeti** | Korisnik je prijavljen i otvorio je stranicu Artic galerije. |
| **Glavni uspješni tok** | 1. Korisnik upisuje pojam za pretragu.<br>2. Sustav šalje upit Artic API-ju i prikazuje pronađena djela iz javne domene s pregledom slike i nazivom.<br>3. Korisnik odabire djelo i dodavanje u radnu okolinu.<br>4. Sustav dohvaća sliku djela s Artic API-ja.<br>5. Sustav sprema sliku u korisnikovu radnu okolinu (uključuje UC-010).<br>6. Sustav obavještava korisnika da je djelo dodano. |
| **Alternativni tokovi / Iznimke** | **2a — Artic API nije dostupan:** Sustav prikazuje poruku da galerija trenutačno nije dostupna; radna okolina ostaje nepromijenjena.<br>**2b — Nema rezultata:** Sustav prikazuje poruku da za zadani pojam nije pronađeno nijedno djelo.<br>**3a — Korisnik odustaje:** Korisnik napušta galeriju bez dodavanja djela. |
| **Posljedice (ishod)** | Nakon uspješnog dodavanja slika djela nalazi se u korisnikovoj privatnoj radnoj okolini; inače radna okolina ostaje nepromijenjena. |

---

## 3.3 Provjera dosljednosti obrazaca uporabe

**Cilj:** Provjeriti međusobnu usklađenost obrazaca uporabe, aktera, zahtjeva i ispitnih slučajeva. Cjelovito mapiranje održava se isključivo u [matrici sljedivosti zahtjeva](2-Analiza-zahtjeva.md#26-sljedivost-zahtjeva).

| Provjera | Pitanje za tim |
| --- | --- |
| Zahtjev | Je li svaki važan obrazac uporabe povezan s postojećim zahtjevom? |
| Akter | Odgovara li akter naveden u obrascu utvrđenoj ulozi i dopuštenim interakcijama? |
| Dijagram | Podudaraju li se nazivi obrazaca i njihovi akteri u specifikacijama i dijagramu? |
| Aplikacija | Može li tim demonstrirati opisani glavni tok i važne alternative ili je opis jasno označen kao trenutačno oblikovanje? |
