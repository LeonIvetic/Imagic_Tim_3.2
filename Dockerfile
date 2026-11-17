# Jedan image za cijelu aplikaciju: FastAPI poslužuje i API (/api) i izgrađeni React.
# Frontend i backend su tako na istoj domeni, pa nema CORS-a i u Auth0 ide jedan URL.

# ---------- 1. faza: build frontenda ----------
FROM node:22-alpine AS frontend
WORKDIR /frontend

# Vite ugrađuje VITE_* varijable u kod pri buildu (ne pri pokretanju),
# pa ih Railway mora predati kao build argumente.
ARG VITE_AUTH0_DOMAIN
ARG VITE_AUTH0_CLIENT_ID
ARG VITE_AUTH0_AUDIENCE

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---------- 2. faza: backend ----------
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FRONTEND_DIST=/app/static

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY --from=frontend /frontend/dist ./static

# Railway zadaje PORT; lokalno je 8000. Migracije se izvode pri svakom pokretanju
# (alembic preskače već primijenjene), pa je baza uvijek usklađena s kodom.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
