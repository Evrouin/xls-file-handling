import os
import logging
import boto3

from botocore.exceptions import ClientError

class S3FetchFileGroupGateway():
    @classmethod
    def get(cls, bucket_name, prefix):

        # Initialize s3
        s3 = boto3.client('s3')

        try:
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix
            )
            
        except ClientError as e:
            logging.error(e)
            return None

        # Return list
        return response

    @classmethod
    def get_item(cls, bucket_name, key):
        s3 = boto3.client('s3')

        response = s3.get_object(Bucket=bucket_name, Key=key) 

        if 'Body' not in response:
            return ''

        return response

    @classmethod
    def not_exist(cls, bucket_name, key):
        # return number of file that matches prefix key
        # if 0, file does not exists 
        # else return number of file found
        try:
            s3 = boto3.resource('s3')
            bucket = s3.Bucket(bucket_name)
            
            objs = list(bucket.objects.filter(Prefix=key))
            return len(objs)

        except Exception as e:
            #logging.error(e)
            print(e)
            return -1

    @classmethod
    def create_unique_item(cls, bucket_name, key):
        file_exist = True
        ctr = 1
        raw_filename = key[0: key.index('.')]

        # loop to check if generated filename already exists
        while (file_exist):

            prefix_key = key[0: key.index('.')] # remove extension

            res = cls.not_exist(bucket_name, prefix_key)

            if res > 0:
                # file already exists, plus 1 counter
                ctr += 1
                key = raw_filename + "-" + str(ctr) + key[key.index('.'):len(key)]

            else: file_exist = False; ctr = 0

        return key