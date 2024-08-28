from datetime import date

from dns.e164 import query
from sqlalchemy import select, func, and_, or_
from app.dao.base import BaseDAO
from app.hotels.model import Hotels
from app.bookings.model import Bookings
from app.database import async_session_maker
from app.hotels.rooms.model import Rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def search_form_hotels(cls, location: str, date_from=date, date_to=date):
        async with async_session_maker() as session:
            query = (
                select(
                    Hotels
                )
            )
            result = await session.execute(query)
            return result.mappings().all()
