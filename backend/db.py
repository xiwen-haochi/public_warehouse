from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, and_, select
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime, date


# 数据库设置
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./backend/sqlite.db"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# 数据库模型
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(Date, default=date.today)
    createTime = Column(DateTime, default=datetime.now())


class Remark(Base):
    __tablename__ = "remarks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    date = Column(Date, default=date.today)
    createTime = Column(DateTime, default=datetime.now())


class BaseTodo(Base):
    __tablename__ = "base_todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    createTime = Column(DateTime, default=datetime.now())

    # 创建数据库表


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

        # 依赖项


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
