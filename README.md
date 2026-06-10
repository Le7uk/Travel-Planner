
# Travel Planner API

A RESTful API for managing travel projects and places to visit, built with FastAPI and SQLite. Places are sourced from the [Art Institute of Chicago API](https://api.artic.edu/docs/).

## Tech Stack

- **Python 3.11** + **FastAPI**
- **SQLAlchemy** + **SQLite**
- **Pydantic v2** — data validation
- **httpx** — async HTTP client
- **Docker** + **docker-compose**

## Features

- Full CRUD for travel projects
- Add/manage places from the Art Institute of Chicago API
- Search artworks by name to find IDs
- Business logic: max 10 places, no duplicates, auto-complete project
- Basic HTTP Authentication
- Interactive API docs via Swagger UI

## Quick Start

### Option 1: Docker (recommended)

```bash
git clone https://github.com/Le7uk/Travel-Planner.git
cd Travel-Planner
cp .env.example .env
docker-compose up --build
```

### Option 2: Local

```bash
git clone https://github.com/Le7uk/Travel-Planner.git
cd Travel-Planner

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

**API:** http://localhost:8000  
**Swagger UI:** http://localhost:8000/docs  
**OpenAPI JSON:** http://localhost:8000/openapi.json

## Authentication

All endpoints require **HTTP Basic Authentication**.

| Credential | Default |
|---|---|
| Username | `admin` |
| Password | `secret` |

Configure in `.env` file.

## Environment Variables

Copy `.env.example` to `.env`:

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | Travel Planner | Application name |
| `APP_VERSION` | 1.0.0 | API version |
| `DATABASE_URL` | `sqlite:///./travel_planner.db` | Database URL |
| `AUTH_USERNAME` | `admin` | Basic auth username |
| `AUTH_PASSWORD` | `secret` | Basic auth password |

## API Endpoints

### Artworks (Art Institute of Chicago)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/artworks/search?q={query}` | Search artworks by name |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/projects` | Create project (with optional places) |
| GET | `/api/v1/projects` | List all projects |
| GET | `/api/v1/projects/{id}` | Get project by ID |
| PATCH | `/api/v1/projects/{id}` | Update project name/description/date |
| DELETE | `/api/v1/projects/{id}` | Delete project |

### Places

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/projects/{id}/places` | Add place to project |
| GET | `/api/v1/projects/{id}/places` | List all places in project |
| GET | `/api/v1/projects/{id}/places/{place_id}` | Get single place |
| PATCH | `/api/v1/projects/{id}/places/{place_id}` | Update notes or visited status |

## Example Workflow

### 1. Search for artworks
```
GET /api/v1/artworks/search?q=sunday
```
Returns list of artworks with IDs, titles, artists.

### 2. Create a project with places
```json
POST /api/v1/projects
{
  "name": "Chicago Trip",
  "description": "Art museum visit",
  "start_date": "2024-07-01",
  "places": [27992, 20684]
}
```

### 3. Add a place to existing project
```json
POST /api/v1/projects/1/places
{
  "external_id": 11434
}
```

### 4. Add a note to a place
```json
PATCH /api/v1/projects/1/places/1
{
  "notes": "Second floor, room 240. Don't miss the audio guide!"
}
```

### 5. Mark place as visited
```json
PATCH /api/v1/projects/1/places/1
{
  "visited": true
}
```
When all places are visited → project status automatically changes to `completed`.

## Business Rules

- Maximum **10 places** per project
- Cannot add the **same place twice** to a project
- Cannot **delete** a project that has visited places
- Project auto-completes when **all places are visited**
- Places are validated against the **AIC API** before saving
