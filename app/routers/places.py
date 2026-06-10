from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.place import Place
from app.models.project import Project
from app.schemas.place import PlaceCreate, PlaceResponse, PlaceUpdate
from app.services.aic_client import get_artwork, get_image_url

router = APIRouter(prefix="/api/v1/projects/{project_id}/places", tags=["Places"])

MAX_PLACES = 10


def get_project_or_404(project_id: int, db: Session) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=PlaceResponse, status_code=201)
async def add_place(project_id: int, data: PlaceCreate, db: Session = Depends(get_db)):
    project = get_project_or_404(project_id, db)

    if len(project.places) >= MAX_PLACES:
        raise HTTPException(
            status_code=422, detail="Project cannot have more than 10 places"
        )

    existing = (
        db.query(Place)
        .filter(Place.project_id == project_id, Place.external_id == data.external_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409, detail="Place already exists in this project"
        )

    artwork = await get_artwork(data.external_id)
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found in AIC API")

    place = Place(
        project_id=project_id,
        external_id=data.external_id,
        title=artwork.get("title", "Unknown"),
        artist=artwork.get("artist_display"),
        image_url=get_image_url(artwork.get("image_id")),
    )
    db.add(place)
    db.commit()
    db.refresh(place)
    return place


@router.get("/", response_model=list[PlaceResponse])
def list_places(project_id: int, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    return db.query(Place).filter(Place.project_id == project_id).all()


@router.get("/{place_id}", response_model=PlaceResponse)
def get_place(project_id: int, place_id: int, db: Session = Depends(get_db)):
    get_project_or_404(project_id, db)
    place = (
        db.query(Place)
        .filter(Place.id == place_id, Place.project_id == project_id)
        .first()
    )
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.patch("/{place_id}", response_model=PlaceResponse)
def update_place(
    project_id: int, place_id: int, data: PlaceUpdate, db: Session = Depends(get_db)
):
    get_project_or_404(project_id, db)
    place = (
        db.query(Place)
        .filter(Place.id == place_id, Place.project_id == project_id)
        .first()
    )
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(place, field, value)

    db.commit()
    db.refresh(place)

    # Auto-complete project if all places are visited
    project = db.query(Project).filter(Project.id == project_id).first()
    all_visited = all(p.visited for p in project.places)
    if all_visited and len(project.places) > 0:
        project.status = "completed"
        db.commit()

    return place
