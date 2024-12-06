import logging
import os

import boto3
from botocore.exceptions import ClientError


def upload(filename, path):
    """Upload a file to S3 via its full URI."""
    _, _, path = path.partition("//")
    parts = path.split("/")
    bucket = parts.pop(0)
    object_name = "/".join(parts)
    upload_file(filename, bucket, object_name)


def upload_file(filename, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(filename)

    # Upload the file
    s3_client = boto3.client("s3")
    try:
        s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
