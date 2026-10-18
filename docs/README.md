# Imagic – opis projekta i smjer razvoja

## 1. Sažetak

Imagic je web platforma za obradu rasterskih slika s mogućnošću uvoza/izvoza, pohrane i javne objave slika. Svaki prijavljeni korisnik ima:

- **privatnu radnu okolinu** (vidljivu samo vlasniku): upload/download, mape i datoteke, prikaz, obrada slika;
- **javnu stranicu** (vidljivu svim prijavljenim korisnicima, uređuje je samo vlasnik): profil i postovi sa slikom i tekstom.

Prijava i registracija rade isključivo preko vanjskih OAuth 2.0 pružatelja (npr. Google, GitHub).

## 2. Što tim stvarno treba realizirati (minimalni opseg)

### 2.1 Autentifikacija
- Registracija/prijava preko OAuth 2.0 (min. 1 pružatelj, poželjno 2).
- Pri prvoj prijavi korisnik u radnu okolinu dobiva **3 testne rasterske slike**.

### 2.2 Radna okolina (privatna)
1. Upload i download slika u **min. 3 formata** (npr. JPEG, PNG, TIF).
2. Pohrana s **katalo­škom strukturom** (mape) te imenovanje i preimenovanje datoteka; brisanje i organizacija.
3. Spremanje rezultata obrade kao **nova datoteka** ili **prepisivanje originala**.
4. Obrada slika, minimalno:
   - 3.1 **5 filtara** (npr. invert, grayscale, pixelate, blur, derivative)
   - 3.2 **4 morfološka operatora** (erosion, dilation, opening, closing)
   - 3.3 **3 geometrijske transformacije** (resize, rotate, flip)
   - 3.4 **1 algoritam segmentacije** (npr. Otsu/threshold)
5. **Prikaz** odabrane slike.

### 2.3 Javna stranica
1. Korisničko ime, slika korisnika, kratki opis.
2. Niz postova (slika + tekstualni opis); dodavanje, uređivanje, brisanje.
3. Svaki post može biti **privatan ili javan**.
4. Pregled javnih stranica drugih korisnika.
5. **Favoriti:** pojedini postovi ili cijela javna stranica.
6. Slike s tuđih stranica: **preuzimanje lokalno** ili **dodavanje u vlastitu radnu okolinu**.

### 2.4 Izvan minimuma (opcijski, samo ako ostane vremena)
Dodatni filtri/operatori, undo/redo, pretraživanje korisnika, lajkovi/komentari, galerija slika s Art Institute of Chicago API-ja.

## 3. Tehnologije

| Sloj | Odabir |
|---|---|
| Frontend | React + JavaScript |
| Backend | FastAPI (Python) |
| Autentifikacija | OAuth 2.0 (npr. Authlib na backendu) |
| Obrada slika | image-js (ImageJS) u pregledniku **ili** Pillow/OpenCV/scikit-image na backendu – *vidi otvorena pitanja* |
| Dohvat slika | Art Institute of Chicago (Artic) API za početne testne slike |
| Baza | PostgreSQL (prijedlog; SQLite za razvoj) |
| Pohrana datoteka | Disk/volumen na poslužitelju ili S3-kompatibilna pohrana |
| Verzioniranje | GitHub, grane + Pull Requesti, Issues, Projects board |

## 4. Prijedlog arhitekture

```
React SPA  <--REST/JSON-->  FastAPI  <-->  PostgreSQL (korisnici, mape, datoteke, postovi, favoriti)
                               |
                               +--> pohrana datoteka (slike)
                               +--> OAuth 2.0 pružatelji, Artic API
```

Glavni modeli podataka: `User`, `Folder` (parent_id), `ImageFile` (folder_id, naziv, format, putanja), `Post` (user_id, image_id, tekst, is_public), `FavoritePost`, `FavoriteProfile`.

## 5. Prijedlog podjele tima (7 članova)

| Područje | Članova | Zadaće |
|---|---|---|
| Auth + korisnici | 1 | OAuth, sesije/JWT, profil, inicijalne 3 slike |
| Radna okolina – backend | 1–2 | datoteke, mape, upload/download, CRUD |
| Obrada slika | 1–2 | filtri, morfologija, geometrija, segmentacija |
| Frontend – radna okolina | 1–2 | stablo mapa, prikaz slike, alati |
| Javna stranica + favoriti | 1–2 | postovi, privatno/javno, favoriti, preuzimanje |

Voditelj tima dodatno vodi board, review PR-ova i komunikaciju s asistentom. Konkretna imena upisati nakon dogovora tima.

## 6. Otvorena pitanja za asistenta

1. Je li potrebno **deployanje** (npr. Render/Fly/VM) ili je dovoljno lokalno pokretanje (Docker Compose)?
2. Je li dopuštena **vlastita baza** (PostgreSQL) i pohrana na disku, ili se traži cloud pohrana?

## 7. Radni proces na GitHubu

- Svaki PR veže se na Issue (`Closes #n`).
- Labeli: `backend`, `frontend`, `auth`, `image-processing`, `docs`, `setup`, `bug`, `enhancement`.
- Milestones: **M1 – Postava i dizajn**, **M2 – Jezgra (auth + datoteke)**, **M3 – Obrada slika**, **M4 – Javna stranica**, **M5 – Testiranje i predaja**.
- GitHub Project board: *Backlog → In progress → In review → Done*.
- Commit poruke: kratke, u imperativu, npr. `Add folder CRUD endpoints`.

