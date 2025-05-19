from datetime import datetime
from pydantic import BaseModel, IPvAnyAddress

class ServerBase(BaseModel):
    name: str
    ip_address: IPvAnyAddress

class ServerCreate(ServerBase):
    pass

class ServerUpdate(BaseModel):
    name: str | None = None
    ip_address: IPvAnyAddress | None = None

class Server(ServerBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
