from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models.status import Status, StatusEnum

async def create_status(db: AsyncSession, server_id: int, status: StatusEnum) -> Status:
    db_status = Status(server_id=server_id, status=status)
    db.add(db_status)
    await db.commit()
    await db.refresh(db_status)
    return db_status

async def get_latest_status(db: AsyncSession, server_id: int) -> Optional[Status]:
    result = await db.execute(
        select(Status)
        .where(Status.server_id == server_id)
        .order_by(Status.checked_at.desc())
        .limit(1)
    )
    return result.scalars().first()
