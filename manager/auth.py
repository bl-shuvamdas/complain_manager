from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db import database
from environment import settings
from models import User, RollType


class AuthManager:
    @staticmethod
    def encode_token(user):
        try:
            payload = {
                "sub": user['id'],
                "exp": datetime.utcnow() + timedelta(minutes=120)
            }
            return jwt.encode(payload, settings.secret_key, algorithm="HS256")
        except Exception as e:
            # Todo logger
            raise e


class AuthBearer(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)
        try:
            payload = jwt.decode(res.credentials, settings.secret_key, algorithms=["HS256"])
            user_data = await database.fetch_one(User.select().where(User.c.id == payload["sub"]))
            request.state.user = user_data
            return user_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid Token")


oauth2_scheme = AuthBearer()


def is_complainer(request: Request):
    print(request.state)
    if not request.state.user["role"] == RollType.complainer:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def is_approver(request: Request):
    if not request.state.user["role"] == RollType.approver:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def is_admin(request: Request):
    if not request.state.user["role"] == RollType.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
