# 6. Postavljanje, instalacija i konfiguracija

**Cilj:** Opisati lokalnu instalaciju, konfiguraciju i javno postavljanje aplikacije.

> Opisano je lokalno pokretanje: PostgreSQL (Docker), backend (FastAPI) i frontend (React + Vite) s prijavom preko Auth0.

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
| `FRONTEND_URL` | Adresa frontenda kojoj backend dopušta pozive (CORS) | `http://localhost:5173` |
| `DATABASE_URL` | Adresa PostgreSQL baze iz `docker-compose.yml` | `postgresql+psycopg://imagic:imagic@localhost:5433/imagic` |
| `AUTH0_DOMAIN` | Auth0 domena, bez `https://` | vrijednost iz `.env.example` |
| `AUTH0_AUDIENCE` | Identifier našeg API-ja u Auth0 | `https://imagic-api` |

**Frontend (`frontend/.env`)**

Vite pregledniku izlaže samo varijable s prefiksom `VITE_`, pa su vidljive svakom korisniku i ovdje se nikad ne stavljaju tajne.

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `VITE_AUTH0_DOMAIN` | Auth0 domena | vrijednost iz `.env.example` |
| `VITE_AUTH0_CLIENT_ID` | Client ID SPA aplikacije „Imagic” u Auth0 | vrijednost iz `.env.example` |
| `VITE_AUTH0_AUDIENCE` | Mora biti znak po znak jednak `AUTH0_AUDIENCE` na backendu | `https://imagic-api` |

Vrijednosti se upisuju bez navodnika i razmaka. Nakon promjene treba ponovno pokrenuti odgovarajući server.

## 6.3 Javno postavljanje

[Dopuniti nakon dogovora s asistentom o platformi.]

## 6.4 Pokretanje baze

Instaliraj Docker (Docker Desktop na Windowsu/Macu).
U korijenu repozitorija: `docker compose up -d`
`cd backend`, aktiviraj virtualno okruženje i `pip install -r requirements.txt`
Kopiraj `.env.example` u `.env` (`cp .env.example .env`)
`alembic upgrade head`
Provjera: `docker compose exec db psql -U imagic -d imagic -c "\d users"`

Zaustavljanje: `docker compose down` (podaci ostaju). Brisanje i podataka: `docker compose down -v`.