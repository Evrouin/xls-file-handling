import os
import logging
import boto3

from botocore.exceptions import UnknownClientMethodError
class S3FileUploadGateway():
    @classmethod
    def put_object(cls, bucket_name, file_key, encoded_output):
        s3 = boto3.resource("s3")
        response = s3.Bucket(bucket_name).put_object(Key=file_key, Body=encoded_output)

        return {"success": True, "response": response}

    @classmethod
    def upload_file(cls, filename, object_name=None):
        bucket_name = os.getenv("S3_BUCKETNAME_FOR_ERRORS")

        if object_name is None:
            object_name = filename
        s3_client = boto3.client('s3')

        try:
            print(f"Uploading {filename} to {bucket_name}, with object name {object_name}")
            response = s3_client.upload_file(filename, bucket_name, object_name)
        except Exception as e:
            logging.error(e)
            return False
        
        return {
            "sent": True,
            "bucket_name": bucket_name,
            "response": response,
            "object_name": object_name
        }

    @classmethod
    def transfer_file(cls, source_bucket, target_bucket, source_key, target_key):
        s3 = boto3.resource('s3')

        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }

        s3.Bucket(target_bucket).copy(copy_source, target_key)
        s3.Object(source_bucket, source_key).delete()

        return True