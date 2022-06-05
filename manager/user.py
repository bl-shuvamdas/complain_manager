from asyncpg import UniqueViolationError
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from manager.auth import AuthManager
from models import RollType
from models.user import User
from pydantic import EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data: dict):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(User.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exist")
        user_do = await database.fetch_one(User.select().where(User.c.id == id_))
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data: dict):
        user_do = await database.fetch_one(User.select().where(User.c.email == user_data["email"]))
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(User.select())

    @staticmethod
    async def get_user_by_email(email: EmailStr):
        return await database.fetch_all(User.select().where(User.c.email == email))

    @staticmethod
    async def change_roll(roll: RollType, user_id: int):
        await database.execute(User.update().where(User.c.id == user_id).values(roll=roll))
