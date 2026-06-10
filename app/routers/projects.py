from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.place import Place
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.aic_client import get_artwork, get_image_url

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    place_ids = data.places or []

    artworks = []
    for external_id in place_ids:
        artwork = await get_artwork(external_id)
        if not artwork:
            raise HTTPException(
                status_code=404, detail=f"Artwork {external_id} not found"
            )
        artworks.append(artwork)

    project = Project(**data.model_dump(exclude={"places"}))
    db.add(project)
    db.commit()
    db.refresh(project)

    for artwork in artworks:
        place = Place(
            project_id=project.id,
            external_id=artwork["id"],
            title=artwork.get("title", "Unknown"),
            artist=artwork.get("artist_display"),
            image_url=get_image_url(artwork.get("image_id")),
        )
        db.add(place)

    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    has_visited = any(p.visited for p in project.places)
    if has_visited:
        raise HTTPException(
            status_code=409, detail="Cannot delete project with visited places"
        )
    db.delete(project)
    db.commit()
