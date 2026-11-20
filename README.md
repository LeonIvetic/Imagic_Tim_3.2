# Imagic

Imagic je web platforma koja korisnicima omogućuje obradu rasterskih slika te njihovu pohranu, organizaciju u mape i javnu objavu u obliku postova.

**Projekt na kolegiju:** Ovu je aplikaciju razvio studentski tim **Git Happens** u sklopu kolegija [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz) na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu (FER).

## Opis aplikacije

Imagic je namijenjen korisnicima koji žele jednostavno obraditi rasterske slike u pregledniku, spremiti ih u vlastitu privatnu radnu okolinu i po želji objaviti na javnoj stranici. Prijava se obavlja isključivo preko vanjskih OAuth 2.0 pružatelja identiteta.

**Trenutačno stanje (studeni 2026.):** aplikacija je javno postavljena i ostvaren je dio funkcionalnosti; ostatak je u izradi.

**Ostvareno**

- Prijava putem Auth0 (OAuth 2.0); pri prvoj prijavi korisnik dobiva korijensku mapu i 3 početne slike s Artic API-ja (ako API nije dostupan, koriste se ugrađene slike).
- Privatna radna okolina: ugniježđene mape (stvaranje, preimenovanje, brisanje), upload i download slika u formatima JPEG, PNG, TIFF i WebP (do 10 MB), preimenovanje, premještanje i brisanje slika, prikaz slike (TIFF se za prikaz pretvara u PNG).
- Obrada slika: 5 filtara (grayscale, invert, pixelate, blur, derivative) koji se mogu primjenjivati uzastopno, uz pregled rezultata, poništavanje zadnjeg filtra te spremanje rezultata kao nove slike ili prepisivanje izvorne.
- Javna stranica: uređivanje profila (korisničko ime, ime za prikaz, opis, URL slike) te stvaranje, uređivanje i brisanje postova s oznakom javan/privatan.

**U izradi**

- Obrada slika: morfološki operatori, geometrijske transformacije i segmentacija.
- Pregled javnih stranica drugih korisnika, favoriti te preuzimanje tuđih slika lokalno ili u svoju radnu okolinu.
- Galerija i pretraga djela s Artic API-ja.

Za potpuni opseg, zahtjeve, oblikovanje i dokaze ispitivanja pogledajte [docs](docs/Home.md).

## Postavljanje (engl. deployment)

**Javno dostupna aplikacija:** <https://imagictim32-production.up.railway.app>

**Isprobajte:** prijavite se i otvorite jednu od početnih slika u radnoj okolini, primijenite nekoliko filtara i spremite rezultat kao novu sliku; zatim je na stranici „Moj profil” objavite kao javni post.

**Platforma:** [Railway](https://railway.com). Frontend i backend postavljeni su kao jedan Docker servis (FastAPI poslužuje i API i izgrađeni React), uz PostgreSQL bazu i volume za slike. Svaki merge na `master` automatski pokreće novo postavljanje.

**Demonstracija:** Prijava je moguća samo putem OAuth 2.0 pružatelja identiteta (Auth0); zasebni korisnički račun ne stvara se. Pri prvoj prijavi automatski se stvaraju korisnik i njegova radna okolina.

**Ograničenja:** Slike se spremaju na disk servisa (Railway volume), a ne na vanjski servis za pohranu, što je dogovoreno s asistentom za prvu predaju. Aplikacija radi na probnom planu Railwaya.

Upute za postavljanje i lokalnu provjeru Docker imagea: [docs/6.3 Javno postavljanje i administracija](docs/6-Postavljanje-instalacija-i-konfiguracija.md#63-javno-postavljanje-i-administracija).

## Brzi početak / instalacija

**Preduvjeti:** Python 3.12 s [uv](https://docs.astral.sh/uv/) (ili `python3-venv` i `pip`), Node.js 22 s npm-om, Docker. Detalji i česte greške: [vodič za instalaciju](docs/6-Postavljanje-instalacija-i-konfiguracija.md#62-lokalna-instalacija-i-konfiguracija).

```bash
git clone https://github.com/LeonIvetic/Imagic_Tim_3.2.git
cd Imagic_Tim_3.2

# Baza (iz korijena repozitorija)
docker compose up -d

# Backend (terminal 1)
cd backend
uv venv .venv && source .venv/bin/activate   # ili: python3 -m venv .venv
uv pip install -r requirements.txt           # ili: pip install -r requirements.txt
cp .env.example .env                         # samo prvi put
alembic upgrade head                         # stvara/ažurira tablice
python -m app.main

# Frontend (terminal 2, iz korijena repozitorija)
cd frontend
npm install
cp .env.example .env                         # samo prvi put
npm run dev
```

Nakon svake promjene u `.env` server treba ponovno pokrenuti jer se `.env` čita samo pri pokretanju.

**Adresa:** frontend <http://localhost:5173>, backend <http://localhost:8000>.

**Provjera:** <http://localhost:8000/api/health> vraća `{"status":"ok"}`; dokumentacija API-ja je na <http://localhost:8000/docs>.

**Konfiguracija:** Backend i frontend imaju svaki svoju datoteku s varijablama okruženja: `backend/.env.example` i `frontend/.env.example`. Svaki član ih kopira u vlastite `backend/.env` i `frontend/.env`, koje Git ignorira. Tajne vrijednosti nikada se ne objavljuju u repozitoriju. Popis varijabli nalazi se u [docs/6.2](docs/6-Postavljanje-instalacija-i-konfiguracija.md#62-lokalna-instalacija-i-konfiguracija).

## Tehnologije

| Tehnologija ili alat | Uloga u ovom projektu | Razlog uporabe ili važno ograničenje |
|----------------------|-----------------------|--------------------------------------|
| React + JavaScript | Korisničko sučelje: radna okolina, prikaz slike i alati za obradu, javne stranice. | Odluka tima; SPA koja komunicira s backendom preko REST API-ja. |
| FastAPI (Python) | Poslužiteljski API: korisnici, mape, slike, obrada slika i postovi. | Odluka tima; REST API prema frontendu. |
| Auth0 (OAuth 2.0) | Prijava i registracija korisnika. | Zahtjev projektnog zadatka; aplikacija ne pohranjuje lozinke. |
| Pillow | Prepoznavanje formata učitanih slika, pretvaranje TIFF-a u PNG za prikaz i 5 filtara; morfologija, geometrija i segmentacija su u izradi. | Odluka tima; obrada slika izvodi se na backendu. |
| PostgreSQL + SQLAlchemy + Alembic | Korisnici, mape, slike i postovi (tablice za favorite već postoje); migracije sheme. | Odluka tima; relacijska baza za povezane podatke korisnika. |
| Artic API | Dohvat 3 početne testne slike pri prvoj prijavi. | Vanjska ovisnost; ako API nije dostupan, koriste se ugrađene slike. |
| Docker + Railway | Javno postavljanje: jedan Docker image (FastAPI + izgrađeni React), PostgreSQL i volume za slike. | Automatsko postavljanje pri svakom mergeu na `master`; vidi [docs/6.3](docs/6-Postavljanje-instalacija-i-konfiguracija.md#63-javno-postavljanje-i-administracija). |

## Članovi tima

| Član | Glavna uloga ili doprinos |
|------|---------------------------|
| Leon Ivetić | Voditelj tima Full-Stack |
| Florijan Blažeka | Frontend |
| Roko Vrdoljak| Backend |
| Feđa Mitić| Backend|
| Lorena Ivanković| Backend |
| Mihaela Miljavac | Backend |
| Alan Ivanković | Baza |

## Doprinos projektu

Zadaci i nedostaci vode se u [GitHub Issues](https://github.com/LeonIvetic/Imagic_Tim_3.2/issues). Promjene koda ulaze preko Pull Requesta uz pregled najmanje jednog člana tima; svaki PR veže se na Issue. Bilješke sa sastanaka nalaze se u [docs/meeting-notes](docs/meeting-notes/).

**Status licence:** Projektu nije dodijeljena licenca koja dopušta javnu ponovnu uporabu koda.

Kod trećih strana, skupovi podataka, slike i ikone zadržavaju vlastite licence i uvjete uporabe.

## Uporaba umjetne inteligencije

Ovaj projekt slijedi FER-ova [pravila o primjerenoj uporabi umjetne inteligencije](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf).

**Izjava:** Za izradu nacrta strukture repozitorija i početnih dokumenata (README, `docs/`, popis početnih Issuea) korišten je alat Claude (Anthropic). Isti alat korišten je i za izradu CSS-a i izgleda početne (login) stranice frontenda, za dio prijave na backendu, za konfiguraciju javnog postavljanja (Docker, Railway), kao opća pomoć pri pisanju koda i otklanjanju grešaka (debugiranju) te za pregled i usklađivanje dokumentacije s kodom. Detaljan zapis nalazi se u [docs/Home.md](docs/Home.md#izjava-o-uporabi-umjetne-inteligencije).

## Kodeks ponašanja i podrška

Od članova tima očekuje se pridržavanje **Kodeksa ponašanja studenata** FER-a, pravila timskog rada na kolegiju i [Etičkog kodeksa IEEE-a](https://www.ieee.org/about/corporate/governance/p7-8.html). Vidi [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

Struktura dokumentacije prilagođena je predlošku kolegija Programsko inženjerstvo FER-a autora [Vlade Sruka](https://www.fer.unizg.hr/vlado.sruk), licenciranom pod [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Aplikaciju i njezin sadržaj izradio je gore navedeni studentski tim.
