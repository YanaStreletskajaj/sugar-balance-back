from sqlalchemy import select, update, delete, func
from models import async_session, User, SugarDose, InsulinDose, FoodDose
from pydantic import BaseModel, ConfigDict
from typing import List

class SugarDose(BaseModel):
    id: int
    sugar: float
    period: bool
    user: int
    data: str

    model_config = ConfigDict(from_attributes=True)

class FoodDose(BaseModel):
    id: int
    food: float
    user: int
    data: str

    model_config = ConfigDict(from_attributes=True)

class InsulinDose(BaseModel):
    id: int
    insulin: float
    user: int
    data: str

    model_config = ConfigDict(from_attributes=True)

async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user
        
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
    
async def get_sugar_doses(user_id):
    async with async_session() as session:
        sugar_doses = await session.scalars(
            select(sugar_doses).where(SugarDose.user_id == user_id)
        )

        serialized_sugardoses = [
            SugarDose.model_validate(s).model_dump() for s in sugar_doses
        ]

        return serialized_sugardoses

async def get_food_doses(user_id):
    async with async_session() as session:
        food_doses = await session.scalars(
            select(food_doses).where(FoodDose.user_id == user_id)
        )

        serialized_sugardoses = [
            FoodDose.model_validate(s).model_dump() for s in food_doses
        ]

        return serialized_sugardoses

async def get_insulin_doses(user_id):
    async with async_session() as session:
        insulin_doses = await session.scalars(
            select(insulin_doses).where(InsulinDose.user_id == user_id)
        )

        serialized_sugardoses = [
            InsulinDose.model_validate(s).model_dump() for s in insulin_doses
        ]

        return serialized_sugardoses
