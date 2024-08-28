from pydantic import BaseModel, EmailStr, validator


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
