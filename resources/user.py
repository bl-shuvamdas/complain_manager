from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from manager import UserManager, oauth2_scheme, is_admin
from models import RollType
from schemas import UserOut

router = APIRouter(tags=["Users"])


@router.get("/users/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], response_model=List[UserOut])
async def get_user(email: Optional[EmailStr] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()


@router.put("/user/{user_id}/make-admin", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def make_admin(user_id: int):
    await UserManager.change_roll(RollType.admin, user_id)


@router.put("/user/{user_id}/make-approver", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def make_approver(user_id: int):
    await UserManager.change_roll(RollType.approver, user_id)
