# Imagic

Imagic je web platforma koja korisnicima omogućuje obradu rasterskih slika te njihovu pohranu, organizaciju u mape i javnu objavu u obliku postova.

**Projekt na kolegiju:** Ovu je aplikaciju razvio studentski tim **Git Happens** u sklopu kolegija [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz) na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu (FER).

## Opis aplikacije

Imagic je namijenjen korisnicima koji žele jednostavno obraditi rasterske slike u pregledniku, spremiti ih u vlastitu privatnu radnu okolinu i po želji objaviti na javnoj stranici. Prijava se obavlja isključivo preko vanjskih OAuth 2.0 pružatelja identiteta.

**Trenutačno stanje:** projekt je u početnoj fazi. Postavljeni su repozitorij, dokumentacija i početni zadaci (Issues); razvoj aplikacije je započet. Dolje navedene funkcionalnosti su **planirane** prema projektnom zadatku, a ne već ostvarene.

**Ključne funkcionalnosti (planirano)**

- Privatna radna okolina: upload/download slika (min. 3 formata), mape i datoteke, prikaz slike.
- Obrada slika: filtri, morfološki operatori, geometrijske transformacije i segmentacija; rezultat se sprema kao nova datoteka ili prepisuje original.
- Javna stranica: profil korisnika i postovi sa slikom i opisom (javni ili privatni), favoriti te preuzimanje tuđih slika u svoju radnu okolinu.

Za potpuni opseg, zahtjeve, oblikovanje i dokaze ispitivanja pogledajte [docs](docs/Home.md).

## Postavljanje (engl. deployment)

**Javno dostupna aplikacija:** [još nije postavljena]

**Isprobajte:** [bit će dopunjeno kad aplikacija bude postavljena]

**Demonstracija:** Prijava je moguća samo putem OAuth 2.0 pružatelja identiteta; zasebni korisnički račun ne stvara se. [Dopuniti načinom pristupa za demonstratore.]

**Ograničenja:** [Dopuniti poznatim ograničenjima postavljene inačice.]

Vodič: [Postavljanje, instalacija i konfiguracija](docs/6-Postavljanje-instalacija-i-konfiguracija.md).

## Brzi početak / instalacija

**Preduvjeti:** Python 3.12 s [uv](https://docs.astral.sh/uv/) (ili `python3-venv` i `pip`), Node.js 22 s npm-om. Detalji i česte greške: [vodič za instalaciju](docs/6-Postavljanje-instalacija-i-konfiguracija.md#61-lokalna-instalacija).

```bash
git clone https://github.com/LeonIvetic/Imagic_Tim_3.2.git
cd Imagic_Tim_3.2

# Backend (terminal 1)
cd backend
uv venv .venv && source .venv/bin/activate   # ili: python3 -m venv .venv
uv pip install -r requirements.txt           # ili: pip install -r requirements.txt
cp .env.example .env
python -m app.main

# Frontend (terminal 2, iz korijena repozitorija)
cd frontend
npm install
npm run dev
```

**Adresa:** frontend <http://localhost:5173>, backend <http://localhost:8000>.

**Provjera:** <http://localhost:8000/api/health> vraća `{"status":"ok"}`; dokumentacija API-ja je na <http://localhost:8000/docs>.

**Konfiguracija:** Varijable okruženja navedene su u `backend/.env.example`; svaki član kopira ga u vlastiti `backend/.env`. Stvarne vrijednosti (npr. OAuth ključevi) nikada se ne objavljuju u repozitoriju.

## Tehnologije

| Tehnologija ili alat | Uloga u ovom projektu | Razlog uporabe ili važno ograničenje |
|----------------------|-----------------------|--------------------------------------|
| React + JavaScript | Korisničko sučelje: radna okolina, prikaz slike i alati za obradu, javne stranice. | Odluka tima; SPA koja komunicira s backendom preko REST API-ja. |
| FastAPI (Python) | Poslužiteljski API: korisnici, datoteke, mape, postovi, favoriti. | Odluka tima; REST API prema frontendu. |
| Auth0 (OAuth 2.0) | Prijava i registracija korisnika. | Zahtjev projektnog zadatka; aplikacija ne pohranjuje lozinke. |
| Pillow/OpenCV | Filtri, morfologija, geometrija, segmentacija. | Odluka tima; obrada slika izvodi se na backendu. |
| PostgreSQL | Korisnici, mape, datoteke, postovi, favoriti. | Odluka tima; relacijska baza za povezane podatke korisnika. |
| Artic API | Dohvat početnih testnih slika. | Vanjska ovisnost; aplikacija mora raditi i kad API nije dostupan. |

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

**Status licence:** Nije dodijeljena

Kod trećih strana, skupovi podataka, slike i ikone zadržavaju vlastite licence i uvjete uporabe.

## Uporaba umjetne inteligencije

Ovaj projekt slijedi FER-ova [pravila o primjerenoj uporabi umjetne inteligencije](https://www.fer.unizg.hr/_download/repository/Policy%20on%20the%20appropriate%20use%20of%20artificial%20intelligence%20at%20the%20faculty%20of%20electrical%20engineering%20and%20computing%5B1%5D.pdf).

**Izjava:** Za izradu nacrta strukture repozitorija i početnih dokumenata (README, `docs/`, popis početnih Issuea) korišten je alat Claude (Anthropic). Detaljan zapis nalazi se u [docs/Home.md](docs/Home.md#izjava-o-uporabi-umjetne-inteligencije).

## Kodeks ponašanja i podrška

Od članova tima očekuje se pridržavanje **Kodeksa ponašanja studenata** FER-a, pravila timskog rada na kolegiju i [Etičkog kodeksa IEEE-a](https://www.ieee.org/about/corporate/governance/p7-8.html). Vidi [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

Struktura dokumentacije prilagođena je predlošku kolegija Programsko inženjerstvo FER-a autora [Vlade Sruka](https://www.fer.unizg.hr/vlado.sruk), licenciranom pod [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Aplikaciju i njezin sadržaj izradio je gore navedeni studentski tim.
