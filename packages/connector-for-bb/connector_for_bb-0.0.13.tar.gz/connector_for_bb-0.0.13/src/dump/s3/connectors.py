import os
from typing import Dict, Optional

import boto3
import pandas as pd
from botocore.config import Config
from pandas import DataFrame as PandasDataFrame

from dump.config_utils import load_config
from dump.files.tmp_util import TemporaryFileSystem


class S3Client:
    def __init__(
        self, creds_section: str, config_filiname: str = "s3_config.ini"
    ) -> None:
        self.creds_section = creds_section

        self.config = load_config(filename=config_filiname, section=creds_section)
        self.conn_config = Config(
            s3={
                "addressing_style": "virtual",
            },
            retries={"max_attempts": 10, "mode": "standard"},
            region_name="us-east-1",
        )

        self.client = boto3.client(
            "s3",
            **self.config,
            config=self.conn_config,
        )

    def get_files_info(self, bucket_name: str, object_folder: Optional[str] = ""):
        files_dict = {}
        response = self.client.list_objects_v2(Bucket=bucket_name, Prefix=object_folder)
        if "Contents" in response:
            for obj in response["Contents"]:
                size = obj["Size"]
                files_dict[obj["Key"]] = {
                    "size_bytes": size,
                    "size_gb": size / 1024**3,
                }
        return files_dict


class S3Upload(S3Client):
    """
    To upload files to s3
    """

    def __init__(
        self,
        bucket_name: str,
        object_folder: str = "",
        creds_section: str = "test",
    ) -> None:
        super().__init__(creds_section)
        self.bucket_name = bucket_name
        self.object_folder = object_folder

    def _get_path(self, file_name: str) -> str:
        """
        creating path where to save file in s3
        """
        path = os.path.join(self.object_folder, file_name)
        return path

    def upload_to_s3(self, tmp_path_file: str, file_name: str):
        """
        tmp_path_file: str - file location that we want to save
        file_name: str - new file name that will be displayed in s3

        upload local file into s3 bucket with new name 'file_name'
        """
        path = self._get_path(file_name)
        self.client.upload_file(tmp_path_file, self.bucket_name, path)


class S3Download(S3Client):
    def __init__(
        self,
        bucket_name: str,
        object_folder: str = "",
        creds_section: str = "test",
    ) -> None:
        super().__init__(creds_section)
        self.bucket_name = bucket_name
        self.object_folder = object_folder

        self.file_system = TemporaryFileSystem()

        # requires for not download same file more than one time
        self.__downloads_history: Dict[str, str] = {}

    def _check_path_exist(self, path: str) -> bool:
        exsist_files = self.get_files_info(self.bucket_name, self.object_folder)
        return path in exsist_files

    def _get_object_path(self, file_name) -> str:
        path = os.path.join(self.object_folder, file_name)
        return path

    def download_from_s3(self, download_file_name: str) -> str:
        """
        downloading file from s3 and put the file into temporary directory
        returns path to file in temporary directory
        """
        object_path = self._get_object_path(download_file_name)
        if self._check_path_exist(object_path):
            if object_path not in self.__downloads_history:
                save_path = self.file_system.save_path()
                self.client.download_file(self.bucket_name, object_path, save_path)
                self.__downloads_history[object_path] = save_path

            return self.__downloads_history[object_path]
        else:
            raise ValueError(f"The file {object_path} was not found")

    def download_from_s3_df(
        self, download_file_name: str, encoding="utf-8"
    ) -> PandasDataFrame:
        df_path = self.download_from_s3(download_file_name)
        return pd.read_csv(df_path, encoding=encoding, low_memory=False)
