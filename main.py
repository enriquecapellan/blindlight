from fastapi import FastAPI, File
from utils import extract_labels

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image_labels")
async def image_labels(image: bytes = File(...)):
    labels = extract_labels(image)
    return labels