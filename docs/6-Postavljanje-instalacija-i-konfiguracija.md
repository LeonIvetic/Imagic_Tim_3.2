# 6. Postavljanje, instalacija i konfiguracija

**Cilj:** Detaljno dokumentirati topologiju izvođenja, postupak lokalne instalacije i konfiguracije iz izvornog koda te način javnog postavljanja i administracije programa. [README](../README.md) navodi javnu adresu i sažeti postupak lokalnog pokretanja; ova stranica donosi potpun postupak.

---

## 6.1 Prikaz razmještaja

**Cilj:** Prikazati okruženja izvođenja, raspodijeljene dijelove programa, spremište podataka i relevantne vanjske usluge te njihovu komunikaciju jednim UML dijagramom razmještaja.

**Dijagram razmještaja:** [Dopuniti UML dijagram razmještaja.]  
**PlantUML izvor:** [Dopuniti.]  
**Javno dostupna aplikacija:** <https://imagictim32-production.up.railway.app>

Produkcijsko okruženje (pojednostavljeni prikaz do izrade UML dijagrama):

```
                Railway projekt
 ┌───────────────────────────────────────────────┐
 │  Servis aplikacije (Docker image)             │
 │  ┌─────────────────────────────────────────┐  │
 │  │ FastAPI (uvicorn)                       │  │      ┌──────────────┐
 │  │  /api/...  → REST API                   │──┼─────▶│  PostgreSQL  │
 │  │  ostalo    → izgrađeni React (static/)  │  │      │  (Railway)   │
 │  └─────────────────────────────────────────┘  │      └──────────────┘
 │  Volume /data → /data/uploads (slike)         │
 └───────────────────────────────────────────────┘
          ▲ HTTPS (*.up.railway.app)
          │
     Preglednik ─────────── prijava ──────────▶ Auth0
```

- Frontend i backend su **jedan servis**: FastAPI poslužuje i API (`/api/...`) i izgrađeni React. Sve rute koje nisu API vraćaju `index.html`, pa React Router radi i nakon osvježavanja stranice. Budući da su na istoj domeni, CORS nije potreban, a u Auth0 se upisuje samo jedan URL.
- **Slike** se spremaju na disk servisa, na Railway volume montiran na `/data`, pa ostaju sačuvane nakon ponovnog postavljanja i restarta. U dogovoru s asistentom slike do prve predaje ne pohranjujemo na vanjskom servisu za pohranu (vidi [bilješke sa sastanka 16.11.2026.](meeting-notes/2026-11-16-generalna-proba.md)).
- **HTTPS** osigurava Railway. Bez njega Auth0 prijava ne bi radila izvan `localhost`.
- Pri prvoj prijavi korisnika backend dohvaća 3 početne slike s **Artic API-ja** (ako nije dostupan, koriste se ugrađene slike).

---

## 6.2 Lokalna instalacija i konfiguracija

**Cilj:** Omogućiti novom članu tima ili ocjenjivaču da iz čiste radne kopije repozitorija instalira i lokalno pokrene cijeli sustav, uključujući bazu podataka i početne podatke.

**Preduvjeti:**

- Python 3.12 i [uv](https://docs.astral.sh/uv/) ili, umjesto uv-a, sistemski paketi `python3-venv` i `python3-pip`
- Node.js 22 i npm
- Docker (Docker Desktop na Windowsu/Macu)

Repozitorij:

```bash
git clone https://github.com/LeonIvetic/Imagic_Tim_3.2.git
cd Imagic_Tim_3.2
```

#### 1. Inicijalizacija baze podataka

U korijenu repozitorija:

```bash
docker compose up -d
```

PostgreSQL 16 radi u Dockeru na portu `5433` (korisnik, lozinka i baza: `imagic`). Tablice se stvaraju migracijama iz `backend/alembic/versions/` (korak 2, `alembic upgrade head`); već primijenjene migracije preskaču se, pa se naredba smije pokrenuti više puta. Početne podatke (korijensku mapu i 3 početne slike) backend stvara sam pri prvoj prijavi svakog korisnika.

Provjera: `docker compose exec db psql -U imagic -d imagic -c "\d users"`

Zaustavljanje: `docker compose down` (podaci ostaju). Brisanje i podataka: `docker compose down -v`.

#### 2. Konfiguracija i pokretanje poslužiteljskog dijela (backend)

Iz direktorija `backend/`:

```bash
uv venv .venv                        # ili: python3 -m venv .venv (samo prvi put)
source .venv/bin/activate            # u svakom novom terminalu
uv pip install -r requirements.txt   # ili: pip install -r requirements.txt
cp .env.example .env                 # samo prvi put
alembic upgrade head                 # stvara/ažurira tablice
python -m app.main
```

Backend radi na <http://localhost:8000> i automatski se ponovno pokreće pri spremanju promjena.

Varijable u `backend/.env` (predložak je `backend/.env.example`; `.env` Git ignorira):

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `FRONTEND_URL` | Adresa frontenda kojoj backend dopušta pozive (CORS). Potrebna samo lokalno; u produkciji se ne postavlja (vidi 6.3) | `http://localhost:5173` |
| `DATABASE_URL` | Adresa PostgreSQL baze iz `docker-compose.yml` | `postgresql+psycopg://imagic:imagic@localhost:5433/imagic` |
| `AUTH0_DOMAIN` | Auth0 domena, bez `https://` | vrijednost iz `.env.example` |
| `AUTH0_AUDIENCE` | Identifier našeg API-ja u Auth0 | `https://imagic-api` |
| `UPLOAD_DIR` | Mapa u koju se spremaju učitane slike | `backend/uploads` |

U predlošcima nema tajni: Auth0 domena, client ID i audience javne su vrijednosti, a lozinka baze vrijedi samo za lokalni Docker. Vrijednosti se upisuju bez navodnika i razmaka; nakon promjene server treba ponovno pokrenuti.

#### 3. Pokretanje klijentskog dijela (frontend)

U drugom terminalu, iz direktorija `frontend/`:

```bash
npm install
cp .env.example .env                 # samo prvi put
npm run dev
```

Frontend radi na <http://localhost:5173>. Vite zahtjeve na `/api/...` prosljeđuje backendu na `localhost:8000`, pa backend mora biti pokrenut da bi frontend dobivao podatke.

Varijable u `frontend/.env` (predložak je `frontend/.env.example`). Vite pregledniku izlaže samo varijable s prefiksom `VITE_`, pa su vidljive svakom korisniku i ovdje se nikad ne stavljaju tajne.

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `VITE_AUTH0_DOMAIN` | Auth0 domena | vrijednost iz `.env.example` |
| `VITE_AUTH0_CLIENT_ID` | Client ID SPA aplikacije „Imagic” u Auth0 | vrijednost iz `.env.example` |
| `VITE_AUTH0_AUDIENCE` | Mora biti znak po znak jednak `AUTH0_AUDIENCE` na backendu | `https://imagic-api` |

Bez `frontend/.env` aplikacija javlja grešku „Auth0 varijable nisu postavljene”.

#### 4. Provjera rada sustava

1. <http://localhost:8000/api/health> vraća `{"status":"ok"}`; interaktivna dokumentacija API-ja nalazi se na <http://localhost:8000/docs>.
2. Na <http://localhost:5173> prijaviti se preko Auth0. Nakon prve prijave radna okolina sadrži 3 početne slike, što potvrđuje da frontend komunicira s backendom i bazom.
3. Učitati sliku, osvježiti stranicu i provjeriti da je slika i dalje u radnoj okolini.

Pogreške backenda ispisuju se u terminalu u kojem radi `python -m app.main`, a pogreške frontenda u konzoli preglednika (F12).

#### Česte poteškoće

| Problem | Rješenje |
|---|---|
| `python3 -m venv` javlja da `ensurepip` nije dostupan | `sudo apt install python3.12-venv python3-pip` ili koristiti `uv venv .venv` |
| VS Code javlja *Import "fastapi" could not be resolved* | `Ctrl+Shift+P` → **Python: Select Interpreter** → `backend/.venv/bin/python` |
| `ModuleNotFoundError: No module named 'app'` | Pokretati s `python -m app.main` iz direktorija `backend/`, a ne `python app/main.py` ni gumbom *Run* |
| `uvicorn` ili `fastapi` nije pronađen | Okruženje nije aktivirano: `source .venv/bin/activate` (potrebno u svakom novom terminalu) |
| Frontend javlja `http proxy error: /api/...` | Backend nije pokrenut ili ne radi na portu 8000 |
| Mapa `.venv` ne vidi se u upravitelju datoteka | Mape koje počinju točkom su skrivene; `Ctrl+H` ih prikazuje |

`backend/.venv/`, `backend/.env` i `frontend/node_modules/` ne commitaju se.

---

## 6.3 Javno postavljanje i administracija

**Cilj:** Dokumentirati točne korake za ponovljivo postavljanje cjelovitog sustava na produkcijsku infrastrukturu, uključujući bazu podataka i veze među postavljenim dijelovima.

Aplikacija je javno dostupna na **<https://imagictim32-production.up.railway.app>** i postavljena je na platformu [Railway](https://railway.com).

| **Postavljeni podsustav** | **Infrastruktura i izvor koda** | **Naredbe izgradnje i pokretanja** | **Konfiguracija i varijable okruženja** |
| --- | --- | --- | --- |
| **Klijentski dio** | Isti Railway servis kao backend; grana `master`, mapa `frontend/` | Prva faza `Dockerfile`a: `npm ci` i `npm run build`; izlaz `dist/` kopira se u `/app/static` | `VITE_AUTH0_DOMAIN`, `VITE_AUTH0_CLIENT_ID`, `VITE_AUTH0_AUDIENCE` (javne, ugrađuju se pri buildu) |
| **Poslužiteljski dio** | Railway servis iz `Dockerfile`a u korijenu repozitorija; grana `master`, mapa `backend/` | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | `PORT` (zadaje Railway), `DATABASE_URL`, `AUTH0_DOMAIN`, `AUTH0_AUDIENCE`, `UPLOAD_DIR=/data/uploads` |
| **Baza podataka** | Railway PostgreSQL u istom projektu | `alembic upgrade head` pri svakom pokretanju kontejnera, prije `uvicorna` | `DATABASE_URL=${{Postgres.DATABASE_URL}}` (referenca koju Railway popunjava; pristupni podaci nisu u repozitoriju) |

Vrijednosti varijabli vide članovi tima s pristupom Railway projektu (**Variables**) i Auth0 tenantu.

**Postavljanje:** projekt koristi **kontinuirano postavljanje** bez CI provjera: svaki merge ili push na `master` automatski pokreće izgradnju i postavljanje na Railwayu. Prije mergea promjene se pregledavaju u Pull Requestu i provjeravaju lokalno.

### Docker image

`Dockerfile` u korijenu repozitorija gradi image u dvije faze:

1. **Node 22:** `npm ci` i `npm run build` u `frontend/`. Varijable `VITE_AUTH0_*` predaju se kao build argumenti jer ih Vite ugrađuje u kod pri buildu, a ne pri pokretanju.
2. **Python 3.12:** instalacija `backend/requirements.txt`, kopiranje backenda i izgrađenog frontenda u `/app/static` (`FRONTEND_DIST`).

Pri svakom pokretanju kontejner najprije izvodi `alembic upgrade head` (već primijenjene migracije preskaču se), a zatim pokreće `uvicorn` na portu iz varijable `PORT`. `.dockerignore` iz imagea isključuje `node_modules`, `.env` datoteke i lokalne slike.

Backend prihvaća `DATABASE_URL` u obliku `postgresql://...` (kakav daje Railway) i sam ga pretvara u `postgresql+psycopg://...` (`normalize_db_url` u `backend/app/db.py`).

### Postupak postavljanja

1. **Projekt i izvor koda:** na [railway.com](https://railway.com) prijava preko GitHuba → **New Project** → **Deploy from GitHub repo** → odabrati repozitorij. Ako ga nema na popisu, **Configure GitHub App** i dati pristup repozitoriju. Prvi deploy će pasti jer još nema baze ni varijabli.
2. Servis aplikacije → **Settings** → **Source** → **Branch**: `master`.
3. **Infrastruktura baze podataka:** na platnu projekta **+ Create** → **Database** → **PostgreSQL**. Migracije se primjenjuju same pri pokretanju aplikacije.
4. **Varijable:** servis aplikacije → **Variables** → **Raw Editor**:

   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   AUTH0_DOMAIN=<domena>
   AUTH0_AUDIENCE=https://imagic-api
   VITE_AUTH0_DOMAIN=<domena>
   VITE_AUTH0_CLIENT_ID=<client id>
   VITE_AUTH0_AUDIENCE=https://imagic-api
   UPLOAD_DIR=/data/uploads
   ```

   `${{Postgres.DATABASE_URL}}` je referenca koju Railway sam zamjenjuje adresom baze. `FRONTEND_URL` se ne postavlja.
5. **Pohrana slika:** desni klik na servis aplikacije → **Attach Volume**, mount path `/data`.
6. **Javna domena:** servis aplikacije → **Settings** → **Networking** → **Generate Domain**. Po želji **Settings** → **Deploy** → **Healthcheck Path**: `/api/health`.
7. **Završno povezivanje (Auth0):** u Auth0 (Applications → SPA aplikacija → Settings) dodati javnu domenu, s `https://` i bez kose crte na kraju, u **Allowed Callback URLs**, **Allowed Logout URLs** i **Allowed Web Origins**. Lokalne adrese (`http://localhost:5173`, `http://localhost:8000`) ostaju u popisu. CORS nije potreban jer su frontend i backend na istoj domeni.
8. **Deploy** i praćenje **Deploy Logs**: očekuju se poruke migracija (`Running upgrade ...`) i `Uvicorn running on http://0.0.0.0:...`.

### Pristup i administracija

- **Nadzor rada i zapisi pogrešaka:** članovi tima s pristupom Railway projektu pregledavaju **Build Logs** (izgradnja imagea) i **Deploy Logs** (migracije, zahtjevi i pogreške aplikacije) pod **Deployments** servisa aplikacije.
- **Upravljanje administratorskim ovlastima:** aplikacija nema administratorsku ni moderatorsku ulogu ni administratorsko sučelje.
- **Postupak ažuriranja:** Railway prati granu `master`; svaki merge ili push na nju automatski pokreće novi build i postavljanje. Baza i slike na volumeu ostaju sačuvane, a nove migracije primjenjuju se same pri pokretanju. Ako build ili migracija ne uspije, prethodna inačica nastavlja raditi, a greška je vidljiva u logovima. Novi Python paket mora biti u `backend/requirements.txt`, a novi npm paket u `frontend/package.json` i `package-lock.json`; promjena varijabli na Railwayu primjenjuje se tek nakon ponovnog postavljanja (**Deploy**).

### Lokalna provjera imagea

Prije promjene `Dockerfile`a ili dodavanja paketa image se može provjeriti lokalno. Iz korijena repozitorija, uz pokrenutu bazu (`docker compose up -d`):

```bash
docker build -t imagic \
  --build-arg VITE_AUTH0_DOMAIN=<domena> \
  --build-arg VITE_AUTH0_CLIENT_ID=<client id> \
  --build-arg VITE_AUTH0_AUDIENCE=https://imagic-api .

docker run --rm --network host \
  -e DATABASE_URL=postgresql://imagic:imagic@localhost:5433/imagic \
  -e AUTH0_DOMAIN=<domena> \
  -e AUTH0_AUDIENCE=https://imagic-api \
  imagic
```

Vrijednosti su u `frontend/.env`. Aplikacija je tada na <http://localhost:8000> (frontend i backend zajedno). Da bi prijava radila, `http://localhost:8000` mora biti upisan u Auth0 (korak 7 postupka postavljanja). Učitane slike u kontejneru nisu vidljive jer kontejner nema pristup lokalnoj mapi `backend/uploads`.

### Česte poteškoće

| Problem | Rješenje |
|---|---|
| Auth0 javlja *Callback URL mismatch* | Adresa s koje se aplikacija otvara nije upisana u Auth0 (korak 7) |
| Prazna stranica, u konzoli greška o Auth0 varijablama | `VITE_AUTH0_*` nisu bile postavljene pri buildu; dodati ih i ponovno postaviti |
| Deploy pada s greškom spajanja na bazu | Provjeriti `DATABASE_URL=${{Postgres.DATABASE_URL}}` i ime servisa baze (`Postgres`) |
| Slike nestaju nakon ponovnog postavljanja | Volume nije spojen na `/data` ili `UPLOAD_DIR` nije `/data/uploads` |
| `/api/...` vraća 404 | Ruta ne postoji na backendu; provjeriti putanju u `frontend/src/data/` |

### Troškovi

Railway naplaćuje stvarnu potrošnju resursa. Projekt trenutno koristi probni period (Trial); prije isteka probnog kredita prelazi se na plan Hobby (5 $ mjesečno, uključuje 5 $ potrošnje) uz postavljeno ograničenje potrošnje (**Usage limits**). Potrošnja se prati u **Usage**.
