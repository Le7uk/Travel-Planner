from fastapi import APIRouter, Query

from app.services.aic_client import get_image_url, search_artworks

router = APIRouter(prefix="/api/v1/artworks", tags=["Artworks"])


@router.get("/search")
async def search(q: str = Query(..., min_length=1, description="Search query")):
    results = await search_artworks(q)
    return [
        {
            "id": item.get("id"),
            "title": item.get("title"),
            "artist": item.get("artist_display"),
            "image_url": get_image_url(item.get("image_id")),
        }
        for item in results
    ]
