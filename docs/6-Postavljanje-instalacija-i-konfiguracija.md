# 6. Postavljanje, instalacija i konfiguracija

**Cilj:** Opisati lokalnu instalaciju, konfiguraciju i javno postavljanje aplikacije.

> Opisano je lokalno pokretanje: PostgreSQL (Docker), backend (FastAPI) i frontend (React + Vite) s prijavom preko Auth0, te javno postavljanje na Railway (6.3).

## 6.1 Lokalna instalacija

**Preduvjeti:**

- Python 3.12 i [uv](https://docs.astral.sh/uv/) ili, umjesto uv-a, sistemski paketi `python3-venv` i `python3-pip`
- Node.js 22 i npm

Repozitorij:

```bash
git clone https://github.com/LeonIvetic/Imagic_Tim_3.2.git
cd Imagic_Tim_3.2
```

### Backend (FastAPI)

Prije backenda pokreni bazu (vidi [6.4](#64-pokretanje-baze)): `docker compose up -d` u korijenu repozitorija.

Iz direktorija `backend/`:

```bash
uv venv .venv                        # ili: python3 -m venv .venv (samo prvi put)
source .venv/bin/activate            # u svakom novom terminalu
uv pip install -r requirements.txt   # ili: pip install -r requirements.txt
cp .env.example .env                 # samo prvi put
alembic upgrade head                 # stvara/ažurira tablice
python -m app.main
```

Backend radi na <http://localhost:8000> i automatski se ponovno pokreće pri spremanju promjena. Provjera: <http://localhost:8000/api/health> vraća `{"status":"ok"}`. Interaktivna dokumentacija API-ja nalazi se na <http://localhost:8000/docs>.

### Frontend (React + Vite)

U drugom terminalu, iz direktorija `frontend/`:

```bash
npm install
cp .env.example .env                 # samo prvi put
npm run dev
```

Bez `frontend/.env` aplikacija javlja grešku „Auth0 varijable nisu postavljene”. Frontend radi na <http://localhost:5173>. Vite zahtjeve na `/api/...` prosljeđuje backendu na `localhost:8000`, pa backend mora biti pokrenut da bi frontend dobivao podatke.

### Česte poteškoće

| Problem | Rješenje |
|---|---|
| `python3 -m venv` javlja da `ensurepip` nije dostupan | `sudo apt install python3.12-venv python3-pip` ili koristiti `uv venv .venv` |
| VS Code javlja *Import "fastapi" could not be resolved* | `Ctrl+Shift+P` → **Python: Select Interpreter** → `backend/.venv/bin/python` |
| `ModuleNotFoundError: No module named 'app'` | Pokretati s `python -m app.main` iz direktorija `backend/`, a ne `python app/main.py` ni gumbom *Run* |
| `uvicorn` ili `fastapi` nije pronađen | Okruženje nije aktivirano: `source .venv/bin/activate` (potrebno u svakom novom terminalu) |
| Frontend javlja `http proxy error: /api/...` | Backend nije pokrenut ili ne radi na portu 8000 |
| Mapa `.venv` ne vidi se u upravitelju datoteka | Mape koje počinju točkom su skrivene; `Ctrl+H` ih prikazuje |

`backend/.venv/`, `backend/.env` i `frontend/node_modules/` ne commitaju se.

## 6.2 Konfiguracija

Backend i frontend imaju svaki svoju datoteku: `backend/.env.example` i `frontend/.env.example`. Svaki član tima kopira ih u vlastite `backend/.env` i `frontend/.env`, koje Git ignorira. U njima nema tajni: Auth0 domena, client ID i audience javne su vrijednosti, a lozinka baze vrijedi samo za lokalni Docker.

**Backend (`backend/.env`)**

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `FRONTEND_URL` | Adresa frontenda kojoj backend dopušta pozive (CORS). Potrebna samo lokalno; u produkciji se ne postavlja (vidi 6.3) | `http://localhost:5173` |
| `DATABASE_URL` | Adresa PostgreSQL baze iz `docker-compose.yml` | `postgresql+psycopg://imagic:imagic@localhost:5433/imagic` |
| `AUTH0_DOMAIN` | Auth0 domena, bez `https://` | vrijednost iz `.env.example` |
| `AUTH0_AUDIENCE` | Identifier našeg API-ja u Auth0 | `https://imagic-api` |
| `UPLOAD_DIR` | Mapa u koju se spremaju učitane slike | `backend/uploads` |

**Frontend (`frontend/.env`)**

Vite pregledniku izlaže samo varijable s prefiksom `VITE_`, pa su vidljive svakom korisniku i ovdje se nikad ne stavljaju tajne.

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `VITE_AUTH0_DOMAIN` | Auth0 domena | vrijednost iz `.env.example` |
| `VITE_AUTH0_CLIENT_ID` | Client ID SPA aplikacije „Imagic” u Auth0 | vrijednost iz `.env.example` |
| `VITE_AUTH0_AUDIENCE` | Mora biti znak po znak jednak `AUTH0_AUDIENCE` na backendu | `https://imagic-api` |

Vrijednosti se upisuju bez navodnika i razmaka. Nakon promjene treba ponovno pokrenuti odgovarajući server.

## 6.3 Javno postavljanje

Aplikacija je javno dostupna na **<https://imagictim32-production.up.railway.app>** i postavljena je na platformu [Railway](https://railway.com).

### Arhitektura postavljanja

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

### Docker image

`Dockerfile` u korijenu repozitorija gradi image u dvije faze:

1. **Node 22:** `npm ci` i `npm run build` u `frontend/`. Varijable `VITE_AUTH0_*` predaju se kao build argumenti jer ih Vite ugrađuje u kod pri buildu, a ne pri pokretanju.
2. **Python 3.12:** instalacija `backend/requirements.txt`, kopiranje backenda i izgrađenog frontenda u `/app/static` (`FRONTEND_DIST`).

Pri svakom pokretanju kontejner najprije izvodi `alembic upgrade head` (već primijenjene migracije preskaču se), a zatim pokreće `uvicorn` na portu iz varijable `PORT`. `.dockerignore` iz imagea isključuje `node_modules`, `.env` datoteke i lokalne slike.

Backend prihvaća `DATABASE_URL` u obliku `postgresql://...` (kakav daje Railway) i sam ga pretvara u `postgresql+psycopg://...` (`normalize_db_url` u `backend/app/db.py`).

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

Vrijednosti su u `frontend/.env`. Aplikacija je tada na <http://localhost:8000> (frontend i backend zajedno). Da bi prijava radila, `http://localhost:8000` mora biti upisan u Auth0 (vidi korak 6). Učitane slike u kontejneru nisu vidljive jer kontejner nema pristup lokalnoj mapi `backend/uploads`.

### Postavljanje na Railway (prvi put)

1. Na [railway.com](https://railway.com) prijava preko GitHuba → **New Project** → **Deploy from GitHub repo** → odabrati repozitorij. Ako ga nema na popisu, **Configure GitHub App** i dati pristup repozitoriju. Prvi deploy će pasti jer još nema baze ni varijabli.
2. Servis aplikacije → **Settings** → **Source** → **Branch**: `master`.
3. Na platnu projekta **+ Create** → **Database** → **PostgreSQL**.
4. Servis aplikacije → **Variables** → **Raw Editor**:

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
5. Desni klik na servis aplikacije → **Attach Volume**, mount path `/data`.
6. Servis aplikacije → **Settings** → **Networking** → **Generate Domain**. Po želji **Settings** → **Deploy** → **Healthcheck Path**: `/api/health`.
7. U Auth0 (Applications → SPA aplikacija → Settings) dodati javnu domenu, s `https://` i bez kose crte na kraju, u **Allowed Callback URLs**, **Allowed Logout URLs** i **Allowed Web Origins**. Lokalne adrese (`http://localhost:5173`, `http://localhost:8000`) ostaju u popisu.
8. **Deploy** i praćenje **Deploy Logs**: očekuju se poruke migracija (`Running upgrade ...`) i `Uvicorn running on http://0.0.0.0:...`.

### Ažuriranje

Railway prati granu `master`: svaki merge ili push na nju automatski pokreće novi build i postavljanje. Baza i slike na volumeu ostaju sačuvane, a nove migracije primjenjuju se same pri pokretanju. Ako build ili migracija ne uspije, prethodna inačica nastavlja raditi, a greška je vidljiva u **Build Logs** ili **Deploy Logs**.

Na što paziti:

- novi Python paket mora biti u `backend/requirements.txt`, a novi npm paket u `frontend/package.json` i `package-lock.json`;
- promjena varijabli na Railwayu primjenjuje se tek nakon ponovnog postavljanja (**Deploy**).

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

## 6.4 Pokretanje baze

Instaliraj Docker (Docker Desktop na Windowsu/Macu).
U korijenu repozitorija: `docker compose up -d`
`cd backend`, aktiviraj virtualno okruženje i `pip install -r requirements.txt`
Kopiraj `.env.example` u `.env` (`cp .env.example .env`)
`alembic upgrade head`
Provjera: `docker compose exec db psql -U imagic -d imagic -c "\d users"`

Zaustavljanje: `docker compose down` (podaci ostaju). Brisanje i podataka: `docker compose down -v`.