import boto3
from deep_translator import GoogleTranslator
import cloudsight

auth = cloudsight.SimpleAuth('9pspcVCOgDF5iTHDUcpNOw')
api = cloudsight.API(auth)

client = boto3.client('rekognition')


def extract_labels(image: bytes):
    print('step 3.1')
    response = client.detect_labels(Image={'Bytes': image}, MaxLabels=10)
    print('step 3.2')
    labels = response["Labels"]
    print('step 3.3')
    return list(map((lambda x: translate(x["Name"])), labels))


def detect_text(image: bytes):
    response = client.detect_text(Image={'Bytes': image})
    return response


def translate(text: str):
    translated = GoogleTranslator(source='en', target='es').translate(text)
    return translated


def describe_image(image: bytes):
    response = api.image_request(image, 'image.jpg', {
        'image_request[locale]': 'es',
    })
    status = api.wait(response['token'], timeout=30)
    if status['status'] != cloudsight.STATUS_NOT_COMPLETED:
        return response
    else:
        return None
