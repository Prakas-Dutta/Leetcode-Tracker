# LeetCode Problem Tracker

A full-stack app for logging solved LeetCode problems by the pattern/approach used to solve them, and visualizing which patterns you've practiced the most.

Backend: **FastAPI + SQLAlchemy + MySQL**
Frontend: **React (Vite) + React Router + Bootstrap**

## Features

- **Auto-synced problem catalog** — on startup, the backend pulls the full LeetCode problem list (ID, title, difficulty) from LeetCode's public problems API and stores it in MySQL. On later runs it only inserts newly released problems instead of re-fetching everything.
- **Log solves by pattern** — record a solved problem along with the technique used (Two Pointers, Sliding Window, Monotonic Stack, DP, Union-Find, etc.), with duplicate (`id`, `approach`) pairs rejected.
- **Update / delete entries** — correct the recorded approach for a problem or remove an entry.
- **Pattern performance dashboard** — a ranked, bar-chart view of how many problems you've solved per pattern.
- **Live solved-problem counter** in the navbar.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, SQLAlchemy-style raw MySQL driver (`mysql-connector-python`), Pydantic |
| Database | MySQL |
| Frontend | React 19, Vite, React Router v7, Bootstrap 5 |

## Project structure

```
Leetcode-Tracker/
├── main.py                    # FastAPI app & routes
├── model.py                   # Pydantic request/response models
├── database.py                # MySQL connection + schema bootstrap
├── leetcode_all_problems.py   # Fetches LeetCode's problem catalog
└── react-app/
    ├── src/
    │   ├── App.jsx             # Route definitions
    │   ├── Components/
    │   │   ├── Home.jsx
    │   │   ├── Navbar.jsx
    │   │   ├── AddProblemForm.jsx
    │   │   ├── DeleteProblemForm.jsx
    │   │   ├── Performance.jsx     # Pattern performance dashboard
    │   │   └── ProblemCount.jsx    # Live solved-count badge
    │   └── services/
    │       └── problemService.js   # API client
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

All write endpoints use parameterized queries and return proper HTTP errors — `404` for an unknown ID/approach pair, `409` for a duplicate entry.

## Getting started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A running MySQL server

### Backend setup

```bash
# from the repo root
pip install fastapi uvicorn mysql-connector-python requests pydantic

# set your MySQL credentials as environment variables rather than
# hardcoding them in database.py (see Security note below), then:
uvicorn main:app --reload
```

On first run, `database.py` creates the `leetcode` database and two tables (`problem_list`, `completed_list`) and populates `problem_list` from LeetCode's public API. The API serves on `http://localhost:8000`.

### Frontend setup

```bash
cd react-app
npm install
npm run dev
```

The Vite dev server runs on `http://localhost:5173` and is pre-configured (via CORS on the backend) to talk to the API at `http://localhost:8000`.

## Security note

`database.py` currently reads MySQL credentials from hardcoded values. Before deploying or sharing this repo publicly, move the host/user/password into environment variables (e.g. via `python-dotenv`) and add `.env` to `.gitignore`.

## Roadmap / ideas

- Move DB credentials to environment variables
- Add authentication for multi-user support
- Replace the raw MySQL driver calls with a proper SQLAlchemy ORM layer
- Add problem difficulty and topic filters to the performance dashboard