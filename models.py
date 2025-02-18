from sqlalchemy import ForeignKey, String, BigInteger, func
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from datetime import datetime

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3', echo=True)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    username: Mapped[str]
    date_of_birth: Mapped[str]
    diabet_type: Mapped[bool]


class SugarDose(Base):
    __tablename__ = 'sugar_doses'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    sugar: Mapped[float]
    period: Mapped[bool]


class FoodDose(Base):
    __tablename__ = 'food_doses'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    food: Mapped[float]

class InsulinDose(Base):
    __tablename__ = 'insulin_doses'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    insulin: Mapped[float]

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)