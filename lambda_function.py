import boto3
import base64
import os
import traceback
import logging.config
import string
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    try:
        s3 = boto3.resource('s3')
        bucekt_name = os.environ['BUCKET_NAME']
        bucket = s3.Bucket(bucekt_name)

        image_body = base64.b64decode(event['body-json'])

        n = 10
        key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])

        bucket.put_object(
            Body=image_body,
            Key=key
        )

        client = boto3.client('rekognition')
        response = client.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': bucekt_name,
                    'Name': key
                }
            },
            Attributes=['ALL']
        )

        logger.info(response)

        return response

    except Exception as e:
        logger.error(traceback.format_exc())
        raise Exception(traceback.format_exc())
