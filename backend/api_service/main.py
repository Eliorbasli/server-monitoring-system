from fastapi import FastAPI
from backend.api_service.routers import server, status
from backend.api_service.logger import setup_logger
from backend.api_service.dependencies import get_db
from backend.app.db.session import engine
from backend.app.db.base import Base
import uvicorn
from sqlalchemy.exc import OperationalError
import asyncio


app = FastAPI(title="Server Monitoring API")

# Setup logger
setup_logger()

async def init_db():
    from backend.app.models import server, status
    retries = 10
    delay = 2
    for i in range(retries):
        try:
            print(f"⏳ Connecting to DB... Attempt {i+1}/{retries}")
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("✅ Database tables created")
                return
        except Exception as e:
            print(f"❌ DB connection failed ({i+1}/{retries}): {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("❌ Could not connect to the database after several attempts.")

@app.on_event("startup")
async def startup():
    # Create database tables if they don't exist
    await init_db()

# Include API routers with prefixes
app.include_router(server.router, prefix="/servers", tags=["servers"])
app.include_router(status.router, prefix="/status", tags=["status"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Server Monitoring API"}

if __name__ == "__main__":
    uvicorn.run("api_service.main:app", host="0.0.0.0", port=8000, reload=True)
