# Travel Planner API

A RESTful API for managing travel projects and places to visit, built with FastAPI and SQLite.

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database
- **Pydantic** — data validation
- **httpx** — async HTTP client for AIC API
- **Docker** — containerization

## Features

- CRUD for travel projects
- Add/manage places from the [Art Institute of Chicago API](https://api.artic.edu/docs/)
- Business rules: max 10 places per project, no duplicates, auto-complete project
- Basic HTTP Authentication
- Interactive API docs (Swagger UI)

## Getting Started

### Option 1: Docker (recommended)

```bash
# 1. Clone the repo
git clone https://github.com/Le7uk/Travel-Planner.git
cd Travel-Planner

# 2. Copy env file
cp .env.example .env

# 3. Run
docker-compose up --build
```

### Option 2: Local

```bash
# 1. Clone and create virtual env
git clone https://github.com/Le7uk/Travel-Planner.git
cd Travel-Planner
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Copy env file
cp .env.example .env

# 4. Run
uvicorn app.main:app --reload
```

API available at: **http://localhost:8000**

## API Documentation

Swagger UI: **http://localhost:8000/docs**

## Authentication

All endpoints require **Basic Authentication**:
- Username: `admin`
- Password: `secret`

(Configurable via `.env` file)

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | Travel Planner | Application name |
| `APP_VERSION` | 1.0.0 | API version |
| `DATABASE_URL` | sqlite:///./travel_planner.db | Database URL |
| `AUTH_USERNAME` | admin | Basic auth username |
| `AUTH_PASSWORD` | secret | Basic auth password |

## API Endpoints

### Projects
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/projects` | Create project (with optional places) |
| GET | `/api/v1/projects` | List all projects |
| GET | `/api/v1/projects/{id}` | Get project by ID |
| PATCH | `/api/v1/projects/{id}` | Update project |
| DELETE | `/api/v1/projects/{id}` | Delete project |

### Places
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/projects/{id}/places` | Add place to project |
| GET | `/api/v1/projects/{id}/places` | List places in project |
| GET | `/api/v1/projects/{id}/places/{place_id}` | Get single place |
| PATCH | `/api/v1/projects/{id}/places/{place_id}` | Update notes/visited |

## Example Requests

### Create project with places
```json
POST /api/v1/projects
{
  "name": "Chicago Trip",
  "description": "Art museum visit",
  "start_date": "2024-07-01",
  "places": [27992, 20684]
}
```

### Mark place as visited
```json
PATCH /api/v1/projects/1/places/1
{
  "visited": true
}
```

### Add note to place
```json
PATCH /api/v1/projects/1/places/1
{
  "notes": "Second floor, room 201"
}
```

## Business Rules

- Maximum **10 places** per project
- Cannot add the **same place twice** to a project
- Cannot **delete a project** that has visited places
- Project status changes to **completed** when all places are visited
- Places are validated against the **Art Institute of Chicago API**
