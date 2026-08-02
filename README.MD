# LeetCode Problem Tracker

A full-stack app for logging solved LeetCode problems by the **pattern/technique** you used to solve them (Two Pointers, Sliding Window, DP, Union-Find, etc.), visualizing which patterns you've practiced most, and getting AI-generated suggestions on what to grind next — based on your actual pattern gaps and recent submission history, not a generic study plan.

Most trackers just count solved problems. This one asks *how* you solved them, so you can actually see which patterns you're weak in.

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

> Note: the frontend expiry check is a UX convenience, not the security boundary — the backend independently re-verifies the token's signature and expiry on every request regardless of what the client believes.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, `mysql-connector-python`, Pydantic, `httpx`, `python-dotenv`, `python-jose`, `passlib[bcrypt]` |
| AI | Google Gemini API (`gemini-3.5-flash-lite`) for practice suggestions |
| Database | MySQL |
| Frontend | React 19, Vite, React Router v7, Bootstrap 5 |

## Architecture

```
┌─────────────┐      REST       ┌──────────────┐      SQL       ┌───────────┐
│  React SPA  │ ───────────────▶│   FastAPI    │ ──────────────▶│   MySQL   │
│  (Vite)     │◀─────────────── │   backend    │◀─────────────── │           │
└─────────────┘        ▲        └──────┬───────┘                 └───────────┘
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
├── main.py                          # FastAPI app, routes, auth, and Gemini suggestion logic
├── model.py                         # Pydantic request/response models
├── database.py                      # MySQL connection + schema bootstrap
├── ai_support.py                    # Gemini prompt builder + JSON response parsing
├── leetcode_all_problems.py         # Fetches LeetCode's problem catalog
├── get_recent_leetcode_solutions.py # Fetches a user's recent accepted submissions (GraphQL)
└── react-app/
    ├── src/
    │   ├── App.jsx                  # Route definitions (auth-required routes wrapped in ProtectedRoute)
    │   ├── Components/
    │   │   ├── LoginForm.jsx
    │   │   ├── SignupForm.jsx
    │   │   ├── ProtectedRoute.jsx   # Guards authenticated routes: checks token presence + expiry
    │   │   ├── Home.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── AddProblemForm.jsx
    │   │   ├── UpdateProblemForm.jsx
    │   │   ├── DeleteProblemForm.jsx
    │   │   ├── Approaches.jsx
    │   │   ├── Performance.jsx      # Pattern performance dashboard
    │   │   ├── ProblemCount.jsx     # Live solved-count badge
    │   │   └── Chatbot.jsx          # AI practice-suggestions view
    │   └── services/
    │       ├── api.js               # Base API URL
    │       └── problemService.js    # API client, auth helpers, token expiry check
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

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running MySQL server
- A [Gemini API key](https://ai.google.dev/) (for the `/suggestions/` endpoint)

### Backend setup

```bash
# from the repo root
pip install fastapi uvicorn mysql-connector-python requests pydantic httpx python-dotenv python-jose[cryptography] "passlib[bcrypt]"

# create a .env file in the repo root with:
# DB_HOST=localhost
# DB_USER=your_mysql_user
# DB_PASSWORD=your_mysql_password
# DB_NAME=leetcode
# GEMINI_API_KEY=your_gemini_key
# LEETCODE_USERNAME=your_leetcode_username
# SECRET_KEY=a_long_random_secret_string
# ALGORITHM=HS256

uvicorn main:app --reload
```

On first run, `database.py` creates the `leetcode` database and three tables (`problem_list`, `user_info`, `completed_list`) and populates `problem_list` from LeetCode's public API. The API serves on `http://localhost:8000`.

### Frontend setup

```bash
cd react-app
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and is pre-configured (via CORS on the backend) to talk to the API at `http://localhost:8000`. Sign up at `/signup`, log in at `/`, and you'll be redirected to `/home`. Visit `/suggestions` to see the AI practice recommendations.

## Roadmap

- [ ] Add refresh tokens so users aren't logged out every 15 minutes
- [ ] Replace raw MySQL driver calls with a SQLAlchemy ORM layer
- [ ] Add a test suite (pytest) around the CRUD and auth endpoints
- [ ] Add problem difficulty and topic filters to the performance dashboard
- [ ] Make the LeetCode username used for AI suggestions configurable from the UI instead of signup-only
- [ ] Move token transport from a custom `token` header to standard `Authorization: Bearer`

## License

MIT