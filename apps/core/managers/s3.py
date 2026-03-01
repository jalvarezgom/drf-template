import io
import os.path
from io import StringIO
from typing import List, Literal

import boto3

from boto3.resources.base import ServiceResource

from apps.core.classes.exceptions.s3 import S3Exception


class S3StorageService:
    def __init__(self):
        self.session = None
        self.__bucket = None
        self.__s3: ServiceResource | None = None

    def init_connection(self, access_id, access_key, service_name, region_name, bucket_name):
        self.session = boto3.Session(
            aws_access_key_id=access_id,
            aws_secret_access_key=access_key,
            region_name=region_name,
        )
        self.__s3 = self.session.resource(
            service_name=service_name,
        )
        self.__bucket = self.__s3.Bucket(bucket_name)

    @property
    def s3(self):
        return self.__s3

    @property
    def bucket(self):
        return self.__bucket

    def get_files(self) -> List:
        files = []
        for file in self.__bucket.objects.all():
            files.append(file.key)
        return files

    def is_file(self, key: str) -> bool:
        objs = list(self.__bucket.objects.filter(Prefix=key))
        if len(objs) == 0:
            raise S3Exception(f'Not found any file with "{key}" key')
        return objs[0].key == key

    def is_dir(self, key: str) -> bool:
        objs = list(self.__bucket.objects.filter(Prefix=key))
        if len(objs) == 0:
            raise S3Exception(f'Not found any dir with "{key}" key')
        return f"{key}/" in objs[0].key

    def read_file(self, s3_filepath, mode: Literal["strIO", "bytes"] = "bytes") -> StringIO | bytes:
        s3_file = self.__bucket.Object(s3_filepath).get()
        data = s3_file["Body"].read()
        if mode == "str":
            data = io.StringIO(data.decode())
        return data

    def download_file(self, s3_filepath, download_path):
        self.__bucket.download_file(s3_filepath, download_path)

    def upload_file(self, filepath, s3_filepath):
        if not os.path.exists(filepath):
            raise Exception(f'File "{filepath}" does not exist')
        with open(filepath, "rb") as data:
            return self.upload_data(data, s3_filepath)

    def upload_data(self, data, s3_filepath):
        return self.__bucket.put_object(Key=s3_filepath, Body=data)

    def delete_file(self, path: str):
        self.__bucket.Object(path).delete()
