# 6. Postavljanje, instalacija i konfiguracija

**Cilj:** Opisati lokalnu instalaciju, konfiguraciju i javno postavljanje aplikacije.

> Opisan je trenutačni minimalni kostur (FastAPI + React). Baza podataka (PostgreSQL) i ostale ovisnosti dodat će se kad budu uvedene u projekt.

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

Iz direktorija `backend/`:

```bash
uv venv .venv                        # ili: python3 -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt   # ili: pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

Backend radi na <http://localhost:8000> i automatski se ponovno pokreće pri spremanju promjena. Provjera: <http://localhost:8000/api/health> vraća `{"status":"ok"}`. Interaktivna dokumentacija API-ja nalazi se na <http://localhost:8000/docs>.

### Frontend (React + Vite)

U drugom terminalu, iz direktorija `frontend/`:

```bash
npm install
npm run dev
```

Frontend radi na <http://localhost:5173>. Vite zahtjeve na `/api/...` prosljeđuje backendu na `localhost:8000`, pa backend mora biti pokrenut da bi frontend dobivao podatke.

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

Varijable okruženja navode se u `backend/.env.example` (bez stvarnih vrijednosti). Svaki član tima kopira ga u vlastiti `backend/.env`, koji Git ignorira.

| Varijabla | Opis | Zadana vrijednost |
|---|---|---|
| `FRONTEND_URL` | Adresa frontenda kojoj backend dopušta pozive (CORS) | `http://localhost:5173` |

[Dopuniti s uvođenjem baze i OAuth prijave, npr. adresa baze, OAuth client ID i secret.]

## 6.3 Javno postavljanje

[Dopuniti nakon dogovora s asistentom o platformi.]
