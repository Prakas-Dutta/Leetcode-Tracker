# LeetCode Problem Tracker

A full-stack app for logging solved LeetCode problems by the **pattern/technique** you used to solve them (Two Pointers, Sliding Window, DP, Union-Find, etc.), visualizing which patterns you've practiced most, and getting AI-generated suggestions on what to grind next — based on your actual pattern gaps and recent submission history, not a generic study plan.

Most trackers just count solved problems. This one asks *how* you solved them, so you can actually see which patterns you're weak in.

## Features

- **Auto-synced problem catalog** — on startup, the backend pulls LeetCode's full problem list (ID, title, difficulty) from its public API into MySQL. Later runs only insert newly released problems instead of re-fetching everything.
- **Log solves by pattern** — record a solved problem along with the technique used. Duplicate `(id, approach)` pairs are rejected with a `409`.
- **Update / delete entries** — correct a recorded approach or remove an entry.
- **Pattern performance dashboard** — a ranked view of how many problems you've solved per pattern.
- **AI-powered practice suggestions** — pulls your pattern breakdown plus your 10 most recent accepted submissions (via LeetCode's GraphQL API) and sends them to Gemini, which returns your weak patterns, a suggested focus area, and recommended problems with links.
- **Live solved-problem counter** in the navbar.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, `mysql-connector-python`, Pydantic, `httpx`, `python-dotenv` |
| AI | Google Gemini API (`gemini-3.5-flash-lite`) for practice suggestions |
| Database | MySQL |
| Frontend | React 19, Vite, React Router v7, Bootstrap 5 |

## Architecture

```
┌─────────────┐      REST       ┌──────────────┐      SQL       ┌───────────┐
│  React SPA  │ ───────────────▶│   FastAPI    │ ──────────────▶│   MySQL   │
│  (Vite)     │◀─────────────── │   backend    │◀─────────────── │           │
└─────────────┘                 └──────┬───────┘                 └───────────┘
                                        │
                          ┌─────────────┼─────────────┐
                          ▼                            ▼
                 LeetCode public API           LeetCode GraphQL API
                 (problem catalog)              (recent submissions)
                                        │
                                        ▼
                                 Gemini API
                              (pattern coaching)
```

## Project structure

```
Leetcode-Tracker/
├── main.py                          # FastAPI app, routes, and Gemini suggestion logic
├── model.py                         # Pydantic request/response models
├── database.py                      # MySQL connection + schema bootstrap
├── ai_support.py                    # Gemini prompt builder + JSON response parsing
├── leetcode_all_problems.py         # Fetches LeetCode's problem catalog
├── get_recent_leetcode_solutions.py # Fetches a user's recent accepted submissions (GraphQL)
└── react-app/
    ├── src/
    │   ├── App.jsx                  # Route definitions
    │   ├── Components/
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
    │       └── problemService.js    # API client
    └── vite.config.js
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/{id}` | Get a problem's title/difficulty by LeetCode ID |
| `GET` | `/problem_list/` | Get total count of solved problems |
| `GET` | `/completed_list/` | Get solved-problem counts grouped by pattern |
| `POST` | `/completed_list/` | Log a solved problem (`leetcode_id`, `approach`) |
| `PATCH` | `/completed_list/` | Update the recorded approach for a solved problem |
| `DELETE` | `/completed_list/` | Remove a solved-problem entry |
| `GET` | `/valid_approaches/{id}` | Get all approaches already logged for a problem |
| `GET` | `/suggestions/` | Get AI-generated weak patterns, focus area, and recommended problems |

All write endpoints use parameterized queries (no raw string interpolation) and return proper HTTP status codes — `404` for an unknown ID/approach pair, `409` for a duplicate entry.

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running MySQL server
- A [Gemini API key](https://ai.google.dev/) (for the `/suggestions/` endpoint)

### Backend setup

```bash
# from the repo root
pip install fastapi uvicorn mysql-connector-python requests pydantic httpx python-dotenv

# create a .env file in the repo root with:
# DB_HOST=localhost
# DB_USER=your_mysql_user
# DB_PASSWORD=your_mysql_password
# DB_NAME=leetcode
# GEMINI_API_KEY=your_gemini_key
# LEETCODE_USERNAME=your_leetcode_username

uvicorn main:app --reload
```

On first run, `database.py` creates the `leetcode` database and two tables (`problem_list`, `completed_list`) and populates `problem_list` from LeetCode's public API. The API serves on `http://localhost:8000`.

### Frontend setup

```bash
cd react-app
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and is pre-configured (via CORS on the backend) to talk to the API at `http://localhost:8000`. Visit `/suggestions` in the app to see the AI practice recommendations.

## Roadmap

- [ ] Add authentication for multi-user support
- [ ] Replace raw MySQL driver calls with a SQLAlchemy ORM layer
- [ ] Add a test suite (pytest) around the CRUD endpoints
- [ ] Add problem difficulty and topic filters to the performance dashboard
- [ ] Make the LeetCode username used for AI suggestions configurable from the UI instead of `.env`-only

## License

MIT