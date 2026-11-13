"""F-001, NF-02: zaštićene rute bez valjanog tokena vraćaju 401."""
import pytest


@pytest.mark.parametrize("path", ["/api/users/me", "/api/folders/root", "/api/folders/1", "/api/images/1"])
def test_bez_tokena_401(anon_client, path):
    assert anon_client.get(path).status_code == 401


def test_neispravan_token_401(anon_client):
    r = anon_client.get("/api/users/me", headers={"Authorization": "Bearer nije.pravi.token"})
    assert r.status_code == 401


def test_health_je_javan(anon_client):
    assert anon_client.get("/api/health").json() == {"status": "ok"}
