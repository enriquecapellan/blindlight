import boto3
from deep_translator import GoogleTranslator
import cloudsight

auth = cloudsight.SimpleAuth('9pspcVCOgDF5iTHDUcpNOw')
api = cloudsight.API(auth)

client = boto3.client('rekognition')


def extract_labels(image: bytes):
    response = client.detect_labels(Image={'Bytes': image}, MaxLabels=10)
    labels = response["Labels"]
    return list(map((lambda x: translate(x["Name"])), labels))


def detect_text(image: bytes):
    response = client.detect_text(Image={'Bytes': image})
    return response


def translate(text: str):
    translated = GoogleTranslator(source='en', target='es').translate(text)
    return translated


async def describe_image(image: bytes):
    response = api.image_request(image, 'image.jpg', {
        'image_request[locale]': 'en-US',
    })

    status = api.wait(response['token'], timeout=60)
    if status['status'] != cloudsight.STATUS_NOT_COMPLETED:
        return status
    else:
        return None
