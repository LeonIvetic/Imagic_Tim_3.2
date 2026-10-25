# init backenda
# treba instalirat dependencies u requirements.txt prije pokretanja
# pokrece se iz backend direktorija sa "python -m app.main"
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Imagic API")


# CORS ce nam trebati jer ce nam backend biti na 8000 a Vite server za React na 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API provjera 
@app.get("/api/health")
def health() -> dict[str, str]:
    """Provjera radi li API."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True, env_file=".env")
