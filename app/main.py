from fastapi import FastAPI, Depends

from app.core.auth import verify_credentials
from app.core.config import settings
from app.database import Base, engine
from app.routers import projects, places

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Travel Planner API - manage travel projects and places",
    dependencies=[Depends(verify_credentials)],
)

app.include_router(projects.router)
app.include_router(places.router)


@app.get("/")
def root():
    return {"message": "Travel Planner API", "version": settings.app_version}
