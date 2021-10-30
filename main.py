from fastapi import FastAPI, File
from utils import extract_labels
import base64
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    image: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image_labels")
async def image_labels(model: Item):
    message_bytes = base64.b64decode(model.image+ "==")


    labels = extract_labels(message_bytes)
    return labels