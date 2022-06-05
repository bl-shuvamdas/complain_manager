from pydantic import BaseModel

from models import RollType
from schemas.base import UserBase


class TokenOut(BaseModel):
    token: str


class UserOut(UserBase):
    id: int
    first_name: str
    last_name: str
    phone: str
    iban: str
    roll: RollType
