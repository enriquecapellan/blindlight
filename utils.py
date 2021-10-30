import boto3

def extract_labels(image: bytes):
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'Bytes':image}, MaxLabels=10)
    labels = response["Labels"]
    return list(map((lambda x: x["Name"]), labels))