# init backenda
# treba instalirat dependencies u requirements.txt prije pokretanja
# pokrece se iz backend direktorija sa "python -m app.main"
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="Imagic API")
from app.users import router as users_router
from app.workspace import router as workspace_router
from app.posts import router as posts_router
app.include_router(users_router)
app.include_router(workspace_router)
app.include_router(posts_router)


# CORS treba samo lokalno (Vite na 5173, backend na 8000). U produkciji FastAPI
# poslužuje i frontend s iste domene, pa FRONTEND_URL nije potreban.
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# API provjera
@app.get("/api/health")
def health() -> dict[str, str]:
    """Provjera radi li API."""
    return {"status": "ok"}


# ---------- Izgrađeni React (samo u produkciji / Docker imageu) ----------
# FRONTEND_DIST postavlja Dockerfile. Lokalno ga nema, pa frontend i dalje poslužuje Vite.
FRONTEND_DIST = os.getenv("FRONTEND_DIST")
if FRONTEND_DIST and Path(FRONTEND_DIST).is_dir():
    dist = Path(FRONTEND_DIST).resolve()

    # Mora biti zadnja ruta: sve što nije API vraća datoteku iz dist/ ili index.html,
    # da React Router radi i kad se osvježi npr. /profil.
    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        if path == "api" or path.startswith("api/"):
            raise HTTPException(404, "Ruta ne postoji.")  # nepostojeći API ne smije vratiti HTML
        file = (dist / path).resolve()
        if path and file.is_file() and file.is_relative_to(dist):  # bez izlaska iz dist/ (../)
            return FileResponse(file)
        return FileResponse(dist / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True, env_file=".env")
