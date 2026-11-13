"""UC-002: radna okolina (F-002, F-003, F-004, F-016, NF-05)."""
import pytest

from tests.conftest import make_image


def root_id(client):
    return client.get("/api/folders/root").json()["id"]


def upload(client, folder_id, name="slika.png", data=None, mime="image/png"):
    return client.post(
        "/api/images",
        data={"folder_id": folder_id},
        files={"file": (name, data if data is not None else make_image(), mime)},
    )


# ---------- Mape (F-003) ----------

def test_korijenska_mapa_postoji_i_jedinstvena(client):
    first = client.get("/api/folders/root").json()
    second = client.get("/api/folders/root").json()
    assert first["id"] == second["id"]
    assert first["parent_id"] is None


def test_ugnijezdene_mape_i_putanja(client):
    root = root_id(client)
    odmor = client.post("/api/folders", json={"parent_id": root, "name": "Odmor"}).json()
    hvar = client.post("/api/folders", json={"parent_id": odmor["id"], "name": "Hvar 2026"}).json()

    content = client.get(f"/api/folders/{hvar['id']}").json()
    assert [p["name"] for p in content["path"]] == ["Radna okolina", "Odmor", "Hvar 2026"]
    assert [f["name"] for f in client.get(f"/api/folders/{root}").json()["folders"]] == ["Odmor"]


def test_isto_ime_mape_u_istoj_nadmapi_409(client):
    root = root_id(client)
    assert client.post("/api/folders", json={"parent_id": root, "name": "A"}).status_code == 201
    assert client.post("/api/folders", json={"parent_id": root, "name": "A"}).status_code == 409


@pytest.mark.parametrize("name", ["", "   ", "a/b", ".."])
def test_neispravno_ime_mape_422(client, name):
    assert client.post("/api/folders", json={"parent_id": root_id(client), "name": name}).status_code == 422


def test_preimenovanje_mape(client):
    root = root_id(client)
    f = client.post("/api/folders", json={"parent_id": root, "name": "Staro"}).json()
    r = client.patch(f"/api/folders/{f['id']}", json={"name": "Novo"})
    assert r.status_code == 200 and r.json()["name"] == "Novo"


def test_mapa_ne_moze_u_svoju_podmapu(client):
    root = root_id(client)
    a = client.post("/api/folders", json={"parent_id": root, "name": "A"}).json()
    b = client.post("/api/folders", json={"parent_id": a["id"], "name": "B"}).json()
    assert client.patch(f"/api/folders/{a['id']}", json={"parent_id": b["id"]}).status_code == 400
    assert client.patch(f"/api/folders/{a['id']}", json={"parent_id": a["id"]}).status_code == 400


def test_korijen_se_ne_brise_ni_preimenuje(client):
    root = root_id(client)
    assert client.delete(f"/api/folders/{root}").status_code == 400
    assert client.patch(f"/api/folders/{root}", json={"name": "X"}).status_code == 400


def test_brisanje_mape_brise_sadrzaj_i_datoteke(client):
    from app import storage

    root = root_id(client)
    a = client.post("/api/folders", json={"parent_id": root, "name": "A"}).json()
    b = client.post("/api/folders", json={"parent_id": a["id"], "name": "B"}).json()
    img = upload(client, b["id"]).json()
    from app.db import SessionLocal
    from app.models import ImageFile
    with SessionLocal() as db:
        path = storage.absolute(db.get(ImageFile, img["id"]).file_path)
    assert path.exists()

    assert client.delete(f"/api/folders/{a['id']}").status_code == 204
    assert client.get(f"/api/folders/{b['id']}").status_code == 404
    assert client.get(f"/api/images/{img['id']}").status_code == 404
    assert not path.exists()


# ---------- Slike (F-002, F-004, NF-05) ----------

@pytest.mark.parametrize("fmt,mime,expected", [
    ("JPEG", "image/jpeg", "jpeg"),
    ("PNG", "image/png", "png"),
    ("TIFF", "image/tiff", "tiff"),
    ("WEBP", "image/webp", "webp"),
])
def test_upload_podrzanih_formata(client, fmt, mime, expected):
    r = upload(client, root_id(client), f"test.{expected}", make_image(fmt), mime)
    assert r.status_code == 201
    assert r.json()["format"] == expected


def test_format_se_odreduje_po_sadrzaju_ne_nastavku(client):
    r = upload(client, root_id(client), "lazna.png", b"ovo nije slika", "image/png")
    assert r.status_code == 415


def test_nepodrzan_format_415(client):
    r = upload(client, root_id(client), "slika.gif", make_image("GIF"), "image/gif")
    assert r.status_code == 415
    assert "JPEG" in r.json()["detail"]


def test_prevelika_datoteka_413(client):
    big = make_image() + b"\0" * (10 * 1024 * 1024)
    assert upload(client, root_id(client), data=big).status_code == 413


def test_isto_ime_dobiva_sufiks(client):
    root = root_id(client)
    upload(client, root, "a.png")
    assert upload(client, root, "a.png").json()["name"] == "a (1).png"


def test_detalji_preuzimanje_i_prikaz(client):
    img = upload(client, root_id(client), "crveno.png").json()
    detail = client.get(f"/api/images/{img['id']}").json()
    assert (detail["width"], detail["height"]) == (40, 30)

    dl = client.get(f"/api/images/{img['id']}/file?download=true")
    assert dl.status_code == 200
    assert dl.headers["content-type"] == "image/png"
    assert "attachment" in dl.headers["content-disposition"]


def test_tiff_se_za_prikaz_pretvara_u_png(client):
    img = upload(client, root_id(client), "t.tif", make_image("TIFF"), "image/tiff").json()
    r = client.get(f"/api/images/{img['id']}/preview")
    assert r.headers["content-type"] == "image/png"
    assert r.content.startswith(b"\x89PNG")


def test_preimenovanje_i_premjestanje_slike(client):
    root = root_id(client)
    folder = client.post("/api/folders", json={"parent_id": root, "name": "Mapa"}).json()
    img = upload(client, root, "a.png").json()

    r = client.patch(f"/api/images/{img['id']}", json={"name": "b.png", "folder_id": folder["id"]})
    assert r.status_code == 200
    assert client.get(f"/api/folders/{root}").json()["images"] == []
    assert [i["name"] for i in client.get(f"/api/folders/{folder['id']}").json()["images"]] == ["b.png"]


def test_brisanje_slike(client):
    img = upload(client, root_id(client)).json()
    assert client.delete(f"/api/images/{img['id']}").status_code == 204
    assert client.get(f"/api/images/{img['id']}").status_code == 404


# ---------- Privatnost (F-016, NF-02) ----------

def test_tudja_radna_okolina_nedostupna(client, login):
    root = root_id(client)
    folder = client.post("/api/folders", json={"parent_id": root, "name": "Tajno"}).json()
    img = upload(client, folder["id"]).json()

    login("ivo")
    assert client.get(f"/api/folders/{folder['id']}").status_code == 404
    assert client.get(f"/api/images/{img['id']}").status_code == 404
    assert client.get(f"/api/images/{img['id']}/file").status_code == 404
    assert client.patch(f"/api/images/{img['id']}", json={"name": "x.png"}).status_code == 404
    assert client.delete(f"/api/folders/{folder['id']}").status_code == 404
    assert upload(client, folder["id"]).status_code == 404
    ivo_root = root_id(client)
    assert client.patch(f"/api/images/{img['id']}", json={"folder_id": ivo_root}).status_code == 404
    assert client.get("/api/folders").json() == [client.get("/api/folders/root").json()]
