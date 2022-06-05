from fastapi import APIRouter, status

from manager.user import UserManager
from schemas.request.user import UserRegisterIn, UserLoginIn
from schemas.response.user import TokenOut

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=TokenOut)
async def register(data: UserRegisterIn):
    token = await UserManager.register(data.dict())
    return {"token": token}


@router.post("/login/", status_code=status.HTTP_200_OK, response_model=TokenOut)
async def login(data: UserLoginIn):
    token = await UserManager.login(data.dict())
    return {"token": token}
