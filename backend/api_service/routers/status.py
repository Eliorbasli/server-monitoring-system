from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.status import Status, StatusEnum
from app.crud.status import get_latest_status, create_status
from api_service.dependencies import get_db

router = APIRouter()

@router.get("/{server_id}", response_model=Status)
async def get_server_status(server_id: int, db: AsyncSession = Depends(get_db)):
    status = await get_latest_status(db, server_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

@router.post("/{server_id}", response_model=Status)
async def manual_status_update(server_id: int, status_in: StatusEnum, db: AsyncSession = Depends(get_db)):
    status = await create_status(db, server_id, status_in)
    return status
