import boto3
from PIL import Image
import os

s3 = boto3.client('s3')

DEST_BUCKET = "image-resizer-output-sahil"

def lambda_handler(event, context):

    print(event)

    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    print(f"Bucket: {source_bucket}")
    print(f"Key: {object_key}")

    download_path = f"/tmp/{object_key}"
    upload_path = f"/tmp/resized-{object_key}"

    s3.download_file(source_bucket, object_key, download_path)

    image = Image.open(download_path)
    image.thumbnail((300, 300))
    image.save(upload_path)

    s3.upload_file(
        upload_path,
        DEST_BUCKET,
        f"resized-{object_key}"
    )

    return {"statusCode": 200}
