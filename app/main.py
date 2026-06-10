from fastapi import FastAPI

from app.core.config import settings
from app.database import Base, engine
from app.routers import projects

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Travel Planner API - manage travel projects and places",
)

app.include_router(projects.router)


@app.get("/")
def root():
    return {"message": "Travel Planner API", "version": settings.app_version}
