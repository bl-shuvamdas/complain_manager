from typing import List

from fastapi import APIRouter, Depends
from fastapi.requests import Request

from manager import (ComplainManager, oauth2_scheme,
                     is_complainer, is_admin, is_approver)
from schemas import ComplaintIn, ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get("/complaints/", response_model=List[ComplaintOut], dependencies=[Depends(oauth2_scheme)])
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplainManager.get_complaints(user=user)


@router.post("/complaints/", response_model=ComplaintOut, dependencies=[Depends(oauth2_scheme), Depends(is_complainer)])
async def create_complaints(request: Request, data: ComplaintIn):
    user = request.state.user
    return await ComplainManager.create_complaint(data=data.dict(), user=user)


@router.delete("/complaints/{pk}", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def delete_complaint(pk: int):
    return await ComplainManager.delete_complaint(id_=pk)


@router.put("/complaints/{pk}/approve/", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_approver)])
async def approve_complaint(pk: int):
    return await ComplainManager.approve(id_=pk)


@router.put("/complaints/{pk}/reject/", status_code=204, dependencies=[Depends(oauth2_scheme), Depends(is_approver)])
async def reject_complaint(pk: int):
    return await ComplainManager.reject(id_=pk)
