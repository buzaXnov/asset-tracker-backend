from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()
# postgresql db
DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5554/filipbutic"

async_engine = create_async_engine(
    DATABASE_URL,
)
async_session = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db():
    async with async_session() as db:
        try:
            yield db
        finally:
            await db.close()
