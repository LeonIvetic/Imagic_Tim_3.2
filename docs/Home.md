# Imagic — Projektna dokumentacija

**Kolegij:** [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz), Fakultet elektrotehnike i računarstva Sveučilišta u Zagrebu  
**Akademska godina:** 2026./2027.  
**Tim:** Git Happens (Imagic_Tim_3.2)  
**Nastavnik:** Vlado Sruk  
**Asistent / demonstrator:** Lovro Bosnar (asistent) 

## Pregled projekta

Imagic je web platforma za obradu rasterskih slika s mogućnošću uvoza/izvoza, pohrane u mape i javne objave slika u obliku postova. Korisnici se prijavljuju isključivo preko OAuth 2.0 pružatelja identiteta. Svaki korisnik ima privatnu radnu okolinu i javnu stranicu vidljivu ostalim prijavljenim korisnicima.

**Aplikacija i osnovno postavljanje:** [README repozitorija](../README.md)  
**Javno dostupna aplikacija:** pogledajte [README – Postavljanje](../README.md#postavljanje-engl-deployment)

## Članovi tima i uloge

Ažurirani popis članova i njihovih uloga nalazi se u [README-u](../README.md#članovi-tima).

## Kazalo dokumentacije

| Stranica | Svrha |
|----------|-------|
| [1. Opseg projekta](1-Projekt.md) | Problem, cilj i granice projekta |
| [2. Analiza zahtjeva](2-Analiza-zahtjeva.md) | Zahtjevi, ograničenja i sljedivost |
| [3. Obrasci uporabe](3-Obrasci-uporabe.md) | Akteri i reprezentativne interakcije korisnika |
| [4. Arhitektura i oblikovanje](4-Arhitektura-i-oblikovanje.md) | Glavne odluke oblikovanja, struktura, podaci i ponašanje |
| [5. Ispitivanje](5-Ispitivanje.md) | Pristup ispitivanju, stvarni rezultati i poznati nedostaci |
| [6. Postavljanje, instalacija i konfiguracija](6-Postavljanje-instalacija-i-konfiguracija.md) | Lokalna instalacija, konfiguracija, javno postavljanje |
| [7. Zaključak i budući rad](7-Zakljucak-i-buduci-rad.md) | Zaključak i moguća daljnja poboljšanja |
| [A. Pregled aktivnosti grupe](A-Pregled-aktivnosti-grupe.md) | Aktivnosti tima, doprinosi i izazovi |
| [Bilješke sa sastanaka](meeting-notes/) | Zapisnici sastanaka tima i s asistentom |

## Ključne točke projekta

| Kontrolna točka | Demonstracija | Video |
|-----------------|---------------|-------|
| Iteracija 1 | [Poveznica na demonstraciju ili inačicu projekta] | [Poveznica na video Demo 1, ako je snimljen] |
| Završni pregled | [Poveznica na završnu inačicu projekta] | [Poveznica na video završne demonstracije, ako je snimljen] |

Dokumentacija se kontinuirano ažurira kako se aplikacija razvija.

## Organizacija projekta i razvojni proces

**Način rada:** Zadaci se vode kao GitHub Issues, grupirani po milestoneovima. Rad se odvija na zasebnim granama uz Pull Request i pregled najmanje jednog člana tima. Tim se sastaje [dopuniti ritam, npr. jednom tjedno]; bilješke sa sastanaka spremaju se u `docs/meeting-notes/`.  
**Praćenje trenutačnih zadataka i nedostataka:** [GitHub Issues](https://github.com/LeonIvetic/Imagic_Tim_3.2/issues)

## Pravila dokumentacije

Dokumentacija se sastoji od međusobno povezanih Markdown stranica. Obavezni UML dijagrami izrađuju se u PlantUML-u; uz izvor (`.puml`) sprema se i čitljiva slika. Pristupni podaci i druge tajne nikada se ne objavljuju u dokumentaciji.

Naš tehnološki skup (React + JavaScript, FastAPI) razlikuje se od primjera u predlošku kolegija; u dokumentaciji opisujemo ono što stvarno koristimo.

## Akademski integritet, ponašanje i licenciranje

README sadrži projektnu [izjavu o uporabi umjetne inteligencije](../README.md#uporaba-umjetne-inteligencije), informacije o [kodeksu ponašanja](../README.md#kodeks-ponašanja-i-podrška) i status licence.

## Izjava o uporabi umjetne inteligencije

Slijedi FER-ova [pravila o primjerenoj uporabi umjetne inteligencije](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf).

### Korišteni alati

| Alat | Inačica ili model | Koristio/la | Glavna svrha |
|------|-------------------|-------------|--------------|
| Claude (Anthropic) | Claude Sonnet 5.5 | Leon Ivetić [potvrditi] | Nacrt strukture repozitorija, nacrt README-a i dokumenata 1 i 2, popis početnih Issuea |

### Opseg doprinosa umjetne inteligencije

| Stranica, datoteka ili artefakt | Vrsta pomoći | Što je alat proizveo | Što je tim zadao i promijenio | Lokacija |
|---------------------------------|--------------|----------------------|-------------------------------|----------|
| README.md, docs/Home.md | Izrada nacrta | Prvu inačicu teksta prema predlošku | Tim je zadao projektni zadatak i naziv tima; [dopuniti što je tim izmijenio] | Repozitorij |
| docs/1-Projekt.md, docs/2-Analiza-zahtjeva.md | Izrada nacrta | Zahtjeve izvedene iz projektnog zadatka | [dopuniti što je tim ispravio ili dodao] | Repozitorij |

Stranice i artefakti koji nisu navedeni iznad izrađeni su bez pomoći generativne umjetne inteligencije. [Ažurirati prema stvarnoj uporabi.]

### Provjera generiranog sadržaja

| Provjera | Kako je provedena | Dokaz |
|----------|-------------------|-------|
| Činjenična točnost | [Usporedba zahtjeva s tekstom projektnog zadatka] | [Imena pregledavatelja, poveznica na PR] |
| Nema tvrdnji o neostvarenim funkcionalnostima | [Provjera da su planirane funkcionalnosti označene kao planirane] | [Poveznica] |
| Dosljednost s drugim stranicama | [Provjera ID-ova i naziva] | [Bilješka pregleda] |
| Povjerljivi sadržaj | [Potvrda da u upite nisu unesene tajne ni osobni podaci] | [Postupak] |

### Pogreške pronađene u izlazu umjetne inteligencije

| Problem | Kako je pronađen | Rješenje |
|---------|------------------|----------|
| [Upisati kad se pronađe] | [Pregled ili usporedba s aplikacijom] | [Ispravak s poveznicom] |
