from fastapi import FastAPI
from domain import game_router, user_router
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(game_router.router)
app.include_router(user_router.router)


