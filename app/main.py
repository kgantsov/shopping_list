import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.shopping_list import router as shopping_list_router
from app.api.v1.users import router as users_router
from app.api.v1.auth import router as auth_router
from app.db import db


app = FastAPI()


app.include_router(shopping_list_router, prefix='/API/v1')
app.include_router(users_router, prefix='/API/v1')
app.include_router(auth_router, prefix='/API/v1')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print('...... STARTUP')
    await db.set_bind(os.environ['DATABASE_URL'])

    # Create tables
    await db.gino.create_all()

    # await db.pop_bind().close()
    print('...... CREATED DB')
