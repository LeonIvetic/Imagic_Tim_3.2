"""UC-004: javna stranica i postovi (F-010, F-011, F-012, NF-02)."""
import pytest

from tests.conftest import make_image


def upload(client, name="slika.png"):
    root = client.get("/api/folders/root").json()["id"]
    return client.post(
        "/api/images",
        data={"folder_id": root},
        files={"file": (name, make_image(), "image/png")},
    ).json()


def new_post(client, image_id, **fields):
    return client.post("/api/posts", json={"image_id": image_id, **fields})


# ---------- Profil (F-010) ----------

def test_uredivanje_profila(client):
    r = client.patch("/api/users/me", json={
        "username": "ana.k", "display_name": "  Ana K  ", "bio": "Fotografkinja", "avatar_url": "https://example.com/a.png",
    })
    assert r.status_code == 200
    me = client.get("/api/users/me").json()
    assert (me["username"], me["display_name"], me["bio"], me["avatar_url"]) == (
        "ana.k", "Ana K", "Fotografkinja", "https://example.com/a.png")


def test_izostavljena_polja_ostaju(client):
    client.patch("/api/users/me", json={"bio": "Opis"})
    client.patch("/api/users/me", json={"display_name": "Ana"})
    assert client.get("/api/users/me").json()["bio"] == "Opis"


@pytest.mark.parametrize("username", ["", "ima razmak", "a/b", "x" * 51])
def test_neispravno_korisnicko_ime_422(client, username):
    assert client.patch("/api/users/me", json={"username": username}).status_code == 422


def test_zauzeto_korisnicko_ime_409(client):
    # "ivo" je korisničko ime drugog korisnika iz conftesta.
    assert client.patch("/api/users/me", json={"username": "ivo"}).status_code == 409


def test_avatar_mora_biti_http_url(client):
    assert client.patch("/api/users/me", json={"avatar_url": "javascript:alert(1)"}).status_code == 422
    assert client.patch("/api/users/me", json={"avatar_url": ""}).json()["avatar_url"] is None


# ---------- Popis slika za odabir ----------

def test_popis_svih_vlastitih_slika(client, login):
    upload(client, "a.png")
    root = client.get("/api/folders/root").json()["id"]
    sub = client.post("/api/folders", json={"parent_id": root, "name": "Mapa"}).json()
    client.post("/api/images", data={"folder_id": sub["id"]}, files={"file": ("b.png", make_image(), "image/png")})
    assert [i["name"] for i in client.get("/api/images").json()] == ["a.png", "b.png"]

    login("ivo")
    assert client.get("/api/images").json() == []


# ---------- Postovi (F-011, F-012) ----------

def test_stvaranje_uredivanje_i_brisanje_posta(client):
    img = upload(client)
    r = new_post(client, img["id"], description="  Zalazak  ")
    assert r.status_code == 201
    post = r.json()
    assert (post["description"], post["is_public"], post["image_name"]) == ("Zalazak", False, "slika.png")

    r = client.patch(f"/api/posts/{post['id']}", json={"description": "Novi opis", "is_public": True})
    assert r.status_code == 200 and r.json()["is_public"] is True
    assert [p["description"] for p in client.get("/api/posts/mine").json()] == ["Novi opis"]

    assert client.delete(f"/api/posts/{post['id']}").status_code == 204
    assert client.get("/api/posts/mine").json() == []


def test_post_s_tudjom_slikom_404(client, login):
    img = upload(client)
    login("ivo")
    assert new_post(client, img["id"]).status_code == 404


def test_tudji_post_ne_moze_se_mijenjati(client, login):
    post = new_post(client, upload(client)["id"], is_public=True).json()
    login("ivo")
    assert client.patch(f"/api/posts/{post['id']}", json={"description": "x"}).status_code == 404
    assert client.delete(f"/api/posts/{post['id']}").status_code == 404
    assert client.get("/api/posts/mine").json() == []


def test_slika_privatnog_posta_vidi_samo_vlasnik(client, login):
    img = upload(client)
    private = new_post(client, img["id"]).json()
    public = new_post(client, img["id"], is_public=True).json()
    assert client.get(f"/api/posts/{private['id']}/image").status_code == 200

    login("ivo")
    assert client.get(f"/api/posts/{private['id']}/image").status_code == 404
    r = client.get(f"/api/posts/{public['id']}/image")
    assert r.status_code == 200 and r.headers["content-type"] == "image/png"
    # Javni post ne otvara ostatak radne okoline.
    assert client.get(f"/api/images/{img['id']}/preview").status_code == 404


def test_brisanje_slike_brise_postove(client):
    img = upload(client)
    new_post(client, img["id"])
    client.delete(f"/api/images/{img['id']}")
    assert client.get("/api/posts/mine").json() == []


def test_postovi_bez_tokena_401(anon_client):
    assert anon_client.get("/api/posts/mine").status_code == 401
    assert anon_client.patch("/api/users/me", json={"bio": "x"}).status_code == 401
