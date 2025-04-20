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


async def add_message(user_id: str, text: str):
    async with AsyncSessionLocal() as session:
        new = AiMessage(user_id=user_id, text=text)

        session.add(new)
        await session.commit()


async def select_message():
    async with AsyncSessionLocal() as session:
        s = await session.execute(select(AiMessage))
        res = s.scalars().all()

        for i in res:
            print(i.user_id, i.text)


async def get_database_tables():
    """Получает список всех таблиц в базе данных с подробной информацией"""
    async with engine.connect() as conn:
        # Получаем список всех таблиц с информацией о схеме и типе
        query = text("""
            SELECT 
                table_schema,
                table_name, 
                table_type
            FROM 
                information_schema.tables
            WHERE 
                table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY 
                table_schema, table_name
        """)

        result = await conn.execute(query)
        tables = result.fetchall()

        print("\nСписок таблиц в базе данных:")
        print("-" * 60)
        print(f"{'Схема':<15} {'Таблица':<25} {'Тип':<15}")
        print("-" * 60)

        for table in tables:
            print(f"{table.table_schema:<15} {table.table_name:<25} {table.table_type:<15}")

        print("-" * 60)
        print(f"Всего таблиц: {len(tables)}\n")

        return tables

'''
async def main():
    await init_db()
    await add_message("1", "d")
    await get_database_tables()
    await select_message()

if __name__ == "__main__":
    asyncio.run(main())
'''