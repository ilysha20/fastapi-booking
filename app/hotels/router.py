import asyncio
from datetime import date
from typing import List
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter
from pydantic.v1 import parse_obj_as

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.shemas import HotelsInfo

router = APIRouter(
 prefix='/hotels',
 tags=['Отели'],
)

@router.get("/{location}")
@cache(expire=20)
async def get_hotel_by_location_and_time(
        location: str,
        date_from: date,
        date_to: date
):
    await asyncio.sleep(1)
    hotels = await HotelDAO.search_form_hotels(location, date_from, date_to)
    hotel_json = hotels
    return hotel_json

@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(hotel_id: int, date_from: date, date_to: date):
    rooms = await RoomDAO.search_form_rooms(hotel_id, date_from, date_to)
    return rooms

@router.get("/id/{room_id}")
async def get_room(room_id: int):
    rooms = await RoomDAO.find_by_id(room_id)
    return rooms


