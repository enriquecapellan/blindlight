from fastapi import FastAPI, File
from starlette.responses import RedirectResponse
import base64
from pydantic import BaseModel
from utils.ai import describe_image, extract_labels, detect_text
from routers import users
from db import connect_db, close_db

app = FastAPI(title='Blind Light')

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

app.include_router(users.router, tags=["users"], prefix="/users")


class Item(BaseModel):
    image: str


@app.get("/")
def read_root():
    return RedirectResponse("/docs")


@app.post("/image_labels")
async def image_labels(model: Item):
    image = model.image.split(",")[1]
    image_bytes = base64.b64decode(image)

    labels = extract_labels(image_bytes)
    return labels


@app.post("/extract_text")
async def extract_text(image: bytes = File(...)):
    text = detect_text(image)
    return text


@app.post("/image_labels_bytes")
async def image_labels(image: bytes = File(...)):
    labels = extract_labels(image)
    return labels


@app.post("/cloudsight")
async def cloudsight(image: bytes = File(...)):
    image_response = describe_image(image)
    return image_response
