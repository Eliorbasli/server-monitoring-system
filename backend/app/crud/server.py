from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from backend.app.models.server import Server
from backend.app.schemas.server import ServerCreate, ServerUpdate

async def get_server_by_id(db: AsyncSession, server_id: int) -> Optional[Server]:
    result = await db.execute(select(Server).where(Server.id == server_id))
    return result.scalars().first()

async def get_server_by_name(db: AsyncSession, name: str) -> Optional[Server]:
    result = await db.execute(select(Server).where(Server.name == name))
    return result.scalars().first()

async def get_all_servers(db: AsyncSession) -> List[Server]:
    result = await db.execute(select(Server))
    return result.scalars().all()

async def create_server(db: AsyncSession, server_in: ServerCreate) -> Server:
    db_server = Server(name=server_in.name, ip_address=str(server_in.ip_address))
    db.add(db_server)
    await db.commit()
    await db.refresh(db_server)
    return db_server

async def update_server(db: AsyncSession, server_id: int, server_in: ServerUpdate) -> Optional[Server]:
    update_data = server_in.dict(exclude_unset=True)
    
    # Convert ip_add to string if it exists
    if 'ip_address' in update_data and update_data['ip_address'] is not None:
        update_data['ip_address'] = str(update_data['ip_address'])
    
    if not update_data:
        return await get_server_by_id(db, server_id)
    stmt = update(Server).where(Server.id == server_id).values(**update_data)
    await db.execute(stmt)
    await db.commit()
    return await get_server_by_id(db, server_id)

async def delete_server(db: AsyncSession, server_id: int) -> None:
    await db.execute(delete(Server).where(Server.id == server_id))
    await db.commit()
