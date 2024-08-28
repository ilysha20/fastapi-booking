from datetime import date

from sqlalchemy import select, func, and_, or_
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.model import Hotels
from app.hotels.rooms.model import Rooms
from app.bookings.model import Bookings

class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def search_form_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            query = (
                select(
                    Rooms
                )
                .outerjoin(
                    Bookings,
                    and_(
                        Rooms.id == Bookings.room_id,
                        or_(
                            and_(Bookings.date_from >= date_from, Bookings.date_to <= date_to),
                            and_(Bookings.date_from <= date_from, Bookings.date_to > date_from),
                        )
                    )
                )
                .where(
                    hotel_id == Rooms.hotel_id,
                )
                .group_by(Rooms.id)
                .having((Rooms.quantity - func.count(Bookings.room_id)) > 0)
            )
            result = await session.execute(query)
            return result.mappings().all()
