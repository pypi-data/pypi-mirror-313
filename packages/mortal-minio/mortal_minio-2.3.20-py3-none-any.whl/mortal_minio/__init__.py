#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Author: MaJian
@Time: 2024/1/19 15:31
@SoftWare: PyCharm
@Project: mortal
@File: __init__.py
"""
from .minio_main import MortalMinioMain


class MortalMinio(MortalMinioMain):
    def __init__(self, config):
        super().__init__(config)

    def connect(self):
        self._connect()

    def create_bucket(self, bucket_name, location="cn-north-1", object_lock=False):
        return self._create_bucket(bucket_name, location, object_lock)

    def remove_bucket(self, bucket_name):
        return self._remove_bucket(bucket_name)

    def bucket_list(self):
        return self._bucket_list()

    def bucket_list_files(self, bucket_name, prefix=""):
        return self._bucket_list_files(bucket_name, prefix)

    def bucket_policy(self, bucket_name):
        return self._bucket_policy(bucket_name)

    def upload_flow(self, bucket_name, object_name, data):
        self._upload_flow(bucket_name, object_name, data)

    def upload_file(self, bucket_name, object_name, file_name, parallel=3):
        self._upload_file(bucket_name, object_name, file_name, parallel)

    def upload_dir(self, bucket_name, dir_path, parallel=3, base_dir=None):
        self._upload_dir(bucket_name, dir_path, parallel, base_dir)

    def download_flow(self, bucket_name, object_name):
        return self._download_flow(bucket_name, object_name)

    def download_file(self, bucket_name, object_name, file_name):
        return self._download_file(bucket_name, object_name, file_name)

    def download_dir(self, bucket_name, object_path, dir_path):
        self._download_dir(bucket_name, object_path, dir_path)

    def remove_object(self, bucket_name, object_name):
        self._remove_object(bucket_name, object_name)

    def remove_objects(self, bucket_name, object_list):
        self._remove_objects(bucket_name, object_list)

    def get_url(self, bucket, object_name, days=7):
        return self._get_url(bucket, object_name, days)
