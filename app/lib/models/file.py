import os
from datetime import date
import io
import json
import zipfile as zipfile
from app.helpers.logger import log, log_error
from app.lib.gateways.s3_fetch_file_group_gateway import S3FetchFileGroupGateway


class File:
    def __init__(self, bucket_name, object_key, file_key):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.file_key = file_key

    def fetch_file_group_content(self, file_key):
        response = S3FetchFileGroupGateway.get_item(
            'xls-file-input-folder',
            file_key
        )
    
        buffer = io.BytesIO(response['Body'].read())

        file = zipfile.ZipFile(buffer)

        return file

    def extract_folder(self, folder_name):
        file = self.fetch_file_group_content(self.file_key)

        file_list = file.namelist()

        folder_path = f'rep/{folder_name}/'
        target_files = [f for f in file_list if f.startswith(folder_path)]

        if target_files:
            extracted_files = {}
            for file_name in target_files:
                extracted_data = file.read(file_name)
                extracted_files[file_name] = extracted_data

            # Print files inside the target folder
            print(f"\nFiles inside '{folder_name}' folder:")
            for file_name, data in extracted_files.items():
                print(file_name)
        else:
            print(f"\n'{folder_name}' folder not found in the extracted content.")

    def perform(self):
        today = date.today().strftime("%Y%m%d")

        file_metadata = {
            "source_filekey": self.object_key,
            "source_s3_bucket": self.bucket_name,
        }

        log('file', 'perform - metadata', file_metadata)

        folder_name = 'DAC' 
        self.extract_folder(folder_name)
