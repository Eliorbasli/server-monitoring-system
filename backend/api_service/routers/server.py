from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.app.schemas.server import Server, ServerCreate, ServerUpdate
from backend.app.crud.server import (
    get_server_by_id,
    get_all_servers,
    create_server,
    update_server,
    delete_server,
)
from backend.api_service.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Server, status_code=status.HTTP_201_CREATED)
async def add_server(server_in: ServerCreate, db: AsyncSession = Depends(get_db)):
    server = await create_server(db, server_in)
    return server

@router.get("/", response_model=List[Server])
async def list_servers(db: AsyncSession = Depends(get_db)):
    servers = await get_all_servers(db)
    return servers

@router.get("/{server_id}", response_model=Server)
async def get_server(server_id: int, db: AsyncSession = Depends(get_db)):
    server = await get_server_by_id(db, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.put("/{server_id}", response_model=Server)
async def update_server_info(server_id: int, server_in: ServerUpdate, db: AsyncSession = Depends(get_db)):
    updated_server = await update_server(db, server_id, server_in)
    if not updated_server:
        raise HTTPException(status_code=404, detail="Server not found")
    return updated_server

@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server_info(server_id: int, db: AsyncSession = Depends(get_db)):
    await delete_server(db, server_id)
