# LeetCode Problem Tracker

A full-stack app for logging solved LeetCode problems by the pattern/approach used to solve them, visualizing which patterns you've practiced the most, and getting AI-generated suggestions on what to practice next.

Backend: **FastAPI + MySQL + Gemini API**
Frontend: **React (Vite) + React Router + Bootstrap**

## Features

- **Auto-synced problem catalog** — on startup, the backend pulls the full LeetCode problem list (ID, title, difficulty) from LeetCode's public problems API and stores it in MySQL. On later runs it only inserts newly released problems instead of re-fetching everything.
- **Log solves by pattern** — record a solved problem along with the technique used (Two Pointers, Sliding Window, Monotonic Stack, DP, Union-Find, etc.), with duplicate (`id`, `approach`) pairs rejected.
- **Update / delete entries** — correct the recorded approach for a problem or remove an entry.
- **Pattern performance dashboard** — a ranked, bar-chart view of how many problems you've solved per pattern.
- **AI-powered practice suggestions** — pulls your pattern breakdown plus your 10 most recent accepted submissions (via LeetCode's GraphQL API) and sends them to Gemini, which returns your weak patterns, a suggested focus area, and a short list of recommended problems with links.
- **Live solved-problem counter** in the navbar.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, `mysql-connector-python`, Pydantic, `httpx`, `python-dotenv` |
| AI | Google Gemini API (`gemini-3.5-flash-lite`) for practice suggestions |
| Database | MySQL |
| Frontend | React 19, Vite, React Router v7, Bootstrap 5 |

## Project structure

```
Leetcode-Tracker/
├── main.py                          # FastAPI app, routes, and Gemini suggestion logic
├── model.py                         # Pydantic request/response models
├── database.py                      # MySQL connection + schema bootstrap
├── leetcode_all_problems.py         # Fetches LeetCode's problem catalog
├── get_recent_leetcode_solutions.py # Fetches a user's recent accepted submissions (GraphQL)
└── react-app/
    ├── src/
    │   ├── App.jsx                  # Route definitions
    │   ├── Components/
    │   │   ├── Home.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── AddProblemForm.jsx
    │   │   ├── DeleteProblemForm.jsx
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
| `GET` | `/chatbot_suggestions/` | Get AI-generated weak patterns, focus area, and recommended problems |

All write endpoints use parameterized queries and return proper HTTP errors — `404` for an unknown ID/approach pair, `409` for a duplicate entry.

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running MySQL server
- A Gemini API key (for the `/chatbot_suggestions/` endpoint)

### Backend setup

```bash
# from the repo root
pip install fastapi uvicorn mysql-connector-python requests pydantic httpx python-dotenv

# create a .env file in the repo root with:
# GEMINI_API_KEY=your_key_here

# set your MySQL credentials as environment variables rather than
# hardcoding them in database.py (see Security note below), then:
uvicorn main:app --reload
```

On first run, `database.py` creates the `leetcode` database and two tables (`problem_list`, `completed_list`) and populates `problem_list` from LeetCode's public API. The API serves on `http://localhost:8000`.

> **Note:** `get_recent_leetcode_solutions.py` fetches your recent accepted submissions from LeetCode's GraphQL API using a hardcoded username (`Prakas26`) inside `main.py`. Update this to your own LeetCode username if you're running the tracker for yourself.

### Frontend setup

```bash
cd react-app
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and is pre-configured (via CORS on the backend) to talk to the API at `http://localhost:8000`. Visit `/suggestions` in the app to see the AI practice recommendations.

## Security note

`database.py` currently reads MySQL credentials from hardcoded values. Before deploying or sharing this repo publicly, move the host/user/password into environment variables (e.g. via `python-dotenv`) and add `.env` to `.gitignore`. The Gemini key is already read from `.env` in `main.py` — make sure that file is never committed.

## Roadmap / ideas

- Move DB credentials to environment variables
- Add authentication for multi-user support
- Replace the raw MySQL driver calls with a proper SQLAlchemy ORM layer
- Add problem difficulty and topic filters to the performance dashboard
- Make the LeetCode username used for AI suggestions configurable from the UI instead of hardcoded