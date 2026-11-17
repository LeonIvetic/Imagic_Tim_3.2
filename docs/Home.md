# Imagic — Projektna dokumentacija

**Kolegij:** [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz), Fakultet elektrotehnike i računarstva Sveučilišta u Zagrebu  
**Akademska godina:** 2026./2027.  
**Tim:** Git Happens (Grupa 3.2)  
**Nastavnik:** Vlado Sruk  
**Asistent / demonstrator:** Lovro Bosnar (asistent) 

## Pregled projekta

Imagic je web platforma za obradu rasterskih slika s mogućnošću uvoza/izvoza, pohrane u mape i javne objave slika u obliku postova. Korisnici se prijavljuju isključivo preko OAuth 2.0 pružatelja identiteta. Svaki korisnik ima privatnu radnu okolinu i javnu stranicu vidljivu ostalim prijavljenim korisnicima.

**Aplikacija i osnovno postavljanje:** [README repozitorija](../README.md)  
**Javno dostupna aplikacija:** <https://imagictim32-production.up.railway.app> (detalji u [README – Postavljanje](../README.md#postavljanje-engl-deployment))

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
| Iteracija 1 | <https://imagictim32-production.up.railway.app> | [Poveznica na video Demo 1, ako je snimljen] |
| Završni pregled | [Poveznica na završnu inačicu projekta] | [Poveznica na video završne demonstracije, ako je snimljen] |

Dokumentacija se kontinuirano ažurira kako se aplikacija razvija.

## Organizacija projekta i razvojni proces

**Način rada:** Zadaci se vode kao GitHub Issues, grupirani po milestoneovima. Rad se odvija na zasebnim granama uz Pull Request i pregled najmanje jednog člana tima. Tim se sastaje jednom tjedno, uživo ili preko WhatsAppa, te na laboratorijskim vježbama s asistentom; bilješke sa sastanaka spremaju se u `docs/meeting-notes/`.  
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
| Claude (Anthropic) | Claude Sonnet 5.5 | Leon Ivetić | Nacrt strukture repozitorija |
| Claude (Anthropic) | Claude Opus 5.5 (Claude Code) | Leon Ivetić | Izrada CSS-a i izgleda početne (login) stranice frontenda |
| Claude (Anthropic) | Claude Sonnet 5.5 | Feđa Mitić | Prijava na backendu |
| Claude (Anthropic) | Claude Opus 5.5 (Claude Code) | Leon Ivetić | Konfiguracija javnog postavljanja (Docker, Railway), upute za postavljanje, bilješke sa sastanka 16.11.2026. i pregled dokumentacije |

### Opseg doprinosa umjetne inteligencije

| Stranica, datoteka ili artefakt | Vrsta pomoći | Što je alat proizveo | Što je tim zadao i promijenio | Lokacija |
|---------------------------------|--------------|----------------------|-------------------------------|----------|
| README.md, docs/Home.md | Izrada nacrta | Prvu inačicu teksta prema predlošku | Tim je zadao projektni zadatak i naziv tima; [dopuniti što je tim izmijenio] | Repozitorij |
| docs/1-Projekt.md, docs/2-Analiza-zahtjeva.md | Izrada nacrta | Zahtjeve izvedene iz projektnog zadatka | [dopuniti što je tim ispravio ili dodao] | Repozitorij |
| `frontend/src/index.css`, `frontend/src/App.css`, fontovi u `frontend/index.html` | Generiranje koda | CSS stilove (paleta boja, tipografija, gumbi, login stranica, responzivnost) | Leon Ivetić zadao upute te popravio greške | Commit `1e0b44d` |
|`backend/app/auth.py`, `backend/app/users.py`, routeri u `backend/app/main.py` | Generiranje koda | Učitavanje varijabli iz .env, PyJWKClient, verify_token, HTTPBearer, get_current_user. | Leon Ivetić je zadao upute, Feđa Mitić je primijenio kod i ispravio greške | Repozitorij |
| `Dockerfile`, `.dockerignore`, posluživanje frontenda u `backend/app/main.py`, `normalize_db_url` u `backend/app/db.py`, `backend/alembic/env.py` | Generiranje koda | Docker image u dvije faze, posluživanje izgrađenog Reacta iz FastAPI-ja, pretvorba adrese baze za Railway | Leon Ivetić je odabrao platformu, zadao upute, lokalno provjerio Docker image i postavio aplikaciju na Railway i Auth0 | PR #48 |
| `docs/6-Postavljanje-instalacija-i-konfiguracija.md` (6.3), `README.md` (Postavljanje) | Izrada teksta | Upute za javno postavljanje i opis arhitekture postavljanja | Leon Ivetić je zadao opseg i upisao javnu domenu | PR #49 |
| `docs/meeting-notes/2026-11-16-generalna-proba.md` | Izrada teksta | Bilješke prema predlošku prijašnjih sastanaka | Leon Ivetić je zadao podjelu posla i odluku o pohrani slika | Repozitorij |
| Cijela dokumentacija (`README.md`, `docs/`) | Pregled i ispravak | Popis proturječja dokumentacije i koda te ispravci (stanje projekta, zahtjevi i sljedivost, arhitektura i model podataka) | Leon Ivetić je pregledao i prihvatio izmjene | Grana `docs/pregled-dokumentacije` |

Stranice i artefakti koji nisu navedeni iznad izrađeni su bez pomoći generativne umjetne inteligencije.

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
