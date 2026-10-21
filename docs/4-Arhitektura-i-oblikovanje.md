# 4. Arhitektura i oblikovanje

**Cilj:** Opisati glavne odluke oblikovanja, strukturu sustava, podatke i ponašanje.

> Radna skica; konačne odluke bit će zabilježene nakon razgovora s asistentom.

## 4.1 Pregled arhitekture

```
React SPA  <--REST/JSON-->  FastAPI  <-->  baza podataka
                               |
                               +--> pohrana datoteka (slike)
                               +--> OAuth 2.0 pružatelj, Artic API
```

## 4.2 Odluke oblikovanja

| Odluka | Status | Razlog |
|--------|--------|--------|
| React + JavaScript (frontend) | Donesena | Odluka tima |
| FastAPI (backend) | Donesena | Odluka tima |
| Mjesto obrade slika (preglednik ili backend) | Otvorena | Čeka potvrdu asistenta |
| Baza podataka | Otvorena | [Dopuniti] |

## 4.3 Model podataka (nacrt)

Entiteti: `User`, `Folder` (parent_id), `ImageFile` (folder_id, naziv, format, putanja), `Post` (user_id, image_id, tekst, is_public), `FavoritePost`, `FavoriteProfile`.

[Dopuniti ER dijagram.]
