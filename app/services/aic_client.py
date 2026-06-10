import httpx

AIC_BASE_URL = "https://api.artic.edu/api/v1"


async def get_artwork(artwork_id: int) -> dict | None:
    """Fetch artwork from Art Institute of Chicago API by ID."""

    url = f"{AIC_BASE_URL}/artworks/{artwork_id}"
    params = {"fields": "id,title,artist_display,image_id"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return data.get("data")
            return None
        except httpx.RequestError:
            return None


def get_image_url(image_id: str | None):
    if not image_id:
        return None
    return f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg"
