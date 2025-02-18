from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import init_db
import requests as rq

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await init_db()
    print('Bot is rready')
    yield

app = FastAPI(title='SugarBalance', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/api/sugar_doses/{tg_id}")
async def get_sugar_doses(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_sugar_doses(user.id)

@app.get("/api/food_doses/{tg_id}")
async def get_food_doses(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_food_doses(user.id)

@app.get("/api/insulin_doses/{tg_id}")
async def get_insulin_doses(tg_id: int):
    user = await rq.add_user(tg_id)
    return await rq.get_insulin_doses(user.id)
