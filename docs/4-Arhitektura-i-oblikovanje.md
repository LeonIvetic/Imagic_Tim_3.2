# 4. Arhitektura i oblikovanje

**Cilj:** Opisati glavne odluke oblikovanja, strukturu sustava, podatke i ponašanje.

## 4.1 Pregled arhitekture

```
React SPA  <--REST/JSON-->  FastAPI  <-->  PostgreSQL
                               |
                               +--> pohrana datoteka (slike)
                               +--> Auth0 (OAuth 2.0), Artic API
```

## 4.2 Odluke oblikovanja

| Odluka | Status | Razlog |
|--------|--------|--------|
| React + JavaScript (frontend) | Donesena | Odluka tima |
| FastAPI (backend) | Donesena | Odluka tima |
| Obrada slika na backendu (Pillow/OpenCV) | Donesena | Odluka tima (31.10.); jedna implementacija alata, neovisna o pregledniku |
| PostgreSQL (baza podataka) | Donesena | Odluka tima (31.10.); relacijski podaci (korisnici, mape, datoteke, postovi, favoriti) |
| Auth0 (OAuth 2.0) za prijavu | Donesena | Odluka tima (31.10.); aplikacija ne pohranjuje lozinke |

## 4.3 Model podataka (nacrt)

Entiteti: `User`, `Folder` (parent_id), `ImageFile` (folder_id, naziv, format, putanja), `Post` (user_id, image_id, tekst, is_public), `FavoritePost`, `FavoriteProfile`.

[Dopuniti ER dijagram.]
