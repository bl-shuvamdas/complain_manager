from fastapi import APIRouter
from resources import auth, complainer, user

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(complainer.router)
api_router.include_router(user.router)
