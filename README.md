# Sentinel Shield (SurakshaSetu)

A full-stack public safety and incident-response platform. Citizens can report incidents, trigger SOS alerts, find safe routes, and engage with a community feed, while administrators manage users, threats, officer dispatch, and analytics from a dedicated admin panel.

## Features

### Citizen Portal
- **Incident Reporting** — file incident reports with details, location, and image uploads
- **SOS** — one-tap emergency alert flow
- **Safe Route** — location-risk-aware route guidance
- **Community** — community feed for posts and discussion (MongoDB-backed)
- **Content Library** — safety resources and educational content
- **AI Chatbot** — floating in-app assistant powered by Google Gemini
- **Dashboard** — personal overview of reports and activity

### Admin Panel (`/admin`)
- **Dashboard** — real-time stats (users, reports, active incidents, resolved cases), live security feed, threat map
- **User Management** — create/delete users, role assignment (User / Moderator / Admin), block/unblock, search
- **Threats & Incidents** — active-threat tracking, high-risk cases, severity and status monitoring
- **Dispatch** — assign available officers to active incidents, track officer status
- **Officers** — officer roster, duty status, resolution stats, location and rating
- **Analytics** — incident trends, category distribution, resolution status charts, high-risk areas
- **Security Operations** — system health (API, DB, WebSocket, Redis), security events and actions
- **Audit Logs** — searchable logs with level filters (INFO / WARN / ERROR / CRITICAL) and IP tracking

See [ADMIN_PANEL_GUIDE.md](ADMIN_PANEL_GUIDE.md) for admin setup and default credentials, and [ADMIN_LOGIN_INSTRUCTIONS.md](ADMIN_LOGIN_INSTRUCTIONS.md) for login steps.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, GSAP, Recharts, React Router, Axios, Lucide icons |
| Backend | FastAPI, SQLModel / SQLAlchemy (async), Pydantic v2, Uvicorn |
| Databases | PostgreSQL (primary, via asyncpg) · MongoDB (community features, via Motor — optional) |
| AI | Google Gemini (`google-genai`), OpenAI fallback, mock provider when no key is set |
| Auth | JWT (python-jose) with access + refresh tokens |
| Media | Pillow image processing, static uploads served at `/uploads` |

## Project Structure

```
DE finale/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # auth, community, incidents, logs, admin, ai
│   │   ├── core/               # settings (all driven by backend/.env)
│   │   ├── db/                 # PostgreSQL session + MongoDB connection
│   │   ├── models/             # user, incident, report, officer, notification, audit_log, ...
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # business logic, AI providers, data seeding
│   │   └── main.py             # FastAPI app entrypoint
│   ├── .env.example            # template — copy to .env and fill in
│   ├── create_admin.py         # bootstrap an admin user
│   ├── migrate.py              # DB migration helper
│   └── seed_community.py       # seed community data
├── frontend/
│   └── src/
│       ├── pages/              # Home, Auth, Dashboard, ReportIncident, SOS, SafeRoute, Community, ...
│       ├── admin/              # AdminLayout, AdminRoutes, admin pages & components
│       ├── components/         # Navbar, Layout, LoginModal, FloatingChatbot, ...
│       ├── contexts/           # React context providers (auth, etc.)
│       └── services/           # API client layer
├── security-portal/            # supplementary portal (WIP)
├── start-dev.ps1               # start backend + frontend together
├── start-backend.ps1
└── start-frontend.ps1
```

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL (running locally, database `sentinel_db`)
- MongoDB (optional — only needed for community features)

### 1. Backend

```powershell
cd backend
pip install -r requirements.txt

# Copy the env template and fill in your values (DB password, Gemini API key, ...)
copy .env.example .env

uvicorn app.main:app --reload --port 8000
```

On startup the backend creates tables automatically and seeds initial data (`SEED_DATA_ON_STARTUP=true`). To create an admin user:

```powershell
python create_admin.py
```

- API root: http://127.0.0.1:8000
- Interactive docs (Swagger): http://127.0.0.1:8000/docs
- OpenAPI spec: `/api/v1/openapi.json`

### 2. Frontend

```powershell
cd frontend
npm install
npm run dev
```

App runs at http://127.0.0.1:5174. The API base URL comes from `frontend/.env` (`VITE_API_URL=http://127.0.0.1:8000/api/v1`) — restart Vite after changing it.

### One-command dev startup

```powershell
.\start-dev.ps1   # launches backend (port 8000) and frontend (port 5174)
```

## Configuration

All backend settings are loaded from `backend/.env` (see `backend/app/core/config.py` for the full list, and `backend/.env.example` for a template):

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_SERVER` / `POSTGRES_PORT` / `POSTGRES_DB` | `postgres` / `root` / `localhost` / `5432` / `sentinel_db` | PostgreSQL connection parts |
| `DATABASE_URL` | assembled from `POSTGRES_*` | Set directly to override the assembled URL |
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection (community) |
| `MONGODB_ENABLED` | `false` | Toggle MongoDB features |
| `SECRET_KEY` | – | JWT signing key — **set a strong value** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token lifetime |
| `SEED_DATA_ON_STARTUP` | `true` | Auto-seed demo data on boot |
| `GEMINI_API_KEY` | – | Google Gemini key for the AI chatbot (preferred) |
| `OPENAI_API_KEY` | – | OpenAI key (used if no Gemini key) |
| `UPLOAD_DIR` | `uploads/` | Upload folder; relative paths resolve against `backend/` |
| `BACKEND_CORS_ORIGINS` | localhost:5173/5174 | Allowed frontend origins |

If neither AI key is set, the chatbot falls back to a mock provider so the app still runs.

## API Overview

All endpoints are prefixed with `/api/v1`:

| Prefix | Purpose |
|---|---|
| `/auth` | Register, login, JWT refresh |
| `/incidents` | Incident reporting and management |
| `/community` | Community posts and feed |
| `/logs` | Audit / activity logs |
| `/admin` | Admin dashboard, users, officers, dispatch, analytics |
| `/ai` | AI chatbot (`/ai/chat`), report analysis, threat explanations |

## Scripts

| Script | Purpose |
|---|---|
| `start-dev.ps1` | Start backend + frontend together |
| `start-backend.ps1` | Start backend only |
| `start-frontend.ps1` | Start frontend only |
| `backend/create_admin.py` | Create an admin user |
| `backend/migrate.py` | Run DB migrations |
| `backend/seed_community.py` | Seed community data |
| `backend/test_admin.ps1` | Smoke-test admin endpoints |

## Production Notes

- Set a strong `SECRET_KEY` and disable `SEED_DATA_ON_STARTUP`
- Change the default admin credentials immediately
- Never commit `backend/.env` — it holds real secrets; `.env.example` is the shareable template
- Build the frontend with `npm run build` (output in `frontend/dist/`)
- A `docker-compose.yml` is available in `backend/` for containerized databases
