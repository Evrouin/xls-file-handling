import traceback
import os
import json

from app.lib.factories.file_factory import FileFactory


class FileBatch:
    def __init__(self, payload):
        self.records = payload["Records"]

    def perform(self):
        for record in self.records:
            bucket_name = record["s3"]["bucket"]["name"]
            object_key = record['s3']['object']['key']
            
            file_factory = FileFactory(bucket_name, object_key)
            file = file_factory.factory_method()

            file.perform()