from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotel_by_location_and_time

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

tamplates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotel_by_location_and_time)
):
    return tamplates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels},
    )