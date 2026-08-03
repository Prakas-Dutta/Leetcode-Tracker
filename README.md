# LeetiBuddy — LeetCode Problem Tracker

A full-stack app for logging solved LeetCode problems by the **pattern/technique** you used to solve them (Two Pointers, Sliding Window, DP, Union-Find, etc.), visualizing which patterns you've practiced most, and getting AI-generated suggestions on what to grind next — based on your actual pattern gaps and recent submission history, not a generic study plan.

Most trackers just count solved problems. This one asks *how* you solved them, so you can actually see which patterns you're weak in.

**Live app:** [leetibuddy-mu.vercel.app](https://leetibuddy-mu.vercel.app/)
**Live API:** `https://leetibuddy.onrender.com/`

> Note: the backend runs on Render's free tier, which spins down after periods of inactivity. The first request after idle time may take 30–50 seconds to respond while the service wakes up.

## Features

- **Multi-user accounts** — signup/login with bcrypt-hashed passwords and JWT-based session auth. Every user's problem list, patterns, and suggestions are fully isolated at the database query level.
- **Auto-synced problem catalog** — on startup, the backend pulls LeetCode's full problem list (ID, title, difficulty) from its public API into MySQL. Later runs only insert newly released problems instead of re-fetching everything.
- **Log solves by pattern** — record a solved problem along with the technique used. Duplicate `(id, user, approach)` combinations are rejected with a `409`.
- **Update / delete entries** — correct a recorded approach or remove an entry.
- **Pattern performance dashboard** — a ranked view of how many problems you've solved per pattern.
- **AI-powered practice suggestions** — pulls your pattern breakdown plus your recent accepted submissions (via LeetCode's GraphQL API) and sends them to Gemini, which returns your weak patterns, a suggested focus area, and recommended problems with links.
- **Live solved-problem counter** in the navbar.

## Security

- **Password storage**: bcrypt via `passlib`, truncated consistently to bcrypt's 72-byte limit on both signup and login.
- **Session auth**: JWT access tokens (15-minute expiry) issued on login, verified on every protected endpoint via a FastAPI dependency.
- **Per-user data isolation**: every query on `completed_list` is scoped by the `user_id` decoded from the token — not just enforced in the UI.
- **Frontend route protection**: a `ProtectedRoute` wrapper checks token presence *and* expiry (by decoding the JWT payload client-side) before rendering any authenticated page, redirecting to login otherwise.
- **Session-scoped token storage**: the JWT is kept in `sessionStorage`, not `localStorage`, so it doesn't persist past the browser tab closing.
- **Generic auth errors**: login returns the same `401 Invalid credentials` whether the username doesn't exist or the password is wrong, to avoid leaking which usernames are registered.
- **Environment-based CORS**: allowed origins are read from an `ALLOWED_ORIGINS` environment variable rather than hardcoded, so the deployed frontend's domain is explicitly allow-listed instead of falling back to a wildcard.
- **TLS to the database**: the production database connection (Aiven MySQL) is made over SSL using a CA certificate, not a plaintext connection.

> Note: the frontend expiry check is a UX convenience, not the security boundary — the backend independently re-verifies the token's signature and expiry on every request regardless of what the client believes.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, `mysql-connector-python`, Pydantic, `httpx`, `python-dotenv`, `python-jose`, `passlib[bcrypt]` |
| AI | Google Gemini API (`gemini-3.5-flash-lite`) for practice suggestions |
| Database | MySQL (hosted on Aiven) |
| Frontend | React 19, Vite, React Router v7, Bootstrap 5 |
| Hosting | Render (backend), Vercel (frontend) |

## Architecture

```
┌─────────────┐      REST       ┌──────────────┐      SQL (TLS)   ┌───────────┐
│  React SPA  │ ───────────────▶│   FastAPI    │ ────────────────▶│   MySQL   │
│  (Vercel)   │◀─────────────── │   (Render)   │◀──────────────── │  (Aiven)  │
└─────────────┘        ▲        └──────┬───────┘                  └───────────┘
       │                │               │
       │        JWT (sessionStorage)    │
       │                │               ▼
       │                │      ┌─────────────────┬─────────────────┐
       │                │      ▼                                    ▼
       │                │  LeetCode public API           LeetCode GraphQL API
       │                │  (problem catalog)              (recent submissions)
       │                │                                          │
       └── ProtectedRoute (token presence + expiry check)          ▼
                                                              Gemini API
                                                           (pattern coaching)
```

## Project structure

```
Leetcode-Tracker/
├── server/
│   ├── main.py                          # FastAPI app, routes, auth, and Gemini suggestion logic
│   ├── model.py                         # Pydantic request/response models
│   ├── database.py                      # MySQL connection + schema bootstrap
│   ├── ai_support.py                    # Gemini prompt builder + JSON response parsing
│   ├── leetcode_all_problems.py         # Fetches LeetCode's problem catalog
│   ├── get_recent_leetcode_solutions.py # Fetches a user's recent accepted submissions (GraphQL)
│   ├── ca.pem                           # CA certificate for TLS connection to Aiven MySQL
│   └── requirements.txt
└── client/
    ├── src/
    │   ├── App.jsx                      # Route definitions (auth-required routes wrapped in ProtectedRoute)
    │   ├── Components/
    │   │   ├── LoginForm.jsx
    │   │   ├── SignupForm.jsx
    │   │   ├── ProtectedRoute.jsx       # Guards authenticated routes: checks token presence + expiry
    │   │   ├── Home.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── AddProblemForm.jsx
    │   │   ├── UpdateProblemForm.jsx
    │   │   ├── DeleteProblemForm.jsx
    │   │   ├── Approaches.jsx
    │   │   ├── Performance.jsx          # Pattern performance dashboard
    │   │   ├── ProblemCount.jsx         # Live solved-count badge
    │   │   └── Chatbot.jsx              # AI practice-suggestions view
    │   └── services/
    │       ├── api.js                   # Base API URL (reads VITE_API_BASE_URL)
    │       └── problemService.js        # API client, auth helpers, token expiry check
    └── vite.config.js
```

## API Endpoints

| Method | Endpoint | Auth required | Description |
|---|---|---|---|
| `POST` | `/signup/` | No | Create a new account (`username`, `leetcode_username`, `password`) |
| `POST` | `/login/` | No | Log in, returns a JWT access token |
| `GET` | `/{id}` | No | Get a problem's title/difficulty by LeetCode ID |
| `GET` | `/problem_list/` | Yes | Get total count of solved problems for the current user |
| `GET` | `/completed_list/` | Yes | Get solved-problem counts grouped by pattern |
| `POST` | `/completed_list/` | Yes | Log a solved problem (`leetcode_id`, `approach`) |
| `PATCH` | `/completed_list/` | Yes | Update the recorded approach for a solved problem |
| `DELETE` | `/completed_list/` | Yes | Remove a solved-problem entry |
| `GET` | `/valid_approaches/{id}/` | Yes | Get all approaches already logged for a problem |
| `GET` | `/suggestions/` | Yes | Get AI-generated weak patterns, focus area, and recommended problems |

Authenticated requests pass the JWT in a `token` header (not `Authorization: Bearer`). All write endpoints use parameterized queries (no raw string interpolation) and return proper HTTP status codes — `401` for missing/invalid/expired tokens, `404` for an unknown ID/approach pair, `409` for a duplicate entry or existing username.

## Getting started (local development)

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running MySQL server (local or hosted, e.g. Aiven's free tier)
- A [Gemini API key](https://ai.google.dev/) (for the `/suggestions/` endpoint)

### Backend setup

```bash
cd server
pip install -r requirements.txt

# create a .env file inside server/ with:
# DB_HOST=your_db_host
# DB_PORT=your_db_port
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_NAME=leetcode
# GEMINI_API_KEY=your_gemini_key
# SECRET_KEY=a_long_random_secret_string
# ALGORITHM=HS256
# ALLOWED_ORIGINS=http://localhost:5173

uvicorn main:app --reload
```

On first run, `database.py` creates the `leetcode` database and three tables (`problem_list`, `user_info`, `completed_list`) and populates `problem_list` from LeetCode's public API. The API serves on `http://localhost:8000`.

> If connecting to a managed MySQL host that requires TLS (e.g. Aiven), download the service's CA certificate, save it as `server/ca.pem`, and it'll be picked up automatically by the existing `ssl_ca` connection parameter.

### Frontend setup

```bash
cd client
npm install

# create a .env file inside client/ with:
# VITE_API_BASE_URL=http://localhost:8000

npm run dev
```

The Vite dev server runs on `http://localhost:5173`. Sign up at `/signup`, log in at `/`, and you'll be redirected to `/home`. Visit `/suggestions` to see the AI practice recommendations.

## Deployment

This project is deployed as two independent services:

- **Backend (Render)** — root directory `server`, build command `pip install -r requirements.txt`, start command `uvicorn main:app --host 0.0.0.0 --port $PORT`. All variables listed in the backend `.env` example above are set as environment variables in the Render dashboard.
- **Frontend (Vercel)** — root directory `client`, build command `npm run build`, output directory `dist`. `VITE_API_BASE_URL` is set in the Vercel dashboard to the live Render URL, and `ALLOWED_ORIGINS` on Render is set to the live Vercel URL to close the CORS loop.

## Roadmap

- [ ] Add refresh tokens so users aren't logged out every 15 minutes
- [ ] Replace raw MySQL driver calls with a SQLAlchemy ORM layer
- [ ] Add a test suite (pytest) around the CRUD and auth endpoints
- [ ] Add problem difficulty and topic filters to the performance dashboard
- [ ] Make the LeetCode username used for AI suggestions configurable from the UI instead of signup-only
- [ ] Move token transport from a custom `token` header to standard `Authorization: Bearer`

## License

MIT