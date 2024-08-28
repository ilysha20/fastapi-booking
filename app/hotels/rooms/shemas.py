from datetime import date

from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: int
    description: date
    price: int
    services: int
    quantity: int
    image_id: int

    class Config:
        from_attributes = True
