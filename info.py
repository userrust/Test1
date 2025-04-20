import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, String, Column, Integer, text

DATABASE_URL = "postgresql+asyncpg://fastbankpost_user:eU2NDKOVu8cHT3Ke61tLWITQ7CTzz0IG@dpg-d01lln3e5dus73bau910-a.frankfurt-postgres.render.com:5432/fastbankpost"


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


class AiMessage(Base):
    __tablename__ = "aimessage"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    text = Column(String)


engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def select_message():
    async with AsyncSessionLocal() as session:
        s = await session.execute(select(AiMessage))
        res = s.scalars().all()

        for i in res:
            print(i.user_id, i.text)


async def main():
    await init_db()
    await select_message()


if __name__ == "__main__":
    asyncio.run(main())
