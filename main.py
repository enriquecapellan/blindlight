from fastapi import FastAPI
from starlette.responses import RedirectResponse

from routers import users, images, places
from db import connect_db, close_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Blind Light')

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, tags=["users"], prefix="/users")
app.include_router(images.router, tags=["images"], prefix="/image")
app.include_router(places.router, tags=["places"], prefix="/places")


@app.get("/")
def read_root():
    return RedirectResponse("/docs")
