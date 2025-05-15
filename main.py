from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from domain import game_router, user_router
from database import Base, engine

app = FastAPI()

app.mount(
     "/media",
     StaticFiles(directory="uploaded_images"),
     name="media"
 )

Base.metadata.create_all(bind=engine)

app.include_router(game_router.router)
app.include_router(user_router.router)


