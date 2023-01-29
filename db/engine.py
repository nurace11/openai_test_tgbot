from typing import Union


from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    # echo - sql logs in console
    # pool_pre_ping - checking for connection with db
    engine = _create_async_engine(url=url, echo=True, pool_pre_ping=True)
    print(type(engine))
    return engine


async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)
