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
            bookings_for_selected_dates = (
                select(
                    Bookings.room_id
                )
                .filter(
                    or_(
                        and_(
                            Bookings.date_from < date_from, Bookings.date_to > date_from
                        ),
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_to <= date_to
                        ),
                    )
                )
                .subquery("filter_booking")
            )
            rooms_left = (
                select(
                    (Rooms.quantity - func.count(bookings_for_selected_dates.c.room_id)).label("rooms_left"),
                    Rooms.id
                )
                .select_from(Rooms)
                .outerjoin(bookings_for_selected_dates, bookings_for_selected_dates.c.room_id == Rooms.id)
                .group_by(Rooms.quantity, Rooms.id)
                .cte("rooms_left")
            )
            get_room_info = (
                select(
                    Rooms.__table__.columns,
                    rooms_left.c.rooms_left
                )
                .select_from(Rooms)
                .join(rooms_left, Rooms.id == rooms_left.c.id)
                .where(Rooms.hotel_id == hotel_id)
            )
            result = await session.execute(get_room_info)
            return result.mappings().all()
