from typing import Optional, Mapping, Union, List

from pydantic import BaseModel


class HotelsInfo(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]] = None
    rooms_quantity: int
    image_id: Optional[int] = None
    rooms_left: int

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
