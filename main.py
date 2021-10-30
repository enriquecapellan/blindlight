from fastapi import FastAPI, File
from utils import extract_labels
import base64

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/image_labels")
async def image_labels(image: str = ''):
    message_bytes = image.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    finalImage = base64_bytes.decode('ascii')

    labels = extract_labels(base64_bytes)
    return labels