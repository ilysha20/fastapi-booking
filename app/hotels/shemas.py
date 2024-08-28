from typing import Optional

from pydantic import BaseModel


class HotelsInfo(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[str]
    rooms_quantity: int
    image_id: Optional[int]
    rooms_left: int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
