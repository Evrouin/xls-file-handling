import os
from urllib.parse import unquote_plus

from app.lib.models.file import File

class FileFactory:

    def __init__(self, bucket_name, object_key):
        self.bucket_name = bucket_name
        self.object_key = object_key
    
    def factory_method(self):
        file_key = unquote_plus(self.object_key)
        return File(self.bucket_name, self.object_key, file_key)