from datetime import date

from fastapi import APIRouter, Request, Depends

from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_current_user
from app.users.model import Users

router = APIRouter(
 prefix='/rooms',
 tags=['Комнаты'],
)