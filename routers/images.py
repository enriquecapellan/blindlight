from fastapi import APIRouter, HTTPException, status, File
from pydantic import BaseModel
import base64

from utils.ai import describe_image, extract_labels, detect_text

router = APIRouter()


class Item(BaseModel):
    image: str


class AnalyzeModel(BaseModel):
    image: str
    extract_labels: bool
    extract_text: bool
    generate_description: bool


@router.post('/labels')
async def get_labels(model: Item):
    image = model.image.split(",")[1]
    image_bytes = base64.b64decode(image)

    labels = extract_labels(image_bytes)
    return labels


@router.post("/text")
async def extract_text(model: Item):
    image = model.image.split(",")[1]
    image_bytes = base64.b64decode(image)
    text = detect_text(image_bytes)
    return text


@router.post("/description")
async def get_description(model: Item):
    image = model.image.split(",")[1]
    image_bytes = base64.b64decode(image)
    description = await describe_image(image_bytes)
    return description


@router.post("/analyze")
async def analyze(model: AnalyzeModel):
    image = model.image.split(",")[1]
    image_bytes = base64.b64decode(image)

    text =''
    labels = ''
    description = ''
    if (model.extract_labels):
        labels = extract_labels(image_bytes)
    if (model.extract_text):
        text = detect_text(image_bytes)
    if (model.generate_description):
        description = await describe_image(image_bytes)
    
    return {'description': description, 'labels': labels, 'text': text}


@router.post("/labels_bytes")
async def image_labels(image: bytes = File(...)):
    labels = extract_labels(image)
    return labels
