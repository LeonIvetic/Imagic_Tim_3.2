"""UC-002: radna okolina (F-002, F-003, F-004, F-016, NF-05)."""
import pytest

from io import BytesIO
from PIL import Image
from tests.conftest import make_image


def root_id(client):
    return client.get("/api/folders/root").json()["id"]


def upload(client, folder_id, name="slika.png", data=None, mime="image/png"):
    return client.post(
        "/api/images",
        data={"folder_id": folder_id},
        files={"file": (name, data if data is not None else make_image(), mime)},
    )

@pytest.mark.parametrize("name,x,expected", [
    ("grayscale", 0, (76, 76, 76)),
    ("invert", 0, (0, 255, 255)),
    ("pixelate", 9, (212, 0, 42)),
    ("blur", 9, (139, 0, 116)),
    ("derivative", 9, (47, 47, 47)),
])
def test_filter_preview(client, name, x, expected):
    source = Image.new("RGB", (24, 24), (255, 0, 0))
    source.paste((0, 0, 255), (10, 0, 24, 24))
    buffer = BytesIO()
    source.save(buffer, format="PNG")
    image = upload(client, root_id(client), data=buffer.getvalue()).json()
    path = f"/api/images/{image['id']}"
    response = client.post(f"{path}/filters", json={
        "action": "preview", "filters": [name], "source_updated_at": image["updated_at"],
    })
    assert response.status_code == 200
    with Image.open(BytesIO(response.content)) as result:
        assert result.size == source.size
        assert result.convert("RGB").getpixel((x, 12)) == pytest.approx(expected, abs=1)
        if name == "derivative":
            assert result.getpixel((23, 12)) == 0
    assert client.get(f"{path}/file").content == buffer.getvalue()
    assert len(client.get("/api/images").json()) == 1


def test_filter_copy_and_overwrite(client, login):
    source = BytesIO()
    Image.new("RGBA", (8, 8), (200, 30, 30, 121)).save(source, format="PNG")
    image = upload(client, root_id(client), data=source.getvalue()).json()
    path = f"/api/images/{image['id']}"
    filters = {"filters": ["grayscale", "invert"], "source_updated_at": image["updated_at"]}
    copy = client.post(f"{path}/filters", json={**filters, "action": "copy", "name": "slika.png"})
    assert copy.status_code == 200
    assert copy.json()["name"] == "slika (1).png"
    assert client.get(f"{path}/file").content == source.getvalue()

    post = client.post("/api/posts", json={"image_id": image["id"], "is_public": True}).json()
    overwritten = client.post(f"{path}/filters", json={**filters, "action": "overwrite"})
    assert overwritten.status_code == 200
    assert overwritten.json()["id"] == image["id"]
    assert overwritten.json()["updated_at"] != image["updated_at"]
    assert client.post(f"{path}/filters", json={**filters, "action": "overwrite"}).status_code == 409
    saved_bytes = client.get(f"{path}/file").content
    assert client.get(f"/api/images/{copy.json()['id']}/file").content == saved_bytes
    with Image.open(BytesIO(saved_bytes)) as result:
        assert result.getpixel((0, 0)) == (174, 174, 174, 121)

    login("ivo")
    assert client.get(f"/api/posts/{post['id']}/image").content == saved_bytes
    assert client.post(f"{path}/filters", json={**filters, "action": "preview"}).status_code == 404

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


# ---------- Nastavak imena odgovara formatu ----------

@pytest.mark.parametrize("name,expected", [
    ("b.png", "b.png"),
    ("b.PNG", "b.PNG"),
    ("b", "b.png"),
    ("b.jpg", "b.png"),
    ("moj.odmor", "moj.odmor.png"),
])
def test_preimenovanje_uskladjuje_nastavak(client, name, expected):
    img = upload(client, root_id(client), "a.png").json()
    r = client.patch(f"/api/images/{img['id']}", json={"name": name})
    assert r.status_code == 200
    assert r.json()["name"] == expected


def test_upload_s_krivim_nastavkom_dobiva_ispravan(client):
    r = upload(client, root_id(client), "fotka.jpg", make_image("PNG"), "image/jpeg")
    assert r.json()["name"] == "fotka.png"
    jpeg = upload(client, root_id(client), "fotka.jpeg", make_image("JPEG"), "image/jpeg")
    assert jpeg.json()["name"] == "fotka.jpeg"


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
