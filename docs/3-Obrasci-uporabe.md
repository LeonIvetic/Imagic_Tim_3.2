# 3. Obrasci uporabe

**Cilj:** Opisati aktere i reprezentativne interakcije korisnika sa sustavom.

> Stranica će se popuniti nakon vježbe 26.10. UML dijagrami izrađuju se u PlantUML-u (izvor `.puml` + slika).

## 3.1 Akteri

Vidi [2.3 Dionici i akteri](2-Analiza-zahtjeva.md#23-dionici-i-akteri).

## 3.2 Popis obrazaca uporabe

| ID | Naziv | Akter | Povezani zahtjevi |
|----|-------|-------|-------------------|
| UC-001 | Prijava putem OAuth 2.0 | Neprijavljeni posjetitelj | F-001, F-002 |
| UC-002 | Upload i organizacija slika | Prijavljeni korisnik | F-003, F-004, F-005 |
| UC-003 | Obrada slike | Prijavljeni korisnik | F-006 – F-010 |
| UC-004 | Objava posta | Prijavljeni korisnik | F-011 – F-013 |
| UC-005 | Pregled tuđe stranice i favoriti | Prijavljeni korisnik | F-014 – F-016 |

## 3.3 Opisi obrazaca uporabe

### UC-001 Prijava putem OAuth 2.0

**Preduvjeti:**
- korisnik je otvorio aplikaciju Imagic
- korisnik nije prijavljen

**Glavni tijek:**
1. Korisnik odabire opciju „Prijava”.
2. Sustav preusmjerava korisnika na Auth0 stranicu za prijavu.
3. Korisnik unosi svoje podatke za prijavu ili odabire prijavu putem Google računa.
4. Auth0 provjerava identitet korisnika.
5. Nakon uspješne autentifikacije korisnik se preusmjerava natrag u aplikaciju Imagic.
6. Aplikacija dohvaća pristupni token i šalje ga backendu radi provjere.
7. Backend provjerava valjanost tokena i traži korisnika u bazi podataka.
8. Ako korisnik ne postoji u bazi, sustav stvara njegov korisnički zapis i dodjeljuje mu tri početne slike.
9. Sustav prikazuje prijavljenom korisniku njegovu radnu okolinu.

**Alternativni tijekovi:**

A1 - Korisnik odustaje od prijave
1. Korisnik odustaje od prijave na Auth0 stranici.
2. Korisnik ostaje neprijavljen i nema pristup zaštićenim funkcionalnostima.

A2 - Auth0 nije dostupan
1. Sustav ne može uspostaviti vezu s Auth0 uslugom.
2. Prijava se ne može dovršiti pa korisnik ostaje neprijavljen.

A3 - Korisnički račun već postoji
1. Sustav pronalazi postojeći korisnički račun u bazi podataka.
2. Korisnik se uspješno prijavljuje i pristupa svojoj radnoj okolini.

**Postuvjeti:**
- nakon uspješne prijave korisnik ima pristup svojoj privatnoj radnoj okolini i javnoj stranici profila
- ako je riječ o prvoj prijavi, stvoren je korisnički račun te su korisniku dodijeljene tri početne slike
- ako prijava nije uspjela ili je korisnik odustao, ostaje neprijavljen i nema pristup zaštićenim funkcionalnostima



