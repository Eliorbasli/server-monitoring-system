from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class StatusEnum(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"

class Status(BaseModel):
    id: int
    server_id: int
    status: StatusEnum
    checked_at: datetime

    class Config:
        orm_mode = True
