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

            # CTE to calculate rooms left for each hotel
            hotels_rooms_left = (
                select(
                    (Hotels.rooms_quantity - func.count(bookings_for_selected_dates.c.room_id)).label("rooms_left"),
                    Rooms.hotel_id
                )
                .select_from(Rooms)
                .outerjoin(bookings_for_selected_dates, bookings_for_selected_dates.c.room_id == Rooms.id)
                .group_by(Hotels.rooms_quantity, Rooms.hotel_id)
                .cte("hotels_rooms_left")
            )

            # Final query to get hotel info and rooms left
            get_hotel_info = (
                select(
                    Hotels.__table__.columns,
                    hotels_rooms_left.c.rooms_left
                )
                .select_from(Hotels)
                .join(hotels_rooms_left, Hotels.id == hotels_rooms_left.c.hotel_id)
                .where(Hotels.location.contains(location.title()))
            )

            hotels_info = await session.execute(get_hotel_info)
            return hotels_info.mappings().all()
